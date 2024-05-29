import os
import pytest
from fastapi.testclient import TestClient
from main import app

# Создание клиента для тестирования
client = TestClient(app)

# Проверяем, что файл модели загружен
@pytest.fixture(scope="session", autouse=True)
def setup_model():
    model_path = 'best.pt'
    if model_path not in os.listdir():
        import gdown
        gdown.download(url='https://drive.google.com/uc?id=1nolYX5CFPJWp8BcyPscUp-urKQ3jTTf-', output=model_path, fuzzy=True)

# Тестируем endpoint /run_model/ с изображением
def test_run_model():
    # Убедитесь, что у вас есть изображение для теста
    test_image_path = 'test_image.jpg'  # Путь к тестовому изображению
    with open(test_image_path, "rb") as file:
        files = {"file": ("test_image.jpg", file, "image/jpeg")}
        response = client.post("/run_model/", files=files)
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"

# Дополнительные тесты можно добавить аналогичным образом
def test_invalid_file():
    # Попытка отправить не изображение
    invalid_file_path = 'test_invalid.txt'  # Путь к тестовому не изображению
    with open(invalid_file_path, "rb") as file:
        files = {"file": ("test_invalid.txt", file, "text/plain")}
        response = client.post("/run_model/", files=files)
    
    assert response.status_code == 422  # Ожидается ошибка из-за неправильного типа файла
