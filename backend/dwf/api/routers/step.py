from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dwf.api.deps import get_current_active_user, get_db
from dwf.domain.models.step import StepCreate, StepResponse, StepUpdate
from dwf.infrastructure.database.models import User
from dwf.services.step_service import StepService

router = APIRouter(prefix="/workflows/{workflow_id}/steps", tags=["steps"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=StepResponse)
async def create_step(
    workflow_id: str,
    data: StepCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    service = StepService(db)
    try:
        step = await service.create_step(workflow_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return step


@router.get("/", response_model=list[StepResponse])
async def list_steps(
    workflow_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    service = StepService(db)
    return await service.list_by_workflow(workflow_id)


@router.get("/{step_id}", response_model=StepResponse)
async def get_step(
    workflow_id: str,
    step_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    service = StepService(db)
    step = await service.get_by_id(step_id, workflow_id)
    if step is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Step not found"
        )
    return step


@router.put("/{step_id}", response_model=StepResponse)
async def update_step(
    workflow_id: str,
    step_id: str,
    data: StepUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    service = StepService(db)
    step = await service.update_step(step_id, workflow_id, data)
    if step is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Step not found"
        )
    return step


@router.delete("/{step_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_step(
    workflow_id: str,
    step_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    service = StepService(db)
    deleted = await service.delete_step(step_id, workflow_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Step not found"
        )
