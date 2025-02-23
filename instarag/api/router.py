from fastapi import APIRouter

app_router = APIRouter()

@app_router.get("/")
def read_root():
    return {"Hello": "World"}

@app_router.get("/healthz")
def read_root():
    return {"result": "ok"}

@app_router.get("/readz")
def read_root():
    return {"result": "ok"}

@app_router.get("/app/details")
def app_details():
    pass

@app_router.post("/chat")
def chat():
    pass