from datetime import datetime

from pydantic import BaseModel, Field


class TaskCommandParseResponse(BaseModel):
    """自然语言解析结果。"""

    intent: str = Field(..., description='识别出的意图，例如 create_task 或 query_task')
    raw_text: str = Field(..., description='用户原始输入文本')

    title: str | None = Field(default=None, description='解析出的任务标题')
    content: str | None = Field(default=None, description='解析出的任务内容')
    task_type: str | None = Field(default=None, description='解析出的任务类型')
    priority: str | None = Field(default=None, description='解析出的任务优先级')

    creator_name: str | None = Field(default=None, description='解析出的创建人姓名')
    assignee_name: str | None = Field(default=None, description='解析出的负责人姓名')
    project_name: str | None = Field(default=None, description='解析出的项目名称')

    start_time: datetime | None = Field(default=None, description='解析出的开始时间')
    due_time: datetime | None = Field(default=None, description='解析出的截止时间')
    end_time: datetime | None = Field(default=None, description='解析出的结束时间')

    status: str | None = Field(default=None, description='解析出的任务状态')
    keyword: str | None = Field(default=None, description='解析出的查询关键字')
    created_from: datetime | None = Field(default=None, description='解析出的创建时间起始')
    created_to: datetime | None = Field(default=None, description='解析出的创建时间截止')
    due_from: datetime | None = Field(default=None, description='解析出的截止时间起始')
    due_to: datetime | None = Field(default=None, description='解析出的截止时间截止')
