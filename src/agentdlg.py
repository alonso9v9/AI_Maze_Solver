# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'agent.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import math
from PyQt5 import QtCore, QtWidgets
import agent

class AgentDialog(QtCore.QObject):
    """ Agent Configuration Dialog """

    applySignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(QtCore.QObject, self).__init__(parent)
        self.maze = None

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(380, 185)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply |
                                          QtWidgets.QDialogButtonBox.Cancel |
                                          QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.sensorsCheck = QtWidgets.QCheckBox(Dialog)
        self.sensorsCheck.setObjectName("sensorsCheck")
        self.verticalLayout.addWidget(self.sensorsCheck)
        self.sensorsLayout = QtWidgets.QHBoxLayout()
        self.sensorsLayout.setObjectName("sensorsLayout")
        self.apertureLabel = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apertureLabel.sizePolicy()
                                     .hasHeightForWidth())
        self.apertureLabel.setSizePolicy(sizePolicy)
        self.apertureLabel.setMaximumSize(QtCore.QSize(91, 16777215))
        self.apertureLabel.setObjectName("apertureLabel")
        self.sensorsLayout.addWidget(self.apertureLabel)
        self.apertureSpin = QtWidgets.QSpinBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apertureSpin.sizePolicy()
                                     .hasHeightForWidth())
        self.apertureSpin.setSizePolicy(sizePolicy)
        self.apertureSpin.setMaximum(360)
        self.apertureSpin.setSingleStep(15)
        self.apertureSpin.setProperty("value", 180)
        self.apertureSpin.setObjectName("apertureSpin")
        self.sensorsLayout.addWidget(self.apertureSpin)
        self.nsensorsLabel = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nsensorsLabel.sizePolicy().
                                     hasHeightForWidth())
        self.nsensorsLabel.setSizePolicy(sizePolicy)
        self.nsensorsLabel.setObjectName("nsensorsLabel")
        self.sensorsLayout.addWidget(self.nsensorsLabel)
        self.numSensorsSpin = QtWidgets.QSpinBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numSensorsSpin.sizePolicy()
                                     .hasHeightForWidth())
        self.numSensorsSpin.setSizePolicy(sizePolicy)
        self.numSensorsSpin.setMaximum(24)
        self.numSensorsSpin.setProperty("value", 3)
        self.numSensorsSpin.setObjectName("numSensorsSpin")
        self.sensorsLayout.addWidget(self.numSensorsSpin)
        self.verticalLayout.addLayout(self.sensorsLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy()
                                     .hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.maxDistSpin = QtWidgets.QDoubleSpinBox(Dialog)
        self.maxDistSpin.setDecimals(0)
        self.maxDistSpin.setMaximum(5000.0)
        self.maxDistSpin.setProperty("value", 20.0)
        self.maxDistSpin.setObjectName("maxDistSpin")
        self.horizontalLayout.addWidget(self.maxDistSpin)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.noiseLayout = QtWidgets.QHBoxLayout()
        self.noiseLayout.setObjectName("noiseLayout")
        self.tnoiseLabel = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tnoiseLabel.sizePolicy()
                                     .hasHeightForWidth())
        self.tnoiseLabel.setSizePolicy(sizePolicy)
        self.tnoiseLabel.setObjectName("tnoiseLabel")
        self.noiseLayout.addWidget(self.tnoiseLabel)
        self.tnoiseSpin = QtWidgets.QDoubleSpinBox(Dialog)
        self.tnoiseSpin.setDecimals(1)
        self.tnoiseSpin.setMaximum(100.0)
        self.tnoiseSpin.setSingleStep(0.1)
        self.tnoiseSpin.setStepType(QtWidgets.QAbstractSpinBox
                                    .AdaptiveDecimalStepType)
        self.tnoiseSpin.setProperty("value", 1.0)
        self.tnoiseSpin.setObjectName("tnoiseSpin")
        self.noiseLayout.addWidget(self.tnoiseSpin)
        self.rnoiseLabel = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rnoiseLabel.sizePolicy()
                                     .hasHeightForWidth())
        self.rnoiseLabel.setSizePolicy(sizePolicy)
        self.rnoiseLabel.setObjectName("rnoiseLabel")
        self.noiseLayout.addWidget(self.rnoiseLabel)
        self.rnoiseSpin = QtWidgets.QDoubleSpinBox(Dialog)
        self.rnoiseSpin.setMaximum(30.0)
        self.rnoiseSpin.setSingleStep(0.1)
        self.rnoiseSpin.setStepType(QtWidgets.QAbstractSpinBox
                                    .AdaptiveDecimalStepType)
        self.rnoiseSpin.setProperty("value", 1.0)
        self.rnoiseSpin.setObjectName("rnoiseSpin")
        self.noiseLayout.addWidget(self.rnoiseSpin)
        self.verticalLayout.addLayout(self.noiseLayout)
        self.geometryLayout = QtWidgets.QHBoxLayout()
        self.geometryLayout.setObjectName("geometryLayout")
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy()
                                     .hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.geometryLayout.addWidget(self.label)
        self.radiusSpin = QtWidgets.QDoubleSpinBox(Dialog)
        self.radiusSpin.setDecimals(1)
        self.radiusSpin.setMinimum(1.0)
        self.radiusSpin.setMaximum(45.0)
        self.radiusSpin.setSingleStep(0.5)
        self.radiusSpin.setProperty("value", 2.5)
        self.radiusSpin.setObjectName("radiusSpin")
        self.geometryLayout.addWidget(self.radiusSpin)
        self.verticalLayout.addLayout(self.geometryLayout)
        self.line_3 = QtWidgets.QFrame(Dialog)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.\
            connect(self.applyChanges)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Agent Properties"))
        self.sensorsCheck.setText(_translate("Dialog",
                                         "Activate agent\'s sensor array"))
        self.apertureLabel.setText(_translate("Dialog", "Aperture"))
        self.apertureSpin.setSuffix(_translate("Dialog", "°"))
        self.nsensorsLabel.setText(_translate("Dialog", "Num Sensors"))
        self.label_2.setText(_translate("Dialog", "Max distance"))
        self.tnoiseLabel.setText(_translate("Dialog", "Translation noise"))
        self.tnoiseSpin.setSuffix(_translate("Dialog", "%"))
        self.rnoiseLabel.setText(_translate("Dialog", "Rotation noise"))
        self.rnoiseSpin.setSuffix(_translate("Dialog", "°"))
        self.label.setText(_translate("Dialog", "Agent\'s radius"))

    def exportValues(self):
        """ Extract the values from the GUI elements and store them into the
            agent 
        """
        
        self.agent.radius = self.radiusSpin.value()
        self.agent.sensors = self.sensorsCheck.isChecked()
        a = self.apertureSpin.value()
        if a > 0:
            s = max(1,self.numSensorsSpin.value())
            if s > 1:
                m = a/(s-1)
                b = -a/2
                sens = [float(i)*m+b for i in range(s)]
            else:
                sens = [0]
            self.agent.sensorArray = sens
        else:   
            self.agent.sensorArray = [0]
        
        self.agent.maxDistance = self.maxDistSpin.value()
        self.agent.translationNoiseFactor = self.tnoiseSpin.value()/100
        self.agent.rotationNoise = self.rnoiseSpin.value()

    def accept(self):
        print("[DBG] Accepting new values")
        self.exportValues()
        self.parentAccept()

    def applyChanges(self):
        print("[DBG] Applying new values")
        self.exportValues()
        self.applySignal.emit()

    def setValues(self, theAgent):
        """ Copy the data from the agent into the dialog settings"""

        print("[DBG] Setting current values into the dialog")
        self.agent = theAgent

        self.radiusSpin.setValue(self.agent.radius)

        if self.agent.sensorArray:
            numSensors = len(self.agent.sensorArray)
            if numSensors > 0:
                self.sensorsCheck.setChecked(self.agent.sensors)
                aperture = self.agent.sensorArray[-1]-self.agent.sensorArray[0]
                self.apertureSpin.setValue(aperture)
                self.numSensorsSpin.setValue(numSensors)
            else:
                self.sensorsCheck.setChecked(False)
        else:
            self.sensorsCheck.setChecked(False)
            self.apertureSpin.setValue(180)  # Default values
            self.numSensorsSpin(3)  # Default values

        self.maxDistSpin.setValue(self.agent.maxDistance)
        self.rnoiseSpin.setValue(self.agent.rotationNoise)
        self.tnoiseSpin.setValue(self.agent.translationNoiseFactor*100)