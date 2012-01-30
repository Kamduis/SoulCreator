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

import ast
import copy

from PySide.QtCore import QObject, QDate, Signal, Slot
from PySide.QtGui import QPixmap

from src.Config import Config
from src.Datatypes.StandardTrait import StandardTrait
from src.Datatypes.SubPowerTrait import SubPowerTrait
from src.Datatypes.Identity import Identity
from src.Calc.Calc import Calc
from src.Calc.ConnectPrerequisites import ConnectPrerequisites
from src.Error import ErrListLength
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
	ageChanged = Signal(int)
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
	equipmentChanged = Signal(object)
	magicalToolChanged = Signal(str)
	nimbusChanged = Signal(str)


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
	# 	"melee": [ weapon1, weapon2 ... ]
	# 	"thrown": [ weapon1, weapon2 ... ]
	# 	"ranged": [ weapon1, weapon2 ... ]
	# }
	__weapons = {}


	def __init__(self, template, parent=None):
		"""
		\todo Eigentlich benötigt Subpower keinen eigenen Datentyp. Da die ganzen Zusatzinformationen ja nur im Template zu stehen haben und nicht auch für den Charakter bekannt sein müssen. Der Wert "level" ist aber interessant und gilt für andere Klassen nicht.
		"""

		QObject.__init__(self, parent)

		self.__storage = template

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
		self.__nimbus = ""

		self.__identity = Identity()
		self.__identities = [self.__identity]

		self.__derangements = {}

		self.dateBirthChanged.connect(self.__calcAge)
		self.dateGameChanged.connect(self.__calcAge)
		self.dateBirthChanged.connect(self.__calcAgeBecoming)
		self.dateBecomingChanged.connect(self.__calcAgeBecoming)
		self.weaponAdded.connect(self.weaponsChanged)
		self.weaponRemoved.connect(self.weaponsChanged)

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
						loop = Config.traitMultipleMax
						custom = True

					for i in xrange(loop):
						trait = None
						if typ == "Subpower":
							trait = SubPowerTrait(self, subitem[1]["name"], val)
							trait.level = subitem[1]["level"]
							trait.powers = subitem[1]["powers"]
						else:
							trait = StandardTrait(self, subitem[1]["name"], val)
							trait.age = subitem[1]["age"]
							trait.era = subitem[1]["era"]
							trait.custom = custom
							trait.customText = customText
						trait.identifier = subitem[0]
						trait.species = subitem[1]["species"]
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



		# Sobald irgendein Aspekt des Charakters verändert wird, muß festgelegt werden, daß sich der Charkater seit dem letzten Speichern verändert hat.
		# Es ist Aufgabe der Speicher-Funktion, dafür zu sorgen, daß beim Speichern diese Inforamtion wieder zurückgesetzt wird.
		self.__identity.identityChanged.connect(self.setModified)
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
		self.magicalToolChanged.connect(self.setModified)
		self.nimbusChanged.connect(self.setModified)

	#connect (self, SIGNAL(realIdentityChanged(cv_Identity)), self, SLOT(emitNameChanged(cv_Identity)));


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
	def identities(self):
		"""
		Eine Liste aller Identitäten des Charkaters. Die Identität an Indexposition 0 ist die echte Identität.
		"""

		return self.__identities


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

	def addWeapon(self, category, weapon):
		"""
		Fügt der Waffenliste eine Waffe hinzu.
		"""

		if category not in self.__weapons:
			self.__weapons.setdefault(category, [])

		if weapon not in self.__weapons[category]:
			self.__weapons[category].append(weapon)
			self.weaponAdded.emit(category, weapon)

	def deleteWeapon(self, category, weapon):
		"""
		Entfernt besagte Waffe aus der Waffenliste.
		"""

		if category in self.__weapons:
			self.__weapons[category].remove(weapon)
			self.weaponRemoved.emit(category, weapon)


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
		if item not in self.__equipment:
			self.__equipment.append(item)
			self.equipmentChanged.emit(self.__equipment)

	def delEquipment(self, item):
		if item in self.__equipment:
			self.__equipment.remove(item)
			self.equipmentChanged.emit(self.__equipment)

	def clearEquipment(self):
		if self.__equipment:
			self.__equipment = []
			self.equipmentChanged.emit(self.__equipment)


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



	#def insertIdentity( self, index, identity ):
		#"""
		#Fügt eine neue Identität an der angegebenen Stelle ein.
		#"""

		#self.__identities.insert( index, identity )
		#self.identityChanged.emit( identity )

	#def addIdentity( self, identity ):
		#"""
		#Hängt eine neue Identität an die Liste aller Identitäten des Charkaters an.
		#"""

		#self.__identities.append( identity )
		#self.identityChanged.emit( identity )

	#def setRealIdentity( self, identity ):
		#"""
		#Legt die \emph{echte} Identität des Charakters fest. Diese Identität hat immer Index 0 in der \ref self.__identities -Liste

		#\todo Momentan ist dies die einzige identität, die von diesem Programm genutzt wird.
		#"""

		#if self.__identities[0] != identity:
			#self.__identities[0] = identity
			#self.identityChanged.emit( identity )
			#self.realIdentityChanged.emit( identity )


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

		age = Calc.years(self.dateGame, self.dateBirth)

		if self.__age != age:
			oldAge = self.__age
			self.__age = age
			self.ageChanged.emit(age)

			#if age < Config.ageAdult <= oldAge or oldAge < Config.ageAdult <= age:
				#self.ageCategoryChanged.emit(Config.getAge(age), age, oldAge)


	def __calcAgeBecoming(self):
		"""
		Zur Berechnung des Alters zum Zeitpunkt der Veränderung (Erwachen, Kuß, erste Verwandlung etc.) werden Geburtsdatum und Datum der Veränderung genutzt.
		"""

		age = Calc.years(self.dateBecoming, self.dateBirth)

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

		if ( self.__breed != breed ):
			self.__breed = breed
			self.breedChanged.emit( breed)

	breed = property(__getBreed, setBreed)


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
		# Zeitalter festlegen.
		self.era = Config.eras[0]

		## Anfangsdatum setzen.
		self.dateGame = QDate.currentDate()
		self.dateBirth = QDate(self.dateGame.year() - Config.ageInitial, self.dateGame.month(), self.dateGame.day())
		self.dateBecoming = QDate(self.dateGame.year() - Config.ageAdult, self.dateGame.month(), self.dateGame.day())

		# Löschen aller Identitäten.
		self.__identity.reset()

		# Standardspezies ist der Mensch.
		self.species = Config.initialSpecies

		#Debug.debug(self.__storage.virtues[0])
		#Debug.debug(self.__storage.virtues[0]["name"])
		self.virtue = self.__storage.virtues[0]["name"]
		self.vice = self.__storage.vices[0]["name"]
		self.faction = ""
		self.height = 1.60
		self.weight = 60
		self.eyes = ""
		self.hair = ""
		self.nationality = ""
		# Nicht notwendig, da ja schon die Spezies gewechselt wird, was automatisch diese Felder zurücksetzt.
		#self.breed = self.__storage.breeds(Config.initialSpecies)[0]
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

		self.morality = Config.moralityTraitDefaultValue

		# Übernatürliche Eigenschaft festlegen.
		self.powerstat = Config.powerstatDefaultValue

		for category in self.__weapons:
			for weapon in self.__weapons[category]:
				self.deleteWeapon(category, weapon)
		self.setArmor(name="")
		self.clearEquipment()
		self.magicalTool = ""
		self.nimbus = ""

		self.picture = QPixmap()


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




