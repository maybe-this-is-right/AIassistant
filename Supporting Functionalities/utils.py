from PyQt5.QtCore import QThread, pyqtSignal
import logging
import datetime
import json
import re
import requests

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Worker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(Exception)

    def __init__(self, func, *args, **kwargs):
        super(Worker, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(e)
            logging.error(f"Error in worker thread: {e}")

def async_execute(func, callback=None):
    def wrapper(*args, **kwargs):
        worker = Worker(func, *args, **kwargs)
        if callback:
            worker.finished.connect(callback)
        else:
            worker.finished.connect(lambda res: logging.info(f"Async execution result: {res}"))
        worker.error.connect(lambda e: logging.error(f"Error in async execution: {e}"))
        worker.start()
        logging.info("Worker thread started for asynchronous execution")
    return wrapper

def get_current_time_formatted():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"JSON file not found: {file_path}")
        return None

def save_json_file(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            logging.info(f"JSON data saved to {file_path}")
    except Exception as e:
        logging.error(f"Error saving JSON data: {e}")

def clean_text(text):
    return re.sub(' +', ' ', re.sub(r'[^\w\s]', '', text))

def download_file(url, destination):
    try:
        response = requests.get(url)
        with open(destination, 'wb') as file:
            file.write(response.content)
        logging.info(f"File downloaded from {url} to {destination}")
    except Exception as e:
        logging.error(f"Error downloading file: {e}")

# Additional utility functions can be added here
# Example: Date and time utilities, data transformation functions, etc.

# Example usage of async_execute
# @async_execute
# def sample_async_function():
#     # Sample function logic here
