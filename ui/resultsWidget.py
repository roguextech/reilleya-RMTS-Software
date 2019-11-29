import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog

from ui.views.ResultsWidget_ui import Ui_ResultsWidget

from lib.firing import Firing

class ResultsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ResultsWidget()
        self.ui.setupUi(self)

        self.firing = None
        self.motorData = None

        self.ui.checkBoxForce.stateChanged.connect(self.regraphData)
        self.ui.checkBoxPressure.stateChanged.connect(self.regraphData)
        self.ui.radioButtonTranslated.toggled.connect(self.regraphData)
        self.ui.radioButtonRaw.toggled.connect(self.regraphData)

        self.ui.pushButtonCSV.pressed.connect(self.saveCSV)

    def processResultsPacket(self, packet):
        if self.firing is not None: 
            self.firing.addDatapoint(packet)

    def setFiring(self, firing):
        self.firing = firing
        self.firing.newGraph.connect(self.showResults)

    def regraphData(self):
        if self.ui.radioButtonTranslated.isChecked():
            if self.motorData is None:
                return
            if self.ui.checkBoxForce.isChecked() and self.ui.checkBoxPressure.isChecked():
                self.ui.widgetGraph.plotData(self.motorData.getTime(), self.motorData.getForce(), self.motorData.getPressure())
            elif self.ui.checkBoxForce.isChecked() and not self.ui.checkBoxPressure.isChecked():
                self.ui.widgetGraph.plotData(self.motorData.getTime(), self.motorData.getForce())
            elif not self.ui.checkBoxForce.isChecked() and self.ui.checkBoxPressure.isChecked():
                self.ui.widgetGraph.plotData(self.motorData.getTime(), self.motorData.getPressure())
        else:
            if self.ui.checkBoxForce.isChecked() and self.ui.checkBoxPressure.isChecked():
                self.ui.widgetGraph.plotData(self.firing.getRawTime(), self.firing.getRawForce(), self.firing.getRawPressure())
            elif self.ui.checkBoxForce.isChecked() and not self.ui.checkBoxPressure.isChecked():
                self.ui.widgetGraph.plotData(self.firing.getRawTime(), self.firing.getRawForce())
            elif not self.ui.checkBoxForce.isChecked() and self.ui.checkBoxPressure.isChecked():
                self.ui.widgetGraph.plotData(self.firing.getRawTime(), self.firing.getRawPressure())

    def showResults(self, motorData):
        self.ui.labelMotorDesignation.setText(motorData.getMotorDesignation())
        self.ui.labelBurnTime.setText("{} s".format(round(motorData.getBurnTime(), 3)))
        self.ui.labelStartupTime.setText("{} s".format(round(motorData.getStartupTime(), 3)))

        self.ui.labelImpulse.setText("{} Ns".format(round(motorData.getImpulse(), 1)))
        self.ui.labelPropellantMass.setText("{} Kg".format(round(motorData.getPropMass(), 3)))
        self.ui.labelISP.setText("{} s".format(round(motorData.getISP(), 3)))

        self.ui.labelPeakThrust.setText("{} N".format(round(motorData.getPeakThrust(), 1)))
        self.ui.labelAverageThrust.setText("{} N".format(round(motorData.getAverageThrust(), 1)))
        self.ui.labelDatapoints.setText(str(motorData.getNumDataPoints()))

        self.ui.labelPeakPressure.setText("{} Pa".format(round(motorData.getPeakPressure(), 3)))
        self.ui.labelAveragePressure.setText("{} Pa".format(round(motorData.getAveragePressure(), 3)))
        self.ui.labelCStar.setText("{} m/s".format(round(motorData.getCStar(), 3)))

        self.motorData = motorData
        self.regraphData()

    def saveCSV(self):
        path = QFileDialog.getSaveFileName(None, 'Save CSV', '', 'Comma Separated Values (*.csv)')[0]
        if path is not None:
            if not path.endswith('.csv'):
                path += '.csv'
            data = self.motorData.getCSV()
            with open(path, 'w') as outFile:
                outFile.write(data)
