"""Limiteur de débit - protège l'hébergement gratuit contre les abus/spam.

En mémoire (pas de Redis) : suffisant pour une seule instance backend a ce
stade. A revoir si on passe un jour a plusieurs instances (Phase 4).
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
