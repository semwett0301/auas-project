from sqlalchemy import create_engine

from preparation_module.settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_URL, POSTGRES_PORT, POSTGRES_DB

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}:{POSTGRES_PORT}/{POSTGRES_DB}")
