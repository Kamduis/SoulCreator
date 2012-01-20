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
	#
	# {
	# 	Spezies1: {
	# 		Breed: [Name, [Bla, Blub, ...]],
	# 		Faction: [Name, [Bla, Blub, ...]],
	# 		Organisation: [Name [Bla, Blub, ...]],
	# 		Party: [Name [Bla, Blub, ...]],
	# 	},
	# 	...
	# }
	#
	# Am Beispiel der Vampire:
	# {
	# 	Vampire: {
	# 		Breed: [Clan, [Daeva, Gangrel, Mekhet, Nosferatu, Ventrue]],
	# 		Faction: [Covenant, [Cartian Movement, Circle of the Crone, Invictus, Lancea Sancta, Ordo Dracul]],
	# 		Organisation: [Bloodline, [Toreador, Brujah, ...]],
	# 		Party: [Coterie],
	# 	},
	# 	...
	# }
	__speciesGroupNames = {}


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
	# {
	# 	Typ1: {
	# 		Kategorie1: {
	# 			Name1: { "species": Species1, "age": Alter1, ... },
	# 			Name2: { "species": Species2, "age": Alter2, ... },
	# 			...
	# 		},
	# 		Kategorie2: {
	# 			Name1: { "species": Species1, "age": Alter1, ... },
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

#QList< cv_Species > StorageTemplate::v_species;
#QList< cv_SpeciesTitle > StorageTemplate::v_titles;
#QList< Trait* > StorageTemplate::v_traits;
#QList< TraitBonus* > StorageTemplate::v_traitsBonus;
#QList< cv_SuperEffect > StorageTemplate::v_superEffects;


	def __init__(self, parent=None):
		QObject.__init__(self, parent)


	def __getTyps(self):
		return self.__traits.keys()

	typs = property(__getTyps)


	def categories(self, typ):
		return self.__traits[typ].keys()


	def __getSpecies(self):
		return self.__species

	species = property(__getSpecies)


#QStringList StorageTemplate::traitNames( cv_AbstractTrait::Type type, cv_AbstractTrait::Category category, cv_Trait::EraFlag era, cv_Trait::AgeFlag age ) const {
	#QList< Trait* > traits = v_traits;
	#QStringList list;

	#for( int i = 0; i < traits.count(); ++i ) {
		#if( traits.at( i )->type() == type && traits.at( i )->category() == category ) {
			#if( traits.at( i )->era().testFlag( era ) ) {
				#if( traits.at( i )->age().testFlag( age ) ) {
					#// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
					#if( !list.contains( traits.at( i )->name() ) ) {
#// 						qDebug() << Q_FUNC_INFO << "Gib aus" << traits.at( i )->name;
						#list.append( traits.at( i )->name() );
					#}
				#}
			#}
		#}
	#}

	#return list;
#}

#QStringList StorageTemplate::virtueNames( cv_Trait::AgeFlag age ) const {
	#return traitNames( cv_AbstractTrait::Virtue, cv_AbstractTrait::CategoryNo, cv_Trait::EraAll, age );
#}

#QStringList StorageTemplate::viceNames( cv_Trait::AgeFlag age ) const {
	#return traitNames( cv_AbstractTrait::Vice, cv_AbstractTrait::CategoryNo, cv_Trait::EraAll, age );
#}

#QString StorageTemplate::breedTitle( cv_Species::SpeciesFlag spe ) const {
	#for( int i = 0; i < v_titles.count(); ++i ) {
		#if( v_titles.at( i ).species.testFlag( spe ) && v_titles.at( i ).title == cv_SpeciesTitle::Breed ) {
			#return v_titles.at( i ).name;
		#}
	#}

	#return "Breed";
#}
#QString StorageTemplate::factionTitle( cv_Species::SpeciesFlag spe ) const {
	#for( int i = 0; i < v_titles.count(); ++i ) {
		#if( v_titles.at( i ).species.testFlag( spe ) && v_titles.at( i ).title == cv_SpeciesTitle::Faction ) {
			#return v_titles.at( i ).name;
		#}
	#}

	#return "Faction";
#}
#QStringList StorageTemplate::powerHeaders( cv_Species::SpeciesFlag spe ) const {
	#QStringList list;

	#for( int i = 0; i < v_titles.count(); ++i ) {
		#if( v_titles.at( i ).species.testFlag( spe ) && v_titles.at( i ).title == cv_SpeciesTitle::Power ) {
			#list.append( v_titles.at( i ).name );
		#}
	#}

	#return list;
#}


#QStringList StorageTemplate::breedNames( cv_Species::SpeciesFlag spe ) const {
	#QList< Trait* > traits = v_traits;
	#QStringList list;

	#for( int i = 0; i < traits.count(); ++i ) {
		#if( traits.at( i )->type() == cv_AbstractTrait::Breed && traits.at( i )->category() == cv_AbstractTrait::CategoryNo ) {
			#if( traits.at( i )->species() == spe ) {
				#// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
				#if( !list.contains( traits.at( i )->name() ) ) {
					#list.append( traits.at( i )->name() );
				#}
			#}
		#}
	#}

	#return list;
#}
#QStringList StorageTemplate::factionNames( cv_Species::SpeciesFlag spe ) const {
	#QList< Trait* > traits = v_traits;
	#QStringList list;

	#for( int i = 0; i < traits.count(); ++i ) {
		#if( traits.at( i )->type() == cv_AbstractTrait::Faction && traits.at( i )->category() == cv_AbstractTrait::CategoryNo ) {
			#if( traits.at( i )->species() == spe ) {
				#// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
				#if( !list.contains( traits.at( i )->name() ) ) {
					#list.append( traits.at( i )->name() );
				#}
			#}
		#}
	#}

	#return list;
#}



	def __getTraits( self ):
		"""
		Gibt eine Liste aller Eigenschaften zurück.
		"""

		return self.__traits

	def __setTraits(self, traits):
		self.__traits = traits

	traits = property(__getTraits, __setTraits)


	def addTrait( self, typ, category, name, data):
		"""
		Fügt eine Eigenschaft zu der entsprechenden Liste hinzu.

		Ist diese Eigenschaft schon vorhanden, werden die Daten der Eigenschaft um die neuen Daten erweitert. Das gilt ausschließlich für die Spezialisierungen. Die restlichen Daten werden überschrieben.

		Die Eigenschaft sollte im Format eines dict daherkommen.

		\param name Der Name der Eigenschaft
		
		\param data Alle Informationen über die Eigenschaft außer dem Namen.
		"""

		if typ not in self.__traits:
			self.__traits.setdefault(typ,{})

		if category not in self.__traits[typ]:
			self.__traits[typ].setdefault(category,{})

		if name not in self.__traits[typ][category]:
			self.__traits[typ][category].setdefault(name, data)
		else:
			specialties = self.__traits[typ][category][name]["specialty"]
			specialties.extend(data["specialty"])
			self.__traits[typ][category][name] = data
			self.__traits[typ][category][name]["specialty"] = specialties

		## Kontrolle zu Debugzwecken:
		#keys = self.__traits.keys()
		#for key in self.__traits:
			#Debug.debug(key)
			#for keyA in self.__traits[key]:
				#Debug.debug(keyA)
				#Debug.debug(self.__traits[key][keyA])


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


	def powerName(self, species, power):
		return self.__powerNames[species][power]

	def setPowerName(self, species, power, name):
		if species not in self.__powerNames:
			self.__powerNames.setdefault(species,{})

			self.__powerNames[species][power] = name


#// cv_Trait StorageTemplate::trait( cv_AbstractTrait::Type type, cv_AbstractTrait::Category category, QString name ) {
#// 	bool trait_exists = false;
#//
#// 	cv_Trait trait;
#//
#// 	for ( int i = 0; i < v_traits.count(); ++i ) {
#// 		if ( v_traits.at( i ).type() == type && v_traits.at( i ).category() == category && v_traits.at( i ).name() == name ) {
#// 			trait = v_traits.at( i );
#// 			trait_exists = true;
#//
#// 			break;
#// 		}
#// 	}
#//
#// 	if ( !trait_exists ) {
#// // 		qDebug() << Q_FUNC_INFO << "Trait" << type << category << name << "existiert nicht!";
#// // 		throw eTraitNotExisting();
#// 	}
#//
#// 	return trait;
#// }


#QList< TraitBonus* > StorageTemplate::traitsBonus( cv_AbstractTrait::Type type, cv_Species::SpeciesFlag species ) const {
	#QList< TraitBonus* > traitsPtr;

	#for( int i = 0; i < v_traitsBonus.count(); ++i ) {
		#if( v_traitsBonus.at( i )->type() == type && v_traitsBonus.at( i )->species().testFlag( species ) ) {
			#traitsPtr.append( v_traitsBonus[i] );
		#}
	#}

	#// Es wird eine leere Liste ausgegeben, wenn keine entsprechende Einträge gefunden werden.
#// 	if ( traitsPtr.isEmpty() ) {
#// 		throw eTraitNotExisting();
#// 	}

	#return traitsPtr;
#}


#// void StorageTemplate::setTraits( QList< cv_Trait > traits ) {
#// 	v_traits = traits;
#// }

	def appendSpecies( self, species, speciesData ):
		if species and species not in self.__species:
			self.__species.setdefault(species, speciesData )



#void StorageTemplate::appendTrait( cv_Trait trait ) {
	#bool exists = false;

	#// Unterschiedliche Klassen für die einzelnen Eigenschafts-Typen:
	#Trait* lcl_trait;
	#if( trait.type() == cv_AbstractTrait::Attribute ) {
		#lcl_trait = new AttributeTrait( trait );
	#} else if( trait.type() == cv_AbstractTrait::Skill ) {
		#lcl_trait = new SkillTrait( trait );
	#} else {
		#lcl_trait = new Trait( trait );
	#}

	#for( int i = 0; i < v_traits.count(); ++i ) {
		#if( v_traits.at( i )->type() == lcl_trait->type() && v_traits.at( i )->name() == lcl_trait->name() ) {
			#exists = true;
			#break;
		#}
	#}
	#if( !exists ) {
		#v_traits.append( lcl_trait );
	#}
#}


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
		return self.__speciesGroupNames[species]["Breed"][1]


	def breedTitle(self, species):
		return self.__speciesGroupNames[species]["Breed"][0]


	def factions(self, species):
		return self.__speciesGroupNames[species]["Faction"][1]


	def factionTitle(self, species):
		return self.__speciesGroupNames[species]["Faction"][0]


	def organisations(self, species):
		return self.__speciesGroupNames[species]["Organisation"][1]


	def organisationTitle(self, species):
		return self.__speciesGroupNames[species]["Organisation"][0]


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


#void StorageTemplate::appendTraitBonus( Trait* tr1, QString breed ) {
	#TraitBonus* lcl_traitBonus = new TraitBonus( tr1, breed );

	#qDebug() << Q_FUNC_INFO << "Füge Bonuseigenschaft" << tr1->name() << "hinzu, die von" << breed << "abhängt.";

	#v_traitsBonus.append( lcl_traitBonus );
#}


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


	def appendBonusTrait( self, species, breed, traitData ):
		"""
		Manche Bruten erhlaten Bonuseigenschaften. Diese werden hier hinzugefügt.
		"""

		if species not in self.__bonusTraits:
			self.__bonusTraits.setdefault(species,{})

		if breed not in self.__bonusTraits[species]:
			self.__bonusTraits[species].setdefault(breed,[])

		self.__bonusTraits[species][breed].append(traitData)

		#print(self.__bonusTraits)


	def appendTitle( self, species, typ, group,  names=None):
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
			self.__speciesGroupNames[species][typ].append([])
		#else:
			#Debug.debug("Gruppe schon vorhanden.")

		if names != None:
			if type(names) == list:
				self.__speciesGroupNames[species][typ].append(names)
			else:
				self.__speciesGroupNames[species][typ][1].append(names)

		#Debug.debug(self.__speciesGroupNames)


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

