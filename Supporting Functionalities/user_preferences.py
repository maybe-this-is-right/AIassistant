from collections import Counter
import json
import logging

class UserPreferenceManager:
    def __init__(self, storage_path='user_prefs.json'):
        self.storage_path = storage_path
        self.query_counter = self._load_preferences()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def _load_preferences(self):
        try:
            with open(self.storage_path, 'r') as file:
                return Counter(json.load(file))
        except FileNotFoundError:
            logging.warning(f"Preferences file not found. Creating a new one at {self.storage_path}")
            return Counter()

    def _save_preferences(self):
        with open(self.storage_path, 'w') as file:
            json.dump(dict(self.query_counter), file)
            logging.info("Preferences saved successfully")

    def update_preferences(self, query):
        self.query_counter[query] += 1
        self._save_preferences()

    def get_frequent_queries(self):
        return self.query_counter.most_common()

    def reset_preferences(self):
        self.query_counter.clear()
        self._save_preferences()
        logging.info("Preferences reset")

    def remove_query_preference(self, query):
        if query in self.query_counter:
            del self.query_counter[query]
            self._save_preferences()
            logging.info(f"Preference for query '{query}' removed")

# Example usage
# user_pref_manager = UserPreferenceManager()
# user_pref_manager.update_preferences("Sample query")
# print(user_pref_manager.get_frequent_queries())
# user_pref_manager.remove_query_preference("Sample query")
# user_pref_manager.reset_preferences()
