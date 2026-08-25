import hashlib
import re
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...core.db import get_db
from ...core.limiter import limiter
from ...models import LinguisticAnalysis, Submission
from ...schemas import SubmissionCreate, SubmissionOut
from ..linguistic.engine import analyze

router = APIRouter(prefix="/api/submissions", tags=["submissions"])


def _content_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


@router.post("", response_model=SubmissionOut)
@limiter.limit("20/minute")
def create_submission(
    request: Request, payload: SubmissionCreate, db: Session = Depends(get_db)
):
    content_hash = _content_hash(payload.texte)

    existing = db.query(Submission).filter_by(content_hash=content_hash).first()
    if existing:
        # Contenu deja soumis : on renvoie l'analyse existante au lieu de
        # relancer le moteur (equivalent d'un cache pour ce volume - un
        # vrai cache Redis prendra le relais si le trafic le justifie).
        return existing

    # Le score/l'analyse ne dependent pas d'un id genere par la base, donc
    # tout est construit AVANT le premier contact avec la DB : un seul
    # commit final, un seul point ou une erreur de concurrence peut
    # survenir, entierement couvert par le try/except ci-dessous.
    result = analyze(payload.texte, language=payload.langue)
    submission = Submission(
        id=str(uuid.uuid4()),
        content_type="texte",
        raw_content=payload.texte,
        content_hash=content_hash,
        language=payload.langue,
        status="en_attente_validation",
    )
    analysis = LinguisticAnalysis(
        submission_id=submission.id,
        score=result["score"],
        suggested_level=result["suggested_level"],
        signals=result["signals"],
        stats=result["stats"],
        model_version=result["model_version"],
        language_supported=result["language_supported"],
    )
    db.add(submission)
    db.add(analysis)
    try:
        db.commit()
    except IntegrityError:
        # Un contenu viral peut etre soumis par deux personnes a quelques
        # millisecondes d'intervalle : la contrainte unique sur
        # content_hash peut alors se declencher entre notre verification
        # ci-dessus et ce commit. Dans ce cas on ne plante pas : on
        # renvoie simplement l'analyse de l'autre soumission, identique.
        db.rollback()
        existing = db.query(Submission).filter_by(content_hash=content_hash).first()
        if existing:
            return existing
        raise
    db.refresh(submission)
    return submission


@router.get("/{submission_id}", response_model=SubmissionOut)
def get_submission(submission_id: str, db: Session = Depends(get_db)):
    submission = db.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Soumission introuvable.")
    return submission
