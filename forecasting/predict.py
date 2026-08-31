import joblib
from config.config import settings

def load_model():
    model = joblib.load(settings["artifacts"]["model_path"])
    return model
  
def predict(new_data):
    model = load_model()
    predictions = model.predict(new_data)
    return predictions
  
  