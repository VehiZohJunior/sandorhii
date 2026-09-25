"""Authentification back-office - version simplifiee phase 1.

Un seul mot de passe partage (variable d'environnement ADMIN_PASSWORD),
verifie via un en-tete X-Admin-Password. Suffisant pour une petite equipe
de lancement ; sera remplace par de vrais comptes Supabase (roles,
JWT, 2FA) des que le projet Supabase existe - voir le blueprint,
section "Auth" du module back-office.
"""

import secrets
import time
from collections import defaultdict, deque

from fastapi import Header, HTTPException, Request, status

from .config import settings

# Limite de tentatives geree ICI, dans la dependance elle-meme, et pas via
# un decorateur @limiter.limit() sur chaque route : quand require_admin()
# leve une HTTPException (mauvais mot de passe), FastAPI resout et rejette
# la requete au niveau de la dependance, AVANT d'appeler le corps de la
# route decore - le decorateur slowapi ne voit donc jamais ces tentatives
# echouees et ne les compte pas (verifie en live : 25 essais avec un
# mauvais mot de passe sont tous passes en 401, aucun 429). En comptant
# ici, chaque tentative - bonne ou mauvaise - est comptee avant meme de
# comparer le mot de passe.
_ATTEMPT_WINDOW_SECONDS = 60
_MAX_ATTEMPTS_PER_WINDOW = 20
_attempts: dict[str, deque] = defaultdict(deque)


def _too_many_attempts(client_ip: str) -> bool:
    now = time.monotonic()
    window = _attempts[client_ip]
    while window and now - window[0] > _ATTEMPT_WINDOW_SECONDS:
        window.popleft()
    if len(window) >= _MAX_ATTEMPTS_PER_WINDOW:
        return True
    window.append(now)
    return False


def require_admin(request: Request, x_admin_password: str = Header(default="")) -> None:
    client_ip = request.client.host if request.client else "unknown"
    if _too_many_attempts(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Trop de tentatives. Reessayez dans une minute.",
        )
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
