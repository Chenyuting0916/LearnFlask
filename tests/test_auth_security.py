import hashlib

from app.services.auth_service import _check_password, _hash_password, _validate_password


def test_password_hash_is_salted_and_verifies():
    stored = _hash_password("correct-horse")
    assert stored != "correct-horse"
    assert not stored == hashlib.sha256(b"correct-horse").hexdigest()
    assert _check_password(stored, "correct-horse")
    assert not _check_password(stored, "wrong-password")


def test_legacy_unsalted_sha256_is_rejected():
    legacy = hashlib.sha256(b"password123").hexdigest()
    assert _check_password(legacy, "password123") is False


def test_short_password_is_rejected():
    assert _validate_password("short")
    assert _validate_password("long-enough") is None
