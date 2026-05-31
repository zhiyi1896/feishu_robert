from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import PushConfig


class PushRepository:

    def __init__(self, db_session: AsyncSession | None):
        self.db_session = db_session

    async def get_enabled_employee_ids(self):

        stmt = select(PushConfig.employee_id).where(PushConfig.is_enabled == 1)
        result = await self.db_session.execute(stmt)

        return list(result.scalars().all())

