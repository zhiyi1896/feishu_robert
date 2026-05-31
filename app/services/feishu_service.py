import json
import lark_oapi as lark
from lark_oapi.api.im.v1 import ReplyMessageRequest, ReplyMessageRequestBody,CreateMessageRequest,CreateMessageRequestBody
from app.config import Settings
from pathlib import Path
import httpx


class FeishuService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = (
            lark.Client.builder()
            .app_id(settings.feishu_app_id)
            .app_secret(settings.feishu_app_secret)
            .log_level(lark.LogLevel.DEBUG)
            .build()
        )


    def reply_text(self, message_id: str, text: str) -> None:
        request = (
            ReplyMessageRequest.builder()
            .message_id(message_id)
            .request_body(
                ReplyMessageRequestBody.builder()
                .msg_type("text")
                .content(json.dumps({"text": text}, ensure_ascii=False))
                .build()
            )
            .build()
        )

        response = self.client.im.v1.message.reply(request)
        if not response.success():
            raise RuntimeError(
                f"reply failed: code={response.code}, msg={response.msg}, "
                f"log_id={response.get_log_id()}"
            )


    async def send_text_to_open_id(self, open_id: str, message: str) -> None:
        request = (
            CreateMessageRequest.builder()
            .receive_id_type("open_id")
            .request_body(
                CreateMessageRequestBody.builder()
                .receive_id(open_id)
                .msg_type("text")
                .content(json.dumps({"text": message}, ensure_ascii=False))
                .build()
            )
            .build()
        )

        response = self.client.im.v1.message.create(request)
        if not response.success():
            raise RuntimeError(
                f"send message failed: code={response.code}, msg={response.msg}, "
                f"log_id={response.get_log_id()}"
            )

    async def get_tenant_access_token(self) -> str:
        """获取 tenant_access_token。"""
        request = lark.BaseRequest.builder() \
            .http_method(lark.HttpMethod.POST) \
            .uri("/open-apis/auth/v3/tenant_access_token/internal") \
            .body(
            {
                "app_id": self.settings.feishu_app_id,
                "app_secret": self.settings.feishu_app_secret,
            }
        ) \
            .build()

        response = self.client.request(request)
        data = json.loads(response.raw.content)

        if data.get("code") != 0:
            raise RuntimeError(
                f"get tenant_access_token failed: code={data.get('code')}, msg={data.get('msg')}"
            )

        return data["tenant_access_token"]


    async def download_audio_file(
            self,
            message_id: str,
            file_key: str,
            save_path: str,
    ) -> str:
        """
        根据 message_id 和 file_key 下载飞书语音消息到本地。
        """
        token = await self.get_tenant_access_token()

        url = (
            f"https://open.feishu.cn/open-apis/im/v1/messages/"
            f"{message_id}/resources/{file_key}?type=file"
        )

        headers = {
            "Authorization": f"Bearer {token}",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

            if response.status_code != 200:
                try:
                    error_data = response.json()
                except Exception:
                    error_data = {}

                raise RuntimeError(
                    f"download audio failed: status={response.status_code}, "
                    f"error={error_data.get('msg', 'unknown')}, "
                    f"log_id={response.headers.get('X-Request-Id', 'N/A')}"
                )

            target = Path(save_path)
            target.write_bytes(response.content)
            return str(target)