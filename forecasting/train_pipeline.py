from pipeline import ForecastingPipeline
from config.config import settings
import joblib

def train():
    pipeline = ForecastingPipeline()
    pipeline.run()

    joblib.dump(pipeline.model, settings["artifacts"]["model_path"])

    return pipeline.model

if __name__ == "__main__":
    train()