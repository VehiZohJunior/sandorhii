from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .core.config import settings
from .core.db import Base, engine
from .core.limiter import limiter
from .modules.linguistic import attribution
from .modules.newsroom.router import router as newsroom_router
from .modules.public.router import router as public_router
from .modules.submissions.router import router as submissions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # Charge les modeles spaCy au demarrage (~7s au total) plutot qu'a la
    # premiere requete utilisateur, qui doit rester rapide (<3s).
    attribution.preload_models()
    yield


app = FastAPI(
    title="SandorHii API",
    description="Plateforme de fact-checking - pilier linguistique (Phase 1)",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(submissions_router)
app.include_router(newsroom_router)
app.include_router(public_router)
