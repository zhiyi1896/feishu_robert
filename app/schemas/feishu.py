from typing import Any

from pydantic import BaseModel, Field


class FeishuEventCallbackRequest(BaseModel):
    """飞书事件回调请求体。"""

    challenge: str | None = Field(default=None, description="URL 校验时返回给飞书的 challenge")
    token: str | None = Field(default=None, description="飞书事件校验 token")
    type: str | None = Field(default=None, description="事件类型，例如 url_verification")
    schema_: str | None = Field(default=None, alias="schema", description="飞书事件协议版本")
    header: dict[str, Any] | None = Field(default=None, description="事件头信息")
    event: dict[str, Any] | None = Field(default=None, description="事件主体内容")