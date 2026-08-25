"""Lexique de vocabulaire alarmiste / desinformation - francais, v1.

Le libelle et l'explication de chaque regle (par id) vivent cote frontend
(messages/fr.json, messages/en.json, cle home.signalCatalog) et non ici.
"""

LEXICON_RULES_FR = [
    {
        "id": "urgence_partage",
        "category": "lexique",
        "weight": 9,
        "patterns": [
            r"\bpartagez? (?:avant|maintenant|vite|au plus vite)\b",
            r"\bavant qu['’ ]?il ne soit trop tard\b",
            r"\bpartagez? un maximum\b",
            r"\bce message va \S*etre supprim\S+\b",
        ],
    },
    {
        "id": "urgence_lexicale",
        "category": "lexique",
        "weight": 5,
        "patterns": [
            r"\burgent\b",
            r"\balerte\b",
            r"\bimm[eé]diat(?:ement)?\b",
            r"\bderni[eè]re minute\b",
        ],
    },
    {
        "id": "superlatifs",
        "category": "lexique",
        "weight": 5,
        "patterns": [
            r"\bjamais vu\b",
            r"\bsans pr[eé]c[eé]dent\b",
            r"\ble pire\b",
            r"\bhistorique\b",
            r"\bcatastrophi[qc]",
            r"\btotalement in[eé]dit\b",
        ],
    },
    {
        "id": "mots_choc",
        "category": "lexique",
        "weight": 4,
        "patterns": [
            r"\bscandale(?:ux)?\b",
            r"\bchoquant\b",
            r"\bhorrible\b",
            r"\bterrifiant\b",
            r"\balarmant\b",
            r"\bglacant\b",
        ],
    },
    {
        "id": "appel_emotion_peur",
        "category": "lexique",
        "weight": 6,
        "patterns": [
            r"\bvous devez avoir peur\b",
            r"\bun danger (?:imminent|mortel) (?:menace|guette)\b",
            r"\bvos enfants (?:sont en danger|risquent)\b",
            r"\bcela pourrait (?:vous|nous) tuer\b",
        ],
    },
    {
        # Ajoute suite a la comparaison avec la grille "9 familles" de
        # X-GRAY (25/08) - correspond a sa famille "verbes d'action forts"
        # et a la lentille "linguistique cognitive" (metaphores de Lakoff)
        # de la grille SandorHii. Volontairement limite au champ lexical
        # de l'invasion/submersion (pas "attaque"/"guerre"/"combat", trop
        # frequents dans un usage neutre - "guerre contre la pauvrete" etc.
        # - pour rester a faible taux de faux positifs).
        "id": "metaphore_guerriere",
        "category": "lexique",
        "weight": 6,
        "patterns": [
            r"\benvahi\w*\b",
            r"\binvasion\b",
            r"\bsubmerg\w*\b",
            r"\bd[ée]ferlante\b",
            # "infiltr*" volontairement exclu : teste et retire le 25/08,
            # faux positif confirme sur un usage journalistique legitime
            # ("un journaliste s'est infiltre pour enqueter").
        ],
    },
]
