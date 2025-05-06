import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
import pandas as pd

print("Tracking URI:", mlflow.get_tracking_uri())
mlflow.set_tracking_uri("http://mlflow:5000")

try:
    mlflow.create_experiment("sepal_prediction")
    print("Expérience créée")
except Exception as e:
    print("Erreur création expérience :", e)

mlflow.set_experiment("sepal_prediction")

df = pd.read_csv("iris.csv", sep=";")
X = df[["petal length (cm)", "petal width (cm)"]]
y = df["sepal length (cm)"]
model = LinearRegression().fit(X, y)

with mlflow.start_run():
    mlflow.sklearn.log_model(model, "model", registered_model_name="sepal_length_predictor")
