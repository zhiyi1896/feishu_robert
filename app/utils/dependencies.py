from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.mysql_client import mysql_client
from app.repositories.task_repository import TaskRepository
from app.services.nlp_service import NLPService
from app.services.task_service import TaskService
from app.repositories.user_repository import UserRepository
from app.repositories.project_repository import ProjectRepository
from app.services.employee_service import EmployeeService
from app.services.project_service import ProjectService
from app.mapper.to_task_mapper import TaskMapper




# Repository 工厂函数（不是实例）
def create_task_repository(session: AsyncSession) -> TaskRepository:
    """创建 TaskRepository 实例"""
    return TaskRepository(db_session=session)

def create_user_repository(session: AsyncSession) -> UserRepository:
    """创建 UserRepository 实例"""
    return UserRepository(db_session=session)

def create_project_repository(session: AsyncSession) -> ProjectRepository:
    """创建 ProjectRepository 实例"""
    return ProjectRepository(db_session=session)


async def get_session():
    """获取数据库会话"""
    async with mysql_client.session_factory() as session:

        yield session


async def get_task_service(session: AsyncSession = Depends(get_session)) -> TaskService:
    """获取 TaskService 实例"""
    repository = create_task_repository(session)
    return TaskService(mysql_repository=repository)


async def get_employee_service(session: AsyncSession = Depends(get_session)) -> EmployeeService:
    """获取 EmployeeService 实例"""
    repository = create_user_repository(session)
    return EmployeeService(mysql_repository=repository)


async def get_project_service(session: AsyncSession = Depends(get_session)) -> ProjectService:
    """获取 ProjectService 实例"""
    repository = create_project_repository(session)
    return ProjectService(mysql_repository=repository)


async def get_nlp_service() -> NLPService:
    """获取 EmployeeService 实例"""
    return NLPService()


async def get_task_mapper(
    employee_service: EmployeeService = Depends(get_employee_service),
    project_service: ProjectService = Depends(get_project_service),
) -> TaskMapper:
    return TaskMapper(employee_service=employee_service, project_service=project_service)


# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.repositories.mysql_client import mysql_client
# from app.repositories.task_repository import TaskRepository
# from app.services.task_service import TaskService
#
# mysql_repository = None
#
#
# def init():
#     global mysql_repository
#     mysql_repository = TaskRepository(None)
#
# async def get_session():
#     async with mysql_client.session_factory() as session:
#         yield session
#
# async def get_mysql_repository(session: AsyncSession = Depends(get_session)):
#
#     mysql_repository.db_session = session
#     return mysql_repository
#
# async def get_query_service(
#         mysql_repository: TaskRepository = Depends(get_mysql_repository)
# ) -> TaskService:
#     return TaskService(
#         mysql_repository=mysql_repository
#     )

