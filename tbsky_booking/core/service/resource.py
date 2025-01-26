from typing import Optional

from fastapi import Cookie, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from ..repository import BlackListTokenRepository
from ..security import decode_jwt_token

__all__ = ["PublicResource", "ProtectedResource", "get_user_id_by_access_token"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


async def get_user_id_by_access_token(
    access_token_from_header: Optional[str] = Depends(oauth2_scheme),
    access_token: Optional[str] = Cookie(None),
    black_list_token_repository: BlackListTokenRepository = Depends(),
) -> str:
    if access_token := (access_token_from_header or access_token):
        access_token_payload = decode_jwt_token(access_token)
        user_id: str = access_token_payload.get("sub")  # type: ignore

        if await black_list_token_repository.get(access_token):
            raise HTTPException(status_code=401, detail="Invalid access token")

        return user_id

    raise HTTPException(status_code=401, detail="Invalid access token")


class PublicResource:
    pass


class ProtectedResource(PublicResource):
    user_id: str = Depends(get_user_id_by_access_token)
