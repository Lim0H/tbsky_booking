from typing import Optional

from fastapi import Cookie, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from ..security import decode_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

__all__ = ["get_user_id_by_access_token"]


async def get_user_id_by_access_token(
    access_token_from_header: Optional[str] = Depends(oauth2_scheme),
    access_token: Optional[str] = Cookie(None),
) -> str:
    from ..repository import BlackListTokenRepository

    black_list_token_repository = BlackListTokenRepository()
    if access_token := (access_token_from_header or access_token):
        access_token_payload = decode_jwt_token(access_token)
        user_id: str = access_token_payload.get("sub")  # type: ignore

        if await black_list_token_repository.get(access_token):
            raise HTTPException(status_code=401, detail="Invalid access token")

        return user_id

    raise HTTPException(status_code=401, detail="Invalid access token")
