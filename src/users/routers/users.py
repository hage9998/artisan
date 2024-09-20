from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get("/users")
def get_user():
    return "bla"
