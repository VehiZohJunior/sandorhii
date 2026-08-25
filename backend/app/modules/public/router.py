from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...core.db import get_db
from ...models import FactCheck
from ...schemas import FeedItemOut, SubmissionOut

router = APIRouter(prefix="/api", tags=["public"])


def _to_feed_item(fc: FactCheck) -> dict:
    extrait = fc.submission.raw_content[:220]
    if len(fc.submission.raw_content) > 220:
        extrait += "…"
    return {
        "submission_id": fc.submission_id,
        "verdict": fc.verdict,
        "global_score": fc.global_score,
        "resume": fc.resume,
        "auteur": fc.auteur,
        "published_at": fc.published_at,
        "extrait": extrait,
    }


@router.get("/feed", response_model=list[FeedItemOut])
def feed(
    db: Session = Depends(get_db),
    verdict: str | None = Query(default=None),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
):
    q = db.query(FactCheck).filter(FactCheck.statut == "publie")
    if verdict:
        q = q.filter(FactCheck.verdict == verdict)
    q = q.order_by(FactCheck.published_at.desc()).offset(offset).limit(limit)
    return [_to_feed_item(fc) for fc in q.all()]


@router.get("/feed/{submission_id}", response_model=SubmissionOut)
def feed_item(submission_id: str, db: Session = Depends(get_db)):
    fc = (
        db.query(FactCheck)
        .filter(FactCheck.submission_id == submission_id, FactCheck.statut == "publie")
        .first()
    )
    if not fc:
        raise HTTPException(status_code=404, detail="Fact-check introuvable ou non publié.")
    return fc.submission
