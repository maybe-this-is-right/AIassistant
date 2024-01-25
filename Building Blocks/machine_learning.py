import joblib
import os
import numpy as np
import logging
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from database_manager import DatabaseManager  # Import the DatabaseManager

logging.basicConfig(level=logging.INFO)

class MachineLearningManager:
    _iris_data = None

    def __init__(self, db_manager: DatabaseManager, model_path='model.joblib'):
        self.db_manager = db_manager
        self.model_path = model_path
        self.model = self.load_model()

    @classmethod
    def get_iris_data(cls):
        if cls._iris_data is None:
            cls._iris_data = load_iris()
        return cls._iris_data

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                logging.info("Loading existing model.")
                return joblib.load(self.model_path)
            except Exception as e:
                logging.error(f"Failed to load model: {e}")
                return None
        else:
            return self.train_new_model()

    def train_new_model(self):
        logging.info("Training a new model.")
        iris = self.get_iris_data()
        X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=42)
        clf = DecisionTreeClassifier()
        clf.fit(X_train, y_train)
        joblib.dump(clf, self.model_path)
        self.evaluate_model(X_test, y_test)
        return clf

    # New method for analyzing user behavior patterns
    def analyze_user_patterns(self, data):
        # Machine learning logic to identify patterns in user data
        # Example: Clustering work habits, analyzing problem-solving styles, etc.
        # Placeholder for actual implementation
        return "Identified patterns"

    def evaluate_model(self, X_test, y_test):
        # Example evaluation logic (replace with actual evaluation)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        logging.info(f"Model Accuracy: {accuracy}")
        return accuracy

# Example usage
# db_manager = DatabaseManager('path_to_database')
# ml_manager = MachineLearningManager(db_manager)
# result = ml_manager.perform_classification([5.1, 3.5, 1.4, 0.2])
# print(result)
