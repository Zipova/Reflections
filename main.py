from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.routes import admin_routes, photos, auth
from src.repository import photos as repository_photos

app = FastAPI()

app.include_router(admin_routes.router, prefix='/api')
app.include_router(photos.router, prefix='/api')
app.include_router(auth.router, prefix='/api')


@app.get("/")
async def all_photos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    photos = await repository_photos.get_all_photos(skip, limit, db)
    return photos

