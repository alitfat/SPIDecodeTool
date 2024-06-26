# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SPIDecodeToolGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

AlignmentFlagDefault = QtCore.Qt.AlignmentFlag(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)

class Ui_SPIDecodeToolGUI(object):
    def setupUi(self, SPIDecodeToolGUI:QtWidgets.QWidget):
        SPIDecodeToolGUI.setObjectName("SPIDecodeToolGUI")
        SPIDecodeToolGUI.setWindowModality(QtCore.Qt.WindowModality.NonModal)
        SPIDecodeToolGUI.setWindowFlags(QtCore.Qt.WindowType.Window)
        SPIDecodeToolGUI.setEnabled(True)
        SPIDecodeToolGUI.resize(800, 375)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SPIDecodeToolGUI.sizePolicy().hasHeightForWidth())
        SPIDecodeToolGUI.setSizePolicy(sizePolicy)
        SPIDecodeToolGUI.setMinimumSize(QtCore.QSize(800, 375))
        SPIDecodeToolGUI.setMaximumSize(QtCore.QSize(800, 375))
        SPIDecodeToolGUI.setAutoFillBackground(False)
        SPIDecodeToolGUI.setStyleSheet("")
        self.menubar = QtWidgets.QMenuBar(SPIDecodeToolGUI)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 1020, 25))
        self.menubar.setAutoFillBackground(False)
        self.menubar.setStyleSheet("")
        self.menubar.setObjectName("menubar")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.lbObjFileName = QtWidgets.QLabel(SPIDecodeToolGUI)
        self.lbObjFileName.setGeometry(QtCore.QRect(10, 40, 101, 16))
        self.lbObjFileName.setAlignment(AlignmentFlagDefault)
        self.lbObjFileName.setObjectName("lbObjFileName")
        self.lbDstFileName = QtWidgets.QLabel(SPIDecodeToolGUI)
        self.lbDstFileName.setGeometry(QtCore.QRect(9, 170, 101, 20))
        self.lbDstFileName.setAlignment(AlignmentFlagDefault)
        self.lbDstFileName.setObjectName("lbDstFileName")
        self.txObjFileName = QtWidgets.QTextEdit(SPIDecodeToolGUI)
        self.txObjFileName.setGeometry(QtCore.QRect(120, 40, 480, 50))
        self.txObjFileName.setDocumentTitle("")
        self.txObjFileName.setObjectName("txObjFileName")
        self.txDstFileName = QtWidgets.QTextEdit(SPIDecodeToolGUI)
        self.txDstFileName.setEnabled(False)
        self.txDstFileName.setGeometry(QtCore.QRect(120, 170, 480, 30))
        self.txDstFileName.setObjectName("txDstFileName")
        self.btObjFileName = QtWidgets.QPushButton(SPIDecodeToolGUI)
        self.btObjFileName.setGeometry(QtCore.QRect(610, 40, 50, 25))
        self.btObjFileName.setObjectName("btObjFileName")
        self.cbDstFileName = QtWidgets.QCheckBox(SPIDecodeToolGUI)
        self.cbDstFileName.setGeometry(QtCore.QRect(610, 170, 101, 16))
        self.cbDstFileName.setObjectName("cbDstFileName")
        self.lbDstFilePath = QtWidgets.QLabel(SPIDecodeToolGUI)
        self.lbDstFilePath.setGeometry(QtCore.QRect(10, 100, 101, 20))
        self.lbDstFilePath.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.lbDstFilePath.setAlignment(AlignmentFlagDefault)
        self.lbDstFilePath.setObjectName("lbDstFilePath")
        self.txDstFilePath = QtWidgets.QTextEdit(SPIDecodeToolGUI)
        self.txDstFilePath.setEnabled(False)
        self.txDstFilePath.setGeometry(QtCore.QRect(120, 100, 480, 50))
        self.txDstFilePath.setObjectName("txDstFilePath")
        self.cbDstFilePath = QtWidgets.QCheckBox(SPIDecodeToolGUI)
        self.cbDstFilePath.setEnabled(True)
        self.cbDstFilePath.setGeometry(QtCore.QRect(610, 100, 91, 16))
        self.cbDstFilePath.setChecked(False)
        self.cbDstFilePath.setObjectName("cbDstFilePath")
        self.btDstFilePath = QtWidgets.QPushButton(SPIDecodeToolGUI)
        self.btDstFilePath.setEnabled(False)
        self.btDstFilePath.setGeometry(QtCore.QRect(610, 120, 50, 25))
        self.btDstFilePath.setObjectName("btDstFilePath")
        self.lbDstFileNote = QtWidgets.QLabel(SPIDecodeToolGUI)
        self.lbDstFileNote.setGeometry(QtCore.QRect(120, 210, 251, 20))
        self.lbDstFileNote.setObjectName("lbDstFileNote")
        self.btDstFileProcess = QtWidgets.QPushButton(SPIDecodeToolGUI)
        self.btDstFileProcess.setGeometry(QtCore.QRect(220, 250, 210, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btDstFileProcess.setFont(font)
        self.btDstFileProcess.setObjectName("btDstFileProcess")
        self.cbDstFileOverWrite = QtWidgets.QCheckBox(SPIDecodeToolGUI)
        self.cbDstFileOverWrite.setGeometry(QtCore.QRect(370, 210, 121, 16))
        self.cbDstFileOverWrite.setChecked(True)
        self.cbDstFileOverWrite.setObjectName("cbDstFileOverWrite")
        self.cb2ExcelFile = QtWidgets.QCheckBox(SPIDecodeToolGUI)
        self.cb2ExcelFile.setEnabled(True)
        self.cb2ExcelFile.setGeometry(QtCore.QRect(510, 210, 121, 16))
        self.cb2ExcelFile.setChecked(False)
        self.cb2ExcelFile.setObjectName("cb2ExcelFile")
        self.actionOther = QtWidgets.QAction(SPIDecodeToolGUI)
        self.actionOther.setObjectName("actionOther")
        self.actionAboutDstDecodeTool = QtWidgets.QAction(SPIDecodeToolGUI)
        self.actionAboutDstDecodeTool.setObjectName("actionAboutDstDecodeTool")
        self.menubar.raise_()
        self.btObjFileName.raise_()
        self.lbObjFileName.raise_()
        self.lbDstFileName.raise_()
        self.txObjFileName.raise_()
        self.txDstFileName.raise_()
        self.cbDstFileName.raise_()
        self.lbDstFilePath.raise_()
        self.txDstFilePath.raise_()
        self.cbDstFilePath.raise_()
        self.btDstFilePath.raise_()
        self.lbDstFileNote.raise_()
        self.btDstFileProcess.raise_()
        self.cbDstFileOverWrite.raise_()
        self.cb2ExcelFile.raise_()
        self.menuSetting.addAction(self.actionOther)
        self.menuHelp.addAction(self.actionAboutDstDecodeTool)
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(SPIDecodeToolGUI)
        QtCore.QMetaObject.connectSlotsByName(SPIDecodeToolGUI)

    def retranslateUi(self, SPIDecodeToolGUI:QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        SPIDecodeToolGUI.setWindowTitle(_translate("SPIDecodeToolGUI", "SPIEditerToolGUI"))
        self.menuSetting.setTitle(_translate("SPIDecodeToolGUI", "menuSetting"))
        self.menuHelp.setTitle(_translate("SPIDecodeToolGUI", "Help"))
        self.lbObjFileName.setText(_translate("SPIDecodeToolGUI", "ObjectFileAddress"))
        self.lbDstFileName.setText(_translate("SPIDecodeToolGUI", "DstFileName"))
        self.txObjFileName.setHtml(_translate("SPIDecodeToolGUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS UI Gothic\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.btObjFileName.setText(_translate("SPIDecodeToolGUI", "select"))
        self.cbDstFileName.setText(_translate("SPIDecodeToolGUI", "Handwritting"))
        self.lbDstFilePath.setText(_translate("SPIDecodeToolGUI", "DstFilePath"))
        self.cbDstFilePath.setText(_translate("SPIDecodeToolGUI", "Handwritting"))
        self.btDstFilePath.setText(_translate("SPIDecodeToolGUI", "select"))
        self.lbDstFileNote.setText(_translate("SPIDecodeToolGUI", "※ 👆 Don\'t input the extension name please."))
        self.btDstFileProcess.setText(_translate("SPIDecodeToolGUI", "DstFileProcess"))
        self.cbDstFileOverWrite.setText(_translate("SPIDecodeToolGUI", "overwrite saving"))
        self.cb2ExcelFile.setText(_translate("SPIDecodeToolGUI", "outputExcelFile"))
        self.actionOther.setText(_translate("SPIDecodeToolGUI", "actionOther(NoUse)"))
        self.actionAboutDstDecodeTool.setText(_translate("SPIDecodeToolGUI", "AboutDstDecodeTool"))
