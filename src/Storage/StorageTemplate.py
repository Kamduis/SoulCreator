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

from PySide.QtCore import QObject

#from src.Config import Config
#from ReadXml import ReadXml
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
	# [
	# 	[Name, Moral, Supertrait, Energie],
	# 	...
	# ]
	__species = []

	# Eine Liste sämtlicher verfügbaren Gruppierungsnamen der einzelnen Spezies.
	#
	# {
	# 	Spezies1: {
	# 		Breed: [Name, [Bla, Blub, ...]],
	# 		Faction: [Name, [Bla, Blub, ...]],
	# 		SubGroup: [Name [Bla, Blub, ...]],
	# 		...
	# 	},
	# 	...
	# }
	#
	# Am Beispiel der Vampire:
	# {
	# 	Vampire: {
	# 		Breed: [Clan, [Daeva, Gangrel, Mekhet, Nosferatu, Ventrue]],
	# 		Faction: [Covenant, [Cartian Movement, Circle of the Crone, Invictus, Lancea Sancta, Ordo Dracul]],
	# 		SubGroup: [Bloodline, [Toreador, Brujah, ...]],
	# 		...
	# 	},
	# 	...
	# }
	__speciesGroupNames = {}

	# Eine Liste sämtlicher verfügbaren Eigenschaften.
	#
	# {
	# 	Typ1: {
	# 		Kategorie1: [
	# 			{ "name": Name1, "species": Species1, "age": Alter1, ... },
	# 			{ "name": Name2, "species": Species2, "age": Alter2, ... },
	# 			...
	# 		],
	# 		Kategorie2: [
	# 			{ "name": Name1, "species": Species1, "age": Alter1, ... },
	# 			...
	# 		],
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

	# Eine Liste der Effekte der Supereigenschaft.
	#
	# {
	# 	Spezies1: [
	# 		{ "value": Wert1, "fuelMax": maximale Energie, "fuelPerTurn": Energie pro Runde, "traitMax": maximale Eigenschaftswerte },
	# 		{ "value": Wert2, "fuelMax": maximale Energie, "fuelPerTurn": Energie pro Runde, "traitMax": maximale Eigenschaftswerte },
	# 		...
	# 	],
	# 	Spezies2: [
	# 		{ "value": Wert1, "fuelMax": maximale Energie, "fuelPerTurn": Energie pro Runde, "traitMax": maximale Eigenschaftswerte },
	# 		{ "value": Wert2, "fuelMax": maximale Energie, "fuelPerTurn": Energie pro Runde, "traitMax": maximale Eigenschaftswerte },
	# 		...
	# 	],
	# 	...
	# }
	__superEffect = {}

	# Eine Liste der Bonuseigenscahften je nach Spezies, Brut und Fraktion etc.
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



	def __getTraits( self, typ=None, category=None, era=None, age=None ):
		"""
		Gibt eine Liste aller Eigenschaften zurück, die den übergebenen Parametern entsprechen.
		
		\note Wenn es keine Eigenschaft mit den übergebenen Parametern gibt, wird eine leere Liste übergeben.

		\note Ohne Argumente, werden alle Eigenscahften zurückgegeben.

		\note Nur mit typ, werden alle Eigenschaften dieses typs zurückgegeben etc.
		"""

		result = []
		if typ == None:
			result = self.__traits
		elif category == None:
			result = self.__traits[typ]
		else:
			result = self.__traits[typ][category]

		## \todo era und age haben noch keinerlei Wirkung

		return result

	def __setTraits(self, traits):
		self.__traits = traits

	traits = property(__getTraits, __setTraits)


#QList< Trait* > StorageTemplate::traits( cv_AbstractTrait::Type type, cv_Species::SpeciesFlag species ) const {
	#QList< Trait* > traitsPtr;

#// 	qDebug() << Q_FUNC_INFO << "Wird aufgerufen!";

	#for( int i = 0; i < v_traits.count(); ++i ) {
		#if( v_traits.at( i )->type() == type && v_traits.at( i )->species().testFlag( species ) ) {
			#traitsPtr.append( v_traits[i] );
#// 			qDebug() << Q_FUNC_INFO << "Füge hinzu:" << v_traits.at(i)->name();
		#}
	#}

	#if( traitsPtr.isEmpty() ) {
#// 		qDebug() << Q_FUNC_INFO << "Trait Typ" << cv_AbstractTrait::toString( type ) << "mit Kategorie" << cv_AbstractTrait::toString( category ) << "existiert nicht!";
		#throw eTraitNotExisting();
	#}

	#return traitsPtr;
#}


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

	def appendSpecies( self, species ):
		self.__species.append( species )



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


#void StorageTemplate::appendTraitBonus( Trait* tr1, QString breed ) {
	#TraitBonus* lcl_traitBonus = new TraitBonus( tr1, breed );

	#qDebug() << Q_FUNC_INFO << "Füge Bonuseigenschaft" << tr1->name() << "hinzu, die von" << breed << "abhängt.";

	#v_traitsBonus.append( lcl_traitBonus );
#}


#int StorageTemplate::traitMax( cv_Species::Species species, int value ) {
	#if( species == cv_Species::Human ) {
		#return Config::traitMax;
	#} else {
		#for( int i = 0; i < v_superEffects.count(); ++i ) {
			#if( v_superEffects.at( i ).species == species && v_superEffects.at( i ).value == value ) {
				#return v_superEffects.at( i ).traitMax;
			#}
		#}
	#}
#}

#int StorageTemplate::fuelMax( cv_Species::Species species, int value ) {
	#if( species == cv_Species::Human ) {
		#return 0;
	#} else {
		#for( int i = 0; i < v_superEffects.count(); ++i ) {
			#if( v_superEffects.at( i ).species == species && v_superEffects.at( i ).value == value ) {
				#return v_superEffects.at( i ).fuelMax;
			#}
		#}
	#}
#}

#int StorageTemplate::fuelPerTurn( cv_Species::Species species, int value ) {
	#if( species == cv_Species::Human ) {
		#return 0;
	#} else {
		#for( int i = 0; i < v_superEffects.count(); ++i ) {
			#if( v_superEffects.at( i ).species == species && v_superEffects.at( i ).value == value ) {
				#return v_superEffects.at( i ).fuelPerTurn;
			#}
		#}
	#}
#}


#cv_CreationPointsList* StorageTemplate::creationPoints() {
	#return &v_creationPointsList;
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


	def appendTrait( self, typ, category, traits):
		"""
		Fügt eine Eigenschaft zu der entsprechenden Liste hinzu.

		Die Eigenschaft sollte im Format eines dict daherkommen.
		"""
		
		if typ not in self.__traits:
			self.__traits.setdefault(typ,{})

		if category not in self.__traits[typ]:
			self.__traits[typ].setdefault(category,[])

		self.__traits[typ][category].append(traits)

		## Kontrolle zu Debugzwecken:
		#keys = self.__traits.keys()
		#for key in self.__traits:
			#print(key)
			#for keyA in self.__traits[key]:
				#print(keyA)
				#print(self.__traits[key][keyA])


	def appendSuperEffect( self, species, effects ):
		"""
		Fügt die Effekte eines neuen Wertes der Supereigenschaft einer bestimmten Spezies der entsprechenden Liste hinzu.

		Die Effekte kommen als dict daher.
		"""

		if species not in self.__superEffect:
			self.__superEffect.setdefault(species,[])

		self.__superEffect[species].append(effects)

		#print(self.__superEffect)


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

		#print(self.__speciesGroupNames)


	def appendCreationPoints( self, species, typ, points ):
		"""
		Fügt einen neuen Satz Erschaffungspunkte zu der entsprechende Liste hinzu.

		\sa __creationPointsList

		Da ein dictionary immer nur einen Schlüssel identischen Namens haben kann, sollte automatisch ein Fehler ausgelöst werden, wenn eine Spezies zweimal drankommt.
		"""
		
		self.__creationPointsList.setdefault(species,{})
		self.__creationPointsList[species].setdefault(typ,[])
		self.__creationPointsList[species][typ].append(points)
