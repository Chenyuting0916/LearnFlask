import hashlib
import json

import pytest

from app.services import auth_service
from config.settings import _secret_key


def _use_temp_store(monkeypatch, tmp_path):
    data_dir = tmp_path / "data"
    monkeypatch.setattr(auth_service, "DATA_DIR", str(data_dir))
    monkeypatch.setattr(auth_service, "USERS_FILE", str(data_dir / "users.json"))
    monkeypatch.setattr(auth_service, "RESET_TOKENS_FILE", str(data_dir / "reset_tokens.json"))
    return data_dir


def test_missing_user_store_is_created_empty(monkeypatch, tmp_path):
    data_dir = _use_temp_store(monkeypatch, tmp_path)

    assert auth_service._load_users() == []
    assert json.loads((data_dir / "users.json").read_text()) == []
    assert json.loads((data_dir / "reset_tokens.json").read_text()) == {}


def test_password_hash_is_salted_and_verifies():
    first = auth_service._hash_password("correct-horse")
    second = auth_service._hash_password("correct-horse")

    assert first != second
    assert first != hashlib.sha256(b"correct-horse").hexdigest()
    assert auth_service._check_password(first, "correct-horse")
    assert not auth_service._check_password(first, "wrong-password")


def test_legacy_unsalted_sha256_cannot_login(monkeypatch, tmp_path):
    data_dir = _use_temp_store(monkeypatch, tmp_path)
    data_dir.mkdir()
    legacy = hashlib.sha256(b"password123").hexdigest()
    (data_dir / "users.json").write_text(json.dumps([
        {
            "id": "1",
            "username": "old",
            "email": "old@example.com",
            "password": legacy,
            "created_at": "2025-01-01T00:00:00",
            "subscription_type": "free",
            "subscription_end_date": None,
        }
    ]))

    user, error = auth_service.login_user("old@example.com", "password123")

    assert user is None
    assert error == "電子郵件或密碼不正確"


def test_register_and_login_round_trip(monkeypatch, tmp_path):
    data_dir = _use_temp_store(monkeypatch, tmp_path)

    created, error = auth_service.register_user("ada", "ada@example.com", "correct-horse")
    assert error is None
    assert "password" not in created

    stored = json.loads((data_dir / "users.json").read_text())
    assert stored[0]["password"] != hashlib.sha256(b"correct-horse").hexdigest()

    logged_in, login_error = auth_service.login_user("ada@example.com", "correct-horse")
    assert login_error is None
    assert logged_in["email"] == "ada@example.com"
    assert "password" not in logged_in

    rejected, reject_error = auth_service.login_user("ada@example.com", "wrong-password")
    assert rejected is None
    assert reject_error == "電子郵件或密碼不正確"


def test_production_rejects_missing_or_placeholder_secret(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.delenv("FLASK_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError):
        _secret_key()

    monkeypatch.setenv("FLASK_SECRET_KEY", "your-secret-key")
    with pytest.raises(RuntimeError):
        _secret_key()


def test_dev_without_secret_gets_a_random_key(monkeypatch):
    monkeypatch.delenv("FLASK_ENV", raising=False)
    monkeypatch.delenv("FLASK_SECRET_KEY", raising=False)

    first = _secret_key()
    second = _secret_key()

    assert first != "your-secret-key"
    assert first != second
    assert len(first) >= 32


def test_explicit_secret_is_used(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.setenv("FLASK_SECRET_KEY", "a" * 32)

    assert _secret_key() == "a" * 32
