from fastapi import Depends

from ..depends.security import get_user_id_by_access_token

__all__ = ["PublicResource", "ProtectedResource"]


class PublicResource:
    pass


class ProtectedResource(PublicResource):
    user_id: str = Depends(get_user_id_by_access_token)
