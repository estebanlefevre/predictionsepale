from fastapi import FastAPI
from pydantic import BaseModel, Field
import mlflow.pyfunc
import pandas as pd
import os

app = FastAPI(
    title="API de prédiction de longueur de sépale",
    description="Utilise un modèle MLflow pour prédire la longueur de sépale à partir de caractéristiques d'iris.",
    version="1.0.0"
)

# Définition du schéma des données entrantes
class IrisFeatures(BaseModel):
    sepal_width: float = Field(..., example=3.0)
    petal_length: float = Field(..., example=4.5)
    petal_width: float = Field(..., example=1.5)
    species: str = Field(..., example="setosa")

# Chargement du modèle depuis le Model Registry de MLflow
MODEL_NAME = "sepal_length_predictor"
MODEL_VERSION = "1"

try:
    model_uri = f"models:/{MODEL_NAME}/{MODEL_VERSION}"
    model = mlflow.pyfunc.load_model(model_uri=model_uri)
except Exception as e:
    model = None
    print(f"Erreur lors du chargement du modèle : {e}")

@app.get("/")
def read_root():
    return {"message": "API de prédiction MLflow opérationnelle."}

@app.post("/predict")
def predict(features: IrisFeatures):
    if model is None:
        return {"error": "Modèle ML non disponible."}

    # Conversion en DataFrame
    data = pd.DataFrame([features.dict()])
    
    try:
        prediction = model.predict(data)
        return {"sepal_length_prediction": prediction[0]}
    except Exception as e:
        return {"error": f"Erreur lors de la prédiction : {str(e)}"}
