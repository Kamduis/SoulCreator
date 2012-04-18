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

import re

from PySide.QtCore import QDate
from PySide.QtGui import QWidget, QIcon#, QLabel, QPixmap, QFileDialog, QMessageBox

#from src.Config import Config
#from src.Tools import PathTools
#from src.Calc.Calc import Calc
from src.Debug import Debug

from ui.ui_TemplateWidget import Ui_TemplateWidget




class TemplateWidget(QWidget):
	"""
	@briefIn diesem Widget kann das übernatürliche Template gewählt werden, welches der Charakter möglicherweise haben soll.
	"""


	def __init__(self, template, character, parent=None):
		super(TemplateWidget, self).__init__(parent)

		self.ui = Ui_TemplateWidget()
		self.ui.setupUi(self)

		self.__storage = template
		self.__character = character

		speciesList = [ species[0] for species in self.__storage.species.items() if species[1]["playable"] ]
		speciesList.sort()
		#self.ui.comboBox_species.addItems(speciesList)
		for species in speciesList:
			self.ui.comboBox_species.addItem(QIcon(":/icons/images/species/{}/Skull.png".format(species)), species)

		self.ui.dateEdit_dateBecoming.setMinimumDate(QDate(100, 1, 1))

		## Speichern der vom Benutzer veränderten Werte
		self.ui.dateEdit_dateBecoming.dateChanged.connect(self.__character.setDateBecoming)
		self.ui.comboBox_species.currentIndexChanged[str].connect(self.__character.setSpecies)
		self.ui.comboBox_breed.currentIndexChanged[str].connect(self.__character.setBreed)
		self.ui.comboBox_bonus.currentIndexChanged[str].connect(self.setCharacterBonus)
		self.ui.comboBox_kith.currentIndexChanged[str].connect(self.__character.setKith)
		self.ui.comboBox_faction.currentIndexChanged[str].connect(self.__character.setFaction)
		self.ui.lineEdit_faction.textEdited.connect(self.__character.setFaction)
		self.ui.comboBox_organisation.currentIndexChanged[str].connect(self.__character.setOrganisation)
		self.ui.lineEdit_party.textEdited.connect(self.__character.setParty)

		## Aktualisieren der Darstellung der im Charakter veränderten Werte.
		self.__character.dateBecomingChanged.connect(self.ui.dateEdit_dateBecoming.setDate)
		self.__character.ageBecomingChanged.connect(self.ui.label_ageBecoming.setNum)
		self.__character.speciesChanged.connect(self.updateSpecies)
		self.__character.breedChanged.connect(self.updateBreed)
		self.__character.breedChanged.connect(self.repopulateBonus)
		self.__character.breedChanged.connect(self.repopulateKiths)
		self.__character.bonusChanged.connect(self.updateBonus)
		self.__character.kithChanged.connect(self.updateKith)
		self.__character.speciesChanged.connect(self.updateBreedTitle)
		self.__character.speciesChanged.connect(self.repopulateBreeds)
		self.__character.factionChanged.connect(self.updateFaction)
		self.__character.speciesChanged.connect(self.updateFactionTitle)
		self.__character.speciesChanged.connect(self.repopulateFactions)
		self.__character.organisationChanged.connect(self.updateOrganisation)
		self.__character.speciesChanged.connect(self.updateOrganisationTitle)
		self.__character.speciesChanged.connect(self.repopulateOrganisations)
		self.__character.partyChanged.connect(self.ui.lineEdit_party.setText)
		self.__character.speciesChanged.connect(self.updatePartyTitle)
		# Menschen können ihre Fraktion selbst eintragen und haben einige Angaben einfach nicht nötig.
		self.__character.speciesChanged.connect(self.hideShowWidgets_species)

		## Das Alter darf nie negativ werden können
		self.__character.dateBirthChanged.connect(self.ui.dateEdit_dateBecoming.setMinimumDate)
		self.__character.dateGameChanged.connect(self.ui.dateEdit_dateBecoming.setMaximumDate)


	def updateSpecies( self, species ):
		"""
		Aktualisiert die Anzeige der Spezies.
		"""

		self.ui.comboBox_species.setCurrentIndex( self.ui.comboBox_species.findText( species ) )


	def updateBreed( self, breed ):
		"""
		Aktualisiert die Anzeige der Brut.
		"""

		self.ui.comboBox_breed.setCurrentIndex( self.ui.comboBox_breed.findText( breed ) )


	def updateBreedTitle( self, species ):
		"""
		Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Bruten.
		"""

		self.ui.label_breed.setText( "{}:".format(self.__storage.breedTitle(species)) )


	def updateBonus( self, bonus ):
		"""
		Aktualisiert die Anzeige der Bonuseigenschaft.
		"""

		if bonus:
			if bonus["type"] == "Skill" and "specialty" in bonus:
				#Debug.debug(bonus["specialty"])
				self.ui.comboBox_bonus.setCurrentIndex( self.ui.comboBox_bonus.findText( bonus["specialty"] ) )
			else:
				self.ui.comboBox_bonus.setCurrentIndex( self.ui.comboBox_bonus.findText( bonus["name"] ) )
		else:
			self.ui.comboBox_bonus.clear()


	def updateKith( self, kith ):
		"""
		Aktualisiert die Anzeige des Kith.
		"""

		self.ui.comboBox_kith.setCurrentIndex( self.ui.comboBox_kith.findText( kith ) )


	def updateFaction( self, faction ):
		"""
		Aktualisiert die Anzeige der Fraktion.
		"""

		self.ui.lineEdit_faction.setText(faction)
		self.ui.comboBox_faction.setCurrentIndex( self.ui.comboBox_faction.findText( faction ) )


	def updateFactionTitle( self, species ):
		"""
		Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Fraktionen
		"""

		self.ui.label_faction.setText( "{}:".format(self.__storage.factionTitle(species)) )


	def updateOrganisation( self, organisation ):
		"""
		Aktualisiert die Anzeige der Organisation (Ritterorden, Legate, Blutlinien, etc.).

		\todo Um einer Organisation beizutreten sind gewisse Anforderungen zu erfüllen. Diese sollten in das programm irgendwie eingebaut werden.
		"""

		self.ui.comboBox_organisation.setCurrentIndex( self.ui.comboBox_organisation.findText( organisation ) )


	def updateOrganisationTitle( self, species ):
		"""
		Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Fraktionen
		"""

		self.ui.label_organisation.setText( "{}:".format(self.__storage.organisationTitle(species)) )


	def updatePartyTitle( self, species ):
		"""
		Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Freundesgruppe.
		"""

		self.ui.label_party.setText( "{}:".format(self.__storage.partyTitle(species)) )


	def repopulateBreeds(self, species):

		self.ui.comboBox_breed.clear()
		for item in self.__storage.breeds(species):
			self.ui.comboBox_breed.addItem(QIcon(":icons/images/species/{}/Breed-{}.svg".format(species, item)), item)


	def repopulateBonus(self, breed):
		"""
		Die Bonuseigenschaften neu festlegen.

		\todo Bei Werwölfen und Wechselbälgern sollten alle Spezialisierungen usgeblendet werden, die der Charkater nicht wählen kann weil die Fertigkeit einen Wert von 0 hat, oder selbige Spezialisierung schon besitzt.

		\todo Nach Ende der Erschaffung muß die Bonus-Eigenschaft unveränderlich gemacht werden.
		"""

		self.ui.comboBox_bonus.clear()
		__list = self.__storage.bonusTraits(self.__character.species, breed)
		if __list:
			bonusList = [ bonus["name"] for bonus in __list ]
			bonusList.sort()
			speciesWithSpecialties = (
				"Changeling",
				"Werewolf",
			)
			if self.__character.species in speciesWithSpecialties:
				for item in bonusList:
					for category in self.__storage.traits["Skill"]:
						if item in self.__storage.traits["Skill"][category]:
							self.ui.comboBox_bonus.addItems( self.__storage.traits["Skill"][category][item]["specialties"] )
			else:
				self.ui.comboBox_bonus.addItems( bonusList )
				self.ui.label_bonus2.setText(__list[0]["name"])

		## Schonmal im Charakter speichern, da Magier nichts wählen können.
		self.setCharacterBonus()


	def setCharacterBonus(self):
		"""
		Legt die Bonuseigenschaft im Charkater fest.
		"""

		__list = self.__storage.bonusTraits(self.__character.species, self.__character.breed)
		if len(__list) > 1:
			bonusName = self.ui.comboBox_bonus.currentText()
			## Bei Bonus-Spezialisierungen muß auch die Fertigkeit gespeichert werden.
			for item in __list:
				if item["type"] == "Skill":
					for skill in self.__storage.traitSkills():
						if item["name"] == skill and bonusName in self.__storage.traitSkills()[skill]["specialties"]:
							item["specialty"] = bonusName
							self.__character.bonus = item
							break
				elif item["name"] == bonusName:
					self.__character.bonus = item
					break
		elif len(__list) > 0:
			self.__character.bonus = __list[0]
		else:
			self.__character.bonus = {}


	def repopulateKiths(self, breed):
		"""
		Jedes Seeming hat eine Reihe möglicher Kiths. Kiths stehen nur Changelings offen.
		"""

		self.ui.comboBox_kith.clear()
		if breed and self.__character.species == "Changeling":
			#Debug.debug(breed)
			self.ui.comboBox_kith.addItems(self.__storage.kiths(breed))


	def repopulateFactions(self, species):
		"""
		Fülle die Fraktionsauswahl neu auf.
		"""

		self.ui.comboBox_faction.clear()
		for item in self.__storage.factions(species):
			self.ui.comboBox_faction.addItem(QIcon(":icons/images/species/{}/Faction-{}.svg".format(species, item.replace(" ", ""))), item)
		#self.ui.comboBox_faction.addItems(self.__storage.factions(species))


	def repopulateOrganisations(self, species):
		"""
		Fülle die Organisationsauswahl neu auf.
		"""

		self.ui.comboBox_organisation.clear()
		self.ui.comboBox_organisation.addItem("")
		self.ui.comboBox_organisation.addItems(self.__storage.organisations(species))


	def hideShowWidgets_species(self, species):
		"""
		Nicht jede Spezies benötigt alle Widgets. Diese Funktion verbirgt/zeigt alle für die gewählte Spezies erforderlichen Auswahl- und Anzeigefelder.
		"""

		visible = True
		if species == "Human":
			visible = False

		## Menschen haben keinen Tag der Verwandlung.
		self.ui.label_dateBecoming.setVisible(visible)
		self.ui.dateEdit_dateBecoming.setVisible(visible)
		self.ui.label_ageBecoming_label.setVisible(visible)
		self.ui.label_ageBecoming.setVisible(visible)

		self.ui.label_breed.setVisible(visible)
		self.ui.comboBox_breed.setVisible(visible)
		self.ui.label_organisation.setVisible(visible)
		self.ui.comboBox_organisation.setVisible(visible)

		self.ui.comboBox_faction.setVisible( visible )
		self.ui.lineEdit_faction.setVisible( not visible )
		self.ui.lineEdit_faction.clear()

		## Das Kith ist nur für Changelings interessant
		if species == "Changeling":
			self.ui.label_kith.setVisible(True)
			self.ui.comboBox_kith.setVisible(True)
		else:
			self.ui.label_kith.setVisible(False)
			self.ui.comboBox_kith.setVisible(False)

		## Nur Magier und Vampire haben Bonus-Attribute. Werwölfe haben allerdings Bonus-Spezialisierungen.
		affectedSpecies = ("Changeling", "Mage", "Vampire", "Werewolf")
		if species in affectedSpecies:
			self.ui.label_bonus.setVisible(True)
			if species == "Mage":
				self.ui.comboBox_bonus.setVisible(False)
				self.ui.label_bonus2.setVisible(True)
			else:
				self.ui.comboBox_bonus.setVisible(True)
				self.ui.label_bonus2.setVisible(False)
		else:
			self.ui.label_bonus.setVisible(False)
			self.ui.comboBox_bonus.setVisible(False)
			self.ui.label_bonus2.setVisible(False)
