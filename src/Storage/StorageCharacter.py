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

from PySide.QtCore import QObject, Signal

#from src.Storage.StorageTemplate import StorageTemplate
from src.Datatypes.Identity import Identity
from src.Error import ErrListLength
from src.Debug import Debug




class StorageCharacter(QObject):
	"""
	@brief In dieser Klasse werden sämtliche Daten des gerade geöffneten Charakters gespeichert.

	Wird ein Wert durch das Programm geändert, muß der Wert tatsächlich in dieser Klasse verändert werden. Denn der Inhalt dieser Klasse wird beim Speichern in eine Datei geschrieben und beim Laden wird diese Klasse aufgefüllt. Die Anzeige nimmt all ihre Daten aus dieser Klasse.

	Außerdem bietet diese Klasse angenehme Zugriffsfunktionen aus den Informationen, welche zum Programmstart aus den Template-Dateien geladen werden.

	\note Bei dieser Klasse handelt es sich um eine Singleton-Klasse. Es kann stets nur eine Instanz dieser Klasse existieren. Einen zeiger auf diese instanz erzeugt man mittels folgendem Code:
	\code
	StorageCharacter* character = StorageCharacter::getInstance();
	\endcode
	"""


	speciesChanged = Signal(str)
	traitChanged = Signal(object)
	virtueChanged = Signal(str)
	viceChanged = Signal(str)
	breedChanged = Signal(str)
	factionChanged = Signal(str)
	superTraitChanged = Signal(int)
	moralityChanged = Signal(int)
	armorChanged = Signal(object)


	# Eine Liste sämtlicher verfügbaren Eigenschaften.
	#
	# {
	# 	Typ1: {
	# 		Kategorie1: [
	# 			{ "name": Name1, "value": Wert1 },
	# 			{ "name": Name1, "value": Wert2 },
	# 			...
	# 		],
	# 		Kategorie2: [
	# 			{ "name": Name1, "value": Wert1 },
	# 			...
	# 		],
	# 		...
	# 	},
	# 	...
	# }
	__traits = {}


	def __new__(type, *args):
		# Falls es noch keine Instanz dieser Klasse gibt, wird eine erstellt und in _the_instance abgelegt.
		# Diese wird dann jedesmal zurückgegeben.
		if not '_the_instance' in type.__dict__:
			type._the_instance = QObject.__new__(type)
		return type._the_instance

	def __init__(self, parent=None):
		if not '_ready' in dir(self):
			# Der Konstruktor wird bei jeder Instanziierung aufgerufen.
			# Einmalige Dinge wie zum Beispiel die Initialisierung von Klassenvariablen müssen also in diesen Block.
			self._ready = True

			QObject.__init__(self, parent)

			#self.__storage = StorageTemplate( self )
			
			self.__modified = False
			self.__species = ""
			self.__virtue = ""
			self.__vice = ""
			self.__breed = ""
			self.__faction = ""
			self.__superTrait = 0
			self.__morality = 0
			self.__armor = [0, 0]

			self.__identity = Identity()
			self.__identities = [self.__identity]

			self.__derangements = []

			# Sobald irgendein Aspekt des Charakters verändert wird, muß festgelegt werden, daß sich der Charkater seit dem letzten Speichern verändert hat.
			# Es ist Aufgabe der Speicher-Funktion, dafür zu sorgen, daß beim Speichern diese Inforamtion wieder zurückgesetzt wird.
			self.__identity.identityChanged.connect(self.setModified)
	#connect( self, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( traitChanged( cv_Trait* ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( derangementsChanged() ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( virtueChanged( QString ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( viceChanged( QString ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( breedChanged( QString ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( factionChanged( QString ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( superTraitChanged( int ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( moralityChanged( int ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( armorChanged( int, int ) ), self, SLOT( setModified() ) );

	#connect (self, SIGNAL(realIdentityChanged(cv_Identity)), self, SLOT(emitNameChanged(cv_Identity)));


	def species(self):
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

			Debug.debug("Spezies in Speicher verändert zu {}!".format(species))

			self.speciesChanged.emit( species )


	def __getIdentities(self):
		"""
		Gibt eine Liste aller Identitäten des Charkaters aus. Die Identität an Indexposition 0 ist die echte Identität.
		"""
		
		return self.__identities

	identities = property(__getIdentities)

	def insertIdentity( self, index, identity ):
		"""
		Fügt eine neue Identität an der angegebenen Stelle ein.
		"""
		
		self.__identities.insert( index, identity )
		self.identityChanged.emit( identity )

	def addIdentity( self, identity ):
		"""
		Hängt eine neue Identität an die Liste aller Identitäten des Charkaters an.
		"""
		
		self.__identities.append( identity )
		self.identityChanged.emit( identity )

	def setRealIdentity( self, identity ):
		"""
		Legt die \emph{echte} Identität des Charakters fest. Diese Identität hat immer Index 0 in der \ref self.__identities -Liste
		
		\todo Momentan ist dies die einzige identität, die von diesem programm genutzt wird.
		"""

		if self.__identities[0] != identity:
			self.__identities[0] = identity
			self.identityChanged.emit( identity )
			self.realIdentityChanged.emit( identity )


#QList< Trait* >* StorageCharacter::traits() const {
	#return &v_traits2;
#}

#QList< Trait* > StorageCharacter::traits( cv_AbstractTrait::Type type ) const {
	#QList< Trait* > list;

	#for ( int i = 0; i < v_traits2.count(); ++i ) {
		#if ( v_traits2.at( i ).type() == type ) {
			#list.append( v_traits2[i] );
		#}
	#}

	#return list;
#}

#QList< Trait* > StorageCharacter::traits( cv_AbstractTrait::Type type, cv_AbstractTrait::Category category ) const {
	#QList< Trait* > list;

	#for ( int i = 0; i < v_traits2.count(); ++i ) {
		#if ( v_traits2.at( i ).type() == type && v_traits2.at( i ).category() == category ) {
			#list.append( v_traits2[i] );
		#}
	#}

	#return list;
#}

	def __getTraits(self):
		return self.__traits

	def __setTraits(self, traits):
		self.__traits = traits

	traits = property(__getTraits, __setTraits)



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


#void StorageCharacter::setSkillSpecialties( QString name, QList< cv_TraitDetail > details ) {
	#bool trait_exists = false;

	#for ( int i = 0; i < v_traits2.count(); ++i ) {
		#// Spezialisieren gibt es nur bei Fertigkeiten.
		#// Spezialisierungen gibt es nur bei Fertigkeiten, die hier schon existieren.
		#// Spezialisierungen gibt es nur bei Fertigkeiten, die einen Wert größer 0 haben.
		#if ( v_traits2.at( i ).type() == cv_AbstractTrait::Skill && v_traits2.at( i ).name() == name && v_traits2.at( i ).value() > 0 ) {
			#trait_exists = true;

			#Trait* trait = v_traits2.at( i );
			#// Erst alle Spezialisieren löschen
#// 			trait.clearDetails();
			#// Das muß ich allerdings so machen, daß kein Signal ausgesandt wird, weswegen ich nicht die übergeordnete Funktion clearDetails() wähle.
			#trait.details().clear();

			#// Dann neu setzen.
			#int detailsCount = details.count();

			#QList< cv_TraitDetail > list;

			#for ( int j = 0; j < detailsCount; ++j ) {
				#cv_TraitDetail specialty;
				#specialty.name = details.at( j ).name;
				#specialty.value = true;
#// 				qDebug() << Q_FUNC_INFO << "Füge Spezialisierung" << specialty.name << "zu Fertigkeit" << name << "hinzu";
				#list.append( specialty );
			#}

			#trait.setDetails(list);

			#break;
		#}
	#}

	#// Existiert die Fertigkeit nicht, für die eine Spezialisierung eingetragen werden soll, muß etwas getan werden. Anlegen ist aber nicht dier richtige Lösung (welcher Wert denn?).
	#if ( !trait_exists ) {
		#qDebug() << Q_FUNC_INFO << "Spezialisierungen nicht angelegt, da Fertigkeit" << name << "nicht existiert.";
	#}
#}
#void StorageCharacter::addSkillSpecialties( QString name, cv_TraitDetail detail )
#{
	#bool trait_exists = false;

	#for ( int i = 0; i < v_traits2.count(); ++i ) {
		#// Spezialisieren gibt es nur bei Fertigkeiten.
		#// Spezialisierungen gibt es nur bei Fertigkeiten, die hier schon existieren.
		#// Spezialisierungen gibt es nur bei Fertigkeiten, die einen Wert größer 0 haben.
		#if ( v_traits2.at( i ).type() == cv_AbstractTrait::Skill
			#&& v_traits2.at( i ).name() == name
			#&& v_traits2.at( i ).value() > 0
		#) {
			#trait_exists = true;

			#v_traits2[i].addDetail(detail);

			#break;
		#}
	#}

	#// Existiert die Fertigkeit nicht, für die eine Spezialisierung eingetragen werden soll, muß etwas getan werden. Anlegen ist aber nicht dier richtige Lösung (welcher Wert denn?).
	#if ( !trait_exists ) {
		#qDebug() << Q_FUNC_INFO << "Spezialisierung nicht hinzugefügt, da Fertigkeit" << name << "nicht existiert.";
	#}
#}


	def virtue(self):
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


	def vice(self):
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


	def breed(self ):
		"""
		Brut (Seeming, Path, Clan, Auspice) des Charakters.
		"""

		self.__breed

	def setBreed( self, breed ):
		"""
		Verändert die Brut.

		Bei einer Veränderung wird das Signal breedChanged() ausgesandt.
		"""

		if ( self.__breed != breed ):
			self.__breed = breed
			self.breedChanged.emit( breed)


	def faction(self):
		"""
		Fraktion (Court, order, Covenant, Tribe) des Charakters.
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


	def superTrait(self):
		"""
		Gibt den Wert des Super-Attributs aus.
		"""

		return self.__superTrait

	def setSuperTrait( self, value ):
		"""
		Verändert den Wert des Super-Attributs.
		
		Bei einer Veränderung wird das Signal superTraitChanged() ausgesandt.
		"""

		if ( self.__superTrait != value ):
			self.__superTrait = value
			self.superTraitChanged.emit( value )


	def morality(self):
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
			self.moralityChanged.emit( value )

	def armor(self):
		"""
		Gibt den Wert der getragenen Rüstung aus. Zurückgegeben wird eine Liste mit zwei EInträgen.
		
		Die erste Zahl stellt den Rüstungswert gegen alle Angriffe mit Ausnahme von Schußwaffen und Bögen dar.

		Die zweite Zahl stellt dagegen den Rüstungswert gegen Schußwaffen und Bögen dar.
		"""

		return self.__armor

	def setArmor( self, general, firearms=0 ):
		"""
		Verändert den Wert der Rüstung.

		Man kann entweder eine Liste mit den Rüstungswerten übergeben oder je einen Rüstungswert als eigenes Argument.
		
		Bei einer Veränderung wird das Signal armorChanged() ausgesandt.
		"""

		if type(general) == list:
			if len(general) == len(self.__armor):
				if self.__armor != general:
					self.__armor = general
					self.armorChanged.emit( self.__armor )
			else:
				raise ErrListLength(len(self.__armor), len(general))
		elif ( self.__armor[0] != general or self.__armor[1] != firearms ):
			self.__armor[0] = general
			self.__armor[1] = firearms
			self.armorChanged.emit( self.__armor )


	def resetCharacter(self, template):
		# Löschen aller Identitäten.
		self.__identity.reset()

		# Standardspezies ist der Mensch.
		self.setSpecies( template.species[1][0] )

		#Debug.debug(template.virtues[0])
		#Debug.debug(template.virtues[0]["name"])
		self.setVirtue( template.virtues[0]["name"] )
		self.setVice( template.vices[0]["name"] )

		# Menschen haben eine Leere liste, also kann ich auch die Indizes nicht ändern.
		#// setBreed(storage.breedNames(species()).at(0));
		#// setFaction(storage.breedNames(species()).at(0));

		# Alle Eigenschaftswerte löschen, aber Attribute auf Anfangswerte setzen.
		self.__traits = {}
		self.__traits.setdefault("Attribute", {})
		for item in template.traits["Attribute"]:
			self.__traits["Attribute"].setdefault(item, [])
			for subitem in template.traits["Attribute"][item]:
				data = {
					"name": subitem["name"],
					"value": 1,
				}
				self.__traits["Attribute"][item].append(data)

			#v_traits2[i].clearDetails();

			#v_traits2[i].setCustomText( "" );

	#// 		emit traitChanged( v_traits2[i] );
		#}

		#v_derangements.clear();

		#setMorality( Config::derangementMoralityTraitMax );

		#emit characterResetted();


	def isModifed(self):
		return self.__modified

	def setModified( self, sw=True ):
		if ( self.__modified != sw ):
			self.__modified = sw


#void StorageCharacter::emitNameChanged( cv_Identity id )
#{
	#emit nameChanged(id.birthName());
#}


