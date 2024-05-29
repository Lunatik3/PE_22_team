import httpx
import pytest

BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_run_model():
    # Убедитесь, что у вас есть изображение для теста
    with open("test_image.jpg", "rb") as file:
        files = {"file": ("test_image.jpg", file, "image/jpeg")}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/run_model/", files=files)
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
