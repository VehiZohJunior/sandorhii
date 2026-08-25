"""Bibliotheque de sophismes (manipulation rhetorique) - francais, v1.

Chaque regle est un motif regex applique phrase par phrase. Les poids sont
volontairement modestes : un seul signal ne doit jamais, a lui seul, faire
basculer un texte en "trompeur" - c'est l'accumulation qui compte.

Le libelle et l'explication de chaque regle (par id) vivent cote frontend
(messages/fr.json, messages/en.json, cle home.signalCatalog) et non ici,
pour eviter d'avoir deux copies du texte a maintenir en synchro.
"""

FALLACY_RULES_FR = [
    {
        "id": "faux_dilemme",
        "category": "sophisme",
        "weight": 8,
        "patterns": [
            r"\bsoit\b[^.!?]{3,80}\bsoit\b",
            r"\bil n['’ ]?y a que deux (choix|options|solutions)\b",
            r"\bsi vous n['’ ]?\S+tes pas avec (nous|eux)\S*,?\s*vous \S+tes contre\b",
            r"\bc['’ ]?est (?:ça|cela) ou rien\b",
        ],
    },
    {
        "id": "pente_glissante",
        "category": "sophisme",
        "weight": 8,
        "patterns": [
            r"\bsi (?:on|nous|ils) (?:accept|laiss|autoris)\S*[^.!?]{0,60}\b(?:bient[oô]t|ensuite|puis)\b",
            r"\bcela m[eè]nera in[eé]vitablement\b",
            r"\bpremi[eè]re? [eé]tape vers\b",
            r"\bouvre(?:nt|z)? la porte [aà]\b",
        ],
    },
    {
        "id": "generalisation_abusive",
        "category": "sophisme",
        "weight": 6,
        "patterns": [
            r"\btous les [a-zàâäéèêëïîôöùûüç]+ sont\b",
            r"\baucun [a-zàâäéèêëïîôöùûüç]+ ne\b",
            r"\btoujours\b[^.!?]{0,40}\b(?:eux|elles?|ils)\b",
            r"\bcomme (?:tout le monde|d['’ ]?habitude)\b[^.!?]{0,30}\bsait\b",
        ],
    },
    {
        "id": "ad_hominem",
        "category": "sophisme",
        "weight": 7,
        "patterns": [
            r"\b(?:il|elle) (?:est|serait) (?:un[e]? )?(?:menteur|menteuse|corrompu[e]?|manipulateur|manipulatrice|traitre|vendu[e]?)\b",
            r"\bces gens[- ]l[àa] (?:sont|veulent)\b",
            r"\bne (?:l['’ ]?|le |la )[eé]coutez pas,? (?:c['’ ]?est|il est|elle est)\b",
        ],
    },
    {
        "id": "autorite_vague",
        "category": "sophisme",
        "weight": 6,
        "patterns": [
            r"\b(?:des|les) experts? (?:affirment|disent|confirment|r[eé]v[eè]lent)\b",
            r"\b(?:des|les) scientifiques (?:affirment|disent|confirment|ont prouv[eé])\b",
            r"\bune [eé]tude (?:r[eé]cente |internationale )?(?:montre|prouve|r[eé]v[eè]le)\b(?![^.!?]{0,60}\b(?:de l['’ ]?|du |de la |des )?(?:universit[eé]|revue|journal|publi)\b)",
        ],
    },
    {
        "id": "complot",
        "category": "sophisme",
        "weight": 10,
        "patterns": [
            r"\bils ne veulent pas que (?:vous|tu|nous) (?:le )?sach\S+\b",
            r"\bla v[eé]rit[eé] (?:cach[eé]e|qu['’ ]?on vous cache)\b",
            r"\bon (?:vous |nous )?cache (?:la v[eé]rit[eé]|des choses)\b",
            r"\b[eé]veillez[- ]vous\b",
            r"\b(?:le|un) complot\b",
        ],
    },
    {
        "id": "detournement_whataboutism",
        "category": "sophisme",
        "weight": 7,
        "patterns": [
            r"\bet (?:vous|eux|les autres),? (?:qu['’ ]?avez[- ]vous fait|pourquoi ne dites[- ]vous rien)\b",
            r"\bparlons plut[oô]t de\b[^.!?]{0,40}\b(?:eux|lui|elle|votre)\b",
            r"\bregardez d['’ ]?abord ce que\b",
        ],
    },
    {
        "id": "homme_de_paille",
        "category": "sophisme",
        "weight": 5,
        "patterns": [
            r"\bce que [a-zàâäéèêëïîôöùûüç]+ veut vraiment dire,? c['’ ]?est\b",
            r"\ben r[eé]alit[eé],? (?:ils|elles) veulent\b",
            r"\bsous couvert de\b[^.!?]{0,50}\b(?:ils|elles) veulent en fait\b",
        ],
    },
]
