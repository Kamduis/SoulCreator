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

from PySide.QtCore import QObject

#from src.Config import Config
from src.Tools import ListTools
from src.Debug import Debug
from src.Error import ErrTraitType




class StorageTemplate(QObject):
	"""
	@brief In dieser Klasse werden sämtliche Daten für das Programm gespeichert.

	Diese Klasse verwaltet die im Programm geladenen Daten. Zum einen gibt es eine Liste, in welcher sämtliche \emph{möglichen} Eigenschaften für die Charaktere gespeichert sind, jene welche nach Programmstart aus den Template-Dateien ausgelesen werden und zum anderen gibt es eine Liste für den aktuell angezeigten Charakter.

	Außerdem bietet diese Klasse angenehme Zugriffsfunktionen aus den Informationen, welche zum Programmstart aus den Template-Dateien geladen werden.
	"""

	# Eine Liste der Erschaffungspunkte. Jeder Listeneintrag steht für eine andere Spezies.
	# {
	# 	Spezies1: {
	# 		Typ1: [Primär, Sekundär, Tertiär],
	# 		Typ2: [Primär, Sekundär, Tertiär],
	# 		...
	# 	},
	# 	...
	# }
	__creationPointsList = {}

	# Eine Liste sämtlicher verfügbaren Spezies.
	# {
	# 	"Name1": { "morale": Moral1, "powerstat": Powerstat1, "fuel": Energie1 },
	# 	"Name2": { "morale": Moral2, "powerstat": Powerstat2, "fuel": Energie2 },
	# 	...
	# }
	__species = {}

	# Eine Liste sämtlicher verfügbaren Gruppierungsnamen der einzelnen Spezies.
	# Changelings haben für jede Brut noch eine Subliste: die Kiths.
	#
	# {
	# 	Spezies1: {
	# 		Breed: [
	# 			Name, {
	# 				Bla: {
	# 					"weakness": text,
	# 					"blessing": text,
	# 				},
	# 				Blub: {
	# 					"weakness": text,
	# 					"blessing": text,
	# 				}
	# 				...
	# 			}
	# 		],
	# 		Faction: [Name, {Bla: {}, Blub: {}, ...}],
	# 		Organisation: [Name, {Bla: {}, Blub: {}, ...}],
	# 		Party: [Name, {Bla: {}, Blub: {}, ...}],
	# 	},
	# 	...
	# }
	#
	# Am Beispiel der Vampire:
	# {
	# 	Vampire: {
	# 		Breed: [
	# 			Clan, {
	# 				"Daeva": {
	# 					"weakness": blablubb,
	# 				}
	# 				"Gangrel": {
	# 					"weakness": blablubb,
	# 				},
	# 				...
	# 			}
	# 		],
	# 		Faction: [Covenant, [Cartian Movement, Circle of the Crone, Invictus, Lancea Sancta, Ordo Dracul]],
	# 		Organisation: [Bloodline, [Toreador, Brujah, ...]],
	# 		Party: [Coterie],
	# 	},
	# 	...
	# }
	__speciesGroupNames = {}

	# Changelings haben für jede Brut noch eine Subliste: die Kiths.
	#
	# {
	# 	Brut1: {
	# 		Kith1: {
	# 			"ability": blablubb,
	# 		},
	# 		Kith2: {
	# 			"ability": blablubb,
	# 		},
	# 		...
	# 	},
	# 	...
	# }
	__kiths = {}


	# Die Bezeichner der Kräfte.
	#
	# {
	# 	species1: {
	# 		"power": powerName,		## bspw. Disciplines oder Renown
	# 		"spell": spellName,		## bspw. Gifts oder Goblin Contracts
	# 		"ritual": powerName,	## bspw. Rituals oder Pledges
	# 	}
	# 	species2: {
	# 		"power": powerName,		## bspw. Disciplines oder Renown
	# 		"spell": spellName,		## bspw. Gifts oder Goblin Contracts
	# 		"ritual": powerName,	## bspw. Rituals oder Pledges
	# 	}
	# }
	__powerNames = {}


	# Eine Liste sämtlicher verfügbaren Eigenschaften.
	#
	# Eigenschaften haben folgende Parameter:
	#
	# "name" 			Name der Eigenschaft (alle)
	# "level"			Stufe der Eigenschaft (Subpowers)
	# "values"			Erlaubte Werte, welche diese Eigenschaft annehmen kann. (Merits)
	# "species"			Die Spezies, für welche diese Eigenschaft zur Verfügung steht.
	# "age"				Die Alterskategorie, für welche diese Eigenschaft zur Verfügung steht.
	# "era"				Eine Liste der Zeitalter, für welche diese Eigenschaft zur Verfügung steht.
	# "custom"			Handelt es sich um eine Kraft mit Zusatztext?
	# "specialties"		Dieser Eigenschaft zugeteilten Spezialisierungen (Skills)
	# "prerequisites"	Voraussetzungen für diese Eigenschaft (Merits, Subpowers)
	#
	# {
	# 	Typ1: {
	# 		Kategorie1: {
	# 			Identifier1: { "name": Name1, "species": Species1, "age": Alter1, ... },
	# 			Identifier2: { "name": Name2, "species": Species2, "age": Alter2, ... },
	# 			...
	# 		},
	# 		Kategorie2: {
	# 			Identifier1: { "name": Name1, "species": Species1, "age": Alter1, ... },
	# 			...
	# 		},
	# 		...
	# 	},
	# 	...
	# }
	__traits = {}

	## Eine Liste aller Tugenden.
	#
	# [
	# 	{"name": Name1, "age": Alter1}
	# 	{"name": Name2, "age": Alter2}
	# 	...
	# ]
	__virtues = []

	## Eine Liste aller Laster.
	#
	# [
	# 	{"name": Name1, "age": Alter1}
	# 	{"name": Name2, "age": Alter2}
	# 	...
	# ]
	__vices = []

	## Eine Liste aller Geistesstörungen.
	#
	# {
	# 	"Name1": {
	# 		"Dependancy": [ severe1, severe2, ... ],
	# 		"Description": Description,
	# 		"Severe": True | False,
	# 		"Species": species1
	# 	},
	# 	"Name2": {
	# 		"Dependancy": [ severe1, severe2, ... ],
	# 		"Description": Description,
	# 		"Severe": True | False,
	# 		"Species": species1
	# 	}
	# 	...
	# }
	__derangements = {}

	# Eine Liste der Effekte der Supereigenschaft.
	#
	# {
	# 	Spezies1: {
	# 		1: { "fuelMax": maximale Energie, "fuelPerTurn": Energie pro Runde, "traitMax": maximale Eigenschaftswerte },
	# 		2: { "fuelMax": maximale Energie, "fuelPerTurn": Energie pro Runde, "traitMax": maximale Eigenschaftswerte },
	# 		...
	# 	},
	# 	Spezies2: {
	# 		1: { "fuelMax": maximale Energie, "fuelPerTurn": Energie pro Runde, "traitMax": maximale Eigenschaftswerte },
	# 		1: { "fuelMax": maximale Energie, "fuelPerTurn": Energie pro Runde, "traitMax": maximale Eigenschaftswerte },
	# 		...
	# 	},
	# 	...
	# }
	__powerstat = {}

	# Eine Liste der Bonuseigenschaften je nach Spezies, Brut und Fraktion etc.
	#
	# {
	# 	Spezies1: {
	# 		"Breed": [
	# 			{"name": Bla, "typ": Blub},
	# 			{"name": Bla, "typ": Blub},
	# 			...
	# 		],
	# 		...
	# 	},
	# 	Spezies2: {
	# 		"Breed": [
	# 			{"name": Bla, "typ": Blub},
	# 			...
	# 		],
	# 		...
	# 	},
	# 	...
	# }
	__bonusTraits = {}

	# Eine Liste der Waffen.
	#
	# {
	# 	"melee": {
	# 		weapon1: {
	# 			"damage": value,
	# 			"size": value,
	# 			"durability": value,
	# 		},
	# 		...
	# 	},
	# 	"thrown": {
	# 		weapon1: {
	# 			"damage": value,
	# 			"size": value,
	# 			"durability": value,
	# 		},
	# 		...
	# 	"ranged": {
	# 		weapon1: {
	# 			"damage": value,
	# 			"ranges": value,
	# 			"capacity": value,
	# 			"strength": value,
	# 			"size": value,
	# 			"durability": value,
	# 		},
	# 		...
	# 	},
	# }
	__weapons = {}

	# Eine Liste der Rüstungen.
	#
	# {
	# 	armor1: {
	# 		"general": value,
	# 		"firearms": value,
	# 		"defense": value,
	# 		"speed": value
	# 	},
	# 	...
	# }
	__armor = {}

	# Eine Liste vorgeschlagenen Equipments
	#
	# {
	# 	equipment1: {
	# 		"durability": value,
	# 		"size": value,
	# 		"cost": value
	# 	},
	# 	...
	# }
	__equipment = {}

	spiritNumina = (
		"Abduct (R)",
		"Ban of Power",
		"Blast",
		"Camouflage",
		"Chain of Death",
		"Chorus",
		"Claim (R)",
		"Clasp",
		"Commune",
		"Concealment",
		"Corpse Ride",
		"Damnation's Path",
		"Dement (R)",
		"Desiccation",
		"Discorporation",
		"Drain",
		"Elemental Immunity",
		"Emotional Aura (R)",
		"Ensnare",
		"Fearstruck",
		"Fetter",
		"Final Strike",
		"Firestarter",
		"Freeze (R)",
		"Gauntlet Breach",
		"Ghost Eater",
		"Greater Influence",
		"Hallucinations",
		"Harrow",
		"Heal",
		"Hibernate",
		"Howl",
		"Innocuous",
		"Left-Handed Spanner",
		"Living Fetter",
		"Manipulate Element",
		"Materialize",
		"Material Vision",
		"echanical Possession",
		"Morphic Form",
		"Mortal Mask",
		"Omen Trance",
		"Pathfinder",
		"Plague of the Dead",
		"Possession (R)",
		"Rapture (R)",
		"Reaching",
		"Rebirth",
		"Regenerate",
		"Revelation",
		"Savant",
		"Seek",
		"Sleep Eater",
		"Soul Harvest",
		"Soul Snatch",
		"Speed",
		"Spirit Minions",
		"Spirit Venom",
		"Spiritual Vision",
		"Stalwart",
		"Swarm Form",
		"Telekinesis (R)",
		"Telepathy",
		"Thieve",
		"Threshold",
		"Transmogrify Victim",
		"Unfetter",
		"Wilds Sense",
		"Abduct",
	)



	def __init__(self, parent=None):
		QObject.__init__(self, parent)


	def __getTyps(self):
		return self.__traits.keys()

	typs = property(__getTyps)


	def categories(self, typ):
		listOfCategories = self.__traits[typ].keys()
		listOfCategories.sort()
		return listOfCategories


	def __getSpecies(self):
		return self.__species

	species = property(__getSpecies)


	def __getTraits( self ):
		"""
		Gibt eine Liste aller Eigenschaften zurück.
		"""

		return self.__traits

	def __setTraits(self, traits):
		self.__traits = traits

	traits = property(__getTraits, __setTraits)

	def traitSkills(self):
		result = {}
		for category in self.__traits["Skill"]:
			result.update(self.__traits["Skill"][category])

		return result


	def addTrait( self, typ, category, identifier, data):
		"""
		Fügt eine Eigenschaft zu der entsprechenden Liste hinzu.

		Ist diese Eigenschaft schon vorhanden, werden die Daten der Eigenschaft um die neuen Daten erweitert. Das gilt ausschließlich für die Spezialisierungen. Die restlichen Daten werden überschrieben.

		Die Eigenschaft sollte im Format eines dict daherkommen.

		Eigenschaften des Typs "Subpower" haben abweichende Attribute und werden deswegen gesondert behandelt.

		\param identifier Die einzigartige Identität der Eigenschaft, meist identisch mit ihrem Namen.
		
		\param data Alle Informationen über die Eigenschaft außer der Identität.
		"""

		if typ not in self.__traits:
			self.__traits.setdefault(typ,{})

		if category not in self.__traits[typ]:
			self.__traits[typ].setdefault(category,{})

		if identifier not in self.__traits[typ][category]:
			self.__traits[typ][category][identifier] = data
		elif (typ != "Subpower"):
			#Debug.debug(data["name"])
			specialties = self.__traits[typ][category][identifier]["specialty"]
			specialties.extend(data["specialty"])
			specialties.sort()
			self.__traits[typ][category][identifier] = data
			self.__traits[typ][category][identifier]["specialty"] = specialties


	def traitNames( self, typ, category, era=None, age=None ):
		"""
		Gibt eine Liste aller Eigenschaftsnamen zurück, die den übergebenen Parametern entsprechen.

		\note Wenn es keine Eigenschaft mit den übergebenen Parametern gibt, wird eine leere Liste übergeben.
		"""

		resultA = self.traits(typ, category, era, age)
		result = []
		for item in resultA:
			result.append(item["name"])

		return result


	def powerName(self, species):
		return self.__powerNames[species]["Power"]

	def setPowerName(self, species, name):
		if species not in self.__powerNames:
			self.__powerNames.setdefault(species,{})

		self.__powerNames[species]["Power"] = name


	def subPowerName(self, species):
		return self.__powerNames[species]["Subpower"]

	def setSubPowerName(self, species, name):
		if species not in self.__powerNames:
			self.__powerNames.setdefault(species,{})

		self.__powerNames[species]["Subpower"] = name


	def appendSpecies( self, species, speciesData ):
		if species and species not in self.__species:
			self.__species.setdefault(species, speciesData )


	def __getVirtues(self):
		return self.__virtues

	def __setVirtues(self, virtues):
		self.__virtues = virtues

	virtues = property(__getVirtues, __setVirtues)


	def __getVices(self):
		return self.__vices

	def __setVices(self, vices):
		self.__vices = vices

	vices = property(__getVices, __setVices)


	def derangementList( self, species, parentDerangement=None ):
		result = []
		if parentDerangement == None:
			for item in self.__derangements:
				#Debug.debug(self.__derangements[item])
				if (not self.__derangements[item]["Species"] or self.__derangements[item]["Species"] == species) and not self.__derangements[item]["Severe"]:
					result.append(item)
			result.sort()
			#Debug.debug(result)
			return result
		else:
			if parentDerangement in self.__derangements:
				result = self.__derangements[parentDerangement]["Dependancy"]
			result.sort()
			#Debug.debug(result)
			return result


	def derangementDescription( self, name ):
		"""
		Gibt die Beschreibung der benannten Geistesstörung aus.
		"""

		return self.__derangements[name]["Description"]


	def breeds(self, species):
		result = self.__speciesGroupNames[species]["Breed"][1].keys()
		result.sort()
		return result


	def breedTitle(self, species):
		return self.__speciesGroupNames[species]["Breed"][0]


	def breedBlessing(self, species, breed):
		return self.__speciesGroupNames[species]["Breed"][1][breed]["blessing"]


	def breedCurse(self, species, breed):
		return self.__speciesGroupNames[species]["Breed"][1][breed]["weakness"]


	def kiths(self, seeming):
		"""
		Gibt eine Liste aller möglichen Kiths für das angegebene Seeming zurück.

		\note Nur für Changelings von Bedeutung.
		"""

		result = self.__kiths[seeming].keys()
		result.sort()
		return result


	def kithAbility(self, seeming, kith):
		"""
		Kibt die Kith Ability des speziellen Kiths zurück.

		\note Nur für Changelings von Bedeutung.
		"""

		return self.__kiths[seeming][kith]["ability"]


	def addKith(self, seeming, kith, kithAbility=None):
		"""
		Fügt dem Seeming seeming ein zusätlzichen Kith hinzu.

		\param kith Kann entweder ein String oder eine Liste von Strings sein.
		"""

		if seeming not in self.__kiths:
			self.__kiths.setdefault(seeming, {})

		if kithAbility:
			self.__kiths[seeming][kith] = { "ability": kithAbility, }
		else:
			self.__kiths[seeming][kith] = {}

		#Debug.debug(self.__kiths)


	def factions(self, species):
		result = self.__speciesGroupNames[species]["Faction"][1].keys()
		result.sort()
		return result


	def factionTitle(self, species):
		return self.__speciesGroupNames[species]["Faction"][0]


	def organisations(self, species):
		result = self.__speciesGroupNames[species]["Organisation"][1].keys()
		result.sort()
		return result


	def organisationTitle(self, species):
		return self.__speciesGroupNames[species]["Organisation"][0]


	def organisationCurse(self, species, organisation):
		if organisation in self.__speciesGroupNames[species]["Organisation"][1] and "weakness" in self.__speciesGroupNames[species]["Organisation"][1][organisation]:
			return self.__speciesGroupNames[species]["Organisation"][1][organisation]["weakness"]
		else:
			return ""


	def partyTitle(self, species):
		return self.__speciesGroupNames[species]["Party"][0]


	def moralityName(self, species):
		return self.__species[species]["morale"]


	def powerstatName(self, species):
		return self.__species[species]["powerstat"]


	def fuelName(self, species):
		return self.__species[species]["fuel"]


	def fuelMax(self, species, powerstat):
		if powerstat > 0:
			#Debug.debug("{} -> {}".format(powerstat, self.__powerstat[species][powerstat]))
			return self.__powerstat[species][powerstat]["fuelMax"]
		else:
			return 0


	def fuelPerTurn(self, species, powerstat):
		if powerstat > 0:
			return self.__powerstat[species][powerstat]["fuelPerTurn"]
		else:
			return 0


	def maxTrait(self, species, powerstat):
		if powerstat > 0:
			return self.__powerstat[species][powerstat]["traitMax"]
		else:
			return 5


	def appendCharacteristic( self, typ, trait ):
		"""
		Fügt eine Charakteristik (Tugend oder Laster) zu der entsprechenden Liste hinzu.
		"""

		if (typ == "Virtue"):
			self.__virtues.append( trait )
		elif (typ == "Vice"):
			self.__vices.append( trait )
		else:
			raise ErrTraitType( ("Virtue", "Vice"), typ )


	def appendDerangement( self, species, name, dependancy, description, isSevere=False ):
		"""
		Fügt eine Geistesstörung mitsamt der Liste daraus möglicherweise erwachsender schwerer Geistesstörungen an die Liste der Geistesstörungen an.

		Eine milde Geistesstörung hat als Abhängigkeit eine beliebig lange Liste von schweren Geistesstörungen. Eine schwere Geistesstörung (isSevere=True) hat als Abhängigkeit eine leere Liste.
		"""

		if name not in self.__derangements:
			self.__derangements.setdefault(name, {})
			self.__derangements[name]["Dependancy"] = dependancy
			self.__derangements[name]["Description"] = description
			self.__derangements[name]["Severe"] = isSevere
			self.__derangements[name]["Species"] = species
		else:
			self.__derangements[name]["Dependancy"].extend(dependancy)
			if description:
				self.__derangements[name]["Description"] = description

		#Debug.debug(self.__derangements)


	def appendTrait( self, typ, category, name, data):
		"""
		Fügt eine Eigenschaft zu der entsprechenden Liste hinzu.

		Die Eigenschaft sollte im Format eines dict daherkommen.
		"""

		if typ not in self.__traits:
			self.__traits.setdefault(typ,{})

		if category not in self.__traits[typ]:
			self.__traits[typ].setdefault(category,{})

		if name not in self.__traits[typ][category]:
			self.__traits[typ][category].setdefault(name, data)

		## Kontrolle zu Debugzwecken:
		#keys = self.__traits.keys()
		#for key in self.__traits:
			#Debug.debug(key)
			#for keyA in self.__traits[key]:
				#Debug.debug(keyA)
				#Debug.debug(self.__traits[key][keyA])


	def appendPowerstat( self, species, value, effects ):
		"""
		Fügt die Effekte eines neuen Wertes der Supereigenschaft einer bestimmten Spezies der entsprechenden Liste hinzu.

		Die Effekte kommen als dict daher.
		"""

		if species not in self.__powerstat:
			self.__powerstat.setdefault(species,{})

		## \warnung, hier kann es vorkommen, daß ein Wert nicht geschrieben wird, wenn ein powerstat-Wert mehrfach in der xml-Datei vorkommt.
		if value not in self.__powerstat:
			self.__powerstat[species].setdefault(value,effects)

		#Debug.debug(self.__powerstat)


	def appendTitle( self, species, typ, group, names=None, infos=None):
		"""
		Fügt die Gruppierungsnamen der entsprechenden Spezies hinzu.
		"""

		if species not in self.__speciesGroupNames:
			self.__speciesGroupNames.setdefault(species,{})
		#else:
			#Debug.debug("Spezies schon vorhanden.")

		if typ not in self.__speciesGroupNames[species]:
			self.__speciesGroupNames[species].setdefault(typ,[])
		#else:
			#Debug.debug("Typ schon vorhanden")

		if group not in self.__speciesGroupNames[species][typ]:
			self.__speciesGroupNames[species][typ].append(group)
			self.__speciesGroupNames[species][typ].append({})
		#else:
			#Debug.debug("Gruppe schon vorhanden.")

		if names != None:
			if type(names) == list:
				for name in names:
					if infos:
						self.__speciesGroupNames[species][typ].setdefault(name, infos)
					else:
						self.__speciesGroupNames[species][typ].setdefault(name, {})
			else:
				if infos:
					self.__speciesGroupNames[species][typ][1].setdefault(names, infos)
				else:
					self.__speciesGroupNames[species][typ][1].setdefault(names, {})

		#Debug.debug(self.__speciesGroupNames)


	def bonusTraits(self, species, breed):
		if species in self.__bonusTraits and breed in self.__bonusTraits[species]:
			return self.__bonusTraits[species][breed]
		else:
			return []


	def appendBonusTrait( self, species, breed, traitData ):
		"""
		Manche Bruten erhlaten Bonuseigenschaften. Diese werden hier hinzugefügt.
		"""

		if species not in self.__bonusTraits:
			self.__bonusTraits.setdefault(species,{})

		if breed not in self.__bonusTraits[species]:
			self.__bonusTraits[species].setdefault(breed,[])

		self.__bonusTraits[species][breed].append(traitData)

		#Debug.debug(self.__bonusTraits)


	@property
	def creationPoints(self):
		return self.__creationPointsList


	def appendCreationPoints( self, species, typ, points ):
		"""
		Fügt einen neuen Satz Erschaffungspunkte zu der entsprechende Liste hinzu.

		\sa __creationPointsList

		Da ein dictionary immer nur einen Schlüssel identischen Namens haben kann, sollte automatisch ein Fehler ausgelöst werden, wenn eine Spezies zweimal drankommt.
		"""

		points.sort()

		if species not in self.__creationPointsList:
			self.__creationPointsList.setdefault(species,{})

		self.__creationPointsList[species][typ] = points


	@property
	def weapons(self):
		"""
		Gibt eine Liste aller Waffen besagter Kategorie zurück.
		"""

		return self.__weapons


	def addWeapon( self, category, name, weaponData ):
		"""
		Fügt eine Waffe hinzu. Falls eine Waffe dieses Namens in der angebenen Kategorie (melee, thrown, ranged) schon vorhanden ist, werden die Daten der vorhandenen Waffe überschrieben.
		"""

		if category not in self.__weapons:
			self.__weapons.setdefault(category, {})

		self.__weapons[category][name] = weaponData

		#Debug.debug(self.__weapons)


	@property
	def armor(self):
		"""
		Gibt eine Liste aller Rüstungen zurück.
		"""

		return self.__armor


	def addArmor( self, name, armorData ):
		"""
		Fügt eine Rüstung hinzu. Falls eine Rüstung dieses Namens schon vorhanden ist, werden die Daten der vorhandenen Rüstung überschrieben.
		"""

		self.__armor[name] = armorData

		#Debug.debug(self.__armor)


	@property
	def equipment(self):
		"""
		Vorgeschlagene Ausrüstung.
		"""

		return self.__equipment


	def addEquipment( self, name, data ):
		"""
		Fügt einen Ausrüstungsgegenstand hinzu. Falls ein Gegenstand dieses Namens schon vorhanden ist, werden die Daten überschrieben.
		"""

		self.__equipment[name] = data

		#Debug.debug(self.__equipment)

