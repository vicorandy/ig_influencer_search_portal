from fastapi import FastAPI

app =FastAPI()

@app.get('/')
def welcome():
    return {"message":"server is up"}