import sys
import logging
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap
from personal_assistant import PersonalAssistant
import time

# New Thread class for system activity monitoring
class SystemActivityMonitor(QThread):
    def run(self):
        while True:
            # Implement your logic to monitor system activity here
            # Example: Log current active window title, timestamp, etc.
            time.sleep(60)  # Adjust the sleep time as needed

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        app = QApplication(sys.argv)

        splash_pix = QPixmap('path/to/splash_image.png')
        if splash_pix.isNull():
            logging.error('Splash screen image not found. Ensure the correct path is specified.')
            sys.exit(1)

        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        app.processEvents()

        assistant = PersonalAssistant()
        assistant.show()
        splash.finish(assistant)

        # Start the system activity monitoring thread
        monitor = SystemActivityMonitor()
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
