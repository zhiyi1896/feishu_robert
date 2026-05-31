from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PushConfigCreateRequest(BaseModel):
    """创建推送配置的请求对象。"""

    employee_id: int = Field(..., description="配置所属员工ID")
    push_time: str = Field(..., description="推送时间，例如 09:00")
    push_scope: str = Field(default="self", description="推送范围，例如 self 或 subordinates")
    push_pending: bool = Field(default=True, description="是否推送待办任务")
    push_due_soon: bool = Field(default=True, description="是否推送临近任务")
    push_overdue: bool = Field(default=True, description="是否推送逾期任务")
    is_enabled: bool = Field(default=True, description="推送配置是否启用")


class PushConfigUpdateRequest(BaseModel):
    """更新推送配置的请求对象。"""

    push_time: str | None = Field(default=None, description="新的推送时间")
    push_scope: str | None = Field(default=None, description="新的推送范围")
    push_pending: bool | None = Field(default=None, description="是否推送待办任务")
    push_due_soon: bool | None = Field(default=None, description="是否推送临近任务")
    push_overdue: bool | None = Field(default=None, description="是否推送逾期任务")
    is_enabled: bool | None = Field(default=None, description="推送配置是否启用")


class PushConfigResponse(BaseModel):
    """推送配置响应对象。"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="推送配置主键ID")
    employee_id: int = Field(..., description="配置所属员工ID")
    push_time: str = Field(..., description="推送时间，例如 09:00")
    push_scope: str = Field(..., description="推送范围")
    push_pending: bool = Field(..., description="是否推送待办任务")
    push_due_soon: bool = Field(..., description="是否推送临近任务")
    push_overdue: bool = Field(..., description="是否推送逾期任务")
    is_enabled: bool = Field(..., description="推送配置是否启用")
    created_at: datetime = Field(..., description="记录创建时间")
    updated_at: datetime = Field(..., description="记录更新时间")