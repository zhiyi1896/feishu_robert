import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import get_settings
from app.repositories.mysql_client import mysql_client
from app.repositories.push_repository import PushRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.services.employee_service import EmployeeService
from app.services.feishu_service import FeishuService
from app.services.push_service import PushService

class SchedulerService:

    def __init__(self):
        pass

    async def start_push_scheduler(self):

        settings = get_settings()

        async with mysql_client.session_factory() as session:

            push_repository = PushRepository(session)
            task_repository = TaskRepository(session)
            user_repository = UserRepository(session)

            employee_service = EmployeeService(user_repository)
            feishu_service = FeishuService(settings)

            push_service = PushService(
                push_repository=push_repository,
                task_repository=task_repository,
                employee_service=employee_service,
                feishu_service=feishu_service,
            )

            await push_service.push_daily_reminders()

    async def start_main(self) -> None:
        mysql_client.init()

        scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
        scheduler.add_job(
            self.start_push_scheduler,
            trigger="interval",
            minutes=1,
            # trigger="cron",
            # hour=9,
            # minute=0,
            id="daily_task_push",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=300,
        )
        scheduler.start()

        try:
            while True:
                await asyncio.sleep(3600)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()


# if __name__ == '__main__':
#     asyncio.run(SchedulerService().start_main())