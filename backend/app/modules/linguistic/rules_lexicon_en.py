"""Alarmist / disinformation vocabulary lexicon - English, v1.

Mirrors rules_lexicon_fr.py: same ids, categories and weights.
"""

LEXICON_RULES_EN = [
    {
        "id": "urgence_partage",
        "category": "lexique",
        "weight": 9,
        "patterns": [
            r"\bshare (?:before|now|immediately)\b",
            r"\bbefore it['’]?s too late\b",
            r"\bshare (?:this )?(?:widely|as much as possible)\b",
            r"\bthis (?:message|post) will be (?:deleted|taken down)\b",
        ],
    },
    {
        "id": "urgence_lexicale",
        "category": "lexique",
        "weight": 5,
        "patterns": [
            r"\burgent\b",
            r"\balert\b",
            r"\bimmediately\b",
            r"\bbreaking\b",
        ],
    },
    {
        "id": "superlatifs",
        "category": "lexique",
        "weight": 5,
        "patterns": [
            r"\bnever (?:seen|happened) before\b",
            r"\bunprecedented\b",
            r"\bthe worst\b",
            r"\bhistoric\b",
            r"\bcatastrophic\b",
            r"\btotally unheard of\b",
        ],
    },
    {
        "id": "mots_choc",
        "category": "lexique",
        "weight": 4,
        "patterns": [
            r"\bscandalous\b",
            r"\bshocking\b",
            r"\bhorrible\b",
            r"\bterrifying\b",
            r"\balarming\b",
            r"\bchilling\b",
        ],
    },
    {
        "id": "appel_emotion_peur",
        "category": "lexique",
        "weight": 6,
        "patterns": [
            r"\byou should be afraid\b",
            r"\ban? (?:imminent|deadly) danger threatens\b",
            r"\byour children are (?:in danger|at risk)\b",
            r"\bthis could kill you\b",
        ],
    },
    {
        "id": "metaphore_guerriere",
        "category": "lexique",
        "weight": 6,
        "patterns": [
            r"\binvad\w*\b",
            r"\binvasion\b",
            r"\bsubmerg\w*\b",
            r"\bflood(?:ed|ing)?\s+(?:by|with|of)\b",
            # "infiltrat*" deliberately excluded : tested and removed on
            # 25/08, confirmed false positive on legitimate journalism
            # ("a reporter infiltrated the organization to investigate").
        ],
    },
]
