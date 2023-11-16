import re
from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class FormData(BaseModel):
    name: Optional[str] = Field(default=None, description="Название формы")
    email: Optional[EmailStr] = Field(default=None, description="Email")
    phone: Optional[str] = Field(default=None, description="Номер телефона")
    created_at: Optional[str] = Field(default=None, description="Дата")

    @field_validator('phone', mode='after')
    def validate_phone(cls, v):
        if v:
            phone_regex = r'^\+7 \d{3} \d{3} \d{2} \d{2}$'
            if not re.match(phone_regex, v):
                raise ValueError("Invalid phone number format")
        return v

    @field_validator('created_at', mode='after')
    def validate_date(cls, v):
        if v:
            date_formats = ["%d.%m.%Y", "%Y-%m-%d"]
            dd_mm_yyyy_regex = re.compile(r"\d{2}\.\d{2}\.\d{4}")
            yyyy_mm_dd_regex = re.compile(r"\d{4}-\d{2}-\d{2}")
            if dd_mm_yyyy_regex.match(v):
                format_to_use = date_formats[0]
            elif yyyy_mm_dd_regex.match(v):
                format_to_use = date_formats[1]
            else:
                raise ValueError("Неправильный формат даты")

            try:
                parsed_date = datetime.strptime(v, format_to_use)
                return parsed_date
            except ValueError:
                raise ValueError("Неправильный формат даты")
        return v


class FormDataOut(FormData):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str
        })
    id: ObjectId = Field(..., alias="_id")


class TemplateName(BaseModel):
    name: Optional[str] = Field(default=None, description="Название формы")


class Failure(BaseModel):
    result: bool = False
    error_type: str
    error_message: str
