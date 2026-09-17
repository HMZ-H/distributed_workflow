from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dwf.domain.models.step import StepCreate, StepUpdate
from dwf.infrastructure.database.models.steps import Step


class StepService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_step(self, workflow_id: str, data: StepCreate) -> Step:
        result = await self.db.execute(
            select(Step).where(
                Step.name == data.name, Step.workflow_id == UUID(workflow_id)
            )
        )
        if result.scalar_one_or_none() is not None:
            raise ValueError("Step with this name already exists")

        step = Step(
            workflow_id=UUID(workflow_id),
            name=data.name,
            type=data.type.value,
            config=data.config,
            position=data.position,
            depends_on=data.depends_on,
        )
        self.db.add(step)
        await self.db.commit()
        await self.db.refresh(step)
        return step

    async def get_by_id(self, step_id: str, workflow_id: str) -> Step | None:
        result = await self.db.execute(
            select(Step).where(
                Step.id == UUID(step_id), Step.workflow_id == UUID(workflow_id)
            )
        )
        return result.scalar_one_or_none()

    async def list_by_workflow(self, workflow_id: str) -> list[Step]:
        result = await self.db.execute(
            select(Step)
            .where(Step.workflow_id == UUID(workflow_id))
            .order_by(Step.position)
        )
        return list(result.scalars().all())

    async def update_step(
        self, step_id: str, workflow_id: str, data: StepUpdate
    ) -> Step | None:
        step = await self.get_by_id(step_id, workflow_id)
        if step is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            if key == "type" and value is not None:
                value = value.value
            setattr(step, key, value)
        await self.db.commit()
        await self.db.refresh(step)
        return step

    async def delete_step(self, step_id: str, workflow_id: str) -> bool:
        step = await self.get_by_id(step_id, workflow_id)
        if step is None:
            return False
        await self.db.delete(step)
        await self.db.commit()
        return True
