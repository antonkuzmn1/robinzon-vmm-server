from typing import Annotated, Optional, List

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.services import get_owner_service
from app.dependencies.auth import get_current_owner
from app.schemas.owner import OwnerOut, OwnerCreate, OwnerUpdate
from app.schemas.token import Token
from app.services.owner_service import OwnerService

router = APIRouter(prefix="/owner", tags=["owner"])


@router.get("/profile", response_model=OwnerOut)
async def get_owner_profile(
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)],
):
    if current_owner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return current_owner


@router.get("/", response_model=List[OwnerOut])
async def get_all_owners(
        owner_service: OwnerService = Depends(get_owner_service),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if not current_owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return await owner_service.get_all()


@router.get("/{owner_id}", response_model=OwnerOut)
async def get_owner_by_id(
        owner_id: int,
        owner_service: OwnerService = Depends(get_owner_service),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if not current_owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return await owner_service.get_by_id(owner_id)


@router.post("/", response_model=OwnerOut)
async def create_owner(
        owner: OwnerCreate,
        owner_service: OwnerService = Depends(get_owner_service),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if not current_owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return await owner_service.create(owner)


@router.put("/{owner_id}", response_model=OwnerOut)
async def update_owner(
        owner_id: int,
        owner: OwnerUpdate,
        owner_service: OwnerService = Depends(get_owner_service),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if not current_owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return await owner_service.update(owner_id, owner)


@router.delete("/{owner_id}", response_model=OwnerOut)
async def delete_owner(
        owner_id: int,
        owner_service: OwnerService = Depends(get_owner_service),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if not current_owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return await owner_service.delete(owner_id)


@router.post("/login", response_model=Optional[Token])
async def login_for_owner_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        owner_service: OwnerService = Depends(get_owner_service),
):
    owner = await owner_service.authenticate_owner(form_data.username, form_data.password)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = await owner_service.create_owner_token(owner)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return {"access_token": access_token, "token_type": "Bearer"}
