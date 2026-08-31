from fastapi import FastAPI
from api import router

app = FastAPI(title="Iran War Fuel Crisis Oil Prediction")
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}