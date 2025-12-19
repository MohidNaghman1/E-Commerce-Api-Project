from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession    
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus 
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()
# 1. Store your raw password in a variable
raw_password = os.environ.get("DATABASE_PASSWORD", "") 
db_name = os.environ.get("DATABASE_NAME", "ecommerce_db")
db_host = os.environ.get("DATABASE_HOST", "localhost")
db_port = os.environ.get("DATABASE_PORT", "5432")


# 2. Encode the password
# This turns "mohid708@" into "mohid708%40"
encoded_password = quote_plus(raw_password)

# 3. Inject the encoded password into the URL using an f-string
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://postgres:{encoded_password}@{db_host}:{db_port}/{db_name}"


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)