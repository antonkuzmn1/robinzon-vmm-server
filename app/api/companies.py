from typing import List, Optional

from fastapi import APIRouter, HTTPException, status, Depends

from app.dependencies.auth import get_current_owner, get_current_admin, get_current_user
from app.schemas.admin import AdminOut
from app.schemas.company import CompanyOut, CompanyCreate, CompanyUpdate
from app.schemas.owner import OwnerOut
from app.schemas.user import UserOut
from app.dependencies.services import get_company_service
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=List[CompanyOut])
async def get_all_companies(
        company_service: CompanyService = Depends(get_company_service),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
        current_user: Optional[UserOut] = Depends(get_current_user),
):
    if current_owner:
        return await company_service.get_all()
    if current_admin:
        return await company_service.get_all_companies_for_admin(current_admin)
    if current_user:
        return await company_service.get_company_for_user(current_user)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.get("/{company_id}", response_model=CompanyOut)
async def get_company_by_id(
        company_id: int,
        company_service: CompanyService = Depends(get_company_service),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
        current_admin: Optional[AdminOut] = Depends(get_current_admin),
        current_user: Optional[UserOut] = Depends(get_current_user),
):
    if current_owner:
        return await company_service.get_by_id(company_id)
    if current_admin:
        return await company_service.get_company_by_id_for_admin(company_id, current_admin)
    if current_user:
        return await company_service.get_company_for_user(current_user)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.post("/", response_model=CompanyOut)
async def create_company(
        company: CompanyCreate,
        company_service: CompanyService = Depends(get_company_service),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        return await company_service.create(company)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.put("/{company_id}", response_model=CompanyOut)
async def update_company(
        company_id: int,
        company: CompanyUpdate,
        company_service: CompanyService = Depends(get_company_service),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        return await company_service.update(company_id, company)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.delete("/{company_id}", response_model=CompanyOut)
async def delete_company(
        company_id: int,
        company_service: CompanyService = Depends(get_company_service),
        current_owner: Optional[OwnerOut] = Depends(get_current_owner),
):
    if current_owner:
        return await company_service.delete(company_id)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
