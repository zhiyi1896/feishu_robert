import sys
from pathlib import Path

from loguru import logger

from app.config import get_settings

app_config = get_settings()

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

logger.remove()

if app_config.log_console_enable:
    logger.add(
        sink=sys.stdout,
        level=app_config.log_console_level,
        format=log_format,
    )

if app_config.log_file_enable:
    project_root = Path(__file__).parents[2]
    log_dir = project_root / app_config.log_file_path
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.add(
        sink=log_dir / "app.log",
        level=app_config.log_file_level,
        format=log_format,
        rotation=app_config.log_file_rotation,
        retention=app_config.log_file_retention,
        encoding="utf-8",
    )