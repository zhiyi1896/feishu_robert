from app.repositories.mysql_client import mysql_client
from app.repositories.push_repository import PushRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.services.employee_service import EmployeeService
from app.services.feishu_service import FeishuService
import asyncio
from app.config import get_settings

class PushService:

    def __init__(self, employee_service: EmployeeService, push_repository: PushRepository, task_repository: TaskRepository,feishu_service: FeishuService,):

        self.employee_service = employee_service
        self.push_repository = push_repository
        self.task_repository = task_repository
        self.feishu_service = feishu_service

    async def push_daily_reminders(self):

        employees_ids = await self.push_repository.get_enabled_employee_ids()

        for employee_id in employees_ids:

            await self.push_one_employee(employee_id)


    async def push_one_employee(self, employee_id):

        pending_tasks = await self.task_repository.get_pending_tasks_by_assignee(employee_id)
        due_soon_tasks = await self.task_repository.get_due_soon_tasks_by_assignee(employee_id)
        overdue_tasks = await self.task_repository.get_overdue_tasks_by_assignee(employee_id)

        if not pending_tasks and not  due_soon_tasks and not overdue_tasks :
            return

        open_id = await self.employee_service.get_open_id_by_employee_id(employee_id)
        if not open_id:
            return

        message = self.build_message(pending_tasks,due_soon_tasks,overdue_tasks)

        await self.feishu_service.send_text_to_open_id(open_id, message)


    def build_message(self, pending_tasks, due_soon_tasks, overdue_tasks)-> str:

        lines = ["今日任务推送"]

        lines.append(f"\n待办任务：共有{len(pending_tasks)}条")
        for task in pending_tasks:
            lines.append(f"- {task.title} | 截止：{task.due_time or '未设置'}")

        lines.append(f"\n临近截止：{len(due_soon_tasks)} 条")
        for task in due_soon_tasks[:5]:
            lines.append(f"- {task.title} | 截止：{task.due_time or '未设置'}")

        lines.append(f"\n逾期任务：{len(overdue_tasks)} 条")
        for task in overdue_tasks[:5]:
            lines.append(f"- {task.title} | 截止：{task.due_time or '未设置'}")

        return "\n".join(lines)


#if __name__ == '__main__':


    # async def main():
    #
    #     settings = get_settings()
    #     mysql_client.init()
    #
    #     async with mysql_client.session_factory() as session:
    #         push_repository = PushRepository(session)
    #         task_repository = TaskRepository(session)
    #         user_repository = UserRepository(session)
    #
    #         employee_service = EmployeeService(user_repository)
    #         feishu_service = FeishuService(settings)
    #
    #         push_service = PushService(
    #             push_repository=push_repository,
    #             task_repository=task_repository,
    #             employee_service=employee_service,
    #             feishu_service=feishu_service,
    #         )
    #
    #         await push_service.push_daily_reminders()
    #
    #
    # asyncio.run(main())