from datetime import datetime,time

from app.schemas import TaskCommandParseResponse, TaskCreateRequest, TaskQueryRequest
from app.services.employee_service import EmployeeService
from app.services.project_service import ProjectService

class TaskMapper:

    def __init__(self,employee_service: EmployeeService, project_service: ProjectService):
        self.employee_service = employee_service
        self.project_service = project_service

    async def to_create_task_mapper(self,parser: TaskCommandParseResponse,current_user_id: int) -> TaskCreateRequest:

        if parser.title is None:
            raise ValueError('任务标题不能为空')

        assignee_id = None
        if parser.assignee_name:
            if parser.assignee_name == "我":
                assignee_id = current_user_id
            else:
                assignee_id = await self.employee_service.get_employee_id_by_name(parser.assignee_name)

        project_id = None
        if parser.project_name:
            project_id = await self.project_service.get_project_id_by_name(parser.project_name)

        return TaskCreateRequest(
            title=parser.title,
            content=parser.content,
            task_type=parser.task_type or "daily",
            priority=parser.priority or "P2",
            creator_id=current_user_id,
            assignee_id=assignee_id,
            project_id=project_id,
            start_time=parser.start_time,
            due_time=parser.due_time,
            end_time=parser.end_time,
            source_text=parser.raw_text
         )


    async def to_query_task_mapper(self,parser: TaskCommandParseResponse,current_user_id: int) -> TaskQueryRequest:

        assignee_id = None
        if parser.assignee_name:
            if parser.assignee_name == "我":
                assignee_id = current_user_id
            else:
                assignee_id = await self.employee_service.get_employee_id_by_name(parser.assignee_name)

        project_id = None
        if parser.project_name:
            project_id = await self.project_service.get_project_id_by_name(parser.project_name)


        creator_id  = None
        if parser.creator_name:
            if parser.creator_name == '我':
                creator_id = current_user_id
            else:
                creator_id = await self.employee_service.get_employee_id_by_name(parser.creator_name)

        if creator_id is None and assignee_id is None:
            creator_id = current_user_id

        due_from = parser.due_from
        due_to = parser.due_to

        if parser.due_time and due_from is None and due_to is None:
            due_from = datetime.combine(parser.due_time.date(), time.min)
            due_to = datetime.combine(parser.due_time.date(), time.max)

        return TaskQueryRequest(
            creator_id=creator_id,
            assignee_id=assignee_id,
            project_id=project_id,
            task_type=parser.task_type,
            status=parser.status,
            priority=parser.priority,
            keyword=parser.keyword,
            created_from=parser.created_from,
            created_to=parser.created_to,
            due_from=due_from,
            due_to=due_to
         )

    async def build_create_reply(self,task,current_user_id,assignee_name: str |  None=None,project_name: str |  None=None):

        current_user_id = await self.employee_service.get_employee_by_id(current_user_id)

        return ("任务已创建\n"
            f"标题：{task.title}\n"
            f"创建人：{current_user_id}\n"
            f"负责人：{assignee_name or '未指派'}\n"
            f"内容：{task.content}\n"
            f"项目：{project_name or '无'}\n"
            f"优先级：{task.priority}\n"
            f"截止时间：{task.due_time}\n"


                )

    async def build_query_reply(self,tasks):

        task_list = []

        if not tasks:
            return "没有找到匹配的任务。"

        for task in tasks:

            creator_name = await self.employee_service.get_employee_by_id(task.creator_id)
            assignee_name = await self.employee_service.get_employee_by_id(task.assignee_id)
            project_name = await self.project_service.get_project_by_id(task.project_id)

            task_list.append(
                f"编号：{task.task_no}\n"
                f"标题：{task.title}\n"
                f"创建人：{creator_name}\n"
                f"负责人：{assignee_name or '未指派'}\n"
                f"内容：{task.content}\n"
                f"项目：{project_name or '无'}\n"
                f"优先级：{task.priority}\n"
                f"截止时间：{task.due_time}\n"
                f"状态：{task.status}\n"
                f"创建时间：{task.created_at}\n"
            )

        return "\n".join(task_list)






