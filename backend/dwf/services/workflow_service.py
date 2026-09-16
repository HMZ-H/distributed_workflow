from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dwf.domain.models.workflow import WorkflowCreate, WorkflowUpdate
from dwf.infrastructure.database.models import Workflow


class WorkflowService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_workflow(self, data: WorkflowCreate, owner_id: str) -> Workflow:
        result = await self.db.execute(
            select(Workflow).where(
                Workflow.name == data.name, Workflow.owner_id == UUID(owner_id)
            )
        )
        if result.scalar_one_or_none() is not None:
            raise ValueError("Workflow with this name already exists")

        workflow = Workflow(
            name=data.name,
            description=data.description,
            owner_id=UUID(owner_id),
        )
        self.db.add(workflow)
        await self.db.commit()
        await self.db.refresh(workflow)
        return workflow

    async def get_by_id(self, workflow_id: str, owner_id: str) -> Workflow | None:
        result = await self.db.execute(
            select(Workflow).where(
                Workflow.id == UUID(workflow_id), Workflow.owner_id == UUID(owner_id)
            )
        )
        return result.scalar_one_or_none()

    async def list_by_owner(self, owner_id: str) -> list[Workflow]:
        result = await self.db.execute(
            select(Workflow).where(Workflow.owner_id == UUID(owner_id))
        )
        return list(result.scalars().all())

    async def update_workflow(
        self, workflow_id: str, owner_id: str, data: WorkflowUpdate
    ) -> Workflow | None:
        workflow = await self.get_by_id(workflow_id, owner_id)
        if workflow is None:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(workflow, key, value)

        await self.db.commit()
        await self.db.refresh(workflow)
        return workflow

    async def delete_workflow(self, workflow_id: str, owner_id: str) -> bool:
        workflow = await self.get_by_id(workflow_id, owner_id)
        if workflow is None:
            return False

        await self.db.delete(workflow)
        await self.db.commit()
        return True
