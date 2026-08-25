"""Authentification back-office - version simplifiee phase 1.

Un seul mot de passe partage (variable d'environnement ADMIN_PASSWORD),
verifie via un en-tete X-Admin-Password. Suffisant pour une petite equipe
de lancement ; sera remplace par de vrais comptes Supabase (roles,
JWT, 2FA) des que le projet Supabase existe - voir le blueprint,
section "Auth" du module back-office.
"""

import secrets

from fastapi import Header, HTTPException, status

from .config import settings


def require_admin(x_admin_password: str = Header(default="")) -> None:
    # secrets.compare_digest plutot que "!=" : une comparaison naive fuit
    # la longueur du mot de passe correct via le temps de reponse (timing
    # attack). Peu probable a ce stade, mais gratuit a corriger.
    valid = bool(settings.admin_password) and secrets.compare_digest(
        x_admin_password, settings.admin_password
    )
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe back-office invalide ou manquant.",
        )
