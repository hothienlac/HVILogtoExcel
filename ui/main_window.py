import os
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QMessageBox
)
from PyQt6.QtCore import QFile, QUrl
from PyQt6.QtGui import QDesktopServices
from typing import Optional
from pathlib import Path
from pandas import DataFrame
from core.csv_reader import read_csv
from core.excel_converter import save_as_excel
from config.settings import APP_NAME
from PyQt6.QtGui import QFont, QIcon

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.csv_data: Optional[DataFrame] = None
        self.csv_file_path: Optional[str] = None
        self.initUI()
        self.load_styles()

    def initUI(self) -> None:
        # Set window properties
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 600, 300)

        # Set central widget
        widget: QWidget = QWidget()
        self.setCentralWidget(widget)

        # Set layout
        layout: QVBoxLayout = QVBoxLayout()
        widget.setLayout(layout)

        # Add label
        self.label: QLabel = QLabel("Select a CSV file to convert to Excel", self)
        self.label.setFont(QFont('Arial', 16))
        layout.addWidget(self.label)

        # Add buttons
        self.btn_open: QPushButton = QPushButton('Open CSV File', self)
        self.btn_open.setIcon(QIcon('resources/icons/open_icon.png'))  # Add an icon if available
        self.btn_open.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.btn_open)

        self.btn_save: QPushButton = QPushButton('Save as Excel', self)
        self.btn_save.setIcon(QIcon('resources/icons/save_icon.png'))  # Add an icon if available
        self.btn_save.clicked.connect(self.save_file_dialog)
        self.btn_save.setEnabled(False)
        layout.addWidget(self.btn_save)

    def open_file_dialog(self) -> None:
        options = QFileDialog.Option.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_path:
            try:
                self.csv_file_path = file_path
                self.csv_data = read_csv(file_path)
                self.label.setText(f"File loaded: {file_path}")
                self.btn_save.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSV file: {str(e)}")

    def save_file_dialog(self) -> None:
        if not self.csv_file_path:
            return

        # Suggest the same file name with .xlsx extension
        suggested_file_path = str(Path(self.csv_file_path).with_suffix('.xlsx'))

        options = QFileDialog.Option.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as Excel File", suggested_file_path, "Excel Files (*.xlsx);;All Files (*)", options=options)

        if file_path:
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'

            try:
                save_as_excel(self.csv_data, file_path)
                QMessageBox.information(self, "Success", f"File saved as: {file_path}")

                # Open file location in explorer
                folder = os.path.dirname(file_path)
                if sys.platform == "win32":
                    os.startfile(folder)
                elif sys.platform == "darwin":
                    QDesktopServices.openUrl(QUrl(f"file://{folder}"))
                else:
                    QDesktopServices.openUrl(QUrl(f"file://{folder}"))
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save Excel file: {str(e)}")

    def load_styles(self) -> None:
        """Load styles from the app_style.qss file."""
        with open("resources/styles/app_style.qss", "r") as style_file:
            self.setStyleSheet(style_file.read())
