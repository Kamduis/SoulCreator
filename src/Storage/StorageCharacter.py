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




from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import QObject, QDate
from PyQt4.QtGui import QPixmap

import src.Config as Config
from src.Datatypes.AbstractTrait import AbstractTrait
from src.Datatypes.StandardTrait import StandardTrait
from src.Datatypes.BonusTrait import BonusTrait
from src.Datatypes.SubPowerTrait import SubPowerTrait
from src.Datatypes.Identity import Identity
from src.Calc.Calc import Calc
from src.Calc.ConnectPrerequisites import ConnectPrerequisites
#from src.Error import ErrListLength
from src.Debug import Debug




class StorageCharacter(QObject):
	"""
	@brief In dieser Klasse werden sämtliche Daten des gerade geöffneten Charakters gespeichert.

	Wird ein Wert durch das Programm geändert, muß der Wert tatsächlich in dieser Klasse verändert werden. Denn der Inhalt dieser Klasse wird beim Speichern in eine Datei geschrieben und beim Laden wird diese Klasse aufgefüllt. Die Anzeige nimmt all ihre Daten aus dieser Klasse.

	Außerdem bietet diese Klasse angenehme Zugriffsfunktionen aus den Informationen, welche zum Programmstart aus den Template-Dateien geladen werden.
	"""


	eraChanged = Signal(str)
	dateBirthChanged = Signal(object)
	dateBecomingChanged = Signal(object)
	dateGameChanged = Signal(object)
	speciesChanged = Signal(str)
	virtueChanged = Signal(str)
	viceChanged = Signal(str)
	breedChanged = Signal(str)
	bonusChanged = Signal(object)
	kithChanged = Signal(str)
	factionChanged = Signal(str)
	organisationChanged = Signal(str)
	partyChanged = Signal(str)
	descriptionChanged = Signal(str)
	powerstatChanged = Signal(int)
	moralityChanged = Signal(int)
	derangementChanged = Signal(int, str)
	#traitChanged = Signal(object)
	#traitsChanged = Signal(object)
	#ageChanged = Signal(int)
	ageChanged = Signal((int,), (str,))
	ageBecomingChanged = Signal(int)
	#ageCategoryChanged = Signal(str, int, int)	# (<Child|Adult>, <neues Alter>, <altes Alter>)
	heightChanged = Signal(float)
	weightChanged = Signal(float)
	eyesChanged = Signal(str)
	hairChanged = Signal(str)
	nationalityChanged = Signal(str)
	pictureChanged = Signal(QPixmap)
	weaponAdded = Signal(str, str)
	weaponRemoved = Signal(str, str)
	weaponsChanged = Signal()
	armorChanged = Signal(str, bool)
	equipmentAdded = Signal(str)
	equipmentRemoved = Signal(str)
	equipmentChanged = Signal()
	automobileAdded = Signal(str, str)
	automobileRemoved = Signal(str, str)
	automobilesChanged = Signal()
	extraordinaryItemAdded = Signal(str, str)
	extraordinaryItemRemoved = Signal(str, str)
	extraordinaryItemsChanged = Signal()
	magicalToolChanged = Signal(str)
	nimbusChanged = Signal(str)
	paradoxMarksChanged = Signal(str)
	companionNameChanged = Signal(str)
	companionPowerChanged = Signal(int)
	companionFinesseChanged = Signal(int)
	companionResistanceChanged = Signal(int)
	companionSizeChanged = Signal(int)
	companionSpeedFactorChanged = Signal(int)
	companionFuelChanged = Signal(int)
	companionNuminaChanged = Signal(object)
	companionBanChanged = Signal(str)

	## Dieses Signal enthält alle möglichen Gründe, um eine Eigenschaft zu verstecken, oder sie zu zeigen. species, age, era, breed, faction
	traitVisibleReasonChanged = Signal(str, str, str, str, str)


	# Eine Liste sämtlicher verfügbaren Eigenschaften.
	#
	# {
	# 	Typ1: {
	# 		Kategorie1: {
	# 			Name1: { "bla": blub, ... }
	# 			Name2: { "bla": blub, ... }
	# 			Name3: { "bla": blub, ... }
	# 			...
	# 		},
	# 		Kategorie2: {
	# 			Name1: { "bla": blub, ... }
	# 			...
	# 		},
	# 		...
	# 	},
	# 	...
	# }
	__traits = {}

	# Eine Liste der Waffen.
	#
	# {
	# 	"melee": [ weapon1, weapon2 ... ],
	# 	"thrown": [ weapon1, weapon2 ... ],
	# 	"ranged": [ weapon1, weapon2 ... ],
	# }
	__weapons = {}

	# Eine Liste der Fahrzeuge.
	#
	# {
	# 	Typ1: [ item1, item2 ... ],
	# 	Typ2: [ item1, item2 ... ],
	# 	...
	# }
	__automobiles = {}

	# Eine Liste der magischen Gegenstände.
	#
	# {
	# 	Typ1: [ item1, item2 ... ],
	# 	Typ2: [ item1, item2 ... ],
	# 	...
	# }
	__extraordinaryItems = {}


	def __init__(self, template, parent=None):
		"""
		\todo Eigentlich benötigt Subpower keinen eigenen Datentyp. Da die ganzen Zusatzinformationen ja nur im Template zu stehen haben und nicht auch für den Charakter bekannt sein müssen. Der Wert "level" ist aber interessant und gilt für andere Klassen nicht.
		"""

		super(StorageCharacter, self).__init__(parent)

		self.__storage = template

		self.isLoading = False
		self.__modified = False
		self.__dateBirth = QDate(0, 0, 0)
		self.__dateBecoming = QDate(0, 0, 0)
		self.__dateGame = QDate(0, 0, 0)
		self.__age = 0
		self.__ageBecoming = 0
		self.__species = ""
		self.__virtue = ""
		self.__vice = ""
		self.__breed = ""
		self.__bonus = {}
		self.__kith = ""
		self.__faction = ""
		self.__organisation = ""
		self.__party = ""
		self.__height = 0.0
		self.__weight = 0.0
		self.__eyes = ""
		self.__hair = ""
		self.__nationality = ""
		self.__description = ""
		self.__powerstat = 0
		self.__morality = 0
		self.__era = ""
		self.__picture = None
		self.__armor = {
			"name": "",
			"dedicated": False,
		}
		self.__equipment = []
		self.__magicalTool = ""

		self.identity = Identity()

		self.__derangements = {}

		self.__nimbus = ""
		self.__paradoxMarks = ""

		self.__vinculi = []
		for i in range(Config.VINCULI_COUNT_MAX):
			vinculum = AbstractTrait()
			self.__vinculi.append(vinculum)
			vinculum.traitChanged.connect(self.setModified)

		self.__companionName = ""
		self.__companionPower = 0
		self.__companionFinesse = 0
		self.__companionResistance = 0
		self.__companionSize = 0
		self.__companionSpeedFactor = 0
		self.__companionFuel = 0
		self.__companionInfluences = []
		for i in range(Config.COMPANION_INFLUENCES_MAX):
			companionInfluence = AbstractTrait()
			self.__companionInfluences.append(companionInfluence)
			companionInfluence.traitChanged.connect(self.setModified)
		self.__companionNumina = []
		self.__companionBan = ""

		self.dateBirthChanged.connect(self.__calcAge)
		self.dateGameChanged.connect(self.__calcAge)
		self.dateBirthChanged.connect(self.__calcAgeBecoming)
		self.dateBecomingChanged.connect(self.__calcAgeBecoming)
		self.weaponAdded.connect(self.weaponsChanged)
		self.weaponRemoved.connect(self.weaponsChanged)
		self.equipmentAdded.connect(self.automobilesChanged)
		self.equipmentRemoved.connect(self.equipmentChanged)
		self.automobileAdded.connect(self.automobilesChanged)
		self.automobileRemoved.connect(self.automobilesChanged)
		self.extraordinaryItemAdded.connect(self.extraordinaryItemsChanged)
		self.extraordinaryItemRemoved.connect(self.extraordinaryItemsChanged)

		# Die Eigenschaften in den Charakter laden.
		self.__traits = {}
		# Eigenschaften setzen.
		for typ in self.__storage.traits.keys():
			self.__traits.setdefault(typ, {})
			for item in template.traits[typ]:
				self.__traits[typ].setdefault(item, {})
				for subitem in template.traits[typ][item].items():
					#Debug.debug(subitem)
					val = 2	# Dies mache ich, damit beim initialen Charakter-Reset, auch alle Voraussetzungen überprüft werden.
					# Eigenschaften, die Zusaztext erhalten können (bspw. Language), werden mehrfach in das Dictionary eingefügt. Aber da ein Dictonary immer nur einen Eintrag desselben Namens haben kann, muß selbiger um ein numerisches Suffix erweitert werden.
					loop = 1
					custom = False
					customText = None
					if typ != "Subpower" and subitem[1]["custom"]:
						loop = Config.MULTIPLE_TRAITS_MAX
						custom = True

					for i in range(loop):
						trait = None
						if typ == "Subpower":
							trait = SubPowerTrait(self, subitem[1]["name"], val)
							trait.level = subitem[1]["level"]
							trait.powers = subitem[1]["powers"]
						else:
							if typ == "Attribute" or typ == "Skill":
								trait = BonusTrait(self, subitem[1]["name"], val)
							else:
								trait = StandardTrait(self, subitem[1]["name"], val)
							trait.age = subitem[1]["age"]
							trait.era = subitem[1]["era"]
							trait.custom = custom
							trait.customText = customText
						trait.identifier = subitem[0]
						trait.species = subitem[1]["species"]
						trait.cheap = subitem[1]["cheap"]
						#if typ == "Subpower" and trait.species == "Werewolf":
							#Debug.debug(subitem[1]["name"], subitem[1]["only"])
						trait.only = subitem[1]["only"]
						if "prerequisites" in subitem[1] and subitem[1]["prerequisites"]:
							trait.hasPrerequisites = True
							trait.prerequisitesText = subitem[1]["prerequisites"]
						# In der Eigenschaft steht der richtige Name aber im Dictionary der Name mit einem numerischen Suffix, damit die Eigenschaft häufiger auftauchen kann.
						dictKey = subitem[0]
						if custom:
							dictKey = "{}{}".format(subitem[0], i)
						self.__traits[typ][item].setdefault(dictKey, trait)

						# Wenn sich eine Eigenschaft ändert, gilt der Charakter als modifiziert.
						trait.traitChanged.connect(self.setModified)
				#if typ == "Subpower":
					#Debug.debug(self.__traits[typ][item])

		self.bonusChanged.connect(self.__changeBonusTrait)

		# Sobald irgendein Aspekt des Charakters verändert wird, muß festgelegt werden, daß sich der Charkater seit dem letzten Speichern verändert hat.
		# Es ist Aufgabe der Speicher-Funktion, dafür zu sorgen, daß beim Speichern diese Inforamtion wieder zurückgesetzt wird.
		self.identity.identityChanged.connect(self.setModified)
		self.eraChanged.connect(self.setModified)
		self.dateBirthChanged.connect(self.setModified)
		self.dateBecomingChanged.connect(self.setModified)
		self.dateGameChanged.connect(self.setModified)
		# Unerwünschte Wirkung
		#self.speciesChanged.connect(self.clearUnusableTraits)
		self.speciesChanged.connect(self.setModified)
		self.virtueChanged.connect(self.setModified)
		self.viceChanged.connect(self.setModified)
		self.breedChanged.connect(self.setModified)
		self.kithChanged.connect(self.setModified)
		self.bonusChanged.connect(self.setModified)
		self.factionChanged.connect(self.setModified)
		self.partyChanged.connect(self.setModified)
		self.descriptionChanged.connect(self.setModified)
		self.powerstatChanged.connect(self.setModified)
		self.moralityChanged.connect(self.setModified)
		self.derangementChanged.connect(self.setModified)
		self.pictureChanged.connect(self.setModified)
		self.weaponsChanged.connect(self.setModified)
		self.armorChanged.connect(self.setModified)
		self.equipmentChanged.connect(self.setModified)
		self.automobilesChanged.connect(self.setModified)
		self.extraordinaryItemsChanged.connect(self.setModified)
		self.magicalToolChanged.connect(self.setModified)
		self.nimbusChanged.connect(self.setModified)
		self.paradoxMarksChanged.connect(self.setModified)
		self.companionPowerChanged.connect(self.setModified)
		self.companionFinesseChanged.connect(self.setModified)
		self.companionResistanceChanged.connect(self.setModified)
		self.companionSizeChanged.connect(self.setModified)
		self.companionSpeedFactorChanged.connect(self.setModified)
		self.companionFuelChanged.connect(self.setModified)
		self.companionNuminaChanged.connect(self.setModified)
		self.companionBanChanged.connect(self.setModified)

		self.ageChanged.connect(self.deselctTraitsWithWrongAge)

		self.speciesChanged.connect(self.__emitTraitVisibleReasonChanged)
		self.ageChanged.connect(self.__emitTraitVisibleReasonChanged)
		self.eraChanged.connect(self.__emitTraitVisibleReasonChanged)
		self.breedChanged.connect(self.__emitTraitVisibleReasonChanged)
		self.factionChanged.connect(self.__emitTraitVisibleReasonChanged)

	#connect (self, SIGNAL(realIdentityChanged(cv_Identity)), self, SLOT(emitNameChanged(cv_Identity)));


	def __emitTraitVisibleReasonChanged(self):
		ageText = Config.getAge(self.age)
		self.traitVisibleReasonChanged.emit(self.species, ageText, self.era, self.breed, self.faction)


	def __getEra(self):
		"""
		Gibt die Ära aus, in welcher der Charakter zuhause ist.
		"""

		return self.__era

	def setEra( self, era ):
		"""
		Legt die Ära fest, in welcher der Charakter zuhause ist.
		"""

		if ( self.__era != era ):
			self.__era = era
			#Debug.debug("Ära verändert zu {}".format(era) )
			self.eraChanged.emit( era )

	era = property(__getEra, setEra)


	def __getDateBirth(self):
		"""
		Geburtsdatum des Charakters.
		"""

		#Debug.debug(self.__dateBirth)
		return self.__dateBirth

	def setDateBirth( self, date ):
		if ( self.__dateBirth != date ):
			self.__dateBirth = date
			self.dateBirthChanged.emit( date )

	dateBirth = property(__getDateBirth, setDateBirth)


	def __getDateBecoming(self):
		"""
		Das Datum, an welchem sich der Charakters zu einem übernatürlichen Wesen veränderte.
		"""

		return self.__dateBecoming

	def setDateBecoming( self, date ):
		if ( self.__dateBecoming != date ):
			self.__dateBecoming = date
			self.dateBecomingChanged.emit( date )

	dateBecoming = property(__getDateBecoming, setDateBecoming)


	def __getDateGame(self):
		"""
		Das aktuelle Datum im Spiel.
		"""

		return self.__dateGame

	def setDateGame( self, date ):
		if ( self.__dateGame != date ):
			self.__dateGame = date
			self.dateGameChanged.emit( date )

	dateGame = property(__getDateGame, setDateGame)


	@property
	def age(self):
		"""
		Alter des Charakters.
		"""

		return self.__age


	@property
	def ageBecoming(self):
		"""
		Alter des Charakters bei der Veränderung.
		"""

		return self.__ageBecoming


	def __getSpecies(self):
		"""
		Gibt die Spezies des Charakters aus.
		"""

		return self.__species

	def setSpecies( self, species ):
		"""
		Legt die Spezies des Charakters fest.
		"""

		if ( self.__species != species ):
			self.__species = species
			#Debug.debug("Spezies in Speicher verändert zu {}!".format(species))
			self.speciesChanged.emit( species )

	species = property(__getSpecies, setSpecies)


	@property
	def derangements(self):
		"""
		Eine Liste aller Identitäten des Charkaters. Die Identität an Indexposition 0 ist die echte Identität.
		"""

		return self.__derangements

	@derangements.setter
	def derangements(self, derangements):
		"""
		Eine Liste aller Identitäten des Charkaters. Die Identität an Indexposition 0 ist die echte Identität.
		"""

		#Debug.debug(derangements)

		if derangements and self.__derangements != derangements:
			self.__derangements = derangements
			## Jetzt müssen in der richtigen Reihenfolge (hoch nach tief) die Signale gesandt werden.
			keys = self.__derangements.keys()
			#Debug.debug(keys, range(min(keys), max(keys)+1)[::-1])
			for i in range(min(keys), max(keys)+1)[::-1]:
				if i in keys:
					self.derangementChanged.emit(i, self.__derangements[i])


	def setDerangement(self, moralityValue, derangement):
		"""
		Legt die Geistesstörung für den zugehörigen Moralwert fest.
		"""

		#Debug.debug(moralityValue, type(moralityValue))
		if moralityValue not in self.__derangements:
			if derangement:
				self.__derangements[moralityValue] = derangement
				#Debug.debug(derangement, moralityValue)
				self.derangementChanged.emit(moralityValue, derangement)
		elif self.__derangements[moralityValue] != derangement:
			# Wird als Geistesstörung ein leerer String übergeben, wird dieser Eintrag aus der Liste gelöscht. Dennoch wird das Signal einer Änderung mit dem leeren String gesandt.
			if derangement:
				self.__derangements[moralityValue] = derangement
				#Debug.debug(derangement, moralityValue)
			else:
				del self.__derangements[moralityValue]
			self.derangementChanged.emit(moralityValue, derangement)


	@property
	def picture(self):
		"""
		Charakterbild.
		"""

		return self.__picture

	@picture.setter
	def picture(self, image):
		if self.__picture != image:
			self.__picture = image
			self.pictureChanged.emit(image)


	@property
	def weapons(self):
		"""
		Die Liste aller Waffen des Charakters.
		"""

		return self.__weapons

	def addWeapon(self, weapon, category):
		"""
		Fügt der Waffenliste eine Waffe hinzu.
		"""

		if category not in self.__weapons:
			self.__weapons.setdefault(category, [])

		if weapon not in self.__weapons[category]:
			self.__weapons[category].append(weapon)
			self.weaponAdded.emit(weapon, category)

	def deleteWeapon(self, weapon, category):
		"""
		Entfernt besagte Waffe aus der Waffenliste.
		"""

		if category in self.__weapons:
			self.__weapons[category].remove(weapon)
			self.weaponRemoved.emit(weapon, category)


	@property
	def armor(self):
		"""
		Die Rüstung (Name) des Charakters
		"""

		return self.__armor

	def setArmor(self, name, dedicated=False):
		if self.__armor["name"] != name or self.__armor["dedicated"] != dedicated:
			self.__armor["name"] = name
			self.__armor["dedicated"] = dedicated
			self.armorChanged.emit(name, dedicated)


	@property
	def equipment(self):
		"""
		Gegenstände im Besitz des Charakters.
		"""

		return self.__equipment

	def addEquipment(self, item):
		#Debug.debug(item)
		if item not in self.__equipment:
			self.__equipment.append(item)
			self.equipmentAdded.emit(item)

	def deleteEquipment(self, item):
		if item in self.__equipment:
			self.__equipment.remove(item)
			self.equipmentRemoved.emit(item)


	@property
	def automobiles(self):
		"""
		Die Liste aller Fahrzeuge des Charakters.
		"""

		return self.__automobiles

	def addAutomobile(self, automobile, category):
		"""
		Fügt der Liste ein Fahrzeug hinzu.
		"""

		if category not in self.__automobiles:
			self.__automobiles.setdefault(category, [])

		if automobile not in self.__automobiles[category]:
			self.__automobiles[category].append(automobile)
			self.automobileAdded.emit(automobile, category)

	def deleteAutomobile(self, automobile, category):
		"""
		Entfernt besagtes Fahrzeug aus der Liste.
		"""

		if category in self.__automobiles:
			self.__automobiles[category].remove(automobile)
			self.automobileRemoved.emit(automobile, category)


	@property
	def extraordinaryItems(self):
		"""
		Die Liste aller magischen Gegenstände des Charakters.
		"""

		return self.__extraordinaryItems

	def addExtraordinaryItem(self, extraordinaryItem, typ):
		"""
		Fügt der Liste der magischen Gegenstände einen hinzu.
		"""

		if typ not in self.__extraordinaryItems:
			self.__extraordinaryItems.setdefault(typ, [])

		if extraordinaryItem not in self.__extraordinaryItems[typ]:
			self.__extraordinaryItems[typ].append(extraordinaryItem)
			self.extraordinaryItemAdded.emit(extraordinaryItem, typ)

	def deleteExtraordinaryItem(self, extraordinaryItem, typ):
		"""
		Entfernt besagten magischen Gegenstand aus der Liste.
		"""

		if typ in self.__extraordinaryItems:
			self.__extraordinaryItems[typ].remove(extraordinaryItem)
			self.extraordinaryItemRemoved.emit(extraordinaryItem, typ)


	def __getMagicalTool(self):
		"""
		Magisches Werkzeug.
		"""

		return self.__magicalTool

	def setMagicalTool(self, tool):

		if self.__magicalTool != tool:
			self.__magicalTool = tool
			self.magicalToolChanged.emit(tool)

	magicalTool = property(__getMagicalTool, setMagicalTool)


	def __getNimbus(self):
		"""
		Der Nimbus eines Magiers.
		"""

		return self.__nimbus

	def setNimbus(self, nimbus):

		if self.__nimbus != nimbus:
			self.__nimbus = nimbus
			self.nimbusChanged.emit(nimbus)

	nimbus = property(__getNimbus, setNimbus)


	def __getParadoxMarks(self):
		"""
		Die Paradoxzeichen eines Magiers.
		"""

		return self.__paradoxMarks

	def setParadoxMarks(self, paradoxMarks):

		if self.__paradoxMarks != paradoxMarks:
			self.__paradoxMarks = paradoxMarks
			self.paradoxMarksChanged.emit(paradoxMarks)

	paradoxMarks = property(__getParadoxMarks, setParadoxMarks)


	@property
	def vinculi(self):
		"""
		Die Vinculi eines Vampirs
		"""

		return self.__vinculi


	def __getCompanionName(self):
		return self.__companionName

	def setCompanionName(self, name):
		if self.__companionName != name:
			self.__companionName = name
			self.companionNameChanged.emit(name)

	companionName = property(__getCompanionName, setCompanionName)


	def __getCompanionPower(self):
		return self.__companionPower

	def setCompanionPower(self, power):
		if self.__companionPower != power:
			self.__companionPower = power
			self.companionPowerChanged.emit(power)

	companionPower = property(__getCompanionPower, setCompanionPower)


	def __getCompanionFinesse(self):
		return self.__companionFinesse

	def setCompanionFinesse(self, finesse):
		if self.__companionFinesse != finesse:
			self.__companionFinesse = finesse
			self.companionFinesseChanged.emit(finesse)

	companionFinesse = property(__getCompanionFinesse, setCompanionFinesse)


	def __getCompanionResistance(self):
		return self.__companionResistance

	def setCompanionResistance(self, resistance):
		if self.__companionResistance != resistance:
			self.__companionResistance = resistance
			self.companionResistanceChanged.emit(resistance)

	companionResistance = property(__getCompanionResistance, setCompanionResistance)


	def __getCompanionSize(self):
		return self.__companionSize

	def setCompanionSize(self, size):
		if self.__companionSize != size:
			self.__companionSize = size
			self.companionSizeChanged.emit(size)

	companionSize = property(__getCompanionSize, setCompanionSize)


	def __getCompanionSpeedFactor(self):
		return self.__companionSpeedFactor

	def setCompanionSpeedFactor(self, speedFactor):
		if self.__companionSpeedFactor != speedFactor:
			self.__companionSpeedFactor = speedFactor
			self.companionSpeedFactorChanged.emit(speedFactor)

	companionSpeedFactor = property(__getCompanionSpeedFactor, setCompanionSpeedFactor)


	def __getCompanionFuel(self):
		return self.__companionFuel

	def setCompanionFuel(self, fuel):
		if self.__companionFuel != fuel:
			self.__companionFuel = fuel
			self.companionFuelChanged.emit(fuel)

	companionFuel = property(__getCompanionFuel, setCompanionFuel)


	@property
	def companionInfluences(self):
		"""
		Die Einflüsse eines Vertrauten-Geistes.
		"""

		return self.__companionInfluences

	@property
	def companionNumina(self):
		return self.__companionNumina

	@companionNumina.setter
	def companionNumina(self, numina):
		if self.__companionNumina != numina:
			self.__companionNumina = numina
			self.companionNuminaChanged.emit(numina)

	def appendCompanionNumen(self, numen):
		self.__companionNumina.append(numen)

	def removeCompanionNumen(self, numen):
		self.__companionNumina.remove(numen)


	def __getCompanionBan(self):
		return self.__companionBan

	def setCompanionBan(self, ban):
		if self.__companionBan != ban:
			self.__companionBan = ban
			self.companionBanChanged.emit(ban)

	companionBan = property(__getCompanionBan, setCompanionBan)


	@property
	def traits(self):
		return self.__traits

	#def __setTraits(self, traits):
		#if self.__traits != traits:
			#self.__traits = traits
			#self.traitsChanged.emit(traits)


	@property
	def subPowers(self):
		return self.__subPowers


	def __calcAge(self):
		"""
		Zur Berechnung des Alters werden Geburtstag und Datum im Spiel herangezogen.
		"""

		age = Calc.years(self.dateBirth, self.dateGame)

		if self.__age != age:
			ageCtagoryChanged = False
			if Config.getAge(self.__age) != Config.getAge(age):
				ageCtagoryChanged = True
			self.__age = age
			self.ageChanged.emit(age)
			if ageCtagoryChanged:
				self.ageChanged[str].emit(Config.getAge(age))


	def __calcAgeBecoming(self):
		"""
		Zur Berechnung des Alters zum Zeitpunkt der Veränderung (Erwachen, Kuß, erste Verwandlung etc.) werden Geburtsdatum und Datum der Veränderung genutzt.
		"""

		age = Calc.years(self.dateBirth, self.dateBecoming)

		if self.__ageBecoming != age:
			self.__ageBecoming = age
			self.ageBecomingChanged.emit(age)


	def __getVirtue(self):
		"""
		Tugend des Charakters
		"""

		return self.__virtue

	def setVirtue( self, virtue ):
		"""
		Verändert die Tugend.

		Bei einer Veränderung wird das Signal virtueChanged() ausgesandt.
		"""

		if ( self.__virtue != virtue ):
			self.__virtue = virtue
			self.virtueChanged.emit( virtue )

	virtue = property(__getVirtue, setVirtue)


	def __getVice(self):
		"""
		Laster des Charakters
		"""

		return self.__vice

	def setVice( self, vice ):
		"""
		Verändert das Laster.

		Bei einer Veränderung wird das Signal viceChanged() ausgesandt.
		"""

		if ( self.__vice != vice ):
			self.__vice = vice
			self.viceChanged.emit( vice )

	vice = property(__getVice, setVice)


	def __getBreed(self ):
		"""
		Brut (Seeming, Path, Clan, Auspice) des Charakters.
		"""

		return self.__breed

	def setBreed( self, breed ):
		"""
		Verändert die Brut.

		Bei einer Veränderung wird das Signal breedChanged() ausgesandt.
		"""

		if self.__breed != breed:
			self.__breed = breed
			self.breedChanged.emit(breed)

	breed = property(__getBreed, setBreed)


	def __getBonus(self ):
		"""
		Bonuseigenschaft
		"""

		return self.__bonus

	def setBonus( self, bonus ):
		"""
		Verändert die Bonuseigenschaft.

		Die Bonuseigenschaft wird folgendermaßen gespeichert. Der Eintrag für die Spezialisierung ist optional.
		{
			"type": Typ,
			"name": Name,
			"specialty": Gewählte Spezialisierung,
		}
		"""

		#Debug.debug(bonus)

		if ( self.__bonus != bonus ):
			#Debug.debug(bonus)
			self.__bonus = bonus
			self.bonusChanged.emit( bonus )

	bonus = property(__getBonus, setBonus)


	def __changeBonusTrait(self, bonus):
		"""
		Ändert die Bonuseigenschaft.

		\todo Wenn die Erschaffungsphase vorüber ist, sollte die Bonuseigenschaft nichtmehr verändert werden können und die davon betroffene Eigenscahft wie eine normale Eigenschaft mit erhöhtem Wert, zusätzlicher Spezialisierung betrachtet werden.
		"""

		## Alle bisherigen Bonuseigenschaften löschen, denn es kann immer nur eine solche geben.
		for typ in self.traits:
			for category in self.traits[typ]:
				for identifier in self.traits[typ][category]:
					if type(self.traits[typ][category][identifier]) == BonusTrait:
						self.traits[typ][category][identifier].clearBonus()

		if bonus:
			for category in self.traits[bonus["type"]]:
				if bonus["name"] in self.traits[bonus["type"]][category].keys():
					if type(self.traits[bonus["type"]][category][bonus["name"]]) == BonusTrait:
						if bonus["type"] == "Attribute":
							self.traits[bonus["type"]][category][bonus["name"]].bonusValue = 1
							#Debug.debug("Bonuseigenschaft {} verändert!".format(self.traits[bonus["type"]][category][bonus["name"]].name))
						elif bonus["type"] == "Skill" and "specialty" in bonus:
							self.traits[bonus["type"]][category][bonus["name"]].bonusSpecialties = [ bonus["specialty"] ]
							#Debug.debug("Bonuseigenschaft {} verändert!".format(self.traits[bonus["type"]][category][bonus["name"]].name))
					break


	def __getKith(self ):
		"""
		Kith der Wechselbälger
		"""

		return self.__kith

	def setKith( self, kith ):
		"""
		Verändert das Kith.
		"""

		if ( self.__kith != kith ):
			self.__kith = kith
			self.kithChanged.emit( kith )

	kith = property(__getKith, setKith)


	def __getFaction(self):
		"""
		Fraktion (Court, Order, Covenant, Tribe) des Charakters.
		"""

		return self.__faction

	def setFaction( self, faction ):
		"""
		Verändert die Fraktion.

		Bei einer Veränderung wird das Signal factionChanged() ausgesandt.
		"""

		if ( self.__faction != faction ):
			self.__faction = faction
			self.factionChanged.emit( faction )

	faction = property(__getFaction, setFaction)


	def __getOrganisation(self):
		"""
		Organisation (Entitlement, Legacy, Bloodline, Lodge) des Charakters.
		"""

		return self.__organisation

	def setOrganisation( self, organisation ):
		"""
		Verändert die Organisation.

		Bei einer Veränderung wird das Signal organisationChanged() ausgesandt.
		"""

		if ( self.__organisation != organisation ):
			self.__organisation = organisation
			self.organisationChanged.emit( organisation )

	organisation = property(__getOrganisation, setOrganisation)


	def __getParty(self):
		"""
		Name der Freundesgruppe des Charakters.
		"""

		return self.__party

	def setParty( self, party ):
		if ( self.__party != party ):
			self.__party = party
			self.partyChanged.emit( party )

	party = property(__getParty, setParty)


	def __getHeight(self):
		"""
		Größe des Charakters in m.
		"""

		return self.__height

	def setHeight( self, height ):
		if ( self.__height != height ):
			self.__height = height
			self.heightChanged.emit( height )

	height = property(__getHeight, setHeight)


	def __getWeight(self):
		"""
		Gewicht des Charakters in kg.
		"""

		return self.__weight

	def setWeight( self, weight ):
		if ( self.__weight != weight ):
			self.__weight = weight
			self.weightChanged.emit( weight )

	weight = property(__getWeight, setWeight)


	def __getEyes(self):
		"""
		Beschreibung der Augen des Charakters.
		"""

		return self.__eyes

	def setEyes( self, eyes ):
		if ( self.__eyes != eyes ):
			self.__eyes = eyes
			self.eyesChanged.emit( eyes )

	eyes = property(__getEyes, setEyes)


	def __getHair(self):
		"""
		Beschreibung der Haare des Charakters.
		"""

		return self.__hair

	def setHair( self, hair ):
		if ( self.__hair != hair ):
			self.__hair = hair
			self.hairChanged.emit( hair )

	hair = property(__getHair, setHair)


	def __getNationality(self):
		"""
		Die Nationalität des Charakters.
		"""

		return self.__nationality

	def setNationality( self, nationality ):
		if ( self.__nationality != nationality ):
			self.__nationality = nationality
			self.nationalityChanged.emit( nationality )

	nationality = property(__getNationality, setNationality)


	@property
	def description(self):
		"""
		Name der Freundesgruppe des Charakters.
		"""

		return self.__description

	@description.setter
	def description( self, text ):
		if ( self.__description != text ):
			self.__description = text
			self.descriptionChanged.emit( text )


	def __getPowerstat(self):
		"""
		Gibt den Wert des Super-Attributs aus.
		"""

		return self.__powerstat

	def setPowerstat( self, value ):
		"""
		Verändert den Wert des Super-Attributs.

		Bei einer Veränderung wird das Signal powerstatChanged() ausgesandt.
		"""

		if ( self.__powerstat != value ):
			self.__powerstat = value
			self.powerstatChanged.emit( value )

	powerstat = property(__getPowerstat, setPowerstat)


	def __getMorality(self):
		"""
		Gibt den Wert der Moral aus.
		"""

		return self.__morality

	def setMorality( self, value ):
		"""
		Verändert den Wert der Moral.

		Bei einer Veränderung wird das Signal moralityChanged() ausgesandt.
		"""

		if ( self.__morality != value ):
			self.__morality = value
			#Debug.debug("Moral verändert auf {}".format(value))
			self.moralityChanged.emit( value )

	morality = property(__getMorality, setMorality)


	def resetCharacter(self):
		## Der Charkater wird umorganisiert, ohne daß wir haufenweise Warnhinweise haben wollen.
		self.isLoading = True
		# Standardspezies ist der Mensch.
		self.species = Config.SPECIES_INITIAL
		# Zeitalter festlegen.
		self.era = Config.ERA_INITIAL
		## Anfangsdatum setzen.
		self.dateGame = QDate.currentDate()
		self.dateBirth = QDate(self.dateGame.year() - Config.AGE_INITIAL, self.dateGame.month(), self.dateGame.day())
		self.dateBecoming = QDate(self.dateGame.year() - Config.AGE_ADULT, self.dateGame.month(), self.dateGame.day())

		# Löschen aller Identitäten.
		self.identity.reset()

		#Debug.debug(self.__storage.virtues[0])
		#Debug.debug(self.__storage.virtues[0]["name"])
		self.virtue = self.__storage.virtues[0]["name"]
		self.vice = self.__storage.vices[0]["name"]
		self.breed = ""
		self.bonus= ""
		self.kith = ""
		self.faction = ""
		self.height = 1.60
		self.weight = 60
		self.eyes = ""
		self.hair = ""
		self.nationality = ""
		# Nicht notwendig, da ja schon die Spezies gewechselt wird, was automatisch diese Felder zurücksetzt.
		#self.breed = self.__storage.breeds(Config.SPECIES_INITIAL)[0]
		self.__derangements = {}
		self.party = ""
		self.description = ""

		# Menschen haben eine Leere liste, also kann ich auch die Indizes nicht ändern.
		#// setBreed(storage.breedNames(species()).at(0));
		#// setFaction(storage.breedNames(species()).at(0));

		# Attribute und andere Eigenschaften auf Anfangswerte setzen.
		for item in self.__traits:
			val = 0
			if item == "Attribute":
				val = 1
			for subitem in self.__traits[item]:
				for subsubitem in self.__traits[item][subitem].values():
					subsubitem.value = val
					subsubitem.customText = ""
					subsubitem.specialties = []

		self.morality = Config.TRAIT_MORALITY_VALUE_DEFAULT

		# Übernatürliche Eigenschaft festlegen.
		self.powerstat = Config.TRAIT_POWERSTAT_VALUE_DEFAULT

		# Beim Löschen ist darauf zu achten, daß ich nicht aus der Liste löschen kann, über die ich iteriere. Sonst wird nicht alles gelöscht.
		for category in self.__weapons:
			weaponList = self.__weapons[category][:]
			for weapon in weaponList:
				self.deleteWeapon(category, weapon)
		self.setArmor(name="")
		eqipmentList = self.__equipment[:]
		for item in eqipmentList:
			self.deleteEquipment(item)
		for category in self.__automobiles:
			automobileList  = self.__automobiles[category][:]
			for automobile in automobileList:
				self.deleteAutomobile(category, automobile)
		for typ in self.__extraordinaryItems:
			extraordinaryItemList = self.__extraordinaryItems[typ][:]
			for item in extraordinaryItemList:
				self.deleteExtraordinaryItem(typ, item)
		self.magicalTool = ""
		self.nimbus = ""
		self.paradoxMarks = ""
		for vinculum in self.__vinculi:
			vinculum.name = ""
			vinculum.value = 0

		self.companionName = ""
		self.companionPower = 0
		self.companionFinesse = 0
		self.companionResistance = 0
		self.companionSize = 0
		self.companionSpeedFactor = 0
		self.companionFuel = 0
		for companionInfluence in self.__companionInfluences:
			companionInfluence.name = ""
			companionInfluence.value = 0
		self.companionNumina = []
		self.companionBan = ""

		self.picture = QPixmap()

		## Fertig mit dem Laden der enuen Werte.
		self.isLoading = False


	def isModifed(self):
		return self.__modified

	def setModified( self, sw=True ):
		if ( self.__modified != sw ):
			self.__modified = sw


	# Unerwünschte Funktion.
	#def clearUnusableTraits(self, species):
		#"""
		#Beim Wechsel der Spezies werden zahlreiche Eigenschaften für den Charakter unnutzbar. Diese werden auf den Wert 0 gesetzt.

		#\todo Möglicherweise will ich das garnicht. Dann kan ich beim Zurücksetzen der Spezies wieder die zuvor gewählten Powers darstellen. Es muß natürlich darauf geachtet werden, daß beim Speichern nur eigenschaft der richtigen Spezies gespeichert werden und auf dem Charakterbogen auch nur die verwendbaren Werte auftauchen.
		#"""

		### Es müssen nur bei ein paar Typen die Eigenschaft durchsucht werden.
		#typesToClear = ( "Merit", "Flaw", "Power", )
		#for typ in typesToClear:
			#for item in self.__traits[typ]:
				#for subitem in self.__traits[typ][item].values():
					#if subitem.species and subitem.species != species and subitem.value != 0:
						##Debug.debug("Setze {} auf 0.".format(subitem.name))
						#subitem.value = 0


	def checkPrerequisites(self, trait):
		"""
		Diese Funktion überprüft, ob die Voraussetzungen der Eigenschaft "trait" erfüllt sind oder nicht.

		\todo Den SyntaxError sollte ich nicht verstecken!
		"""

		ConnectPrerequisites.checkPrerequisites(trait, self.__storage, self)


	def deselctTraitsWithWrongAge(self, age):
		"""
		\todo Man sollte nicht bei jedem Alterswechsel über alle Eigenschaften laufen, sondern zu Beginn des Programms alle Eigenschaften mit "Kid" bzw. "Adult" mit ageChanged verknüpfen.
		"""

		for typ in self.__traits:
			for category in self.__traits[typ]:
				for trait in self.__traits[typ][category].values():
					if type(trait) == StandardTrait and trait.age and trait.age != Config.getAge(self.age) and trait.value > 0:
						trait.value = 0




