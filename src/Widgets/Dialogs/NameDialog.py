# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) 2011 by Victor von Rhein

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

#from PySide.QtCore import Signal
from PySide.QtGui import QDialog

##from src.Config import Config
#from src.Widgets.Components.CharaSpecies import CharaSpecies
from src.Datatypes.Identity import Identity

from ui.ui_NameDialog import Ui_NameDialog




class NameDialog(QDialog):
	"""
	@brief Dialog zur Auswahl der darzustellenden Merits.

	Alle Merits darzustellen ist wohl etwas viel. Über diesen Dialog kann der Benutzer auswählen, welche und im Falle von Merits mit Zusatztext, wieviele er angezeigt haben möchte.
	"""

	def __init__(self, character, parent=None):
		QDialog.__init__(self, parent)

		self.ui = Ui_NameDialog()
		self.ui.setupUi(self)

		self.__character = character

		self.ui.lineEdit_firstName.textChanged.connect(self.showNames)
		self.ui.lineEdit_additionalForenames.textChanged.connect(self.showNames)
		self.ui.lineEdit_surename.textChanged.connect(self.showNames)
		self.ui.lineEdit_honorificName.textChanged.connect(self.showNames)
		self.ui.lineEdit_nickname.textChanged.connect(self.showNames)
		self.ui.lineEdit_specialName.textChanged.connect(self.showNames)
		self.ui.buttonBox.accepted.connect(self.saveNames)
		self.ui.buttonBox.rejected.connect(self.reject)

		self.getNames()

	def getNames(self):
		"""
		Liest die Namen des Charakters aus und zeigt sie gleich an.

		Besteht ein Namen nur aus Whitespace, wird er nicht beachtet. Leer darf er allerdings sein.

		\note Momentan wird nur die echte Identität berücksichtigt, also immer nur die Identität an INdexposition 0.
		"""

		foreNames = " ".join(self.__character.identities[0].forenames[1:])

		self.ui.lineEdit_firstName.setText( self.__character.identities[0].firstname )
		self.ui.lineEdit_additionalForenames.setText( foreNames )
		self.ui.lineEdit_surename.setText( self.__character.identities[0].surename )
		self.ui.lineEdit_honorificName.setText( self.__character.identities[0].honorname )
		self.ui.lineEdit_nickname.setText( self.__character.identities[0].nickname )
		self.ui.lineEdit_specialName.setText( self.__character.identities[0].supername )

		self.showNames()


	def showNames(self):
		"""
		Zeigt den resultierenden Namen an. Einmal der Name, wie er später auf der Schaltfläche zu sehen sein wird, die diesen Dialog aufruft, einmal den vollständigen Namen mit allen Bestandteilen.
		"""
		
		forenames = self.ui.lineEdit_additionalForenames.text().split( " " )
		forenames.insert( 0, self.ui.lineEdit_firstName.text() )

		self.ui.label_displayFull.setText( Identity.displayNameFull( self.ui.lineEdit_surename.text(), forenames ) )
		self.ui.label_displayDisplay.setText( Identity.displayNameDisplay( self.ui.lineEdit_surename.text(), self.ui.lineEdit_firstName.text(), self.ui.lineEdit_nickname.text() ) )
		self.ui.label_displayHonorific.setText( Identity.displayNameHonor( self.ui.lineEdit_firstName.text(), self.ui.lineEdit_honorificName.text() ) )
		self.ui.label_displaySuper.setText( self.ui.lineEdit_specialName.text() )


	def saveNames(self):
		"""
		Speichert die eingegebenen Namen im Charakter-Speicher.

		\note Derzeit wird nur /eine/, die echte Identität unterstüzt. Also wird immer nur die Identität an Indexposition 0 überschrieben.

		Ein Textfeld, das nur aus Whitespace besteht, wird als leer betrachtet.
		"""

		if not (self.ui.lineEdit_additionalForenames.text() + self.ui.lineEdit_firstName.text()).isspace():
			foreNames = self.ui.lineEdit_additionalForenames.text()
			foreNames = foreNames.split(" ")
			foreNames.insert(0, self.ui.lineEdit_firstName.text())
			self.__character.identities[0].forenames = foreNames
		else:
			self.__character.identities[0].forenames = [""]

		if not self.ui.lineEdit_surename.text().isspace():
			self.__character.identities[0].surename = self.ui.lineEdit_surename.text()
		else:
			self.__character.identities[0].surename = ""

		if not self.ui.lineEdit_honorificName.text().isspace():
			self.__character.identities[0].honorname = self.ui.lineEdit_honorificName.text()
		else:
			self.__character.identities[0].honorname = ""

		if not self.ui.lineEdit_nickname.text().isspace():
			self.__character.identities[0].nickname = self.ui.lineEdit_nickname.text()
		else:
			self.__character.identities[0].nickname = ""

		if not self.ui.lineEdit_specialName.text().isspace():
			self.__character.identities[0].supername = self.ui.lineEdit_specialName.text()
		else:
			self.__character.identities[0].supername = ""

		self.accept()

