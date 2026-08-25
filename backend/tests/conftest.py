import os

os.environ["DATABASE_URL"] = "sqlite:///./test_sandorhii.db"
os.environ["ADMIN_PASSWORD"] = "test-password"

import pytest
from fastapi.testclient import TestClient

from app.core.db import Base, engine
from app.core.limiter import limiter
from app.main import app


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Le limiteur de debit est un singleton global (memoire) - sans ce
    # reset, un test qui epuise sa limite ferait echouer les tests
    # suivants avec des 429 inattendus.
    limiter.reset()
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def admin_headers():
    return {"X-Admin-Password": "test-password"}
