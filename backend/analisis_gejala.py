from fastapi import FastAPI
import tensorflow as tf
import numpy as np
from typing import List
from fastapi.middleware.cors import CORSMiddleware
# Inisialisasi aplikasi FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Muat model Keras yang telah disimpan
model = tf.keras.models.load_model(
    "model\\model_nn.keras")  # Ganti dengan path modelmu

# Model input data menggunakan tipe standar Python (tanpa Pydantic)


class InputData:
    def __init__(self, CO, NS, BD, FV, CP, SP, IS, LP, CH, LC, IR, LA, LE, LNE, SBP, BMI):
        self.CO = CO
        self.NS = NS
        self.BD = BD
        self.FV = FV
        self.CP = CP
        self.SP = SP
        self.IS = IS
        self.LP = LP
        self.CH = CH
        self.LC = LC
        self.IR = IR
        self.LA = LA
        self.LE = LE
        self.LNE = LNE
        self.SBP = SBP
        self.BMI = BMI


def predict(input_data: InputData):
    # Convert input data to numpy array format
    input_array = np.array([[
        input_data.CO, input_data.NS, input_data.BD, input_data.FV,
        input_data.CP, input_data.SP, input_data.IS, input_data.LP,
        input_data.CH, input_data.LC, input_data.IR, input_data.LA,
        input_data.LE, input_data.LNE, input_data.SBP, input_data.BMI
    ]])

    prediction = model.predict(input_array)

    prediction_value = prediction[0][0]*100
    hasil = f"{prediction_value:.2f}%"
    return hasil  # Return as list


@app.post("/predict/")
async def get_prediction(data: List[int]):
    # Convert the list of integers to an InputData instance
    input_data = InputData(*data)
    prediction = predict(input_data)
    return {"prediction": prediction}
