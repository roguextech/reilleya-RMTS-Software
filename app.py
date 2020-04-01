import sys

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import pyqtSignal

from lib.sensorProfileManager import SensorProfileManager
from lib.preferencesManager import PreferencesManager
from lib.logger import logger
from ui.mainWindow import MainWindow

class App(QApplication):

    newConverter = pyqtSignal(object)
    newFiringConfig = pyqtSignal(object)

    def __init__(self, args):
        super().__init__(args)
        self.sensorProfileManager = SensorProfileManager()
        self.sensorProfileManager.loadProfiles()
        self.preferencesManager = PreferencesManager()
        self.preferencesManager.loadPreferences()

        self.window = MainWindow(self)
        logger.log('Showing window')
        self.window.show()

    def outputMessage(self, content, title='RMTSI'):
        msg = QMessageBox()
        msg.setText(content)
        msg.setWindowTitle(title)
        msg.exec_()

    def outputException(self, exception, text, title='RMTSI - Error'):
        msg = QMessageBox()
        msg.setText(text)
        msg.setInformativeText(str(exception))
        msg.setWindowTitle(title)
        msg.exec_()

    def convertToUserUnits(self, value, units):
        return self.preferencesManager.preferences.convert(value, units)

    def convertAllToUserUnits(self, values, units):
        return self.preferencesManager.preferences.convertAll(values, units)

    def convertToUserAndFormat(self, value, units, places):
        return self.preferencesManager.preferences.convFormat(value, units, places)

    def getUserUnit(self, unit):
        return self.preferencesManager.preferences.getUnit(unit)

    def getPreferences(self):
        return self.preferencesManager.preferences

    def newResult(self, motorInfo):
        self.window.ui.pageResults.showResults(motorInfo)
