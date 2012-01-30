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

from PySide.QtCore import Signal
from PySide.QtGui import QDialog, QIcon, QListWidgetItem

from src.Config import Config
from src.Error import ErrListLength
#from src.Widgets.Components.CharaSpecies import CharaSpecies
from src.Datatypes.Identity import Identity
from src.Debug import Debug

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
		QDialog.__init__(self, parent)

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

		self.identities = [
			self.__character.realIdentity,
		]
		self.identities.extend(self.__character.falseIdentities)
		for i in xrange(len(self.__character.falseIdentities)):
			## Alle Identitäten außer der echten in Combobox einfügen
			self.ui.comboBox_identities.addItem("#{}".format(i + 1))

		for item in Config.genders:
			self.ui.comboBox_gender.addItem( QIcon(item[1]), item[0] )

		self.ui.comboBox_identities.currentIndexChanged[int].connect(self.selectIdentity)
		self.ui.pushButton_add.clicked.connect(self.addIdentity)
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
		self.ui.pushButton_delete.clicked.connect(self.deleteIdentity)
		self.ui.buttonBox.accepted.connect(self.saveNames)
		self.ui.buttonBox.rejected.connect(self.reject)

		#self.__character.speciesChanged.connect(self.renameSpecialNameLabel)
		self.renameSpecialNameLabel(self.__character.species)

		self.selectIdentity(0)


	def selectIdentity(self, index):
		"""
		Eine andere Identität wird angezeigt.
		"""

		## Index darf nicht größer als maximaler Index +1 sein.
		if index >= len(self.identities) or index < 0:
			raise ErrListLength(len(self.identities)-1, index)

		if index == 0:
			self.ui.groupBox_id.setTitle("Real Identity")
		else:
			self.ui.groupBox_id.setTitle("False Identity")

		#Debug.debug(index, self.identities[index].forenames)

		additionalForenames = ""
		additionalForenames = " ".join(self.identities[index].forenames[1:])

		self.ui.lineEdit_firstName.setText( self.identities[index].firstname )
		self.ui.lineEdit_additionalForenames.setText( additionalForenames )
		self.ui.lineEdit_surname.setText( self.identities[index].surname )
		self.ui.lineEdit_honorificName.setText( self.identities[index].honorname )
		self.ui.lineEdit_nickname.setText( self.identities[index].nickname )
		self.ui.lineEdit_specialName.setText( self.identities[index].supername )

		self.showNames()


	def addIdentity(self):
		"""
		Fügt eine Identität hinzu. Aber nur, wenn keine der bereits vorhandenen Identitäten leer ist. In diesem Falle wird einfach zu selbiger gewechselt.
		"""

		emptyIdentity = Identity()
		emptyIdentityExists = False
		for i in xrange(len(self.identities)):
			if self.identities[i] == emptyIdentity:
				self.ui.comboBox_identities.setCurrentIndex(i)
				emptyIdentityExists = True
				break

		if not emptyIdentityExists:
			self.identities.append(emptyIdentity)
			self.ui.comboBox_identities.addItem("#{}".format(len(self.identities) - 1))
			self.ui.comboBox_identities.setCurrentIndex(len(self.identities) - 1)


	def deleteIdentity(self, index):
		"""
		Löscht die Identität an der angegebenen Indexposition.
		"""

		if 0 < index < len(self.identities):
			self.ui.comboBox_identities.setCurrentIndex(0)
			del self.identities[index]


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
			self.identities[self.ui.comboBox_identities.currentIndex()].forenames = foreNames
		else:
			self.identities[self.ui.comboBox_identities.currentIndex()].forenames = [""]


	def updateSurname(self):
		"""
		Aktualisiert den Nachnamen in der gewählten Identität.
		"""

		if not self.ui.lineEdit_surname.text().isspace():
			self.identities[self.ui.comboBox_identities.currentIndex()].surname = self.ui.lineEdit_surname.text()
		else:
			self.identities[self.ui.comboBox_identities.currentIndex()].surname = ""


	def updateHonorificName(self):
		"""
		Aktualisiert den Ehrennamen in der gewählten Identität.
		"""

		if not self.ui.lineEdit_honorificName.text().isspace():
			self.identities[self.ui.comboBox_identities.currentIndex()].honorname = self.ui.lineEdit_honorificName.text()
		else:
			self.identities[self.ui.comboBox_identities.currentIndex()].honorname = ""


	def updateNickname(self):
		"""
		Aktualisiert den Rufnamen in der gewählten Identität.
		"""

		if not self.ui.lineEdit_nickname.text().isspace():
			self.identities[self.ui.comboBox_identities.currentIndex()].nickname = self.ui.lineEdit_nickname.text()
		else:
			self.identities[self.ui.comboBox_identities.currentIndex()].nickname = ""


	def updateSpecialName(self):
		"""
		Aktualisiert den Besonderen Namen in der gewählten Identität.
		"""

		if not self.ui.lineEdit_specialName.text().isspace():
			self.identities[self.ui.comboBox_identities.currentIndex()].supername = self.ui.lineEdit_specialName.text()
		else:
			self.identities[self.ui.comboBox_identities.currentIndex()].supername = ""


	def updateGender(self, text):
		"""
		Aktualisiert das Geschlecht in der gewählten Identität.
		"""

		self.identities[self.ui.comboBox_identities.currentIndex()].gender = text


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

		self.__character.realIdentity.forenames = self.identities[0].forenames
		self.__character.realIdentity.surname = self.identities[0].surname
		self.__character.realIdentity.honorname = self.identities[0].honorname
		self.__character.realIdentity.nickname = self.identities[0].nickname
		self.__character.realIdentity.supername = self.identities[0].supername
		self.__character.realIdentity.gender = self.identities[0].gender
		self.__character.falseIdentities = self.identities[1:]

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

