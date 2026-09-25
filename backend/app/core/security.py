"""En-tetes de securite HTTP + limite de taille des requetes.

FastAPI n'ajoute rien de tout ca par defaut. Chaque en-tete corrige un
scenario d'attaque precis (voir commentaires) plutot que d'etre copie
sans raison - inutile d'en ajouter d'autres sans savoir contre quoi.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

MAX_BODY_BYTES = 200_000  # tres large par rapport aux 20 000 caracteres
# max deja imposes par SubmissionCreate : ca ne genera jamais un usage
# legitime, mais ca stoppe un payload de plusieurs Mo avant meme qu'il
# soit parse en JSON.


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        # Empeche le navigateur de "deviner" un autre type de contenu que
        # celui declare (protection contre certaines attaques XSS).
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Interdit d'afficher l'API dans une <iframe> (anti-clickjacking).
        response.headers["X-Frame-Options"] = "DENY"
        # N'envoie jamais l'URL complete (avec ses parametres) comme
        # "referrer" vers un autre site.
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Coupe l'acces a des capteurs que cette API n'utilise jamais,
        # meme si un jour un script tiers malveillant s'y glissait.
        response.headers["Permissions-Policy"] = (
            "geolocation=(), camera=(), microphone=(), payment=()"
        )
        # Ignoree par le navigateur tant que la connexion n'est pas en
        # HTTPS (donc inoffensive en local) ; utile une fois deploye
        # derriere Render/Vercel, qui servent tout en HTTPS.
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        return response


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_BODY_BYTES:
            return JSONResponse(
                status_code=413,
                content={"detail": "Requete trop volumineuse."},
            )
        return await call_next(request)
