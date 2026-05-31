from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Employee

class UserRepository:

    def __init__(self, db_session: AsyncSession | None):
        self.db_session = db_session

    async def get_employee_id_by_name(self, assignee_name):

        stmt = select(Employee.id).where(Employee.name == assignee_name)
        result = await self.db_session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_current_user_id(self, open_id):

        stmt = select(Employee.id).where(Employee.feishu_open_id  == open_id)
        result = await self.db_session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_employee_by_creator_id(self, creator_id):

        stmt = select(Employee.name).where(Employee.id == creator_id)
        result = await self.db_session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_subordinate_ids(self, id):

        stmt = select(Employee.id).where(Employee.manager_id == id)
        result = await self.db_session.execute(stmt)

        return list(result.scalars().all())

    async def get_open_id_by_employee_id(self, employee_id):

        stmt = select(Employee.feishu_open_id).where(Employee.id == employee_id)
        result = await self.db_session.execute(stmt)

        return result.scalar_one_or_none()

