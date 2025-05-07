from fastapi import FastAPI
import mlflow.pyfunc
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à adapter si besoin (mettre ["http://localhost:5173"] par ex.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        model = mlflow.pyfunc.load_model("models:/sepal_length_predictor/Production")
        print("✅ Modèle chargé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle : {e}")
        model = None

@app.post("/predict")
def predict(input_data: Dict[str, float]):
    try:
        # Convertir explicitement toutes les valeurs en float
        input_df = pd.DataFrame([{
            key: float(value) for key, value in input_data.items()
        }])

        # Prédiction avec le modèle
        prediction = model.predict(input_df)[0]
        return {"prediction": prediction}
    except Exception as e:
        return {"error": f"Erreur de prédiction : {e}"}
