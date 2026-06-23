import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class RoleClassifier:

    
    def __init__(self):

        self.model = Pipeline(
            [
                ("tfidf", TfidfVectorizer()),
                ("classifier", LogisticRegression(max_iter=1000))
            ]
        )

    def load_dataset(self, dataset_path):

        return pd.read_csv(dataset_path)

    def train_model(self, dataset_path):

        df = self.load_dataset(dataset_path)

        X = df["text"]
        y = df["role"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
        )

        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)

        accuracy = accuracy_score(
            y_test,
            predictions,
        )

        print(f"Accuracy: {accuracy:.2f}")

        return accuracy

    def save_model(
        self,
        model_path="ml_models/role_prediction/role_classifier.pkl",
    ):

        joblib.dump(
            self.model,
            model_path,
        )

    def load_model(
        self,
        model_path="ml_models/role_prediction/role_classifier.pkl",
    ):

        self.model = joblib.load(model_path)

    def predict_role(self, resume_text):

        prediction = self.model.predict(
            [resume_text]
        )

        return prediction[0]
    

if __name__ == "__main__":


    classifier = RoleClassifier()

    classifier.train_model(
        "datasets/raw/role_training_data.csv"
    )

    classifier.save_model()

    sample_resume = (
        "Python SQL Spark Kafka Airflow ETL"
    )

    role = classifier.predict_role(
        sample_resume
    )

    print(f"Predicted Role: {role}")

