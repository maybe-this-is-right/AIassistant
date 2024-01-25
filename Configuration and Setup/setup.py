import hashlib
import json
from cryptography.fernet import Fernet
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class SetupUI(QWidget):
    def __init__(self, config_path):
        super().__init__()
        self.config_path = config_path
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Please create a password for your AI assistant:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.onSubmit)

        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.setWindowTitle("AI Assistant Setup")
        self.show()

    def onSubmit(self):
        password = self.password_input.text()
        if password:
            try:
                setup_configuration(password, self.config_path)
                self.label.setText("Setup complete.")
            except Exception as e:
                self.label.setText(f"Error: {e}")
        else:
            self.label.setText("Password cannot be empty.")

def generate_fernet_key():
    return Fernet.generate_key()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_configuration(key, hashed_password, config_path):
    with open(config_path, 'w') as config_file:
        json.dump({"fernet_key": key.decode(), "hashed_password": hashed_password}, config_file)

def setup_configuration(password, config_path):
    key = generate_fernet_key()
    hashed_password = hash_password(password)
    save_configuration(key, hashed_password, config_path)

def run_setup(config_path):
    app = QApplication(sys.argv)
    ex = SetupUI(config_path)
    sys.exit(app.exec_())

if __name__ == "__main__":
    config_directory = "C:/Users/rudym/Desktop/PersonalAI/Config"
    config_filename = "config.json"
    config_path = os.path.join(config_directory, config_filename)

    if not os.path.exists(config_directory):
        os.makedirs(config_directory)

    run_setup(config_path)
