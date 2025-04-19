from typing import Annotated
from fastapi import Depends

from api.dependencies.dependencies import spimex_crud
from crud.spimexs import SpimexCRUD
from schemas.spimex import (
    SpimexFiltersDynamics,
    SpimexFiltersResults,
    Pagination,
)

SpimexCrud = Annotated[SpimexCRUD, Depends(spimex_crud)]
SpimexFiltersD = Annotated[SpimexFiltersDynamics, Depends()]
SpimexFiltersR = Annotated[SpimexFiltersResults, Depends()]
PaginationDep = Annotated[Pagination, Depends()]
