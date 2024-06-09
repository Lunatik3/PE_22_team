FROM python:3.10
EXPOSE 8000
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD uvicorn main:app --reload --port 8000 
CMD streamlit run st_a7pp.py
