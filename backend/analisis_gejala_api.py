# analisis_gejala_api.py

from fastapi import APIRouter
import tensorflow as tf
import numpy as np
from typing import List

router = APIRouter()

model = tf.keras.models.load_model("model/model_nn.keras")


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
    input_array = np.array([[input_data.CO, input_data.NS, input_data.BD, input_data.FV,
                             input_data.CP, input_data.SP, input_data.IS, input_data.LP,
                             input_data.CH, input_data.LC, input_data.IR, input_data.LA,
                             input_data.LE, input_data.LNE, input_data.SBP, input_data.BMI]])
    prediction = model.predict(input_array)
    prediction_value = prediction[0][0]*100
    return f"{prediction_value:.2f}%"


@router.post("/predict/")
async def get_prediction(data: List[int]):
    input_data = InputData(*data)
    prediction = predict(input_data)
    return {"prediction": prediction}
