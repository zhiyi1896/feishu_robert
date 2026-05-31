from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Employee(Base):
    """员工主数据模型。"""

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="员工主键ID")
    employee_no: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, comment="员工编号")
    name: Mapped[str] = mapped_column(String(128), nullable=False, comment="员工姓名")
    feishu_open_id: Mapped[str | None] = mapped_column(String(128), unique=True, nullable=True, comment="飞书 open_id，用于机器人消息身份映射")
    feishu_user_id: Mapped[str | None] = mapped_column(String(128), unique=True, nullable=True, comment="飞书 user_id，用于通讯录接口")
    job_level: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="员工职级，例如 P5、P6、M1")
    department_name: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="员工所在部门名称")
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True, comment="直属上级员工ID")
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, comment="员工是否有效")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False, comment="记录创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="记录更新时间")

    # 直属上级对象。
    manager: Mapped["Employee | None"] = relationship(remote_side=[id], back_populates="subordinates")
    # 下属员工列表。
    subordinates: Mapped[list["Employee"]] = relationship(back_populates="manager")