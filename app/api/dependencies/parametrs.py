from typing import Annotated
from fastapi import Depends, Query

from api.dependencies.dependencies import spimex_crud
from crud.spimexs import SpimexCRUD
from schemas.spimex import SpimexFiltersBase


SpimexCrud = Annotated[SpimexCRUD, Depends(spimex_crud)]
SpimexFilters = Annotated[SpimexFiltersBase, Depends()]
LimitDependency = Annotated[int, Query()]
OffsetDependency = Annotated[int, Query()]
