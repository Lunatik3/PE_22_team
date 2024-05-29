# Импорт библиотек
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
    result_image_path = f"images_test/results.jpg"
    results[0].save(filename=result_image_path)
    return FileResponse(result_image_path, media_type="image/jpeg")

# Функция для запуска API сервера
def run_api():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Запуск API сервера в отдельном потоке
api_thread = Thread(target=run_api, daemon=True)
api_thread.start()


# Создание Streamlit приложения
st.title('Model')

def get_result(file):
    files = {
        'file': (file.name, file.getvalue(), file.type),
        'Content-Type': 'image/jpeg',
    }
    response = requests.post('http://127.0.0.1:8000/run_model/', files=files)
    if response.status_code == 500:
        st.error('Ошибка в работе модели')
        return
    st.image(image=response.content)

file = st.file_uploader(label='Загрузите файл', type=['jpeg', 'jpg', 'webp', 'png'])

if file:
    st.button(label='Запустить модель', on_click=get_result, args=(file,))

if __name__ == '__st_app__':
    uvicorn.run(host='0.0.0.0', port=8000, app="st_app:app")

