from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(360, 162)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        Form.setFont(font)
        self.computerPlayButton = QtWidgets.QPushButton(Form)
        self.computerPlayButton.setGeometry(QtCore.QRect(10, 60, 340, 41))
        self.computerPlayButton.setObjectName("computerPlayButton")
        self.singlePlayButton = QtWidgets.QPushButton(Form)
        self.singlePlayButton.setGeometry(QtCore.QRect(10, 10, 340, 41))
        self.singlePlayButton.setObjectName("singlePlayButton")
        self.exitButton = QtWidgets.QPushButton(Form)
        self.exitButton.setGeometry(QtCore.QRect(10, 110, 340, 41))
        self.exitButton.setObjectName("exitButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Клещи - Меню"))
        self.computerPlayButton.setText(_translate("Form", "Играть с компьютером"))
        self.singlePlayButton.setText(_translate("Form", "Одиночная игра"))
        self.exitButton.setText(_translate("Form", "Выход"))
