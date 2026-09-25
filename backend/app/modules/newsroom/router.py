from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...core.db import get_db
from ...core.deps import require_admin
from ...models import FactCheck, Submission
from ...schemas import FactCheckOut, FactCheckPublish, SubmissionOut

router = APIRouter(
    prefix="/api/newsroom",
    tags=["newsroom"],
    dependencies=[Depends(require_admin)],
)
# La limite de tentatives (bonnes ou mauvaises) vit dans require_admin()
# lui-meme (app/core/deps.py) - voir le commentaire la-bas pour pourquoi
# un @limiter.limit() ici ne suffirait pas a bloquer les mots de passe
# incorrects.


@router.get("/queue", response_model=list[SubmissionOut])
def queue(db: Session = Depends(get_db)):
    """File d'attente : soumissions analysees, pas encore publiees."""
    return (
        db.query(Submission)
        .filter(Submission.status == "en_attente_validation")
        .order_by(Submission.created_at.asc())
        .all()
    )


@router.post("/{submission_id}/publish", response_model=FactCheckOut)
def publish(submission_id: str, payload: FactCheckPublish, db: Session = Depends(get_db)):
    submission = db.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Soumission introuvable.")
    if not submission.linguistic_analysis:
        raise HTTPException(status_code=409, detail="Analyse linguistique manquante.")

    fact_check = submission.fact_check or FactCheck(submission_id=submission.id)
    fact_check.verdict = payload.verdict
    fact_check.global_score = submission.linguistic_analysis.score
    fact_check.resume = payload.resume
    fact_check.auteur = payload.auteur
    fact_check.statut = "publie"
    fact_check.published_at = datetime.now(timezone.utc)

    submission.status = "publie"
    db.add(fact_check)
    db.commit()
    db.refresh(fact_check)
    return fact_check


@router.post("/{submission_id}/reject", response_model=SubmissionOut)
def reject(submission_id: str, db: Session = Depends(get_db)):
    submission = db.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Soumission introuvable.")
    submission.status = "rejete"
    db.commit()
    db.refresh(submission)
    return submission
