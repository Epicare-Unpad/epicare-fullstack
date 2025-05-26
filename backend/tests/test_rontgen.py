import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from routers.analisis_rontgen_api import router
from io import BytesIO
from PIL import Image
import numpy as np

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def generate_dummy_image():
    img = Image.new("RGB", (384, 384), color=(255, 255, 255))
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf


class TestRontgenPredictAPI(unittest.TestCase):

    @patch("routers.analisis_rontgen_api.best_model")
    def test_predict_rontgen_success(self, mock_model):
        mock_model.predict.return_value = np.array([[0.85]])

        file_data = generate_dummy_image()

        response = client.post(
            "/predict-rontgen/",
            files={"file": ("test.png", file_data, "image/png")}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("label", response.json())
        self.assertIn("confidence", response.json())

    @patch("routers.analisis_rontgen_api.best_model", None)
    def test_model_not_loaded(self):
        file_data = generate_dummy_image()

        response = client.post(
            "/predict-rontgen/",
            files={"file": ("test.png", file_data, "image/png")}
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["error"],
                         "Model tidak ditemukan di server")


if __name__ == "__main__":
    unittest.main()
