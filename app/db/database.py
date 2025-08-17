from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from app.config import settings
from app.db.naming import camel_to_snake


DATABASE_URL = (
            f'postgresql+asyncpg://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}'
            f'@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
        )

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = camel_to_snake(cls.__name__)
        return f'{name}s'
