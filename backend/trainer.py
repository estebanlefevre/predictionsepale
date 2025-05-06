import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.linear_model import LinearRegression

# Configuration MLflow
mlflow.set_tracking_uri("http://mlflow:5000")

experiment_name = "sepal_prediction"
model_name = "sepal_length_predictor"

# Créer ou utiliser l'expérience
mlflow.set_experiment(experiment_name)

# Chargement des données
df = pd.read_csv("iris.csv", sep=";")
X = df[["petal_length", "petal_width"]]
y = df["sepal_length"]

# Entraînement
model = LinearRegression().fit(X, y)

# Enregistrement
with mlflow.start_run():
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=model_name
    )
    mlflow.log_params({"fit_intercept": model.fit_intercept})
    print(f"✅ Modèle enregistré sous le nom '{model_name}'")
