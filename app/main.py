from fastapi import FastAPI
from app.API.test_user import router as test_router
from app.API.test_workout import router as test_router2
from app.API.test_exercise import router as test_router3
from app.API.test_auth import router as test_router4
app = FastAPI()

@app.get("/")
def example():
    return {
        "message": "Hello World!"
    }

app.include_router(test_router)
app.include_router(test_router2)
app.include_router(test_router3)
app.include_router(test_router4)