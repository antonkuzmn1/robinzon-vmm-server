from typing import List, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import get_current_admin, get_current_owner, get_current_user
from app.schemas.admin import AdminCreate, AdminOut, AdminUpdate
from app.schemas.owner import OwnerOut
from app.schemas.token import Token
from app.schemas.user import UserOut
from app.services.admin_service import AdminService
from app.dependencies.services import get_admin_service

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.get("/profile", response_model=AdminOut)
async def get_admin_profile(
        current_admin: Annotated[AdminOut, Depends(get_current_admin)],
):
    if current_admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return current_admin


@router.get("/", response_model=List[AdminOut])
async def get_all_admins(
        admin_service: Annotated[AdminService, Depends(get_admin_service)],
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
        current_user: Optional[UserOut] = Depends(get_current_user),
):
    if current_owner:
        return await admin_service.get_all()
    if current_admin:
        return await admin_service.get_all_admins_for_admin(current_admin)
    if current_user:
        return await admin_service.get_all_admins_for_user(current_user)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.get("/{admin_id}", response_model=AdminOut)
async def get_admin_by_id(
        admin_id: int,
        admin_service: Annotated[AdminService, Depends(get_admin_service)],
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
        current_user: Optional[UserOut] = Depends(get_current_user),
):
    if current_owner:
        return await admin_service.get_by_id(admin_id)
    if current_admin:
        return await admin_service.get_admin_by_id_for_admin(admin_id, current_admin)
    if current_user:
        return await admin_service.get_admin_by_id_for_user(admin_id, current_user)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/", response_model=AdminOut)
async def create_admin(
        admin: AdminCreate,
        admin_service: Annotated[AdminService, Depends(get_admin_service)],
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        return await admin_service.create(admin)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.put("/{admin_id}", response_model=AdminOut)
async def update_admin(
        admin_id: int,
        admin: AdminUpdate,
        admin_service: Annotated[AdminService, Depends(get_admin_service)],
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        return await admin_service.update(admin_id, admin)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.delete("/{admin_id}", response_model=AdminOut)
async def delete_admin(
        admin_id: int,
        admin_service: Annotated[AdminService, Depends(get_admin_service)],
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        return await admin_service.delete(admin_id)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/{admin_id}/companies/{company_id}", response_model=AdminOut)
async def create_m2m_admin_company(
        admin_id: int,
        company_id: int,
        admin_service: Annotated[AdminService, Depends(get_admin_service)],
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        return await admin_service.add_company_to_admin(admin_id, company_id)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.delete("/{admin_id}/companies/{company_id}", response_model=AdminOut)
async def remove_m2m_admin_company(
        admin_id: int,
        company_id: int,
        admin_service: Annotated[AdminService, Depends(get_admin_service)],
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        return await admin_service.remove_company_from_admin(admin_id, company_id)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/login", response_model=Token)
async def login_for_admin_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        admin_service: Annotated[AdminService, Depends(get_admin_service)],
):
    admin = await admin_service.authenticate_admin(form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token = await admin_service.create_admin_token(admin)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return {"access_token": access_token, "token_type": "bearer"}
