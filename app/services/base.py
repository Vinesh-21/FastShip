from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

### Base Class - it is Inherited by all Service Class For Basic CRUD Operations
class BaseService:
    # While Inheriting it should be Super Initializied with the DB Model(table), DB Session
    def __init__(self, model: SQLModel, session: AsyncSession):
        self.model = model
        self.session = session

    # Read Operation
    async def _get(self, id: UUID):
        return await self.session.get(self.model, id)
    # Create Operation
    async def _add(self, entity: SQLModel):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
    # Update Operation
    async def _update(self, entity: SQLModel):
        return await self._add(entity)
    # Delete Operation
    async def _delete(self, entity: SQLModel):
        await self.session.delete(entity)