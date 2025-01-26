import base64
from datetime import UTC, datetime

import dateparser
import jwt
from cryptography.fernet import Fernet
from fastapi import HTTPException

from .config import AppSettings

__all__ = ["decode_jwt_token", "PublicSafelyBase64Tools", "Base64Tools", "CryptoTools"]


class CryptoTools:
    @classmethod
    def encrypt(cls, value: str) -> str:
        return (
            Fernet(AppSettings.security.CRYPTO_KEY.get_secret_value())
            .encrypt(value.encode("utf-8"))
            .decode("utf-8")
        )

    @classmethod
    def decrypt(cls, value: str) -> str:
        return (
            Fernet(AppSettings.security.CRYPTO_KEY.get_secret_value())
            .decrypt(value.encode("utf-8"))
            .decode("utf-8")
        )


class Base64Tools:
    @classmethod
    def encode(cls, value: str) -> str:
        return base64.urlsafe_b64encode(value.encode("ascii")).decode("ascii")

    @classmethod
    def decode(cls, value: str) -> str:
        return base64.urlsafe_b64decode(value).decode("utf-8")


class PublicSafelyBase64Tools:
    base64 = Base64Tools
    crypto = CryptoTools

    @classmethod
    def encode(cls, value: str) -> str:
        return cls.base64.encode(cls.crypto.encrypt(value))

    @classmethod
    def decode(cls, value: str) -> str:
        return cls.crypto.decrypt(cls.base64.decode(value))


def decode_jwt_token(token: str) -> dict:
    try:
        payload: dict = jwt.decode(
            token,
            AppSettings.security.SECRET_KEY.get_secret_value(),
            algorithms=[AppSettings.security.JWT_ALGORITHM],
        )
        expire = dateparser.parse(payload.pop("expire"))
        if expire is None:
            raise jwt.InvalidTokenError
        if datetime.now(UTC).replace(tzinfo=None) > expire:
            raise jwt.ExpiredSignatureError
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token expired, please log in again"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
