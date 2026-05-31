from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, mysql_repository: ProjectRepository):

        self.mysql_repository = mysql_repository

    async def get_project_id_by_name(self, project_name):

        project_id = await self.mysql_repository.get_project_id_by_name(project_name)

        return project_id

    async def get_project_by_id(self, project_id):

        project_name = await self.mysql_repository.get_project_by_id(project_id)

        return project_name