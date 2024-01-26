# machine_learning_manager.py
import numpy as np
from sklearn.cluster import KMeans
from database_manager import DatabaseManager
import logging

logging.basicConfig(level=logging.INFO)

class MachineLearningManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def cluster_user_activities(self):
        activities = self.db_manager.get_all_user_activities()
        # Assuming activities data is available in a suitable format
        data = np.array([[activity.attribute1, activity.attribute2] for activity in activities])
        
        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=3)  # Example: 3 clusters
        kmeans.fit(data)

        # Assign clusters to activities and return
        clusters = kmeans.predict(data)
        return clusters

# Example usage
# db_manager = DatabaseManager('path_to_database')
# ml_manager = MachineLearningManager(db_manager)
# clusters = ml_manager.cluster_user_activities()
# print(clusters)
