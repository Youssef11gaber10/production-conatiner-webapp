

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio
import os
from dotenv import load_dotenv
import uvicorn
import redis.asyncio as redis  # Modern Redis library
from sqlalchemy import text 

load_dotenv()

app = FastAPI()

# PostgreSQL (Async)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/postgres")
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Redis (Async)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)  # ✅ use redis.Redis

@app.get("/")
async def root():
    return {"message": "FastAPI app with Redis and PostgreSQL"}

@app.get("/redis")
async def test_redis():
    try:
        await redis_client.set("fastapi_key", "Hello from Redis!", ex=60)
        val = await redis_client.get("fastapi_key")
        return {"redis_value": val}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/postgres")
async def test_postgres():
    try:
        async with SessionLocal() as session:
            # result = await session.execute("SELECT version();")
            result = await session.execute(text("SELECT version();"))
            version = result.scalar()
            return {"postgres_version": version}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)
