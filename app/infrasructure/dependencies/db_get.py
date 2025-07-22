from typing import AsyncGenerator
from app.infrasructure.db.database import Session

async def get_db() -> AsyncGenerator:
    async with Session() as session:
        yield session
