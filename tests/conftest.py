from typing import Generator
from app.database import Base
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.dependency import get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(
    bind=test_engine,autocommit=False, autoflush=False)

def get_test_db() -> Generator[Session, None, None]:
    with TestSessionLocal.begin() as db:
        yield db

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    with TestSessionLocal() as db:
            yield db

app.dependency_overrides[get_db] = get_test_db

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True, scope="function")
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)