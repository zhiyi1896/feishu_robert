from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Project
from sqlalchemy.future import select

class ProjectRepository:

    def __init__(self, db_session: AsyncSession | None):
        self.db_session = db_session

    async def get_project_id_by_name(self, project_name):

        stmt = select(Project.id).where(Project.project_name == project_name)
        result = await self.db_session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_project_by_id(self, project_id):

        stmt = select(Project.project_name).where(Project.id == project_id)
        result = await self.db_session.execute(stmt)

        return result.scalar_one_or_none()