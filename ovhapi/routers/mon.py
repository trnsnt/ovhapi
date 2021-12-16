from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/ping", response_model=str)
async def monitoring() -> str:
    return "pong"
