from fastapi import FastAPI, Depends
from database.db import engine, get_session, Base

from repositories.routers import router as router_task


app = FastAPI(title="Task Tracker")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
app.include_router(router_task)
