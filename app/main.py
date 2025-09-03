from fastapi import FastAPI
from app.API.user_routes import user_router as test_router
from app.API.workout_routes import workout_router as test_router2
from app.API.auth_routes import auth_router as test_router4
app = FastAPI()

@app.get("/")
def example():
    return {
        "message": "Hello World!"
    }

app.include_router(test_router)
app.include_router(test_router2)
app.include_router(test_router4)