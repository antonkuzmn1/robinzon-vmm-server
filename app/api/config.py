from typing import Annotated, List

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from app.dependencies.auth import get_current_owner
from app.dependencies.services import get_config_service
from app.schemas.config import ConfigOut, ConfigCreate, ConfigUpdate
from app.schemas.owner import OwnerOut
from app.services.config_service import ConfigService

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/", response_model=List[ConfigOut])
async def get_all_configs(
        config_service: ConfigService = Depends(get_config_service),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        return await config_service.get_all()

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.get("/{owner_id}", response_model=ConfigOut)
async def get_config_by_key(
        config_key: str,
        config_service: ConfigService = Depends(get_config_service),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        return await config_service.get_by_key(config_key)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/", response_model=ConfigOut)
async def create_config(
        owner: ConfigCreate,
        config_service: ConfigService = Depends(get_config_service),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        return await config_service.create(owner)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.put("/{config_key}", response_model=ConfigOut)
async def update_config(
        config_key: str,
        config: ConfigUpdate,
        config_service: ConfigService = Depends(get_config_service),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        return await config_service.update(config_key, config)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.delete("/{config_key}", response_model=ConfigOut)
async def delete_config(
        config_key: str,
        config_service: ConfigService = Depends(get_config_service),
        current_owner: Annotated[OwnerOut, Depends(get_current_owner)] = None,
):
    if current_owner:
        return await config_service.delete(config_key)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )
