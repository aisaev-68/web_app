from typing import Dict


def get_field_types(data) -> Dict:
    """
    Функция для возвращения типов
    """
    field_order = ['created_at', 'phone', 'email', 'name']
    result = {}
    for field_name in field_order:
        if field_name in data:
            value = data[field_name]
            if field_name == 'created_at':
                result[field_name] = 'datetime'
            elif field_name == 'phone':
                result[field_name] = 'phone'
            elif field_name == 'email':
                result[field_name] = 'email'
            elif field_name == 'name':
                result[field_name] = 'text'
    return result
