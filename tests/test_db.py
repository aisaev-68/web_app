import pytest

from .conftest import mock_crud_form, test_client


@pytest.mark.asyncio
async def test_get_all_form(test_client, mock_crud_form):
    response = await test_client.get("/get_all_form")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_form(test_client, mock_crud_form):
    test_data = {"name": "Test Name", "email": "test@example.com", "phone": "+7 123 456 78 90",
                 "created_at": "2023-11-15"}
    response = await test_client.post("/get_form", json=test_data)
    assert response.status_code == 200
