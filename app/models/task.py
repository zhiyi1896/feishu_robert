from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Task(Base):
    """任务主表模型。"""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="任务主键ID")
    task_no: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, comment="任务编号")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="任务标题")
    content: Mapped[str | None] = mapped_column(Text, nullable=True, comment="任务详细内容")
    task_type: Mapped[str] = mapped_column(String(64), default="daily", nullable=False, comment="任务类型，例如 daily 或 project")
    status: Mapped[str] = mapped_column(String(32), default="待办", nullable=False, comment="任务状态，例如 待办、已完成、逾期")
    priority: Mapped[str] = mapped_column(String(16), default="P2", nullable=False, comment="任务优先级，例如 P1、P2")
    creator_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, comment="创建人员工ID")
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True, comment="负责人员工ID")
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True, comment="所属项目ID")
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="任务开始时间")
    due_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="任务截止时间")
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="任务完成或关闭时间")
    source_text: Mapped[str | None] = mapped_column(Text, nullable=True, comment="创建任务时的原始文本")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False, comment="记录创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="记录更新时间")

    # 任务创建人对象。
    creator: Mapped["Employee"] = relationship(foreign_keys=[creator_id])
    # 任务负责人对象。
    assignee: Mapped["Employee | None"] = relationship(foreign_keys=[assignee_id])
    # 所属项目对象。
    project: Mapped["Project | None"] = relationship()
    # 任务操作日志列表。
    logs: Mapped[list["TaskLog"]] = relationship(back_populates="task", cascade="all, delete-orphan")