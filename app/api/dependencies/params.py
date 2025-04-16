from typing import Annotated
from fastapi import Depends, Query

from api.dependencies.dependencies import spimex_crud
from crud.spimexs import SpimexCRUD
from schemas.spimex import (
    SpimexFiltersDynamics,
    SpimexFiltersResults,
)


SpimexCrud = Annotated[SpimexCRUD, Depends(spimex_crud)]
SpimexFiltersD = Annotated[SpimexFiltersDynamics, Depends()]
SpimexFiltersR = Annotated[SpimexFiltersResults, Depends()]
LimitDependency = Annotated[int, Query(gt=0, lt=1000)]
OffsetDependency = Annotated[int, Query(ge=0)]
