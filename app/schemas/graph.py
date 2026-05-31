from pydantic import BaseModel, Field


class GraphResponse(BaseModel):
    """图流程返回结果。"""

    response_text: str = Field(..., description="机器人最终回复给用户的文本")