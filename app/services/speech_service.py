from openai import OpenAI
from app.config import Settings
import subprocess
from pathlib import Path

class SpeechService:

    def __init__(self, settings: Settings) -> None:
        self.client = OpenAI(
            api_key=settings.api_key2,
            base_url=settings.llm_url2,
        )

    def transcribe_audio(self, file_path: str) -> str:
        """将本地音频文件转写为文本。"""
        with open(file_path, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file,
            )

        return response.text.strip()

    def convert_to_wav(self, source_path: str) -> str:
        source = Path(source_path)
        target = source.with_suffix(".wav")

        subprocess.run(
            [
                r"C:\Users\17431\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe",
                "-y",
                "-i",
                str(source),
                "-ar",
                "16000",
                "-ac",
                "1",
                str(target),
            ],
            check=True,
            capture_output=True,
        )

        return str(target)