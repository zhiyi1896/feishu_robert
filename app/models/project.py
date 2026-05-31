from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Project(Base):
    """项目主数据模型。"""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="项目主键ID")
    project_code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, comment="项目编号")
    project_name: Mapped[str] = mapped_column(String(128), nullable=False, comment="项目名称")
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True, comment="项目负责人员工ID")
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False, comment="项目状态，例如 active 或 closed")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False, comment="记录创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="记录更新时间")

    # 项目负责人对象。
    owner: Mapped["Employee | None"] = relationship()
    # 项目成员关联列表。
    members: Mapped[list["ProjectMember"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class ProjectMember(Base):
    """项目成员关联模型。"""

    __tablename__ = "project_members"
    __table_args__ = (UniqueConstraint("project_id", "employee_id", name="uk_project_members_project_employee"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="项目成员记录主键ID")
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="所属项目ID")
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="成员员工ID")
    role_name: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="成员在项目中的角色名称")
    joined_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False, comment="加入项目时间")

    # 所属项目对象。
    project: Mapped[Project] = relationship(back_populates="members")
    # 项目成员员工对象。
    employee: Mapped["Employee"] = relationship()