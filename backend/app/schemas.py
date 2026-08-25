from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .models import VERDICTS


class SubmissionCreate(BaseModel):
    texte: str = Field(min_length=20, max_length=20000)
    langue: str = "fr"


class SignalOut(BaseModel):
    """Donnees brutes uniquement (id/poids/occurrences/extrait) : le libelle
    et l'explication de chaque signal sont traduits cote frontend a partir
    de `id`, pour que l'interface reste correcte quelle que soit la langue
    choisie par l'utilisateur (voir messages/fr.json et en.json, cle
    `home.signalCatalog`)."""

    id: str
    category: str
    weight: float
    occurrences: int
    excerpt: str


class LinguisticAnalysisOut(BaseModel):
    score: float
    suggested_level: str
    signals: list[SignalOut]
    stats: dict
    model_version: str
    language_supported: bool


class SubmissionOut(BaseModel):
    id: str
    content_type: str
    raw_content: str
    language: str
    status: str
    created_at: datetime
    linguistic_analysis: LinguisticAnalysisOut | None = None
    fact_check: "FactCheckOut | None" = None

    model_config = ConfigDict(from_attributes=True)


class FactCheckPublish(BaseModel):
    verdict: str = Field(pattern="^(" + "|".join(VERDICTS) + ")$")
    resume: str = Field(min_length=10, max_length=4000)
    auteur: str = Field(min_length=2, max_length=120)


class FactCheckOut(BaseModel):
    id: str
    verdict: str
    global_score: float
    resume: str
    auteur: str
    statut: str
    created_at: datetime
    published_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class FeedItemOut(BaseModel):
    submission_id: str
    verdict: str
    global_score: float
    resume: str
    auteur: str
    published_at: datetime | None
    extrait: str

    model_config = ConfigDict(from_attributes=True)
