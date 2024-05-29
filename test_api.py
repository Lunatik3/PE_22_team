import pytest
from fastapi.testclient import TestClient
from PIL import Image
import io
from main import app

client = TestClient(app)


def test_upload_valid_img_file():
    # Создаем временное изображение
    img = Image.new('RGB', (10, 10))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Сохраняем изображение с расширением .img
    files = {'file': ('test.img', img_bytes, 'image/png')}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert response.json()['message'] == "File successfully uploaded"


def test_upload_invalid_extension():
    # Создаем временное изображение
    img = Image.new('RGB', (10, 10))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Сохраняем изображение с неправильным расширением .jpg
    files = {'file': ('test.jpg', img_bytes, 'image/png')}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert response.json()['detail'] == "File is not an .img file"


def test_upload_non_image_file():
    # Создаем временный текстовый файл
    text_file = io.BytesIO(b"This is not an image")
    text_file.seek(0)

    # Сохраняем текстовый файл с расширением .img
    files = {'file': ('test.img', text_file, 'text/plain')}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert response.json()['detail'] == "File is not a valid image"


def test_upload_no_file():
    response = client.post("/upload")
    assert response.status_code == 422  # Ошибка валидации, так как файл не был отправлен
