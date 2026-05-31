import uuid
from datetime import datetime,timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task, Employee
from app.schemas import TaskCreateRequest, TaskQueryRequest
from sqlalchemy import and_, or_
from sqlalchemy.future import select
from sqlalchemy import update

class TaskRepository:

    def __init__(self, db_session:AsyncSession| None):
        self.db_session = db_session

    async def create_task(self,query: TaskCreateRequest):

        task = Task(
            task_no=str(uuid.uuid4()),
            title=query.title,
            content=query.content,
            task_type=query.task_type,
            priority=query.priority,
            creator_id=query.creator_id,
            assignee_id=query.assignee_id,
            project_id=query.project_id,
            start_time=query.start_time,
            due_time=query.due_time,
            end_time=query.end_time,
            source_text=query.source_text,
            status="待办",
        )

        self.db_session.add(task)
        await self.db_session.flush()
        await self.db_session.refresh(task)

        return  task

    async def search_tasks(self, query: TaskQueryRequest):

        # Build dynamic query conditions.
        conditions = []

        if query.creator_id is not None:
            conditions.append(Task.creator_id == query.creator_id)

        if query.assignee_id is not None:
            conditions.append(Task.assignee_id == query.assignee_id)

        if query.project_id is not None:
            conditions.append(Task.project_id == query.project_id)

        if query.task_type is not None:
            conditions.append(Task.task_type == query.task_type)

        if query.status is not None:
            conditions.append(Task.status == query.status)

        if query.priority is not None:
            conditions.append(Task.priority == query.priority)

        if query.keyword is not None:
            keyword_pattern = f"%{query.keyword}%"
            conditions.append(
                or_(
                    Task.title.like(keyword_pattern),
                    Task.content.like(keyword_pattern)
                )
            )

        if query.created_from is not None:
            conditions.append(Task.created_at >= query.created_from)

        if query.created_to is not None:
            conditions.append(Task.created_at <= query.created_to)

        if query.due_from is not None:
            conditions.append(Task.due_time >= query.due_from)

        if query.due_to is not None:
            conditions.append(Task.due_time <= query.due_to)

        stmt = select(Task)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.order_by(Task.created_at.desc())

        result = await self.db_session.execute(stmt)
        tasks = result.scalars().all()

        return list(tasks)

    async def get_employee_by_creator_id(self, creator_id):

        stmt = select(Employee).where(Employee.id == creator_id)
        result = await self.db_session.execute(stmt)

        return result.scalar_one_or_none()


    async def get_employee_by_assignee_id(self, assignee_id):

        stmt = select(Employee).where(Employee.id == assignee_id)
        result = await self.db_session.execute(stmt)

        return result.scalar_one_or_none()

    async def update_task(self, task):

        self.db_session.add(task)
        await self.db_session.flush()
        await self.db_session.refresh(task)
        return task

    async def refresh_overdue_status(self) -> None:
        now = datetime.now()

        stmt = (
            update(Task)
            .where(
                Task.status == "待办",
                Task.due_time.is_not(None),
                Task.due_time < now,
            )
            .values(status="逾期")
        )

        await self.db_session.execute(stmt)

    async def get_pending_tasks_by_assignee(self, employee_id):

        stmt = (
            select(Task).where(
            Task.status == "待办",
            Task.assignee_id == employee_id,
        )
        .order_by(Task.due_time.asc(), Task.created_at.desc()))
        result = await self.db_session.execute(stmt)

        return list(result.scalars().all())

    async def get_due_soon_tasks_by_assignee(self, employee_id):

        stmt = (
            select(Task).where(
                Task.status == "待办",
                Task.assignee_id == employee_id,
                Task.due_time.is_not(None),
                Task.due_time >= datetime.now(),
                Task.due_time <= datetime.now() + timedelta(hours=24),
            )
            .order_by(Task.due_time.asc(), Task.created_at.desc())
            )
        result = await self.db_session.execute(stmt)

        return list(result.scalars().all())

    async def get_overdue_tasks_by_assignee(self, employee_id):

        stmt = (
            select(Task).where(
                Task.status == "逾期",
                Task.assignee_id == employee_id,
            )
            .order_by(Task.due_time.asc(), Task.created_at.desc())
            )
        result = await self.db_session.execute(stmt)

        return list(result.scalars().all())

