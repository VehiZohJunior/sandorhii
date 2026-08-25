import json
from pathlib import Path

from app.modules.linguistic.engine import RULES_BY_LANGUAGE, STRUCTURAL_SIGNAL_IDS, analyze

MANIPULATIVE_TEXT_FR = (
    "URGENT !!! Partagez avant qu'il ne soit trop tard !!! Les experts "
    "affirment que TOUS les responsables sont corrompus et qu'ils nous "
    "cachent la verite. Soit vous nous croyez, soit vous etes complices. "
    "C'est un scandale sans precedent."
)

MANIPULATIVE_TEXT_EN = (
    "URGENT !!! Share before it's too late !!! Experts claim that ALL "
    "officials are corrupt and they don't want you to know the truth. "
    "Either you believe us or you're against us. It's a scandal, "
    "unprecedented."
)

NEUTRAL_TEXT = (
    "Le ministre de l'economie a presente ce lundi le budget 2026 devant "
    "l'Assemblee nationale. Le texte prevoit une hausse de 3 pour cent des "
    "depenses publiques, principalement destinee aux infrastructures "
    "routieres et a la sante."
)

FRONTEND_MESSAGES_DIR = (
    Path(__file__).resolve().parents[2] / "frontend" / "messages"
)


def test_neutral_text_has_no_signals():
    result = analyze(NEUTRAL_TEXT, language="fr")
    assert result["score"] == 0
    assert result["signals"] == []
    assert result["suggested_level"] == "aucun"


def test_manipulative_text_triggers_multiple_signals_fr():
    result = analyze(MANIPULATIVE_TEXT_FR, language="fr")
    assert result["score"] > 0
    ids = {s["id"] for s in result["signals"]}
    assert "faux_dilemme" in ids
    assert "generalisation_abusive" in ids
    assert "autorite_vague" in ids
    assert "urgence_partage" in ids
    assert "ponctuation_excessive" in ids


def test_manipulative_text_triggers_multiple_signals_en():
    result = analyze(MANIPULATIVE_TEXT_EN, language="en")
    assert result["language_supported"] is True
    assert result["score"] > 0
    ids = {s["id"] for s in result["signals"]}
    assert "faux_dilemme" in ids
    assert "generalisation_abusive" in ids
    assert "autorite_vague" in ids
    assert "urgence_partage" in ids
    assert "complot" in ids


def test_every_signal_has_a_translation_in_both_locales():
    """Chaque id de regle (fr + en + signaux structurels) doit avoir un
    libelle/explication dans messages/fr.json ET messages/en.json, sinon
    l'interface planterait ou afficherait une cle brute pour l'utilisateur.
    """
    all_ids = set(STRUCTURAL_SIGNAL_IDS)
    for rules in RULES_BY_LANGUAGE.values():
        all_ids |= {rule["id"] for rule in rules}

    for locale in ("fr", "en"):
        messages = json.loads((FRONTEND_MESSAGES_DIR / f"{locale}.json").read_text(encoding="utf-8"))
        catalog = messages["home"]["signalCatalog"]
        for signal_id in all_ids:
            assert signal_id in catalog, f"'{signal_id}' manquant dans {locale}.json"
            assert catalog[signal_id]["label"]
            assert catalog[signal_id]["explanation"]


def test_every_signal_has_excerpt_and_positive_weight():
    result = analyze(MANIPULATIVE_TEXT_FR, language="fr")
    assert result["signals"], "le texte de test doit declencher au moins un signal"
    for signal in result["signals"]:
        assert signal["excerpt"]
        assert signal["weight"] > 0


def test_score_is_capped_at_100():
    spam = " ".join([MANIPULATIVE_TEXT_FR] * 20)
    result = analyze(spam, language="fr")
    assert result["score"] <= 100


def test_unsupported_language_only_gets_structural_signals():
    result = analyze(MANIPULATIVE_TEXT_FR, language="es")
    assert result["language_supported"] is False
    categories = {s["category"] for s in result["signals"]}
    # Aucune regle de sophisme/lexique n'existe pour l'espagnol pour l'instant.
    assert "sophisme" not in categories


def test_empty_text_does_not_crash():
    result = analyze("", language="fr")
    assert result["score"] == 0
    assert result["signals"] == []


def test_rules_match_regardless_of_apostrophe_style():
    # Beaucoup d'utilisateurs collent du texte sans apostrophe typographique
    # (clavier, copier-coller depuis WhatsApp, etc.) - les regles doivent
    # rester robustes aux trois variantes : ' (droite), ' (courbe), rien.
    variants = [
        "Il n'y a que deux choix possibles ici.",
        "Il n’y a que deux choix possibles ici.",
        "Il n y a que deux choix possibles ici.",
    ]
    for text in variants:
        result = analyze(text, language="fr")
        ids = {s["id"] for s in result["signals"]}
        assert "faux_dilemme" in ids, f"echec pour: {text!r}"


def test_repetition_signal_detects_repeated_slogan():
    slogan = "le gouvernement nous ment depuis toujours"
    text = (
        f"{slogan}, tout le monde le sait. Regardez les faits, vous verrez "
        f"que {slogan} et que rien ne change jamais dans ce pays."
    )
    result = analyze(text, language="fr")
    ids = {s["id"] for s in result["signals"]}
    assert "repetition_suspecte" in ids


def test_repetition_signal_absent_on_neutral_text():
    result = analyze(NEUTRAL_TEXT, language="fr")
    ids = {s["id"] for s in result["signals"]}
    assert "repetition_suspecte" not in ids


def test_whataboutism_signal_detected():
    text = "Et vous, qu'avez-vous fait quand ce probleme est arrive ?"
    result = analyze(text, language="fr")
    ids = {s["id"] for s in result["signals"]}
    assert "detournement_whataboutism" in ids


def test_attribution_flags_unnamed_source_fr():
    text = (
        "Selon des experts, la situation est catastrophique. Des scientifiques "
        "affirment que ce produit est extremement dangereux pour la sante."
    )
    result = analyze(text, language="fr")
    ids = {s["id"] for s in result["signals"]}
    assert "attribution_non_identifiee" in ids


def test_attribution_ignores_named_source_fr():
    text = (
        "Selon Marie Curie, physicienne reconnue, cette experience confirme "
        "l'hypothese initiale et ouvre de nouvelles pistes de recherche."
    )
    result = analyze(text, language="fr")
    ids = {s["id"] for s in result["signals"]}
    assert "attribution_non_identifiee" not in ids


def test_attribution_flags_unnamed_source_en():
    text = (
        "According to experts, the situation is catastrophic. Scientists "
        "claim this product is extremely dangerous for public health."
    )
    result = analyze(text, language="en")
    ids = {s["id"] for s in result["signals"]}
    assert "attribution_non_identifiee" in ids


def test_attribution_ignores_named_source_en():
    text = (
        "According to Marie Curie, a recognized physicist, this experiment "
        "confirms the initial hypothesis and opens new research avenues."
    )
    result = analyze(text, language="en")
    ids = {s["id"] for s in result["signals"]}
    assert "attribution_non_identifiee" not in ids


def test_metaphore_guerriere_detected_fr():
    text = "Notre pays est envahi par une vague migratoire qui submerge nos frontieres."
    result = analyze(text, language="fr")
    ids = {s["id"] for s in result["signals"]}
    assert "metaphore_guerriere" in ids


def test_metaphore_guerriere_detected_en():
    text = "Our country is being invaded by a wave of migrants flooding across the border."
    result = analyze(text, language="en")
    ids = {s["id"] for s in result["signals"]}
    assert "metaphore_guerriere" in ids


def test_metaphore_guerriere_absent_on_neutral_text():
    result = analyze(NEUTRAL_TEXT, language="fr")
    ids = {s["id"] for s in result["signals"]}
    assert "metaphore_guerriere" not in ids


def test_attribution_absent_without_trigger_words():
    result = analyze(NEUTRAL_TEXT, language="fr")
    ids = {s["id"] for s in result["signals"]}
    assert "attribution_non_identifiee" not in ids
