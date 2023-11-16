from typing import List, Any

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends

from app.db.db import get_db
from app.config import settings
from app.crud.utils import get_field_types
from app.schemas import FormDataOut, TemplateName


class CRUDForm:
    """
    Сервис для работы с базой
    """

    def __init__(self, db_client: AsyncIOMotorClient = Depends(get_db)):
        self.db = db_client
        self.db_client = db_client
        self.db_name = settings.MONGO_DB
        self.collection_name = "form_templates"

    async def get_collection(self):
        return self.db_client[self.db_name][self.collection_name]

    async def get_all_form(self) -> List[FormDataOut]:
        collection = await self.get_collection()
        cursor = collection.find()
        results = await cursor.to_list(length=100)
        return [FormDataOut(**res) for res in results]

    async def is_collection_empty(self) -> bool:
        result = await self.get_collection()
        return result.count_documents({}) == 0

    async def get_form_template(self, data) -> Any:
        collection = await self.get_collection()
        results = await collection.find(data).to_list(length=None)

        if len(results) > 1:
            form_data = [TemplateName(name=res['name']) for res in results]
        elif len(results) == 0:
            return get_field_types(data)
        else:
            form_data = TemplateName(name=results[0]['name'])

        return form_data
