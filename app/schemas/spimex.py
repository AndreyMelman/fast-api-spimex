import enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date


class PriorityEnum(str, enum.Enum):
    A = "A"
    B = "B"
    C = "D"
    D = "D"
    F = "F"
    J = "J"
    K = "K"
    P = "P"
    R = "R"
    S = "S"
    U = "U"
    W = "W"


class SpimexTradingDate(BaseModel):
    date: Annotated[date, Field(...)]


class SpimexFiltersBase(BaseModel):
    oil_id: Annotated[
        str | None,
        Field(
            min_length=4,
            max_length=4,
            pattern=r"^[A-Z0-9\-]{4}$",
            description="4 символа: заглавные буквы, цифры или дефис (например: A1B-)",
        ),
    ] = None
    delivery_basis_id: Annotated[
        str | None,
        Field(
            min_length=3,
            max_length=3,
            pattern=r"^[A-Z0-9]{3}$",
            description="3 символа: заглавные буквы или цифры",
        ),
    ] = None
    delivery_type_id: Annotated[PriorityEnum | None, Field()] = None
    start_date: Annotated[date | None, Field(validate_default=True)] = None
    end_date: Annotated[date | None, Field(validate_default=True), ] = None

    @field_validator("start_date")
    @classmethod
    def validate_start_date(cls, value):
        if value is not None and value > date.today():
            raise ValueError("дата не может быть больше сегодняшнего дня")
        return value

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, value):
        if value is not None and value > date.today():
            raise ValueError("конец периода не может быть больше сегодняшнего дня")
        return value



class Spimex(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    exchange_product_id: Annotated[str, Field(...)]
    exchange_product_name: Annotated[str, Field(...)]
    oil_id: Annotated[str, Field(...)]
    delivery_basis_id: Annotated[str, Field(...)]
    delivery_basis_name: Annotated[str, Field(...)]
    delivery_type_id: Annotated[str, Field(...)]
    volume: Annotated[float, Field(...)]
    total: Annotated[float, Field(...)]
    count: Annotated[float, Field(...)]
    date: Annotated[date, Field(...)]
