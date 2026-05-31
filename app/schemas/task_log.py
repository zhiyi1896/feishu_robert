from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskLogResponse(BaseModel):
    """任务日志响应对象。"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="日志主键ID")
    task_id: int = Field(..., description="关联任务ID")
    operator_id: int | None = Field(default=None, description="操作人员工ID")
    action_type: str = Field(..., description="操作类型")
    action_detail: str | None = Field(default=None, description="操作详情说明")
    created_at: datetime = Field(..., description="日志创建时间")