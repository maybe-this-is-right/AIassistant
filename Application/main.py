import sys
import logging
import datetime
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap
from personal_assistant import PersonalAssistant
from database_manager import DatabaseManager
import time

class SystemActivityMonitor(QThread):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.logon_time = datetime.datetime.now()

    def run(self):
        while True:
            time.sleep(3600)  # 1 hour
            self.logoff_time = datetime.datetime.now()
            self.log_activity()
            self.logon_time = datetime.datetime.now()  # Reset logon time for the next cycle

    def log_activity(self):
        duration = int((self.logoff_time - self.logon_time).total_seconds() / 60)
        self.db_manager.add_time_management_log(self.logon_time, self.logoff_time, duration)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        app = QApplication(sys.argv)

        splash_pix = QPixmap('path/to/splash_image.png')
        if splash_pix.isNull():
            logging.error('Splash screen image not found. Ensure the correct path is specified.')
            sys.exit(1)

        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.show()
        app.processEvents()

        db_manager = DatabaseManager('path/to/your/database.db')
        assistant = PersonalAssistant(db_manager)
        assistant.show()
        splash.finish(assistant)

        monitor = SystemActivityMonitor(db_manager)
        monitor.start()

        sys.exit(app.exec_())
    except ImportError as e:
        logging.error(f"PyQt5 import error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
