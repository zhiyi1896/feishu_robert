
from loguru import logger
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreateRequest, TaskQueryRequest, TaskResponse
from app.services.employee_service import EmployeeService


class TaskService:
    def __init__(self, mysql_repository: TaskRepository,employee_service: EmployeeService,):

        self.mysql_repository = mysql_repository
        self.employee_service = employee_service


    async def create_task(self, query: TaskCreateRequest) -> TaskResponse:

        await self.validate_create_query(query)

        try:
            task = await self.mysql_repository.create_task(query)
            await self.mysql_repository.db_session.commit()
        except Exception:
            await self.mysql_repository.db_session.rollback()
            raise

        logger.info(f'Created task successfully: {task.task_no}')

        return TaskResponse.model_validate(task)

    async def search_tasks(self, query: TaskQueryRequest, current_user_id: int) -> list[TaskResponse]:

        await self.validate_search_query(query)
        await self.validate_query_permission(query, current_user_id)

        try:
            await self.mysql_repository.refresh_overdue_status()
            tasks = await self.mysql_repository.search_tasks(query)
            await self.mysql_repository.db_session.commit()
        except Exception:
            await self.mysql_repository.db_session.rollback()
            raise

        logger.info(f'Searched tasks successfully: {len(tasks)} items')

        return [TaskResponse.model_validate(task) for task in tasks]


    async def validate_query_permission(self, query: TaskQueryRequest, current_user_id: int):

        subordinate_ids = await self.employee_service.get_all_subordinate_ids(current_user_id)

        allowed_ids = set(subordinate_ids)
        allowed_ids.add(current_user_id)

        if query.creator_id and query.creator_id not in allowed_ids:
            raise ValueError('无权查看该任务')
        if query.assignee_id and query.assignee_id not in allowed_ids:
            raise ValueError('无权查看该任务')


    async def validate_create_query(self, query: TaskCreateRequest):

        if not query.title:
            raise ValueError('任务标题不得为空')

        if len(query.title.strip()) > 255:
            raise ValueError('任务标题长度不得超过 255 个字符')

        if not query.creator_id:
            raise ValueError('任务创建人不得为空')

        if not query.assignee_id:
            raise ValueError('任务负责人不能为空')

        if query.start_time and query.due_time and query.start_time > query.due_time:
            raise ValueError('任务开始时间不得晚于截止时间')

        if query.end_time and query.start_time and query.end_time < query.start_time:
            raise ValueError('任务完成时间不得早于开始时间')

        creator_id = await self.mysql_repository.get_employee_by_creator_id(query.creator_id)
        assignee_id = await self.mysql_repository.get_employee_by_assignee_id(query.assignee_id)

        if not creator_id:
            raise ValueError('任务创建人不存在')

        if query.assignee_id and not assignee_id:
            raise ValueError('任务负责人不存在')

    async def validate_search_query(self, query: TaskQueryRequest):

        if query.created_from and query.created_to and query.created_from > query.created_to:
            raise ValueError("创建开始时间不能晚于创建结束时间")

        if query.due_from and query.due_to and query.due_from > query.due_to:
            raise ValueError("截止开始时间不能晚于截止结束时间")

