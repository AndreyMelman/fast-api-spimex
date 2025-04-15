from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from crud.spimexs import SpimexCRUD


def spimex_crud(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_session),
    ],
) -> SpimexCRUD:
    return SpimexCRUD(session)