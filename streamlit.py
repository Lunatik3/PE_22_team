# Импорт библиотек
import streamlit as st
import requests
import uvicorn

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

if __name__ == '__streamlit__':
    uvicorn.run(host='0.0.0.0', port=8000, app="main:app")
