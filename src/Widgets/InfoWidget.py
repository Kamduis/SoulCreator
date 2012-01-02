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

from PySide.QtCore import Qt, Signal
from PySide.QtGui import QWidget, QGridLayout, QLabel, QPushButton, QComboBox, QIcon, QSpinBox

from src.Config import Config
from src.Datatypes.Identity import Identity
from src.Widgets.Components.CharaSpecies import CharaSpecies
from src.Widgets.Dialogs.NameDialog import NameDialog
from src.Debug import Debug




class InfoWidget(QWidget):
	"""
	@brief Das Widget, in welchem wichtige Informationen dargestellt werden.

	Spezies, Namen etc. des Charakters werden hier dargestellt.
	"""


	nameChanged = Signal(str)


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)
		
		self.__storage = template
		self.__character = character

		self.__layout = QGridLayout()
		self.setLayout( self.__layout )

		self.__namePushButton = QPushButton( self.tr( "Name" ) )

		self.__labelGender = QLabel( self.tr( "Gender:" ) )
		self.__genderCombobox = QComboBox( self )
		for item in Config.genders:
			self.__genderCombobox.addItem( QIcon(item[1]), item[0] )

		self.__labelAge = QLabel( self.tr( "Age:" ) )
		self.__spinBoxAge = QSpinBox( self )
		self.__spinBoxAge.setMinimum(6)
		self.__spinBoxAge.setMaximum(999)

		self.__labelSpecies = QLabel( self.tr( "Species:" ) )
		self.__speciesComboBox = CharaSpecies( self)
		for item in self.__storage.species:
			self.__speciesComboBox.addItem(item["name"])

		self.__labelVirtue = QLabel( self.tr( "Virtue:" ) )
		self.__virtueCombobox = QComboBox( self )

		self.__labelVice = QLabel( self.tr( "Vice:" ) )
		self.__viceCombobox = QComboBox( self )

		self.__labelBreed = QLabel( self.tr( "Breed:" ) )
		self.__breedCombobox = QComboBox( self )

		self.__labelFaction = QLabel( self.tr( "Faction:" ) )
		self.__factionCombobox = QComboBox( self )

		self.__labelEra = QLabel( self.tr( "Era:" ) )
		self.__comboBoxEra = QComboBox( self )
		self.__comboBoxEra.addItems( Config.eras )

		self.__layout.addWidget( self.__namePushButton, 0, 0, 1, 2, Qt.AlignTop )
		self.__layout.addWidget( self.__labelGender, 1, 0 )
		self.__layout.addWidget( self.__genderCombobox, 1, 1 )
		self.__layout.addWidget( self.__labelAge, 2, 0 )
		self.__layout.addWidget( self.__spinBoxAge, 2, 1 )
		self.__layout.addWidget( self.__labelSpecies, 3, 0 )
		self.__layout.addWidget( self.__speciesComboBox, 3, 1 )
		self.__layout.addWidget( self.__labelVirtue, 4, 0 )
		self.__layout.addWidget( self.__virtueCombobox, 4, 1 )
		self.__layout.addWidget( self.__labelVice, 5, 0 )
		self.__layout.addWidget( self.__viceCombobox, 5, 1 )
		self.__layout.addWidget( self.__labelBreed, 6, 0 )
		self.__layout.addWidget( self.__breedCombobox, 6, 1 )
		self.__layout.addWidget( self.__labelFaction, 7, 0 )
		self.__layout.addWidget( self.__factionCombobox, 7, 1 )
		self.__layout.addWidget( self.__labelEra, 0, 3 )
		self.__layout.addWidget( self.__comboBoxEra, 0, 4 )

		self.__namePushButton.clicked.connect(self.openNameDialog)
		self.__genderCombobox.currentIndexChanged[str].connect(self.changeGender)
		self.__spinBoxAge.valueChanged[int].connect(self.changeAge)
		self.__speciesComboBox.currentIndexChanged[str].connect(self.changeSpecies)
		self.__virtueCombobox.currentIndexChanged[str].connect(self.changeVirtue)
		self.__viceCombobox.currentIndexChanged[str].connect(self.changeVice)
		self.__breedCombobox.currentIndexChanged[str].connect(self.changeBreed)
		self.__factionCombobox.currentIndexChanged[str].connect(self.changeFaction)
		self.__comboBoxEra.currentIndexChanged[str].connect(self.changeEra)
		self.__character.identities[0].nameChanged.connect(self.updateName)
		self.__character.identities[0].genderChanged.connect(self.updateGender)
		self.__character.ageChanged.connect(self.updateAge)
		self.__character.speciesChanged.connect(self.updateSpecies)
		self.__character.virtueChanged.connect(self.updateVirtue)
		self.__character.ageChanged.connect(self.repopulateVirtues)
		self.__character.viceChanged.connect(self.updateVice)
		self.__character.ageChanged.connect(self.repopulateVices)
		self.__character.speciesChanged.connect(self.updateBreedTitle)
		self.__character.speciesChanged.connect(self.repopulateBreeds)
		self.__character.speciesChanged.connect(self.updateFactionTitle)
		self.__character.speciesChanged.connect(self.repopulateFactions)
		self.__character.eraChanged.connect(self.updateEra)


	def openNameDialog(self):
		"""
		Ruft einen Dialog auf, in welchem die zahlreichen Namen des Charakters eingetragen werden können.
		"""
		
		dialog = NameDialog( self.__character, self )
		dialog.exec_()


	def changeGender( self, gender ):
		"""
		Legt das Geschlecht des Charakters fest.
		"""

		self.__character.identities[0].gender = gender


	def changeAge( self, age ):
		"""
		Legt das Alter des Charakters fest.
		"""

		self.__character.age = age


	def changeSpecies( self, species ):
		"""
		Verändert die Spezies des Charakters.
		"""

		self.__character.species = species


	def changeVirtue( self, virtue ):
		"""
		Verändert die Tugend des Charakters.
		"""

		self.__character.virtue = virtue


	def changeVice( self, vice ):
		"""
		Verändert das Laster des Charakters.
		"""

		self.__character.vice = vice


	def changeBreed( self, breed ):
		"""
		Verändert die Brut des Charakters.
		"""

		self.__character.breed = breed


	def changeFaction( self, faction ):
		"""
		Verändert die Fraktion des Charakters.
		"""

		self.__character.faction = faction


	def changeEra( self, era ):
		"""
		Legt die zeitliche Ära fest, in welcher der Charakter zuhause ist.
		"""

		self.__character.era = era


	def updateName( self ):
		"""
		Aktualisiert die Anzeige des Namens.
		"""

		nameStr = Identity.displayNameDisplay(self.__character.identities[0].surename, self.__character.identities[0].firstname, self.__character.identities[0].nickname)
		nameDisplay = nameStr
		if not nameStr:
			nameStr = self.tr("Name")
		self.__namePushButton.setText( nameStr )
		self.nameChanged.emit(nameDisplay)


	def updateGender( self, gender ):
		"""
		Aktualisiert die Anzeige des Geschlechts.
		"""

		self.__genderCombobox.setCurrentIndex( self.__genderCombobox.findText(gender))


	def updateAge(self, age):
		"""
		Aktualisiert die Anzeige des Alters.
		"""

		#Debug.debug("Verändere Anzeige des Alters auf {}".format(age))
		self.__spinBoxAge.setValue(age)


	def updateSpecies( self, species ):
		"""
		Aktualisiert die Anzeige der Spezies.
		"""

		self.__speciesComboBox.setCurrentIndex( self.__speciesComboBox.findText( species ) )


	def updateVirtue( self, virtue ):
		"""
		Aktualisiert die Anzeige der Tugend.
		"""

		self.__virtueCombobox.setCurrentIndex( self.__virtueCombobox.findText( virtue ) )


	def updateVice( self, vice ):
		"""
		Aktualisiert die Anzeige des Lasters.
		"""

		self.__viceCombobox.setCurrentIndex( self.__viceCombobox.findText( vice ) )


	def updateBreed( self, breed ):
		"""
		Aktualisiert die Anzeige der Brut.
		"""

		self.__breedCombobox.setCurrentIndex( self.__breedCombobox.findText( breed ) )


	def updateBreedTitle( self, species ):
		"""
		Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Bruten.
		"""

		self.__labelBreed.setText( "{}:".format(self.__storage.breedTitle(species)) )


	def updateFaction( self, faction ):
		"""
		Aktualisiert die Anzeige der Fraktion.
		"""

		self.__factionCombobox.setCurrentIndex( self.__factionCombobox.findText( faction ) )


	def updateFactionTitle( self, species ):
		"""
		Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Fraktionen
		"""

		self.__labelFaction.setText( "{}:".format(self.__storage.factionTitle(species)) )


	def updateEra(self, era):
		"""
		Aktualisiert die Anzeige der Ära
		"""

		#Debug.debug("Verändere Anzeige der Ära auf {}".format(era))
		self.__comboBoxEra.setCurrentIndex(self.__comboBoxEra.findText(era))


	def repopulateVirtues(self, age):
		ageStr = Config.ages[0]
		if age < Config.adultAge:
			ageStr = Config.ages[1]

		virtueList = []
		for item in self.__storage.virtues:
			if item["age"] == ageStr:
				virtueList.append(item["name"])

		self.__virtueCombobox.clear()
		self.__virtueCombobox.addItems(virtueList)


	def repopulateVices(self, age):
		ageStr = Config.ages[0]
		if age < Config.adultAge:
			ageStr = Config.ages[1]

		viceList = []
		for item in self.__storage.vices:
			if item["age"] == ageStr:
				viceList.append(item["name"])

		self.__viceCombobox.clear()
		self.__viceCombobox.addItems(viceList)


	def repopulateBreeds(self, species):

		self.__breedCombobox.clear()
		self.__breedCombobox.addItems(self.__storage.breeds(species))


	def repopulateFactions(self, species):

		self.__factionCombobox.clear()
		self.__factionCombobox.addItems(self.__storage.factions(species))
