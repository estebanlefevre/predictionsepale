from fastapi import FastAPI
import mlflow.pyfunc
import pandas as pd

app = FastAPI()

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
def predict(features: dict):
    if model is None:
        return {"error": "Modèle non chargé"}

    try:
        df = pd.DataFrame([features])
        prediction = model.predict(df)
        return {"sepal_length_prediction": prediction[0]}
    except Exception as e:
        return {"error": f"Erreur de prédiction : {str(e)}"}
