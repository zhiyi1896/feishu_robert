from fastapi import FastAPI

from app.api.feishu_webhook import router as feishu_webhook_router
from app.api.health import router as health_router
from app.api.tasks import router as tasks_router

import uuid

def create_app() -> FastAPI:
    app = FastAPI(title="Feishu Task Bot")
    app.include_router(health_router)
    app.include_router(feishu_webhook_router, prefix="/api/feishu", tags=["feishu"])
    app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
    return app


app = create_app()

