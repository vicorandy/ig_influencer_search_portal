from fastapi import FastAPI
from app.core.database import Base,engine
from app.db.models import ig_model
from app.api.api import api_router

ig_model.Base.metadata.create_all(engine)
Base.metadata.create_all(engine)

app =FastAPI()
app.include_router(api_router)
@app.get('/')
def welcome():
    return {"message":"server is up"}