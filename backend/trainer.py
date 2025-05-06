import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.linear_model import LinearRegression
from mlflow.exceptions import MlflowException

mlflow.set_tracking_uri("http://mlflow:5000")

experiment_name = "sepal_prediction"
model_name = "sepal_length_predictor"

# Créer ou utiliser l’expérience
mlflow.set_experiment(experiment_name)

# Chargement des données
df = pd.read_csv("iris.csv", sep=";")
X = df[["sepal_width"]]  # ✅ Nouveau feature
y = df["sepal_length"]

model = LinearRegression().fit(X, y)

with mlflow.start_run() as run:
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=model_name,
        input_example=X.iloc[[0]],
    )
    mlflow.log_params({"fit_intercept": model.fit_intercept})
    print(f"✅ Modèle enregistré sous le nom '{model_name}'")

    # ✅ Mise en production automatique
    client = mlflow.tracking.MlflowClient()
    model_version = client.get_latest_versions(model_name, stages=["None"])[-1].version

    try:
        client.transition_model_version_stage(
            name=model_name,
            version=model_version,
            stage="Production",
            archive_existing_versions=True
        )
        print(f"🚀 Modèle version {model_version} mis en production")
    except MlflowException as e:
        print(f"❌ Erreur de mise en production : {e}")
