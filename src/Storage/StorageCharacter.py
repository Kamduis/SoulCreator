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

from PySide.QtCore import QObject, QDate, Signal, Slot
from PySide.QtGui import QPixmap

from src.Config import Config
from src.Datatypes.Trait import Trait
from src.Datatypes.Identity import Identity
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
	factionChanged = Signal(str)
	organisationChanged = Signal(str)
	partyChanged = Signal(str)
	descriptionChanged = Signal(str)
	powerstatChanged = Signal(int)
	moralityChanged = Signal(int)
	derangementChanged = Signal(int, str)
	armorChanged = Signal(object)
	#traitChanged = Signal(object)
	#traitsChanged = Signal(object)
	ageChanged = Signal(int)
	ageBecomingChanged = Signal(int)
	heightChanged = Signal(float)
	weightChanged = Signal(float)
	eyesChanged = Signal(str)
	hairChanged = Signal(str)
	nationalityChanged = Signal(str)
	pictureChanged = Signal(QPixmap)


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


	def __init__(self, template, parent=None):
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
		self.__armor = [0, 0]
		self.__era = ""
		self.__picture = None

		self.__identity = Identity()
		self.__identities = [self.__identity]

		self.__derangements = {}

		self.dateBirthChanged.connect(self.__calcAge)
		self.dateGameChanged.connect(self.__calcAge)
		self.dateBecomingChanged.connect(self.__calcAgeBecoming)
		self.dateGameChanged.connect(self.__calcAgeBecoming)

		# Die Eigenschaften in den Charakter laden.
		self.__traits = {}
		# Eigenscahften setzen.
		for typ in Config.typs:
			self.__traits.setdefault(typ, {})
			for item in template.traits[typ]:
				self.__traits[typ].setdefault(item, {})
				for subitem in template.traits[typ][item].items():
					#Debug.debug(subitem)
					val = 0
					# Eigenschaften, die Zusaztext erhalten können (bspw. Language), werden mehrfach in das Dictionary eingefügt. Aber da ein Dictonary immer nur einen Eintrag desselben Namens haben kann, muß selbiger um ein numerisches Suffix erweitert werden.
					loop = 1
					custom = False
					customText = None
					if subitem[1]["custom"]:
						loop = Config.traitMultipleMax
						custom = True

					for i in xrange(loop):
						trait = Trait(self, subitem[0], val)
						trait.age = subitem[1]["age"]
						trait.era = subitem[1]["era"]
						trait.species = subitem[1]["species"]
						trait.custom = custom
						trait.customText = customText
						if "prerequisite" in subitem[1]:
							trait.hasPrerequisites = True
							trait.prerequisitesText = subitem[1]["prerequisite"]
						# In der Eigenschaft steht der richtige Name aber im Dictionary der Name mit einem numerischen Suffix, damit die Eigenschaft häufiger auftauchen kann.
						dictKey = subitem[0]
						if custom:
							dictKey = "{}{}".format(subitem[0], i)
						self.__traits[typ][item].setdefault(dictKey, trait)

						# Wenn sich eine Eigenschaft ändert, gilt der Charakter als modifiziert.
						trait.traitChanged.connect(self.setModified)

					

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
		self.armorChanged.connect(self.setModified)
		self.pictureChanged.connect(self.setModified)

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


	def __getTraits(self):
		return self.__traits

	#def __setTraits(self, traits):
		#if self.__traits != traits:
			#self.__traits = traits
			#self.traitsChanged.emit(traits)

	traits = property(__getTraits)


	def __calcAge(self):
		"""
		Zur Berechnung des Alters werden Geburtstag und Datum im Spiel herangezogen.
		"""

		age = self.dateGame.year() - self.dateBirth.year()
		if self.dateGame.month() < self.dateBirth.month() or (self.dateGame.month() == self.dateBirth.month() and self.dateGame.day() < self.dateBirth.day()):
			age -= 1

		if self.__age != age:
			self.__age = age
			self.ageChanged.emit(age)


	def __calcAgeBecoming(self):
		"""
		Zur Berechnung des Alters zum Zeitpunkt der Veränderung (Erwachen, Kuß, erste Verwandlung etc.) werden Geburtsdatum und Datum der Veränderung genutzt.
		"""

		age = self.dateBecoming.year() - self.dateBirth.year()
		if self.dateBecoming.month() < self.dateBirth.month() or (self.dateBecoming.month() == self.dateBirth.month() and self.dateBecoming.day() < self.dateBirth.day()):
			age -= 1

		if self.__ageBecoming != age:
			self.__ageBecoming = age
			self.ageBecomingChanged.emit(age)


	#def addTrait( self, typ, category, trait ):
		#"""
		#Fügt dem Speicher eine neue Eigenschaft hinzu.
		 
		#\note Doppelte Eigenschaften werden mit dem neuen Wert überschrieben.
		 
		#\todo Eigenschaften mit Zusatztext werden nur gespeichert, wenn dieser Text auch vorhanden ist.
		#"""

		#if typ not in self.__traits:
			#self.__traits.setdefault(typ,{})

		#if category not in self.__traits[typ]:
			#self.__traits[typ].setdefault(category,[])

		#self.__traits[typ][category].append(trait)

		#return self.__traits[typ][category][:-1]


	#def modifyTrait( self, typ, category, trait ):
		#"""
		#Ändert eine Eigenschaft im Speicher.
		#"""

		#for item in self.__traits[typ][category]:
			#if trait["name"] == item["name"]:
				#if item["value"] != trait["value"]:
					#item["value"] = trait["value"]
					#self.traitChanged.emit(item)
				## Es fehlen noch "customText" und "Details"
				#break


#QList< cv_Derangement >* StorageCharacter::derangements() const {
	#return &v_derangements;
#}

#QList< cv_Derangement* > StorageCharacter::derangements( cv_AbstractTrait::Category category ) const {
	#QList< cv_Derangement* > list;

	#for ( int i = 0; i < v_derangements.count(); ++i ) {
		#if ( v_derangements.at( i ).category() == category ) {
			#list.append( &v_derangements[i] );
		#}
	#}

	#return list;
#}

#void StorageCharacter::addDerangement( cv_Derangement derang ) {
	#if ( !derang.name().isEmpty() && !v_derangements.contains( derang ) ) {
#// 		qDebug() << Q_FUNC_INFO << derang.name << derang.morality;
		#v_derangements.append( derang );

		#emit derangementsChanged();
	#}
#}

#void StorageCharacter::removeDerangement( cv_Derangement derang ) {
	#if ( v_derangements.contains( derang ) ) {
		#v_derangements.removeAll( derang );
		#emit derangementsChanged();
	#}
#}


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


	def __getArmor(self):
		"""
		Gibt den Wert der getragenen Rüstung aus. Zurückgegeben wird eine Liste mit zwei EInträgen.
		
		Die erste Zahl stellt den Rüstungswert gegen alle Angriffe mit Ausnahme von Schußwaffen und Bögen dar.

		Die zweite Zahl stellt dagegen den Rüstungswert gegen Schußwaffen und Bögen dar.
		"""

		return self.__armor

	def __setArmor( self, armor ):
		"""
		Verändert den Wert der Rüstung.

		Es muß eine Liste mit zwei Elementen übergeben werden.
		
		Bei einer Veränderung wird das Signal armorChanged() ausgesandt.
		"""

		if len(armor) == 2:
			if self.__armor != armor:
				self.__armor = armor
				self.armorChanged.emit( self.__armor )
		else:
			raise ErrListLength(len(self.__armor), len(armor))

	armor = property(__getArmor, __setArmor)


	def resetCharacter(self):
		# Zeitalter festlegen.
		self.era = Config.eras[0]

		## Anfangsdatum setzen.
		self.dateGame = QDate.currentDate()
		self.dateBirth = QDate(self.dateGame.year() - Config.initialAge, self.dateGame.month(), self.dateGame.day())
		self.dateBecoming = QDate(self.dateGame.year() - Config.adultAge, self.dateGame.month(), self.dateGame.day())

		# Löschen aller Identitäten.
		self.__identity.reset()

		# Standardspezies ist der Mensch.
		self.species = Config.initialSpecies

		#Debug.debug(self.__storage.virtues[0])
		#Debug.debug(self.__storage.virtues[0]["name"])
		self.virtue = self.__storage.virtues[0]["name"]
		self.vice = self.__storage.vices[0]["name"]
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
		Diese Funktion überprüft, ob die Voraussetzungen der Eigenscahft "trait" erfüllt sind ode rnicht.
		"""

		if type(trait) != Trait:
			Debug.debug("Error!")
		else:
			if trait.hasPrerequisites:
				traitPrerequisites = trait.prerequisitesText[0]
				for item in Config.typs:
					categories = self.__storage.categories(item)
					for subitem in categories:
						for subsubitem in self.traits[item][subitem].values():
							# Überprüfen ob die Eigenschaft im Anforderungstext des Merits vorkommt.
							if subsubitem.name in traitPrerequisites:
								# Vor dem Fertigkeitsnamen darf kein anderes Wort außer "and", "or" und "(" stehen.
								idxA = traitPrerequisites.index(subsubitem.name)
								strBefore = traitPrerequisites[:idxA]
								strBefore = strBefore.rstrip()
								strBeforeList = strBefore.split(" ")
								if not strBeforeList[-1] or strBeforeList[-1] == u"and" or strBeforeList[-1] == u"or" or strBeforeList[-1] == u"(":
									# Wenn Spezialisierungen vorausgesetzt werden.
									if "." in traitPrerequisites and "{}.".format(subsubitem.name) in traitPrerequisites:
										idx =[0,0]
										idx[0] = traitPrerequisites.index("{}.".format(subsubitem.name))
										idx[1] = traitPrerequisites.index(" ", idx[0])
										specialty = traitPrerequisites[idx[0]:idx[1]].replace("{}.".format(subsubitem.name), "")
										if specialty in subsubitem.specialties:
											traitPrerequisites = traitPrerequisites.replace(".{}".format(specialty), "")
										else:
											traitPrerequisites = traitPrerequisites.replace("{}.{}".format(subsubitem.name, specialty), "0")
									traitPrerequisites = traitPrerequisites.replace(subsubitem.name, unicode(subsubitem.value))
				# Es kann auch die Supereigenschaft als Voraussetzung vorkommen.
				if Config.powerstatIdentifier in traitPrerequisites:
					traitPrerequisites = traitPrerequisites.replace(Config.powerstatIdentifier, unicode(self.__powerstat))

				# Die Voraussetzungen sollten jetzt nurnoch aus Zahlen und logischen Operatoren bestehen.
				try:
					result = eval(traitPrerequisites)
					#print("Eigenschaft {} ({} = {})".format(trait.name, traitPrerequisites, result))
				except (NameError, SyntaxError) as e:
					Debug.debug("Error: {}".format(traitPrerequisites))
					result = False

				trait.setAvailable(result)

