from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EmployeeResponse(BaseModel):
    """员工响应对象。"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="员工主键ID")
    employee_no: str = Field(..., description="员工编号")
    name: str = Field(..., description="员工姓名")
    feishu_open_id: str | None = Field(default=None, description="飞书 open_id")
    feishu_user_id: str | None = Field(default=None, description="飞书 user_id")
    job_level: str | None = Field(default=None, description="员工职级，例如 P5、P6、M1")
    department_name: str | None = Field(default=None, description="部门名称")
    manager_id: int | None = Field(default=None, description="直属上级员工ID")
    is_active: bool = Field(..., description="员工是否有效")
    created_at: datetime = Field(..., description="记录创建时间")
    updated_at: datetime = Field(..., description="记录更新时间")