from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.infrasructure.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.database_url, echo=False)

Session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
