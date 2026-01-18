import sys

from PyQt5.QtWidgets import QApplication

from app.eeg_app import EEGAnalyzerApp
from gui.panels import _base_stylesheet


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(_base_stylesheet())
    window = EEGAnalyzerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
