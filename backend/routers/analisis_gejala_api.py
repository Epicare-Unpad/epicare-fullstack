from fastapi import APIRouter, Body
import tensorflow as tf
import numpy as np
from typing import List
import os

router = APIRouter()

# Cegah error saat testing jika model tidak tersedia
MODEL_PATH = "model/model_nn.keras"
model = None
if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)

feature_names = [
    "Batuk", "Berkeringat di Malam Hari", "Kesulitan Bernapas", "Demam",
    "Nyeri Dada", "Dahak", "Penekanan Sistem Imun", "Kehilangan Rasa Senang",
    "Menggigil", "Kehilangan Konsentrasi", "Mudah Tersinggung", "Kehilangan Nafsu Makan",
    "Kehilangan Energi", "Pembengkakan Kelenjar Getah Bening",
    "Tekanan Darah Sistolik", "Kategori BMI"
]


class InputData:
    def __init__(
        self,
        Batuk, Berkeringat_di_Malam_Hari, Kesulitan_Bernapas, Demam,
        Nyeri_Dada, Dahak, Penekanan_Sistem_Imun, Kehilangan_Rasa_Senang,
        Menggigil, Kehilangan_Konsentrasi, Mudah_Tersinggung, Kehilangan_Nafsu_Makan,
        Kehilangan_Energi, Pembengkakan_Kelenjar_Getah_Bening,
        Tekanan_Darah_Sistolik, BMI_kategori
    ):
        self.Batuk = Batuk
        self.Berkeringat_di_Malam_Hari = Berkeringat_di_Malam_Hari
        self.Kesulitan_Bernapas = Kesulitan_Bernapas
        self.Demam = Demam
        self.Nyeri_Dada = Nyeri_Dada
        self.Dahak = Dahak
        self.Penekanan_Sistem_Imun = Penekanan_Sistem_Imun
        self.Kehilangan_Rasa_Senang = Kehilangan_Rasa_Senang
        self.Menggigil = Menggigil
        self.Kehilangan_Konsentrasi = Kehilangan_Konsentrasi
        self.Mudah_Tersinggung = Mudah_Tersinggung
        self.Kehilangan_Nafsu_Makan = Kehilangan_Nafsu_Makan
        self.Kehilangan_Energi = Kehilangan_Energi
        self.Pembengkakan_Kelenjar_Getah_Bening = Pembengkakan_Kelenjar_Getah_Bening
        self.Tekanan_Darah_Sistolik = Tekanan_Darah_Sistolik
        self.BMI = BMI_kategori


def hitung_kategori_bmi(berat_kg: float, tinggi_cm: float) -> int:
    tinggi_m = tinggi_cm / 100
    bmi = berat_kg / (tinggi_m ** 2)
    if bmi < 18.5:
        return 0
    elif bmi < 25:
        return 1
    else:
        return 2


def predict(input_data: InputData):
    input_array = np.array([[  # Susun array input
        input_data.Batuk,
        input_data.Berkeringat_di_Malam_Hari,
        input_data.Kesulitan_Bernapas,
        input_data.Demam,
        input_data.Nyeri_Dada,
        input_data.Dahak,
        input_data.Penekanan_Sistem_Imun,
        input_data.Kehilangan_Rasa_Senang,
        input_data.Menggigil,
        input_data.Kehilangan_Konsentrasi,
        input_data.Mudah_Tersinggung,
        input_data.Kehilangan_Nafsu_Makan,
        input_data.Kehilangan_Energi,
        input_data.Pembengkakan_Kelenjar_Getah_Bening,
        input_data.Tekanan_Darah_Sistolik,
        input_data.BMI
    ]])
    prediction = model.predict(input_array)
    prediction_value = prediction[0][0] * 100
    return f"{prediction_value:.2f}%"


@router.post("/predict/")
async def get_prediction(data: List[float] = Body(...)):
    if len(data) != 17:
        return {"error": "Input harus 17 elemen: 15 fitur + berat + tinggi"}

    *fitur, berat, tinggi = data
    bmi_kategori = hitung_kategori_bmi(berat, tinggi)

    input_data = InputData(*fitur, bmi_kategori)
    prediction = predict(input_data)
    return {"prediction": prediction}
