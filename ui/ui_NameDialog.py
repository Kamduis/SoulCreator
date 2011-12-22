# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_NameDialog.ui'
#
# Created: Thu Dec 22 11:21:17 2011
#      by: pyside-uic 0.2.11 running on PySide 1.0.6
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NameDialog(object):
	def setupUi(self, NameDialog):
		NameDialog.setObjectName("NameDialog")
		NameDialog.resize(316, 237)
		self.verticalLayout = QtGui.QVBoxLayout(NameDialog)
		self.verticalLayout.setObjectName("verticalLayout")
		self.label_displayFull = QtGui.QLabel(NameDialog)
		self.label_displayFull.setText("")
		self.label_displayFull.setAlignment(QtCore.Qt.AlignCenter)
		self.label_displayFull.setObjectName("label_displayFull")
		self.verticalLayout.addWidget(self.label_displayFull)
		self.label_displayDisplay = QtGui.QLabel(NameDialog)
		self.label_displayDisplay.setText("")
		self.label_displayDisplay.setAlignment(QtCore.Qt.AlignCenter)
		self.label_displayDisplay.setObjectName("label_displayDisplay")
		self.verticalLayout.addWidget(self.label_displayDisplay)
		self.label_displayHonorific = QtGui.QLabel(NameDialog)
		self.label_displayHonorific.setText("")
		self.label_displayHonorific.setAlignment(QtCore.Qt.AlignCenter)
		self.label_displayHonorific.setObjectName("label_displayHonorific")
		self.verticalLayout.addWidget(self.label_displayHonorific)
		self.label_displaySuper = QtGui.QLabel(NameDialog)
		self.label_displaySuper.setText("")
		self.label_displaySuper.setAlignment(QtCore.Qt.AlignCenter)
		self.label_displaySuper.setObjectName("label_displaySuper")
		self.verticalLayout.addWidget(self.label_displaySuper)
		self.formLayout = QtGui.QFormLayout()
		self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
		self.formLayout.setObjectName("formLayout")
		self.label_firstName = QtGui.QLabel(NameDialog)
		self.label_firstName.setObjectName("label_firstName")
		self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_firstName)
		self.lineEdit_firstName = QtGui.QLineEdit(NameDialog)
		self.lineEdit_firstName.setObjectName("lineEdit_firstName")
		self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_firstName)
		self.label_additionalForenames = QtGui.QLabel(NameDialog)
		self.label_additionalForenames.setObjectName("label_additionalForenames")
		self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_additionalForenames)
		self.lineEdit_additionalForenames = QtGui.QLineEdit(NameDialog)
		self.lineEdit_additionalForenames.setObjectName("lineEdit_additionalForenames")
		self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_additionalForenames)
		self.label_surename = QtGui.QLabel(NameDialog)
		self.label_surename.setObjectName("label_surename")
		self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_surename)
		self.lineEdit_surename = QtGui.QLineEdit(NameDialog)
		self.lineEdit_surename.setObjectName("lineEdit_surename")
		self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_surename)
		self.label_honorificName = QtGui.QLabel(NameDialog)
		self.label_honorificName.setObjectName("label_honorificName")
		self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_honorificName)
		self.lineEdit_honorificName = QtGui.QLineEdit(NameDialog)
		self.lineEdit_honorificName.setObjectName("lineEdit_honorificName")
		self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_honorificName)
		self.label_nickname = QtGui.QLabel(NameDialog)
		self.label_nickname.setObjectName("label_nickname")
		self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_nickname)
		self.lineEdit_nickname = QtGui.QLineEdit(NameDialog)
		self.lineEdit_nickname.setObjectName("lineEdit_nickname")
		self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_nickname)
		self.label_specialName = QtGui.QLabel(NameDialog)
		self.label_specialName.setObjectName("label_specialName")
		self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_specialName)
		self.lineEdit_specialName = QtGui.QLineEdit(NameDialog)
		self.lineEdit_specialName.setObjectName("lineEdit_specialName")
		self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineEdit_specialName)
		self.verticalLayout.addLayout(self.formLayout)
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)
		self.buttonBox = QtGui.QDialogButtonBox(NameDialog)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName("buttonBox")
		self.horizontalLayout.addWidget(self.buttonBox)
		self.verticalLayout.addLayout(self.horizontalLayout)

		self.retranslateUi(NameDialog)
		QtCore.QMetaObject.connectSlotsByName(NameDialog)

	def retranslateUi(self, NameDialog):
		NameDialog.setWindowTitle(QtGui.QApplication.translate("NameDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
		self.label_firstName.setToolTip(QtGui.QApplication.translate("NameDialog", "First forename of the Character. The name, he is called by friends and family (if they don\'t use the nickname, of course).", None, QtGui.QApplication.UnicodeUTF8))
		self.label_firstName.setText(QtGui.QApplication.translate("NameDialog", "First Name", None, QtGui.QApplication.UnicodeUTF8))
		self.label_additionalForenames.setToolTip(QtGui.QApplication.translate("NameDialog", "Other forenames of the character. If the character has more than one additional forenames, seperate them by space.", None, QtGui.QApplication.UnicodeUTF8))
		self.label_additionalForenames.setText(QtGui.QApplication.translate("NameDialog", "Additional Fornames", None, QtGui.QApplication.UnicodeUTF8))
		self.label_surename.setToolTip(QtGui.QApplication.translate("NameDialog", "The surename of the Character.", None, QtGui.QApplication.UnicodeUTF8))
		self.label_surename.setText(QtGui.QApplication.translate("NameDialog", "Surename", None, QtGui.QApplication.UnicodeUTF8))
		self.label_honorificName.setToolTip(QtGui.QApplication.translate("NameDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The honorific name is a postfix name, normally used after his first name. Hermann <span style=\" font-style:italic;\">the Strong</span>, Jasmin <span style=\" font-style:italic;\">the Fair</span> or Philippe <span style=\" font-style:italic;\">the Wise</span>.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
		self.label_honorificName.setText(QtGui.QApplication.translate("NameDialog", "Honorific Name", None, QtGui.QApplication.UnicodeUTF8))
		self.label_nickname.setToolTip(QtGui.QApplication.translate("NameDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The nickname normally given by friends. Frederick my be called <span style=\" font-style:italic;\">Freddy</span> or Thomas may have earnd the Name <span style=\" font-style:italic;\">Dragon</span> in his Gang.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
		self.label_nickname.setText(QtGui.QApplication.translate("NameDialog", "Nickname", None, QtGui.QApplication.UnicodeUTF8))
		self.label_specialName.setToolTip(QtGui.QApplication.translate("NameDialog", "The special name is the Name a Charcter uses inside his own supernatural society. Mages call this name the Shadow Name, Werewolfs have their Deed names and even Changelings and Vampires may have their own special names among their peers.", None, QtGui.QApplication.UnicodeUTF8))
		self.label_specialName.setText(QtGui.QApplication.translate("NameDialog", "Special Name", None, QtGui.QApplication.UnicodeUTF8))

