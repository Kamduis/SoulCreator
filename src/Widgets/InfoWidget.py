# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) Victor von Rhein, 2011, 2012

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

import os

from PySide.QtCore import Qt, QSize, QFile, QDate, Signal
from PySide.QtGui import QWidget, QIcon, QLabel, QPixmap, QFileDialog, QMessageBox

from src.Config import Config
from src.Tools import PathTools
from src.Calc.Calc import Calc
from src.Datatypes.Identity import Identity
from src.Widgets.Dialogs.NameDialog import NameDialog
from src.Debug import Debug

from ui.ui_InfoWidget import Ui_InfoWidget




class InfoWidget(QWidget):
	"""
	@brief Das Widget, in welchem wichtige Informationen dargestellt werden.

	Namen, Alter, Nationalität etc. des Charakters werden hier dargestellt.

	\note Der Beschreibungstext wird nur gespeichert, wenn das Textfeld, indem er eingetragen wird, den Fokus verliert. Müßte aber ausreichen, da ihm bspw. schon das Speichern den Fokus raubt.
	"""


	nameChanged = Signal(str)
	notificationSent = Signal(str)


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.ui = Ui_InfoWidget()
		self.ui.setupUi(self)

		self.__storage = template
		self.__character = character

		self.ui.comboBox_era.addItems( Config.eras )

		self.ui.dateEdit_dateBirth.setMinimumDate(QDate(100, 1, 1))
		self.ui.dateEdit_dateGame.setMinimumDate(QDate(100, 1, 1))

		self.ui.pushButton_pictureClear.setIcon(QIcon(":/icons/images/actions/cancel.png"))
		self.ui.pushButton_pictureClear.setText("")
		self.ui.pushButton_pictureClear.setEnabled(False)

		## Speichern der vom Benutzer veränderten Werte
		self.ui.pushButton_name.clicked.connect(self.openNameDialog)
		self.ui.comboBox_era.currentIndexChanged[str].connect(self.__character.setEra)
		self.ui.dateEdit_dateBirth.dateEdited.connect(self.setCharacterDateBirth)
		#self.ui.dateEdit_dateBirth.dateChanged.connect(self.__character.setDateBirth)
		self.ui.dateEdit_dateGame.dateEdited.connect(self.setCharacterDateGame)
		#self.ui.dateEdit_dateGame.dateChanged.connect(self.__character.setDateGame)
		self.ui.comboBox_virtue.currentIndexChanged[str].connect(self.__character.setVirtue)
		self.ui.comboBox_vice.currentIndexChanged[str].connect(self.__character.setVice)
		self.ui.doubleSpinBox_height.valueChanged[float].connect(self.setCharacterHeight)
		self.ui.spinBox_weight.valueChanged[int].connect(self.__character.setWeight)
		self.ui.lineEdit_eyes.textEdited.connect(self.__character.setEyes)
		self.ui.lineEdit_hair.textEdited.connect(self.__character.setHair)
		self.ui.lineEdit_nationality.textEdited.connect(self.__character.setNationality)
		self.ui.pushButton_picture.clicked.connect(self.openImage)
		self.ui.pushButton_pictureClear.clicked.connect(self.clearImage)
		#self.ui.textEdit_description.textChanged.connect(self.saveDescription)	## Kann ich nicht nutzen, da sonst der Curser bei jeder änderung an den Angang springt.
		self.ui.textEdit_description.focusLost.connect(self.changeDescription)

		## Aktualisieren der Darstellung der im Charakter veränderten Werte.
		self.__character.identity.identityChanged.connect(self.updateButtonText)
		self.__character.eraChanged.connect(self.updateEra)
		self.__character.dateBirthChanged.connect(self.ui.dateEdit_dateBirth.setDate)
		#self.__character.dateBecomingChanged.connect(self.ui.dateEdit_dateBecoming.setDate)
		self.__character.dateGameChanged.connect(self.ui.dateEdit_dateGame.setDate)
		self.__character.ageChanged.connect(self.ui.label_age.setNum)
		#self.__character.ageBecomingChanged.connect(self.ui.label_ageBecoming.setNum)
		self.__character.virtueChanged.connect(self.updateVirtue)
		self.__character.viceChanged.connect(self.updateVice)
		self.__character.heightChanged.connect(self.ui.doubleSpinBox_height.setValue)
		self.__character.weightChanged.connect(self.ui.spinBox_weight.setValue)
		self.__character.eyesChanged.connect(self.ui.lineEdit_eyes.setText)
		self.__character.hairChanged.connect(self.ui.lineEdit_hair.setText)
		self.__character.nationalityChanged.connect(self.ui.lineEdit_nationality.setText)
		self.__character.pictureChanged.connect(self.updatePicture)
		self.__character.descriptionChanged.connect(self.ui.textEdit_description.setPlainText)

		## Das Alter darf nie negativ werden können
		#self.ui.dateEdit_dateBirth.dateChanged.connect(self.ui.dateEdit_dateBecoming.setMinimumDate)
		self.ui.dateEdit_dateGame.dateChanged.connect(self.setMaxBirthday)

		## Ändert sich das Alter, gibt es andere Virtues und Vices.
		self.__character.ageChanged.connect(self.updateVirtueTitle)
		self.__character.ageChanged.connect(self.repopulateVirtues)
		self.__character.ageChanged.connect(self.updateViceTitle)
		self.__character.ageChanged.connect(self.repopulateVices)

		self.__character.ageChanged.connect(self.setHeightMinMax)
		self.__character.traits["Merit"]["Physical"]["Giant"].valueChanged.connect(self.updateHeight)
		self.__character.traits["Flaw"]["Physical"]["Dwarf"].valueChanged.connect(self.updateHeight)



	def openNameDialog(self):
		"""
		Ruft einen Dialog auf, in welchem die zahlreichen Namen des Charakters eingetragen werden können.
		"""

		dialog = NameDialog( self.__character, self )
		dialog.exec_()


	def changeDescription( self ):
		"""
		Verändert den Beschreibungstext im Speicher.
		"""

		self.__character.description = self.ui.textEdit_description.toPlainText()


	def updateButtonText( self ):
		"""
		Aktualisiert die Anzeige des Namens.
		"""

		nameStr = Identity.displayNameDisplay(self.__character.identity.surname, self.__character.identity.firstname, self.__character.identity.nickname)
		nameDisplay = nameStr
		if not nameStr:
			nameStr = self.tr("Name")
		self.ui.pushButton_name.setText( nameStr )
		genderIcon = QIcon()
		for item in Config.genders:
			if self.__character.identity.gender == item[0]:
				self.ui.pushButton_name.setIcon(QIcon(item[1]))
				break
		self.nameChanged.emit(nameDisplay)


	def updateEra(self, era):
		"""
		Aktualisiert die Anzeige der Ära
		"""

		#Debug.debug("Verändere Anzeige der Ära auf {}".format(era))
		self.ui.comboBox_era.setCurrentIndex(self.ui.comboBox_era.findText(era))


	def updateVirtue( self, virtue ):
		"""
		Aktualisiert die Anzeige der Tugend.
		"""

		self.ui.comboBox_virtue.setCurrentIndex( self.ui.comboBox_virtue.findText( virtue ) )


	def updateVice( self, vice ):
		"""
		Aktualisiert die Anzeige des Lasters.
		"""

		self.ui.comboBox_vice.setCurrentIndex( self.ui.comboBox_vice.findText( vice ) )


	def updateVirtueTitle( self, age ):
		"""
		Wenn die Alterskategorie sich ändert, ändert sich auch der Bezeichner für die Tugenden.
		"""

		label = self.tr("Virtue")
		if age < Config.ageAdult:
			label = self.tr("Asset")
		if self.ui.label_virtue.text() != label:
			self.ui.label_virtue.setText( "{}:".format(label) )


	def updateViceTitle( self, age ):
		"""
		Wenn die Alterskategorie sich ändert, ändert sich auch der Bezeichner für die Laster.
		"""

		label = self.tr("Vice")
		if age < Config.ageAdult:
			label = self.tr("Fault")
		if self.ui.label_vice.text() != label:
			self.ui.label_vice.setText( "{}:".format(label) )


	def repopulateVirtues(self, age):
		ageStr = Config.ages[0]
		if age < Config.ageAdult:
			ageStr = Config.ages[1]

		virtueList = []
		for item in self.__storage.virtues:
			if item["age"] == ageStr:
				virtueList.append(item["name"])

		## Die Liste soll nur aktualisiert werden, wenn eine neue Alterskategorie erreicht wird.
		if self.ui.comboBox_virtue.itemText(0) not in virtueList:
			self.ui.comboBox_virtue.clear()
			self.ui.comboBox_virtue.addItems(virtueList)


	def repopulateVices(self, age):
		ageStr = Config.ages[0]
		if age < Config.ageAdult:
			ageStr = Config.ages[1]

		viceList = []
		for item in self.__storage.vices:
			if item["age"] == ageStr:
				viceList.append(item["name"])

		## Die Liste soll nur aktualisiert werden, wenn eine neue Alterskategorie erreicht wird.
		if self.ui.comboBox_vice.itemText(0) not in viceList:
			self.ui.comboBox_vice.clear()
			self.ui.comboBox_vice.addItems(viceList)


	def openImage(self ):
		"""
		Öffnet einen Dialog zum Laden eines Charakterbildes und speichert selbiges im Charakter-Speicher.

		\note Das Bild wird auf eine in der Configurationsdatei festgelegte Maximalgröße skaliert, um die Größe überschaubar zu halten.
		"""

		appPath = PathTools.getPath()

		# Pfad zum Speicherverzeichnis
		savePath = ""
		if os.name == "nt":
			savePath = os.environ['HOMEPATH']
		else:
			savePath = os.environ['HOME']

		# Wenn Unterverzeichnis nicht existiert, suche im Programmverzeichnis.
		if ( not os.path.exists( savePath ) ):
			savePath = appPath

		filePath = QFileDialog.getOpenFileName(
			self,
			self.tr( "Select Image File" ),
			savePath,
			self.tr( "Images (*.jpg *.jpeg *.png *.bmp *.gif *.pgm *.pbm *.ppm *.svg )" )
		)

		if ( filePath[0] ):
			image = QPixmap(filePath[0])
			if image.width() > Config.pictureWidthMax or image.height() > Config.pictureHeightMax:
				image = image.scaled(800, 800, Qt.KeepAspectRatio)

			self.updatePicture(image)

			self.__character.picture = image


	def clearImage(self):
		"""
		Löscht das Charakterbild.
		"""

		self.__character.picture = QPixmap()


	def updatePicture(self, image):
		"""
		Stellt das Charakterbild dar.
		"""

		if image.isNull():
			self.ui.pushButton_picture.setIcon(QIcon())
			self.ui.pushButton_picture.setText("Open Picture")
			self.ui.pushButton_pictureClear.setEnabled(False)
		else:
			self.ui.pushButton_picture.setText("")
			self.ui.pushButton_picture.setIcon(image)
			self.ui.pushButton_pictureClear.setEnabled(True)


	def setCharacterDateBirth(self, date):
		"""
		Speichert das Geburtsdatum des Charakters im Speicher.

		Allerdings muß zuvor möglicherweise um Erlaubnis gefragt werden.
		"""

		years = Calc.years(self.ui.dateEdit_dateBirth.date(), self.ui.dateEdit_dateGame.date())
		if (self.__character.age < Config.ageAdult <= years or years < Config.ageAdult <= self.__character.age) and not self.warnAgeChange(years):
			self.ui.dateEdit_dateBirth.setDate(self.__character.dateBirth)
		else:
			self.__character.setDateBirth(date)


	def setCharacterDateGame(self, date):
		"""
		Speichert das Geburtsdatum des Charakters im Speicher.

		Allerdings muß zuvor möglicherweise um Erlaubnis gefragt werden.
		"""

		years = Calc.years(self.ui.dateEdit_dateBirth.date(), self.ui.dateEdit_dateGame.date())
		if (self.__character.age < Config.ageAdult <= years or years < Config.ageAdult <= self.__character.age) and not self.warnAgeChange(years):
			self.ui.dateEdit_dateGame.setDate(self.__character.dateGame)
		else:
			self.__character.setDateGame(date)


	def setMaxBirthday(self):
		"""
		Ändert sich die Zeit im Spiel, ändert sich das maximal einzustellende Geburtsdatum, so daß der Charakter nicht jünger sein kann als der vorgegebene Minimalwert.
		"""

		maxDateBirth = self.ui.dateEdit_dateGame.date().addYears(-1 * Config.ageMin)
		self.ui.dateEdit_dateBirth.setMaximumDate(maxDateBirth)
		## Damit auch im Charakter das Geburtsdatum geändert wird, immerhin wird nur das dateEdited-Signal ausgewertet...
		if maxDateBirth <= self.ui.dateEdit_dateBirth.date():
			self.__character.dateBirth = maxDateBirth


	def warnAgeChange(self, newAge):
		"""
		Wird der Charakter vom Erwachsenen zum Kind (oder umgekehrt), sollte eine Bestätigung eingefordert werden.

		Wird auf "No" geklickt, wird das Geburtsdatum wieder so verändert, daß das alte Alter beibehalten bleibt.
		"""

		text = self.tr("Your character is going to be an adult.")
		if newAge < Config.ageAdult:
			text = self.tr("Your character is going to be a child.")
		ret = QMessageBox.warning(
			self,
			self.tr( "Age category changed" ),
			self.tr( "{} Do you want that to happen?".format(text) ),
			QMessageBox.Yes | QMessageBox.No
		)
		if ret == QMessageBox.StandardButton.No:
			return False
		else:
			return True


	def setHeightMinMax(self, age):
		self.ui.doubleSpinBox_height.setMinimum(Config.heightMin[Config.getAge(age)])
		self.ui.doubleSpinBox_height.setMaximum(Config.heightMax[Config.getAge(age)])


	def setCharacterHeight(self, height):
		"""
		Ändert sich die Körpergröße zu sehr, sollautomatisch der Merit Giant bzw. der Flaw Dwarf vorgeschlagen werden.

		\todo Bei Kindern heißt der Dwarf-Flaw "Tiny"
		"""

		ageText = Config.getAge(self.__character.age)

		if height >= Config.heightGiant[ageText]:
			if self.__character.traits["Merit"]["Physical"]["Giant"].value > 0:
				pass
			elif self.warnHeightChange(height):
				self.__character.traits["Merit"]["Physical"]["Giant"].value = 4
				self.notificationSent.emit(self.tr("Added the Giant Merit."))
			else:
				self.ui.doubleSpinBox_height.setValue(self.__character.height)
		elif height <= Config.heightDwarf[ageText]:
			if self.__character.traits["Flaw"]["Physical"]["Dwarf"].value > 0:
				pass
			elif self.warnHeightChange(height):
				self.__character.traits["Flaw"]["Physical"]["Dwarf"].value = 2
				self.notificationSent.emit(self.tr("Added the Dwarf Flaw."))
			else:
				self.ui.doubleSpinBox_height.setValue(self.__character.height)
		elif self.__character.traits["Merit"]["Physical"]["Giant"].value:
			self.__character.traits["Merit"]["Physical"]["Giant"].value = 0
			self.notificationSent.emit(self.tr("Removed the Giant Merit."))
		elif self.__character.traits["Flaw"]["Physical"]["Dwarf"].value:
			self.__character.traits["Flaw"]["Physical"]["Dwarf"].value = 0
			self.notificationSent.emit(self.tr("Removed the Dwarf Flaw."))

		self.__character.height = height


	def warnHeightChange(self, newHeight):
		"""
		Ändert sich die Körpergröße zu sehr, sollautomatisch der Merit Giant bzw. der Flaw Dwarf vorgeschlagen werden.
		"""

		title = self.tr("Too big")
		text = self.tr("To be this big, the character needs to purchase the Giant Merit.")
		if newHeight <= Config.heightDwarf[Config.getAge(self.__character.age)]:
			title = self.tr("Too small")
			text = self.tr("To be this small, the character needs to get the Dwarf Flaw.")
		ret = QMessageBox.warning(
			self,
			title,
			self.tr( "{} Do you want that to happen?".format(text) ),
			QMessageBox.Yes | QMessageBox.No
		)
		if ret == QMessageBox.StandardButton.No:
			return False
		else:
			return True


	def updateHeight(self):
		"""
		Werden der Giant-Merit oder der Dwarf-Flaw verändert, muß die Körpergröße angepaßt werden.
		"""

		ageText = Config.getAge(self.__character.age)
		if self.__character.traits["Merit"]["Physical"]["Giant"].value > 0 and self.ui.doubleSpinBox_height.value() < Config.heightGiant[ageText]:
			self.ui.doubleSpinBox_height.setValue(Config.heightGiant[ageText])
			self.notificationSent.emit(self.tr("Height changed to {} meters".format(Config.heightGiant[ageText])))
		elif self.__character.traits["Merit"]["Physical"]["Giant"].value < 1 and self.ui.doubleSpinBox_height.value() >= Config.heightGiant[ageText]:
			newHeight = Config.heightGiant[ageText] - 0.01
			self.ui.doubleSpinBox_height.setValue(newHeight)
			self.notificationSent.emit(self.tr("Height changed to {} meters".format(newHeight)))
		elif self.__character.traits["Flaw"]["Physical"]["Dwarf"].value > 0 and self.ui.doubleSpinBox_height.value() > Config.heightDwarf[ageText]:
			self.ui.doubleSpinBox_height.setValue(Config.heightDwarf[ageText])
			self.notificationSent.emit(self.tr("Height changed to {} meters".format(Config.heightDwarf[ageText])))
		elif self.__character.traits["Flaw"]["Physical"]["Dwarf"].value < 1 and self.ui.doubleSpinBox_height.value() <= Config.heightDwarf[ageText]:
			newHeight = Config.heightDwarf[ageText] + 0.01
			self.ui.doubleSpinBox_height.setValue(newHeight)
			self.notificationSent.emit(self.tr("Height changed to {} meters".format(newHeight)))
