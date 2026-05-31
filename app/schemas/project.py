from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectMemberResponse(BaseModel):
    """项目成员响应对象。"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="项目成员记录主键ID")
    project_id: int = Field(..., description="所属项目ID")
    employee_id: int = Field(..., description="成员员工ID")
    role_name: str | None = Field(default=None, description="成员在项目中的角色名称")
    joined_at: datetime = Field(..., description="加入项目时间")


class ProjectResponse(BaseModel):
    """项目基础响应对象。"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="项目主键ID")
    project_code: str = Field(..., description="项目编号")
    project_name: str = Field(..., description="项目名称")
    owner_id: int | None = Field(default=None, description="项目负责人员工ID")
    status: str = Field(..., description="项目状态")
    created_at: datetime = Field(..., description="记录创建时间")
    updated_at: datetime = Field(..., description="记录更新时间")


class ProjectDetailResponse(ProjectResponse):
    """项目详情响应对象，包含成员列表。"""

    members: list[ProjectMemberResponse] = Field(default_factory=list, description="项目成员列表")