from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
import io

router = APIRouter()

best_model = tf.keras.models.load_model("model/best_model.h5")


@router.post("/predict-rontgen/")
async def predict_rontgen(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = image.load_img(io.BytesIO(contents), target_size=(384, 384))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        pred = best_model.predict(img_array)[0][0]
        label = "Tuberculosis" if pred > 0.5 else "Normal"
        confidence = pred if pred > 0.5 else 1 - pred

        return JSONResponse(content={
            "label": label,
            "confidence": float(confidence)
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
