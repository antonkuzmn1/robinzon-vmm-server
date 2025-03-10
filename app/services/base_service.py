from typing import Optional, Type, TypeVar, Generic, Sequence

from app.repositories.base_repo import BaseRepository

T = TypeVar("T", bound=BaseRepository)
SchemaOut = TypeVar("SchemaOut")
SchemaBase = TypeVar("SchemaBase")


class BaseService(Generic[T]):
    def __init__(self, repository: T, schema_out: Type[SchemaOut]):
        self.repository = repository
        self.schema_out = schema_out

    async def get_all(self, *filters) -> list[SchemaOut]:
        records = await self.repository.get_all(*filters)
        return [self.schema_out.model_validate(record) for record in records]

    async def get_by_id(self, record_id: int, *filters) -> Optional[SchemaOut]:
        record = await self.repository.get_by_id(record_id, *filters)
        return self.schema_out.model_validate(record) if record else None

    async def create(self, data: SchemaBase) -> Optional[SchemaOut]:
        if not isinstance(data, dict):
            data = data.model_dump()

        record = await self.repository.create(data)
        return self.schema_out.model_validate(record)

    async def update(self, record_id: int, data: SchemaBase) -> Optional[SchemaOut]:
        if not isinstance(data, dict):
            data = data.model_dump()

        record = await self.repository.update(record_id, data)
        if record:
            return self.schema_out.model_validate(record)
        return None

    async def delete(self, record_id: int) -> Optional[SchemaOut]:
        record = await self.repository.delete(record_id)
        if record:
            return self.schema_out.model_validate(record)
        return None
