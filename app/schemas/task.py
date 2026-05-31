from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreateRequest(BaseModel):
    """创建任务请求对象。"""

    title: str = Field(..., description='任务标题')
    content: str | None = Field(default=None, description='任务详细内容')
    task_type: str = Field(default='daily', description='任务类型，如 daily 或 project')
    priority: str = Field(default='P2', description='任务优先级，如 P1、P2、P3、P4')
    creator_id: int = Field(..., description='创建人员工ID')
    assignee_id: int | None = Field(default=None, description='负责人员工ID')
    project_id: int | None = Field(default=None, description='关联项目ID')
    start_time: datetime | None = Field(default=None, description='任务开始时间')
    due_time: datetime | None = Field(default=None, description='任务截止时间')
    end_time: datetime | None = Field(default=None, description='任务结束时间')
    source_text: str | None = Field(default=None, description='原始输入文本')


class TaskQueryRequest(BaseModel):
    """任务查询请求对象。"""

    creator_id: int | None = Field(default=None, description='按创建人员工ID筛选')
    assignee_id: int | None = Field(default=None, description='按负责人员工ID筛选')
    project_id: int | None = Field(default=None, description='按关联项目ID筛选')
    task_type: str | None = Field(default=None, description='按任务类型筛选')
    status: str | None = Field(default=None, description='按任务状态筛选')
    priority: str | None = Field(default=None, description='按任务优先级筛选')
    keyword: str | None = Field(default=None, description='按标题或内容关键字筛选')
    created_from: datetime | None = Field(default=None, description='创建时间起始')
    created_to: datetime | None = Field(default=None, description='创建时间截止')
    due_from: datetime | None = Field(default=None, description='截止时间起始')
    due_to: datetime | None = Field(default=None, description='截止时间截止')


class TaskResponse(BaseModel):
    """任务响应对象。"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='任务主键')
    task_no: str = Field(..., description='任务编号')
    title: str = Field(..., description='任务标题')
    content: str | None = Field(default=None, description='任务详细内容')
    task_type: str = Field(..., description='任务类型')
    status: str = Field(..., description='任务状态')
    priority: str = Field(..., description='任务优先级')
    creator_id: int = Field(..., description='创建人员工ID')
    assignee_id: int | None = Field(default=None, description='负责人员工ID')
    project_id: int | None = Field(default=None, description='关联项目ID')
    start_time: datetime | None = Field(default=None, description='任务开始时间')
    due_time: datetime | None = Field(default=None, description='任务截止时间')
    end_time: datetime | None = Field(default=None, description='任务结束时间')
    source_text: str | None = Field(default=None, description='原始输入文本')
    created_at: datetime = Field(..., description='记录创建时间')
    updated_at: datetime = Field(..., description='记录更新时间')
