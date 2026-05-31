from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import get_settings
import asyncio
from sqlalchemy import text

class MySQLClient:

    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self.engine = None
        self.session_factory = None

    def init(self):

        self.engine = create_async_engine(  self.db_url)
        self.session_factory = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    async def close(self) -> None:

        await self.engine.dispose()


settings = get_settings()

mysql_client = MySQLClient(settings.database_url)

if __name__ == '__main__':
    mysql_client.init()

    async def test():
        async with mysql_client.session_factory() as session:
            reslut = await session.execute(text("SELECT 1"))
            print(reslut.fetchall())
        await mysql_client.close()

    asyncio.run(test())