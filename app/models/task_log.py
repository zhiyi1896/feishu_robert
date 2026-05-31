from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TaskLog(Base):
    """任务操作日志模型。"""

    __tablename__ = "task_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="日志主键ID")
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="关联任务ID")
    operator_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True, comment="操作人员工ID")
    action_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作类型，例如 create、update、complete")
    action_detail: Mapped[str | None] = mapped_column(Text, nullable=True, comment="操作详情说明")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False, comment="日志创建时间")

    # 所属任务对象。
    task: Mapped["Task"] = relationship(back_populates="logs")
    # 操作人对象。
    operator: Mapped["Employee | None"] = relationship()