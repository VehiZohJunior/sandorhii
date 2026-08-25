"""Fallacy library (rhetorical manipulation) - English, v1.

Mirrors rules_fallacies_fr.py exactly: same ids, categories and weights, so
the frontend translation catalog (keyed by id) works unchanged for either
language. Only the regex patterns differ.
"""

FALLACY_RULES_EN = [
    {
        "id": "faux_dilemme",
        "category": "sophisme",
        "weight": 8,
        "patterns": [
            r"\beither\b[^.!?]{3,80}\bor\b",
            r"\bthere (?:is|are) only two (?:choices|options|solutions)\b",
            r"\bif you['’]?re not with (?:us|them)\S*,?\s*you['’]?re against\b",
            r"\bit['’]?s (?:this|that) or nothing\b",
        ],
    },
    {
        "id": "pente_glissante",
        "category": "sophisme",
        "weight": 8,
        "patterns": [
            r"\bif (?:we|they|you) (?:allow|accept|permit)\S*[^.!?]{0,60}\b(?:soon|next|then)\b",
            r"\bwill inevitably lead to\b",
            r"\ba? first steps? toward\b",
            r"\bopens? the door to\b",
        ],
    },
    {
        "id": "generalisation_abusive",
        "category": "sophisme",
        "weight": 6,
        "patterns": [
            r"\ball [a-z]+ are\b",
            r"\bnone of (?:them|us) (?:ever|is|are)\b",
            r"\balways\b[^.!?]{0,40}\b(?:them|they)\b",
            r"\beveryone knows\b",
        ],
    },
    {
        "id": "ad_hominem",
        "category": "sophisme",
        "weight": 7,
        "patterns": [
            r"\b(?:he|she) (?:is|would be) (?:a )?(?:liar|corrupt|a traitor|a sellout|a manipulator)\b",
            r"\bthose people (?:are|want)\b",
            r"\bdon['’]?t listen to (?:him|her),? (?:he['’]?s|she['’]?s|it['’]?s)\b",
        ],
    },
    {
        "id": "autorite_vague",
        "category": "sophisme",
        "weight": 6,
        "patterns": [
            r"\bexperts (?:say|claim|confirm|reveal)\b",
            r"\bscientists (?:say|claim|confirm|have proven)\b",
            r"\ba (?:recent |international )?study (?:shows|proves|reveals)\b(?![^.!?]{0,60}\b(?:from |by )?(?:university|journal|published)\b)",
        ],
    },
    {
        "id": "complot",
        "category": "sophisme",
        "weight": 10,
        "patterns": [
            r"\bthey don['’]?t want you to know\b",
            r"\bthe truth (?:they['’]?re hiding|hidden from you)\b",
            r"\bthey['’]?re hiding (?:the truth|something)\b",
            r"\bwake up\b",
            r"\bthe conspiracy\b",
        ],
    },
    {
        "id": "detournement_whataboutism",
        "category": "sophisme",
        "weight": 7,
        "patterns": [
            r"\band you,? what did you do when\b",
            r"\blet['’]?s talk about\b[^.!?]{0,40}\b(?:them|him|her|your)\b",
            r"\blook first at what\b",
        ],
    },
    {
        "id": "homme_de_paille",
        "category": "sophisme",
        "weight": 5,
        "patterns": [
            r"\bwhat [a-z]+ really means is\b",
            r"\bin reality,? they want\b",
            r"\bunder the guise of\b[^.!?]{0,50}\bthey actually want\b",
        ],
    },
]
