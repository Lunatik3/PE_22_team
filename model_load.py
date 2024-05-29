from ultralytics import YOLO
import gdown
import os

if 'best.pt' not in os.listdir():
  gdown.download(url='https://drive.google.com/file/d/1nolYX5CFPJWp8BcyPscUp-urKQ3jTTf-/view?usp=drive_link', fuzzy=True)

model = YOLO('best.pt')
