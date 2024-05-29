import os
import streamlit as st
import requests
from fastapi import FastAPI, File, UploadFile
from threading import Thread
import uvicorn
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from ultralytics import YOLO
import gdown

# Загрузка модели с Google Drive
model_path = 'best.pt'
if 'best.pt' not in os.listdir():
    gdown.download(url='https://drive.google.com/uc?id=1nolYX5CFPJWp8BcyPscUp-urKQ3jTTf-', fuzzy=True)

# Создание FastAPI приложения
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)

# Загрузка модели YOLO
model = YOLO(model_path)

@app.post("/run_model/")
async def run_model(file: UploadFile):
    img = Image.open(file.file)
    results = model.predict(img)
    result_image_path = f"images/results.jpg"
    results[0].save(filename=result_image_path)
    return FileResponse(result_image_path, media_type="image/jpeg")

# Функция для запуска API сервера
def run_api():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Запуск API сервера в отдельном потоке
api_thread = Thread(target=run_api, daemon=True)
api_thread.start()

# Запуск сервера uvicorn
if __name__ == '__main__':
    uvicorn.run(host='0.0.0.0', port=8000, app="main:app")
