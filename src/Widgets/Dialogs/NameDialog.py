# -*- coding: utf-8 -*-

"""
# Copyright

Copyright (C) 2012 by Victor
victor@caern.de

# License

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




import copy

from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtGui import QDialog, QIcon

import src.Config as Config
#from src.Error import ErrListLength
#from src.Widgets.Components.CharaSpecies import CharaSpecies
from src.Datatypes.Identity import Identity
#from src.Debug import Debug

from ui.ui_NameDialog import Ui_NameDialog




class NameDialog(QDialog):
	"""
	@brief Dialog zur Auswahl der darzustellenden Merits.

	Alle Merits darzustellen ist wohl etwas viel. Über diesen Dialog kann der Benutzer auswählen, welche und im Falle von Merits mit Zusatztext, wieviele er angezeigt haben möchte.

	\note Für jeden Merit "New Identity steht dem Charkater von Anfang an eine falsche Identität zu. Er kann mehr haben, aber diese haben alle New Identity 0"

	\todo Die Abhängigkeit vom New Identity-Merit fehlt.
	"""


	identityIndexChanged = Signal(int)


	def __init__(self, character, parent=None):
		super(NameDialog, self).__init__(parent)

		self.ui = Ui_NameDialog()
		self.ui.setupUi(self)

		self.__character = character

		self.nameDict = {
			"Human": "",
			"Changeling": "AKA",
			"Mage": "Shadow Name",
			"Vampire": "AKA",
			"Werewolf": "Deed Name",
		}

		## Die Identitäten werden nur kopiert. Überschrieben werden sie erst, wenn man den Dialog bestätigt.
		## Unschöner Hack, da deepcopy zum Programmabsturz führt.
		#realIdentity = copy.deepcopy(self.__character.realIdentity)
		self.identityLcl = Identity()
		self.identityLcl._name = copy.deepcopy(self.__character.identity._name)
		self.identityLcl._gender = copy.deepcopy(self.__character.identity._gender)
		#falseIdentities = copy.deepcopy(self.__character.falseIdentities)

		for item in Config.GENDERS[1:]:
			self.ui.comboBox_gender.addItem( QIcon(item[1]), item[0] )

		self.ui.lineEdit_firstName.textChanged.connect(self.updateForenames)
		self.ui.lineEdit_additionalForenames.textChanged.connect(self.updateForenames)
		self.ui.lineEdit_surname.textChanged.connect(self.updateSurname)
		self.ui.lineEdit_honorificName.textChanged.connect(self.updateHonorificName)
		self.ui.lineEdit_nickname.textChanged.connect(self.updateNickname)
		self.ui.lineEdit_specialName.textChanged.connect(self.updateSpecialName)
		self.ui.comboBox_gender.currentIndexChanged[str].connect(self.updateGender)
		self.ui.lineEdit_firstName.textChanged.connect(self.showNames)
		self.ui.lineEdit_additionalForenames.textChanged.connect(self.showNames)
		self.ui.lineEdit_surname.textChanged.connect(self.showNames)
		self.ui.lineEdit_honorificName.textChanged.connect(self.showNames)
		self.ui.lineEdit_nickname.textChanged.connect(self.showNames)
		self.ui.lineEdit_specialName.textChanged.connect(self.showNames)
		self.ui.buttonBox.accepted.connect(self.saveNames)
		self.ui.buttonBox.rejected.connect(self.reject)

		#self.__character.speciesChanged.connect(self.renameSpecialNameLabel)
		self.renameSpecialNameLabel(self.__character.species)

		self.selectIdentity()


	def selectIdentity(self):
		"""
		Eine andere Identität wird angezeigt.
		"""

		additionalForenames = ""
		additionalForenames = " ".join(self.identityLcl.forenames[1:])

		self.ui.lineEdit_firstName.setText( self.identityLcl.firstname )
		self.ui.lineEdit_additionalForenames.setText( additionalForenames )
		self.ui.lineEdit_surname.setText( self.identityLcl.surname )
		self.ui.lineEdit_honorificName.setText( self.identityLcl.honorname )
		self.ui.lineEdit_nickname.setText( self.identityLcl.nickname )
		self.ui.lineEdit_specialName.setText( self.identityLcl.supername )
		self.ui.comboBox_gender.setCurrentIndex(self.ui.comboBox_gender.findText(self.identityLcl.gender))

		self.showNames()


	def updateForenames(self):
		"""
		Aktualisiert die Vornamen in der gewählten Identität.
		"""

		if not (self.ui.lineEdit_additionalForenames.text() + self.ui.lineEdit_firstName.text()).isspace():
			foreNames = self.ui.lineEdit_additionalForenames.text()
			if foreNames:
				foreNames = foreNames.split(" ")
			else:
				foreNames = []
			foreNames.insert(0, self.ui.lineEdit_firstName.text())
			self.identityLcl.forenames = foreNames
		else:
			self.identityLcl.forenames = [""]


	def updateSurname(self):
		"""
		Aktualisiert den Nachnamen in der gewählten Identität.
		"""

		if not self.ui.lineEdit_surname.text().isspace():
			self.identityLcl.surname = self.ui.lineEdit_surname.text()
		else:
			self.identityLcl.surname = ""


	def updateHonorificName(self):
		"""
		Aktualisiert den Ehrennamen in der gewählten Identität.
		"""

		if not self.ui.lineEdit_honorificName.text().isspace():
			self.identityLcl.honorname = self.ui.lineEdit_honorificName.text()
		else:
			self.identityLcl.honorname = ""


	def updateNickname(self):
		"""
		Aktualisiert den Rufnamen in der gewählten Identität.
		"""

		if not self.ui.lineEdit_nickname.text().isspace():
			self.identityLcl.nickname = self.ui.lineEdit_nickname.text()
		else:
			self.identityLcl.nickname = ""


	def updateSpecialName(self):
		"""
		Aktualisiert den Besonderen Namen in der gewählten Identität.
		"""

		if not self.ui.lineEdit_specialName.text().isspace():
			self.identityLcl.supername = self.ui.lineEdit_specialName.text()
		else:
			self.identityLcl.supername = ""


	def updateGender(self, text):
		"""
		Aktualisiert das Geschlecht in der gewählten Identität.
		"""

		self.identityLcl.gender = text


	def showNames(self):
		"""
		Zeigt den resultierenden Namen an. Einmal der Name, wie er später auf der Schaltfläche zu sehen sein wird, die diesen Dialog aufruft, einmal den vollständigen Namen mit allen Bestandteilen.
		"""

		forenames = self.ui.lineEdit_additionalForenames.text().split( " " )
		forenames.insert( 0, self.ui.lineEdit_firstName.text() )

		self.ui.label_displayFull.setText( Identity.displayNameFull( self.ui.lineEdit_surname.text(), forenames ) )
		self.ui.label_displayDisplay.setText( Identity.displayNameDisplay( self.ui.lineEdit_surname.text(), self.ui.lineEdit_firstName.text(), self.ui.lineEdit_nickname.text() ) )
		self.ui.label_displayHonorific.setText( Identity.displayNameHonor( self.ui.lineEdit_firstName.text(), self.ui.lineEdit_honorificName.text() ) )
		self.ui.label_displaySuper.setText( self.ui.lineEdit_specialName.text() )


	def saveNames(self):
		"""
		Speichert die eingegebenen Namen im Charakter-Speicher.
		"""

		self.__character.identity.forenames = self.identityLcl.forenames
		self.__character.identity.surname = self.identityLcl.surname
		self.__character.identity.honorname = self.identityLcl.honorname
		self.__character.identity.nickname = self.identityLcl.nickname
		self.__character.identity.supername = self.identityLcl.supername
		self.__character.identity.gender = self.identityLcl.gender

		self.accept()


	def renameSpecialNameLabel(self, species):
		"""
		Der Bezeichner für den Spezialnamen ist von Spezies zu Spezies unterschiedlich.
		"""

		if species == "Human":
			self.ui.label_specialName.setVisible(False)
			self.ui.lineEdit_specialName.setVisible(False)
		else:
			self.ui.label_specialName.setVisible(True)
			self.ui.lineEdit_specialName.setVisible(True)
			self.ui.label_specialName.setText("{}:".format(self.nameDict[species]))

