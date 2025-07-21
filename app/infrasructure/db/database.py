from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrasructure.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
