from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result

from core.models import Spimex

from schemas.spimex import (
    SpimexFiltersDynamics,
    SpimexFiltersResults,
    SpimexTradingDate,
)


class SpimexCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_last_trading_dates(
        self, limit: int, offset: int
    ) -> list[SpimexTradingDate]:
        stmt_dates = (
            select(Spimex.date)
            .group_by(Spimex.date)
            .order_by(Spimex.date.desc())
            .limit(limit)
            .offset(offset)
        )
        result_dates: Result = await self.session.execute(stmt_dates)
        dates = result_dates.scalars().all()

        return [SpimexTradingDate(date=d) for d in dates]

    async def get_dynamics(
        self,
        filters: SpimexFiltersDynamics,
        limit: int,
        offset: int,
    ) -> list[Spimex]:
        stmt = select(Spimex)

        if filters.oil_id:
            stmt = stmt.where(Spimex.oil_id == filters.oil_id)

        if filters.delivery_basis_id:
            stmt = stmt.where(Spimex.delivery_basis_id == filters.delivery_basis_id)

        if filters.delivery_type_id:
            stmt = stmt.where(Spimex.delivery_type_id == filters.delivery_type_id)

        if filters.start_date:
            stmt = stmt.where(Spimex.date >= filters.start_date)

        if filters.end_date:
            stmt = stmt.where(Spimex.date <= filters.end_date)

        stmt = stmt.order_by(Spimex.date.desc()).limit(limit).offset(offset)

        result: Result = await self.session.execute(stmt)
        dynamics = result.scalars().all()

        return list(dynamics)

    async def get_trading_results(
        self,
        filters: SpimexFiltersResults,
        limit: int,
        offset: int,
    ) -> list[Spimex]:
        stmt = select(Spimex)

        if filters.oil_id:
            stmt = stmt.where(Spimex.oil_id == filters.oil_id)

        if filters.delivery_basis_id:
            stmt = stmt.where(Spimex.delivery_basis_id == filters.delivery_basis_id)

        if filters.delivery_type_id:
            stmt = stmt.where(Spimex.delivery_type_id == filters.delivery_type_id)

        stmt = stmt.order_by(Spimex.date.desc()).limit(limit).offset(offset)

        result: Result = await self.session.execute(stmt)
        results = result.scalars().all()

        return list(results)
