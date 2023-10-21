from fastapi import APIRouter

router = APIRouter()


@router.get("/api/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/api/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/api/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
