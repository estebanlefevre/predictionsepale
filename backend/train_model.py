import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import mlflow
import mlflow.sklearn
import os

# Lecture du CSV avec séparateur ;
df = pd.read_csv("iris.csv", sep=";")

# Encodage de la variable 'species' en valeurs numériques (sinon régression impossible)
df["species"] = df["species"].astype("category").cat.codes

# Variables explicatives et cible
X = df.drop("sepal_length", axis=1)
y = df["sepal_length"]

# Séparation train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Configuration de MLflow
mlflow.set_tracking_uri("http://0.0.0.0:5000")
mlflow.set_experiment("Prediction Sepale")

# Chemin absolu du fichier
file_path = os.path.abspath("iris.csv")

with mlflow.start_run():  # Démarre un run MLflow
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)

    # Log des métriques
    mlflow.log_metric("mse", mse)
    mlflow.log_param("n_estimators", 100)

    # Enregistrement du modèle
    mlflow.sklearn.log_model(model, "model", registered_model_name="sepal_length_predictor")

    # Log du fichier CSV (si tu veux loguer iris.csv)
    mlflow.log_artifact(file_path)  # Cette ligne enregistre le fichier iris.csv dans les artefacts du run
