from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd

app = FastAPI()

model_uri = "models:/sepal_length_predictor/Production"  
model = mlflow.pyfunc.load_model(model_uri)

class InputData(BaseModel):
    sepal_width: float
    petal_length: float
    petal_width: float
    species: int  

@app.post("/predict")
def predict(input_data: InputData):
    input_df = pd.DataFrame([input_data.dict()])
    
    prediction = model.predict(input_df)
    
    return {"predicted_sepal_length": prediction[0]}

