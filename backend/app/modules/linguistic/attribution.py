"""Detection des citations a source non identifiee (polyphonie + heterogeneite).

Repose sur spaCy : on repere les phrases contenant un marqueur
d'attribution ("selon...", "affirment que"...) puis on verifie si CETTE
MEME phrase contient une entite nommee (personne/organisation). Si non,
la source est vague ("des experts", "on dit que") - un signal classique
de desinformation et de pseudoscience (grille linguistique, lentilles
Polyphonie enonciative + Heterogeneite enonciative montree).

Approche volontairement au niveau de la phrase plutot que de l'arbre
syntaxique (sujet grammatical exact du verbe) : plus robuste aux erreurs
d'analyse des modeles spaCy "sm" (legers, gratuits) qu'une extraction
precise, au prix d'un peu de precision - acceptable pour un signal parmi
d'autres dans un score qui additionne (jamais un verdict sur un seul
indice).
"""

from __future__ import annotations

import spacy

MODEL_NAMES = {"fr": "fr_core_news_sm", "en": "en_core_web_sm"}

# Types d'entites acceptes comme "source nommee". Elargi au-dela de
# PER/ORG(PERSON) pour compenser la NER modeste des modeles "sm" (ex.
# une institution parfois etiquetee MISC/LOC plutot qu'ORG) : mieux vaut
# sous-detecter le signal negatif que pénaliser une source réellement
# nommée mal etiquetee par le modele.
_NAMED_ENTITY_LABELS = {
    "fr": {"PER", "ORG", "MISC", "LOC"},
    "en": {"PERSON", "ORG", "GPE", "FAC", "NORP"},
}

_ATTRIBUTION_LEMMAS = {
    "fr": {
        "selon", "affirmer", "déclarer", "dire", "révéler", "rapporter",
        "prétendre", "souligner", "confirmer", "annoncer", "assurer",
        "expliquer", "indiquer", "préciser",
    },
    "en": {
        "accord",  # lemme de "According (to)"
        "say", "claim", "state", "reveal", "report", "allege", "confirm",
        "announce", "assure", "explain", "indicate",
    },
}

_nlp_cache: dict[str, "spacy.language.Language"] = {}


def _get_nlp(language: str):
    if language not in _nlp_cache:
        _nlp_cache[language] = spacy.load(MODEL_NAMES[language])
    return _nlp_cache[language]


def preload_models() -> None:
    """Charge les modeles spaCy immediatement (quelques secondes) plutot
    que paresseusement au premier appel. A appeler au demarrage du serveur
    (voir app/main.py) pour que ce cout ne retombe jamais sur le premier
    utilisateur reel - l'exigence est <3s de reponse."""
    for language in MODEL_NAMES:
        _get_nlp(language)


def detect_unnamed_attribution(text: str, language: str) -> list[str]:
    """Retourne le texte de chaque phrase qui attribue une affirmation
    a une source jamais nommee precisement."""
    if language not in MODEL_NAMES or not text:
        return []

    nlp = _get_nlp(language)
    doc = nlp(text)
    lemmas = _ATTRIBUTION_LEMMAS[language]
    named_labels = _NAMED_ENTITY_LABELS[language]

    flagged: list[str] = []
    for sent in doc.sents:
        if not any(tok.lemma_.lower() in lemmas for tok in sent):
            continue
        has_named_source = any(
            ent.label_ in named_labels
            for ent in doc.ents
            if ent.start >= sent.start and ent.end <= sent.end
        )
        if not has_named_source:
            flagged.append(sent.text.strip())
    return flagged
