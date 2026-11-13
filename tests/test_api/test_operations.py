from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User, Wallet
from tests.conftest import db_session


def test_add_expense_succsess(db_session: Session, client):
    #Arrange
    user = User(login="test", email="testuser@example.com", hashed_password="hashedpassword")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=100.0, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    #Act
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 50.0,
            "description": "Test expense",
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    #Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Expense added successfully",
        "wallet_name": wallet.name,
        "description": "Test expense",
        "balance": 50.0,
    }

def test_add_expense_negative_amount(db_session: Session, client):
    #Arrange
    user = User(login="test", email="testuser@example.com", hashed_password="hashedpassword")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=100.0, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    #Act
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": -50.0,
            "description": "Test expense",
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    #Assert
    assert response.status_code == 422
    assert "Amount must be a positive number" in response.json()["detail"][0]["msg"]

def test_add_expense_insufficient_funds(db_session: Session, client: TestClient):
    #Arrange
    user = User(login="test", email="testuser@example.com", hashed_password="hashedpassword")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=100.0, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    #Act
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 150.0,
            "description": "Test expense",
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    #Assert
    assert response.status_code == 400
    assert "Insufficient funds" in response.json()["detail"]

def test_add_expense_wallet_not_found(db_session: Session, client: TestClient):
    #Arrange
    user = User(login="test", email="testuser@example.com", hashed_password="hashedpassword")
    db_session.add(user)
    db_session.commit()

    wallet_name = "nonexistent"

    #Act
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": wallet_name,
            "amount": 50.0,
            "description": "Test expense",
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    #Assert
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Wallet '{wallet_name}' not found"
    }

