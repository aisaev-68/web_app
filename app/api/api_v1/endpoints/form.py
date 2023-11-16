from typing import Annotated, Optional, Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from app.crud import CRUDForm
from app.schemas.form import FormData

router = APIRouter()


#
@router.get("/get_all_form")
async def get_all_form(service: Annotated[CRUDForm, Depends()]) -> Any:
    """
    Получение всех данных
    """
    try:
        form = await service.get_all_form()
        return form
    except Exception as err:
        raise HTTPException(status_code=422, detail=f'{type(err).__name__}: {str(err)}')


@router.post("/get_form")
async def get_form(
        service: Annotated[CRUDForm, Depends()],
        created_at: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
) -> Any:
    """
    Обработка входных данных вида f_name1=value1&f_name2=value2
    Можно передать любые из следующих полей:
    * **name**: в формате текста
    * **email**: в формате email
    * **phone**: в формате +7 xxx xxx xx xx
    * **created_at**: в формате DD.MM.YYYY или YYYY-MM-DD
    """

    try:
        form_data = FormData(name=name, email=email, phone=phone, created_at=created_at)
        data = jsonable_encoder(form_data, exclude_none=True)
        form = await service.get_form_template(data)
        return form
    except Exception as err:
        raise HTTPException(status_code=422, detail=f'{type(err).__name__}: {str(err)}')
