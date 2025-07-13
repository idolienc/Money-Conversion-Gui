from PySide6 import QtWidgets, QtGui, QtCore
import sys
import requests
from config import key, currencies

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Money Convertor")
        self.setFixedWidth(265)
        self.setFixedHeight(110)

        self.top_input_selection = QtWidgets.QComboBox()
        self.top_input_selection.addItems(currencies.keys())
        self.top_input = QtWidgets.QDoubleSpinBox()
        top_selected_currency = self.top_input_selection.currentText()
        self.top_input.setPrefix(currencies[top_selected_currency]["symbol"])
        self.top_input.setMaximum(999999999999999)

        self.bottom_input_selection = QtWidgets.QComboBox()
        self.bottom_input_selection.addItems(currencies.keys())
        self.bottom_input = QtWidgets.QDoubleSpinBox()
        bottom_selected_currency = self.bottom_input_selection.currentText()
        self.bottom_input.setPrefix(currencies[bottom_selected_currency]["symbol"])
        self.bottom_input.setMaximum(999999999999999)

        self.top_input_selection.currentTextChanged.connect(self.on_top_currency_changed)
        self.bottom_input_selection.currentTextChanged.connect(self.on_bottom_currency_changed)

        self.top_input.valueChanged.connect(self.on_top_input_text_changed)
        self.bottom_input.valueChanged.connect(self.on_bottom_input_text_changed)

        self.top_input_selection.currentTextChanged.connect(self.on_top_selection_changed)
        self.bottom_input_selection.currentTextChanged.connect(self.on_bottom_selection_changed)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.top_input_selection)
        layout.addWidget(self.top_input)
        layout.addWidget(self.bottom_input_selection)
        layout.addWidget(self.bottom_input)

        container = QtWidgets.QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
    
    def on_top_currency_changed(self):
        top_selected_currency = self.top_input_selection.currentText()
        self.top_input.setPrefix(currencies[top_selected_currency]["symbol"])

    def on_bottom_currency_changed(self):
        bottom_selected_currency = self.bottom_input_selection.currentText()
        self.bottom_input.setPrefix(currencies[bottom_selected_currency]["symbol"])

    def on_top_input_text_changed(self, value: float) -> None:
        top_currency = self.top_input_selection.currentText()
        bottom_currency = self.bottom_input_selection.currentText()
        self.bottom_input.blockSignals(True)
        if value == "":
            return 
        rate = self.get_exchange_rate(key, top_currency, bottom_currency)
        converted = self.conversion(value, rate)
        self.bottom_input.setValue(converted)
        self.bottom_input.blockSignals(False)
    
    def on_bottom_input_text_changed(self, value: float) -> None:
        top_currency = self.top_input_selection.currentText()
        bottom_currency = self.bottom_input_selection.currentText()
        self.top_input.blockSignals(True)
        if value == "":
            return 
        rate = self.get_exchange_rate(key, bottom_currency, top_currency)
        converted = self.conversion(value, rate)
        self.top_input.setValue(converted)
        self.top_input.blockSignals(False)

    def on_top_selection_changed(self):
        top_currency = self.top_input_selection.currentText()
        bottom_currency = self.bottom_input_selection.currentText()
        value = self.top_input.value()
        self.bottom_input.blockSignals(True)
        if value == "":
            self.bottom_input.blockSignals(False)
            return 
        if top_currency == bottom_currency:
            self.bottom_input.setValue(self.top_input.value())
        else:
            rate = self.get_exchange_rate(key, top_currency, bottom_currency)
            converted = self.conversion(value, rate)
            self.bottom_input.setValue(converted)
        self.bottom_input.blockSignals(False)

    def on_bottom_selection_changed(self):
        top_currency = self.top_input_selection.currentText()
        bottom_currency = self.bottom_input_selection.currentText()
        value = self.top_input.value()
        self.bottom_input.blockSignals(True)
        if value == "":
            return
        rate = self.get_exchange_rate(key, top_currency, bottom_currency)
        converted = self.conversion(value, rate)
        self.bottom_input.setValue(converted)
        self.bottom_input.blockSignals(False)

    def get_exchange_rate(self, api_key: str, base: str, target: str) -> float:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data["conversion_rates"][f"{target}"]
        else:
            return 

    def conversion(self, value: float, multiplier: float) -> float:
        return value * multiplier

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()