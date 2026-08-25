"""Modeles ORM - phase 1 (soumission texte + pilier linguistique + fact-check).

Les tables media_analyses, tech_analyses, sources, themes, veille_signals et
reports existent deja dans supabase/schema.sql (phases 2+) mais n'ont pas
besoin d'un modele ORM tant que le code ne les utilise pas.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .core.db import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    content_type: Mapped[str] = mapped_column(String(20), default="texte")
    raw_content: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    language: Mapped[str] = mapped_column(String(8), default="fr")
    status: Mapped[str] = mapped_column(String(30), default="nouveau")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    linguistic_analysis: Mapped["LinguisticAnalysis | None"] = relationship(
        back_populates="submission", uselist=False, cascade="all, delete-orphan"
    )
    fact_check: Mapped["FactCheck | None"] = relationship(
        back_populates="submission", uselist=False, cascade="all, delete-orphan"
    )


class LinguisticAnalysis(Base):
    __tablename__ = "linguistic_analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    submission_id: Mapped[str] = mapped_column(ForeignKey("submissions.id"), unique=True)
    score: Mapped[float] = mapped_column(Float)
    suggested_level: Mapped[str] = mapped_column(String(20))
    signals: Mapped[list] = mapped_column(JSON)
    stats: Mapped[dict] = mapped_column(JSON)
    model_version: Mapped[str] = mapped_column(String(40))
    language_supported: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    submission: Mapped["Submission"] = relationship(back_populates="linguistic_analysis")


VERDICTS = ("vrai", "faux", "partiellement_vrai", "non_verifiable", "trompeur")


class FactCheck(Base):
    __tablename__ = "fact_checks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    submission_id: Mapped[str] = mapped_column(ForeignKey("submissions.id"), unique=True)
    verdict: Mapped[str] = mapped_column(String(30))
    global_score: Mapped[float] = mapped_column(Float)
    resume: Mapped[str] = mapped_column(Text)
    auteur: Mapped[str] = mapped_column(String(120))
    statut: Mapped[str] = mapped_column(String(20), default="brouillon")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    submission: Mapped["Submission"] = relationship(back_populates="fact_check")
