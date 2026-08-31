from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from processing.data_manager import load_merge_data
from processing.features import create_x_and_y
from config.config import settings


class ForecastingPipeline:
    def __init__(self):
        self.model = None
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None

    def run(self):
        master = load_merge_data()
        self.x_train, self.x_test, self.y_train, self.y_test = create_x_and_y(master)

        self.model = Pipeline([
            ("scaler", StandardScaler()),
            ("model", Lasso(
                alpha=settings["model"]["alpha"],
                max_iter=settings["model"]["max_iter"]
            ))
        ])

        self.model.fit(self.x_train, self.y_train)

        return self.model