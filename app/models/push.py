from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PushConfig(Base):
    """定时推送配置模型。"""

    __tablename__ = "push_configs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="推送配置主键ID")
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="配置所属员工ID")
    push_time: Mapped[str] = mapped_column(String(16),default="09:00", nullable=False, comment="推送时间，例如 09:00")
    push_scope: Mapped[str] = mapped_column(String(32), default="self", nullable=False, comment="推送范围，例如 self 或 subordinates")
    push_pending: Mapped[bool] = mapped_column(default=True, nullable=False, comment="是否包含待办任务")
    push_due_soon: Mapped[bool] = mapped_column(default=True, nullable=False, comment="是否包含临近任务")
    push_overdue: Mapped[bool] = mapped_column(default=True, nullable=False, comment="是否包含逾期任务")
    is_enabled: Mapped[bool] = mapped_column(default=True, nullable=False, comment="推送配置是否启用")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False, comment="记录创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="记录更新时间")

    # 配置所属员工对象。
    employee: Mapped["Employee"] = relationship()