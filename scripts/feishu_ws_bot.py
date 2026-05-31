import asyncio
import json
import sys
from pathlib import Path
import lark_oapi as lark
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1
from app.config import get_settings
from app.mapper.to_task_mapper import TaskMapper
from app.repositories.mysql_client import mysql_client
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.services.employee_service import EmployeeService
from app.services.feishu_service import FeishuService
from app.services.nlp_service import NLPService
from app.services.project_service import ProjectService
from app.services.scheduler_service import SchedulerService
from app.services.speech_service import SpeechService
from app.services.task_service import TaskService
import tempfile
import os
import app.utils.logger

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

settings = get_settings()
feishu_service = FeishuService(settings)


async def build_default_reply(
        text: str,
        sender_open_id: str
                        ) -> str | None:

    """
    整合识别意图，提取文本逻辑，构造回复文本。
    """

    async with mysql_client.session_factory() as session:

        task_repository = TaskRepository(db_session=session)
        employee_repository = UserRepository(db_session=session)
        project_repository = ProjectRepository(db_session=session)

        nlp_service = NLPService()
        employee_service = EmployeeService(mysql_repository=employee_repository)
        project_service = ProjectService(mysql_repository=project_repository)
        task_service = TaskService(mysql_repository=task_repository, employee_service=employee_service)
        task_mapper = TaskMapper(employee_service=employee_service, project_service=project_service)

        current_user_id = await employee_service.get_current_user_id(sender_open_id)
        if current_user_id is None:
            return "未找到当前用户对应的员工信息，请先同步员工数据。"

        parsed  = await nlp_service.router(text)
        print(parsed.model_dump())

        if parsed.intent == NLPService.CREATE_TASK:
            request = await task_mapper.to_create_task_mapper(parsed,current_user_id)
            response = await task_service.create_task(request)
            result = await task_mapper.build_create_reply(response,current_user_id,parsed.assignee_name,parsed.project_name)

        elif parsed.intent == NLPService.QUERY_TASK:
            request = await task_mapper.to_query_task_mapper(parsed,current_user_id)
            print(request.model_dump())
            responses = await task_service.search_tasks(request, current_user_id)
            result = await task_mapper.build_query_reply(responses)

        else:
            result = "我暂时没理解你的任务意图。你可以试试说：帮我创建一个测试任务，明天完成 / 查一下我的任务。"

    return result


async def handle_text_message(message_id: str, text: str, sender_open_id: str) -> None:
    """处理单条文本消息。

    当前只保留最小入口，不做固定格式命令解析。
    后续可以在这里统一接入 NLPService、Mapper 和 TaskService。
    """
    normalized_text = text.strip()
    try:
        reply_text = await build_default_reply(
            normalized_text,
            sender_open_id
        )
    except ValueError as exc:
        reply_text = f"处理失败：{exc}"
    except Exception as exc:
        print(f"处理飞书消息失败: {exc}")
        reply_text = "处理失败，请稍后再试。"

    feishu_service.reply_text(message_id, reply_text)


async def handle_audio_message(
    message_id: str,
    message_content: str,
    sender_open_id: str,
) -> None:
    """
    处理飞书语音消息：
    下载音频 -> 转写文本 -> 复用现有文本任务链路
    """
    speech_service = SpeechService(settings)

    try:
        content = json.loads(message_content or "{}")
    except json.JSONDecodeError:
        content = {}

    file_key = content.get("file_key")
    if not file_key:
        feishu_service.reply_text(message_id, "未找到语音文件信息。")
        return

    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, f"{file_key}.bin")
    wav_path = None



    try:
        await feishu_service.download_audio_file(message_id, file_key, audio_path)
        wav_path = speech_service.convert_to_wav(audio_path)


        print("wav_path :", wav_path)
        print("audio exists:", os.path.exists(wav_path))
        print("audio size:", os.path.getsize(wav_path))

        text = speech_service.transcribe_audio(wav_path)
        print("transcribed text:", text)

        if not text:
            feishu_service.reply_text(message_id, "语音识别结果为空，请重试。")
            return

        reply_text = await build_default_reply(text, sender_open_id)
        feishu_service.reply_text(message_id, reply_text)

    except ValueError as exc:
        feishu_service.reply_text(message_id, f"处理失败：{exc}")
    except Exception as exc:
        print(f"处理语音消息失败: {exc}")
        feishu_service.reply_text(message_id, "语音处理失败，请稍后再试。")
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)



def _log_task_failure(task: asyncio.Task) -> None:
    """打印后台异步任务的异常，避免协程错误被静默吞掉。"""
    try:
        task.result()
    except Exception as exc:
        print(f'处理飞书消息失败: {exc}')



def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    """飞书消息事件入口。"""
    message = data.event.message
    message_id = message.message_id
    sender_open_id = data.event.sender.sender_id.open_id
    loop = asyncio.get_running_loop()

    if message.message_type == "text":
        try:
            content = json.loads(message.content or "{}")
        except json.JSONDecodeError:
            content = {}

        text = content.get("text", "").strip()
        task = loop.create_task(handle_text_message(message_id, text, sender_open_id))
        task.add_done_callback(_log_task_failure)
        return

    if message.message_type == "audio":
        print("audio content:", message.content)
        task = loop.create_task(
            handle_audio_message(message_id, message.content, sender_open_id)
        )
        task.add_done_callback(_log_task_failure)
        return

    feishu_service.reply_text(message_id, "暂时只支持文本和语音消息。")



event_handler = (
    lark.EventDispatcherHandler.builder('', '')
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1)
    .build()
)



def main() -> None:
    """启动飞书长连接客户端。"""
    if not settings.feishu_app_id or not settings.feishu_app_secret:
        raise RuntimeError('缺少 FEISHU_APP_ID 或 FEISHU_APP_SECRET 配置。')

    mysql_client.init()

    # 启动定时任务
    scheduler_service = SchedulerService()
    scheduler_service.start_main()

    ws_client = lark.ws.Client(
        settings.feishu_app_id,
        settings.feishu_app_secret,
        event_handler=event_handler,
        log_level=lark.LogLevel.DEBUG,
    )
    ws_client.start()


if __name__ == '__main__':
    main()
