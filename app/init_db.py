import asyncio

from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import re

from config import settings

fake = Faker('ru_RU')

db_client = AsyncIOMotorClient(
    settings.MONGO_URI,
    maxPoolSize=settings.MAX_CONNECTIONS_COUNT,
    minPoolSize=settings.MIN_CONNECTIONS_COUNT,
    uuidRepresentation="standard",
)
db_name = settings.MONGO_DB
collection_name = "form_templates"


def is_valid_phone_number(phone):
    """
    Функция для проверки формата номера телефона
    """
    phone_regex = r'^\+7 \d{3} \d{3} \d{2} \d{2}$'
    return bool(re.match(phone_regex, phone))


def is_valid_date(date_text):
    """
    Функция для проверки формата даты
    """
    date_formats = ["%d.%m.%Y", "%Y-%m-%d"]
    dd_mm_yyyy_regex = re.compile(r"\d{2}\.\d{2}\.\d{4}")
    yyyy_mm_dd_regex = re.compile(r"\d{4}-\d{2}-\d{2}")
    if dd_mm_yyyy_regex.match(date_text):
        format_to_use = date_formats[0]
    elif yyyy_mm_dd_regex.match(date_text):
        format_to_use = date_formats[1]
    else:
        return False
    try:
        datetime.strptime(date_text, format_to_use)
        return True
    except ValueError:
        return False


async def insert_data():
    """
    Функция вставки фейковых данных
    """

    db = db_client[db_name][collection_name]
    count = await db.count_documents({})

    if not count:
        for _ in range(300):
            name = fake.name()
            email = fake.email()
            phone = fake.phone_number()
            created_at = fake.date()

            if is_valid_phone_number(phone) and is_valid_date(created_at):
                data = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "created_at": created_at
                }

                await db.insert_one(data)


asyncio.run(insert_data())
