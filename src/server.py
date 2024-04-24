import io
import pickle

import cv2
import numpy as np
import uvicorn
from PIL import Image

from fastapi import FastAPI, UploadFile, File

from database import Database
from images_dataset import IMAGE_SIZE, extract_hog_features
from service import Service
from utils.common_utils import cur_file_path

db = Database()
service = Service(db)

app = FastAPI()

pretrained_path = str(cur_file_path().parent.parent.parent) + '/data/random_forest_pretrained.pkl'
with open(pretrained_path, 'rb') as f:
    rf_classifier = pickle.load(f)


def extract_hog_embs(pil_image):
    img = np.array(pil_image)
    img_resized = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    hog_features = extract_hog_features(img_gray)

    return hog_features


@app.post('/upload/')
async def upload_file(file: UploadFile = File(...)):
    image = await file.read()
    image = Image.open(io.BytesIO(image)).convert('RGB')

    hog_embs = extract_hog_embs(image)

    is_male = rf_classifier.predict([hog_embs])  # e.g [1] or [0]

    response = {
        'filename': file.filename,
        'is_male': 'male' if is_male else 'female',
    }

    service.save_image_prediction(
        image_name=file.filename,
        is_male=True if is_male else False,
    )

    return response


def main():
    service.init_db()
    uvicorn.run(
        'src.server:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )


if __name__ == '__main__':
    main()
