"""Moteur d'analyse linguistique v1 - regles explicables.

Volontairement simple et 100% transparent : chaque point de score est
tracable a une regle precise (par id) et a un extrait du texte. Pas de
boite noire. Le libelle/l'explication de chaque regle ne sont PAS stockes
ici : ils vivent dans les catalogues de traduction du frontend
(messages/fr.json, messages/en.json, cle home.signalCatalog), pour que
l'interface reste correcte quelle que soit la langue choisie par
l'utilisateur, sans dupliquer le texte a deux endroits.

Langues couvertes par le detecteur de regles (Vague 1 du blueprint) :
francais et anglais. Les langues locales ivoiriennes/africaines suivront
en Vague 2/3 - voir la section "Stratégie multilingue" du blueprint.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from . import attribution
from .rules_fallacies_en import FALLACY_RULES_EN
from .rules_fallacies_fr import FALLACY_RULES_FR
from .rules_lexicon_en import LEXICON_RULES_EN
from .rules_lexicon_fr import LEXICON_RULES_FR

MODEL_VERSION = "regles-v2"

RULES_BY_LANGUAGE = {
    "fr": FALLACY_RULES_FR + LEXICON_RULES_FR,
    "en": FALLACY_RULES_EN + LEXICON_RULES_EN,
}

# Ids des signaux qui ne viennent pas d'une regle regex (RULES_BY_LANGUAGE) :
# calcules directement en Python. Centralise ici pour que les tests et la
# verification de couverture i18n (fr.json/en.json) n'aient qu'un seul
# endroit a tenir a jour quand on ajoute un nouveau signal de ce type.
STRUCTURAL_SIGNAL_IDS = {
    "majuscules_excessives",
    "ponctuation_excessive",
    "repetition_suspecte",
    "attribution_non_identifiee",
}

# Un mot en majuscules (>=3 lettres) compte comme signal de "cri"
_CAPS_WORD_RE = re.compile(r"\b[A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜÇ]{3,}\b")
_WORD_RE = re.compile(r"\b[a-zàâäéèêëïîôöùûüç]+\b", re.IGNORECASE)
_EXCERPT_WINDOW = 60  # caracteres de contexte de chaque cote du match
_MAX_OCCURRENCES_COUNTED = 3  # rendements decroissants au-dela
_REPETITION_NGRAM_SIZE = 6  # longueur (en mots) d'une phrase repetee suspecte


@dataclass
class Signal:
    id: str
    category: str
    weight: float
    occurrences: int
    excerpt: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "category": self.category,
            "weight": round(self.weight, 1),
            "occurrences": self.occurrences,
            "excerpt": self.excerpt,
        }


def _make_excerpt(text: str, start: int, end: int) -> str:
    lo = max(0, start - _EXCERPT_WINDOW)
    hi = min(len(text), end + _EXCERPT_WINDOW)
    prefix = "…" if lo > 0 else ""
    suffix = "…" if hi < len(text) else ""
    return f"{prefix}{text[lo:hi].strip()}{suffix}"


def _scan_rule_based_signals(text: str, language: str) -> list[Signal]:
    rules = RULES_BY_LANGUAGE.get(language, [])
    signals: list[Signal] = []
    for rule in rules:
        matches: list[re.Match] = []
        for pattern in rule["patterns"]:
            matches.extend(re.finditer(pattern, text, flags=re.IGNORECASE | re.UNICODE))
        if not matches:
            continue
        matches.sort(key=lambda m: m.start())
        occurrences = len(matches)
        counted = min(occurrences, _MAX_OCCURRENCES_COUNTED)
        first = matches[0]
        signals.append(
            Signal(
                id=rule["id"],
                category=rule["category"],
                weight=rule["weight"] * counted / _MAX_OCCURRENCES_COUNTED,
                occurrences=occurrences,
                excerpt=_make_excerpt(text, first.start(), first.end()),
            )
        )
    return signals


def _repetition_signal(text: str) -> Signal | None:
    """Detecte une meme expression de plusieurs mots repetee mot pour mot.

    Signal independant de la langue : "repeter le mensonge" (repetition
    d'un slogan/d'une affirmation) est une technique de propagande connue,
    pas un phenomene francais ou anglais specifiquement.
    """
    matches = list(_WORD_RE.finditer(text))
    n = _REPETITION_NGRAM_SIZE
    if len(matches) < n * 2:
        return None

    first_seen: dict[str, tuple[int, int]] = {}
    counts: dict[str, int] = {}
    for i in range(len(matches) - n + 1):
        chunk = matches[i : i + n]
        ngram = " ".join(m.group().lower() for m in chunk)
        counts[ngram] = counts.get(ngram, 0) + 1
        first_seen.setdefault(ngram, (chunk[0].start(), chunk[-1].end()))

    repeated = {ngram: c for ngram, c in counts.items() if c >= 2}
    if not repeated:
        return None

    top_ngram = max(repeated, key=repeated.get)
    occurrences = repeated[top_ngram]
    start, end = first_seen[top_ngram]
    weight = min(9.0, 4.0 + occurrences * 1.5)
    return Signal(
        id="repetition_suspecte",
        category="lexique",
        weight=weight,
        occurrences=occurrences,
        excerpt=_make_excerpt(text, start, end),
    )


def _attribution_signal(text: str, language: str) -> Signal | None:
    """Phrases qui attribuent une affirmation a une source jamais nommee
    precisement ("selon des experts", "on affirme que..."). Voir
    modules/linguistic/attribution.py - repose sur spaCy (polyphonie +
    heterogeneite enonciative)."""
    occurrences = attribution.detect_unnamed_attribution(text, language)
    if not occurrences:
        return None

    counted = min(len(occurrences), _MAX_OCCURRENCES_COUNTED)
    weight = 6.0 * counted / _MAX_OCCURRENCES_COUNTED
    excerpt = occurrences[0]
    if len(excerpt) > 160:
        excerpt = excerpt[:160].rstrip() + "…"
    return Signal(
        id="attribution_non_identifiee",
        category="attribution",
        weight=weight,
        occurrences=len(occurrences),
        excerpt=excerpt,
    )


def _structural_signals(text: str) -> tuple[list[Signal], dict]:
    words = _WORD_RE.findall(text)
    word_count = max(len(words), 1)
    caps_words = _CAPS_WORD_RE.findall(text)
    caps_ratio = len(caps_words) / word_count
    exclamations = text.count("!")
    exclam_per_100 = (exclamations / word_count) * 100

    signals: list[Signal] = []

    if caps_ratio > 0.08 and len(caps_words) >= 2:
        weight = min(10.0, caps_ratio * 60)
        signals.append(
            Signal(
                id="majuscules_excessives",
                category="lexique",
                weight=weight,
                occurrences=len(caps_words),
                excerpt=", ".join(caps_words[:5]),
            )
        )

    if exclam_per_100 > 2.5 and exclamations >= 2:
        weight = min(8.0, exclam_per_100 * 1.5)
        first_mark = text.find("!")
        signals.append(
            Signal(
                id="ponctuation_excessive",
                category="lexique",
                weight=weight,
                occurrences=exclamations,
                excerpt=_make_excerpt(text, first_mark, first_mark + 1),
            )
        )

    repetition = _repetition_signal(text)
    if repetition:
        signals.append(repetition)

    stats = {
        "word_count": word_count,
        "caps_ratio": round(caps_ratio, 3),
        "exclamations": exclamations,
    }
    return signals, stats


def _suggested_level(score: float) -> str:
    """Code de niveau, pas de texte : la traduction vit cote frontend
    (comme pour les labels/explications des signaux) pour que l'interface
    reste correcte quelle que soit la langue choisie par l'utilisateur.
    """
    if score < 15:
        return "aucun"
    if score < 35:
        return "a_surveiller"
    if score < 60:
        return "modere"
    return "eleve"


def analyze(text: str, language: str = "fr") -> dict:
    """Analyse un texte et retourne un score explicable 0-100.

    Le score n'est PAS un verdict de verite : il mesure uniquement la
    presence de techniques de manipulation rhetorique/lexicale connues.
    Le verdict final (Vrai/Faux/...) reste toujours decide par un humain
    en back-office.
    """
    text = text or ""
    rule_signals = _scan_rule_based_signals(text, language)
    structural, stats = _structural_signals(text)
    attribution_signal = _attribution_signal(text, language)
    signals = rule_signals + structural
    if attribution_signal:
        signals.append(attribution_signal)
    signals.sort(key=lambda s: s.weight, reverse=True)

    raw_score = sum(s.weight for s in signals)
    score = min(100.0, raw_score)

    return {
        "score": round(score, 1),
        "suggested_level": _suggested_level(score),
        "signals": [s.to_dict() for s in signals],
        "stats": stats,
        "model_version": MODEL_VERSION,
        "language_supported": language in RULES_BY_LANGUAGE,
    }
