import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from routers.analisis_gejala_api import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


class TestPredictAPI(unittest.TestCase):

    @patch("routers.analisis_gejala_api.model")
    def test_valid_input_prediction(self, mock_model):
        mock_model.predict.return_value = [[0.85]]  # 85%
        input_data = [1] * 15 + [60.0, 170.0]  # Berat, Tinggi

        response = client.post("/predict/", json=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["prediction"], "85.00%")

    def test_invalid_input_length(self):
        input_data = [1] * 10  # Kurang dari 17
        response = client.post("/predict/", json=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.json())
        self.assertEqual(
            response.json()["error"], "Input harus 17 elemen: 15 fitur + berat + tinggi")


if __name__ == "__main__":
    unittest.main()
