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

from PySide.QtCore import QObject, Signal

#from src.Config import Config
#from ReadXml import ReadXml
from src.Debug import Debug
#from src.Error import ErrTraitType




class Trait(QObject):
	"""
	@brief Speichert alle Eigenschaften einer einzigen Charaktereigenschaft.

	Simple Eigenschaften wie Attribute haben nur Name und Wert. Bei Fertigkeiten kommen bereits die Spezialisierungen hinzu, bei  Vorzügen noch die Einschränkungen etc.
	"""


	valueChanged = Signal(int)
	#valueChanged = Signal(object)
	customTextChanged = Signal(str)
	specialtiesChanged = Signal(object)
	availableChanged = Signal(bool)
	traitChanged = Signal(object)


	def __init__(self, character, name="", value=0, parent=None):
		"""
		Die Referenz auf character benötige ich nur, damit ich bei Eigenschaften mit Voraussetzungen diese auch überprüfen kann.

		\ref checkPrerequisites
		"""
		
		QObject.__init__(self, parent)

		self.__character = character

		self.__name = name
		self.__value = value
		self.__specialties = []
		self.__age = ""
		self.__era = ""
		self.__species = ""
		self.__custom = False
		self.__customText = ""
		self.__prerequisites = False
		self.__prerequisitesText = ""
		self.__available = True


	def __getName(self):
		return self.__name

	def __setName(self, name):
		self.__name = name

	name = property(__getName, __setName)


	def __getValue(self):
		return self.__value

	def setValue(self, value):
		"""
		Verändert den Wert der Eigenschaft.
		"""
		
		if self.__value != value:
			self.__value = value
			#Debug.debug("Ändere Eigenschaft {} zu {}".format(self.name, self.value))
			self.valueChanged.emit(value)
			self.traitChanged.emit(self)

	value = property(__getValue, setValue)


	def __getSpecialties(self):
		return self.__specialties

	def __setSpecialties(self, specialties):
		if self.__specialties != specialties:
			self.__specialties = specialties
			self.specialtiesChanged.emit(specialties)
			self.traitChanged.emit(self)

	specialties = property(__getSpecialties, __setSpecialties)

	def appendSpecialty(self, name):
		"""
		Fügt der Liste von SPezialisierungen eine hinzu.

		\note Diese Methode muß verwendet werden, wenn man das Signal \ref specialtyChanged nutzen möchte.
		"""

		self.__specialties.append(name)
		self.specialtiesChanged.emit(self.specialties)
		self.traitChanged.emit(self)

	def removeSpecialty(self, name):
		"""
		Fügt der Liste von SPezialisierungen eine hinzu.

		\note Diese Methode muß verwendet werden, wenn man das Signal \ref specialtyChanged nutzen möchte.
		"""

		self.__specialties.remove(name)
		self.specialtiesChanged.emit(self.specialties)
		self.traitChanged.emit(self)


	def __getEra(self):
		return self.__era

	def __setEra(self, era):
		self.__era = era

	era = property(__getEra, __setEra)


	def __getAge(self):
		return self.__age

	def __setAge(self, age):
		self.__age = age

	age = property(__getAge, __setAge)


	def __getSpecies(self):
		return self.__species

	def __setSpecies(self, species):
		self.__species = species

	species = property(__getSpecies, __setSpecies)


	def isCustom(self):
		return self.__custom

	def setCustom(self, custom):
		self.__custom = custom


	def __getCustomText(self):
		return self.__customText

	def __setCustomText(self, text):
		if self.__customText != text:
			self.__customText = text
			self.customTextChanged.emit(text)

	customText = property(__getCustomText, __setCustomText)


	def __getPrerequisites(self):
		return self.__prerequisites

	def __setPrerequisites(self, prerequisites):
		self.__prerequisites = prerequisites

	hasPrerequisites = property(__getPrerequisites, __setPrerequisites)


	def __getPrerequisitesText(self):
		return self.__prerequisitesText

	def __setPrerequisitesText(self, text):
		if self.__prerequisitesText != text:
			self.__prerequisitesText = text
			#self.prerequisitesTextChanged.emit(text)

	prerequisitesText = property(__getPrerequisitesText, __setPrerequisitesText)


#Trait::Trait( QString txt, int val, cv_Species::Species spe, cv_AbstractTrait::Type ty, cv_AbstractTrait::Category ca, QObject* parent ) : QObject( parent ), cv_Trait( txt, val, spe, ty, ca ) {
	#construct();
#}

#Trait::Trait( cv_Trait trait, QObject* parent ) : QObject( parent ), cv_Trait( trait.name(), trait.value(), trait.species(), trait.type(), trait.category() ) {
	#construct();

	#setEra( trait.era() );
	#setAge( trait.age() );
	#setPrerequisites( trait.prerequisites() );
	#setCustom( trait.custom() );
	#setCustomText( trait.customText() );
	#setDetails( trait.details() );
	#setPossibleValues( trait.possibleValues() );
#}

#Trait::Trait( Trait* trait, QObject* parent ) : QObject( parent ), cv_Trait( trait->name(), trait->value(), trait->species(), trait->type(), trait->category() ) {
	#construct();

	#setEra( trait->era() );
	#setAge( trait->age() );
	#setPrerequisites( trait->prerequisites() );
	#setCustom( trait->custom() );
	#setCustomText( trait->customText() );
	#setDetails( trait->details() );
	#setPossibleValues( trait->possibleValues() );
#}


#void Trait::construct() {
	#// Am Anfang stehen alle Fertigkeiten zur Verfügung, aber wenn dann die Voraussetzungen geprüft werden, kann sich das ändern.
	#v_available = true;

	#connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( emitTraitChanged() ) );
	#connect( this, SIGNAL( detailsChanged( int ) ), this, SLOT( emitTraitChanged() ) );
	#connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( clearDetails( int ) ) );
#}


#void Trait::setDetails( QList< cv_TraitDetail > list ) {
	#"""
	#Legt die Zusatzeigenschaften fest.
	#"""
	
	#if ( details() != list ) {
		#cv_Trait::setDetails( list );

		#emit detailsChanged( list.count() );
	#}
#}
#void Trait::addDetail( cv_TraitDetail det ) {
	#"""
	#Fügt eine Zusatzeigenscahft hinzu.
	#"""
	
	#if ( !details().contains( det ) ) {
		#cv_Trait::addDetail( det );

		#emit detailsChanged( details().count() );
	#} else {
#// 		qDebug() << Q_FUNC_INFO << "Spezialisierung" << det.name << "existiert schon";
	#}
#}
#void Trait::clearDetails() {
	#"""
	#Löscht sämtliche Zusatzeigenschaften.
	#
	#Wenn der Wert einer Fertigkeit auf 0 sinkt, werden alle ihre Spezialisierungen gelöscht.
	#"""
	
#// 	qDebug() << Q_FUNC_INFO << "Hallo?";
	#if ( !details().isEmpty() ) {
		#cv_Trait::clearDetails();

		#emit detailsChanged( 0 );
	#}
#}
#void Trait::clearDetails( int val ) {
	#if ( val < 1 ) {
		#this->clearDetails();
	#}
#}


#void Trait::setType( cv_AbstractTrait::Type typ ) {
	#"""
	#Legt den Typ fest und sendet ein entsprechendes Signal aus.
	#"""
	
	#if ( type() != typ ) {
		#cv_AbstractTrait::setType( typ );

		#emit typeChanged( typ );
	#}
#}

	def isAvailable(self):
		"""
		Gibt zurück, ob die Voraussetzungen der Eigenschaft erfüllt sind, ode rnicht.
		"""

		return self.__available

	def setAvailable( self, sw ):
		"""
		Legt fest, ob die Eigenschaft zur Verfügung steht oder nicht.
		"""

		if ( self.__available != sw ):
			self.__available = sw
			self.availableChanged.emit( sw )

		
#void Trait::setBonus( bool sw ) {
	#"""
	#Legt fest, ob diese Eigenschaft eine Bonuseigenschaft ist.
	#"""
	
	#qDebug() << Q_FUNC_INFO << "Wird aufgerufen!";
	#if ( isBonus() == sw ) {
		#cv_Trait::setBonus( sw );

		#emit bonusChanged( sw );
	#}
#}


	def checkPrerequisites(self, trait):
		self.__character.checkPrerequisites(self)


#QList< Trait* > Trait::prerequisitePtrs() const {
	#return v_prerequisitePtrs;
#}
#void Trait::clearPrerequisitePtrs() {
	#v_prerequisitePtrs.clear();
#}
#void Trait::addPrerequisitePtrs( Trait* replacement ) {
	#if ( !prerequisites().isEmpty() && ( prerequisites().contains( replacement->name() ) ) ) {
		#// In die Liste einfügen.
		#v_prerequisitePtrs.append( replacement );
	#}
#}


#void Trait::checkPrerequisites( Trait* trait ) {
	"""
	Überprüft, ob alle Voraussetzungen für diese Eigenschaft erfüllt werden.
	"""
	
	#if ( !prerequisitePtrs().isEmpty() ) {
#// 		qDebug() << Q_FUNC_INFO << "Wird für" << this->name() << "ausgeführt, weil sich Fertigkeit" << trait->name() << "geändert hat";

		#QString lcl_prerequisites = parsePrerequisites( prerequisites(), prerequisitePtrs() );

		#// Alles was an Wörtern übriggeblieben ist durch 0 ersetzen.
		#// Wäre schön, wenn das der Parser könnte, da kriege ich das aber nicht hin.
		#QString replacementText;
		#QRegExp rx( "([a-zA-Z]+)\\s*[<>=]+" );

		#while ( lcl_prerequisites.contains( rx ) ) {
#// 			qDebug() << Q_FUNC_INFO << name() << prerequisites;
			#lcl_prerequisites.replace( "AND", "999" );
			#lcl_prerequisites.replace( "OR", "88" );
			#lcl_prerequisites.replace( QRegExp( "([a-zA-Z]+)" ), "0" );
			#lcl_prerequisites.replace( ".0", "0" );
#// 			prerequisites.replace(QRegExp("(0 0)"), '0');
			#lcl_prerequisites.replace( "999", "AND" );
			#lcl_prerequisites.replace( "88", "OR" );
		#}

#// 		qDebug() << Q_FUNC_INFO << "Voraussetzungen für" << this->name() << "sind" << lcl_prerequisites;

		#StringBoolParser parser;

		#try {
			#if ( parser.validate( lcl_prerequisites ) ) {
				#setAvailability( true );
			#} else {
				#setAvailability( false );
			#}
		#} catch ( Exception &e ) {
			#qDebug() << Q_FUNC_INFO << name() << lcl_prerequisites << e.description() << e.message();
		#}

#// 		qDebug() << Q_FUNC_INFO << "Wurde für" << this->name() << "ausgeführt, weil sich Fertigkeit" << trait->name() << "geändert hat. Ergebnis ist:" << isAvailable();
	#}
#}


#QString Trait::parsePrerequisites( QString text, QList< Trait* > list ) {
	#"""
	#Hilfsfunktion für checkTraitPrerequisites().
	#"""
	
	#QString prerequisites = text;

	#// Ersetze alle Atrtribute, Fertigkeiten etc. in dem Textstring mit den entsprechenden Zahlen, damit diese später über den Parser ausgewertet werden können.
	#// Nicht vorhandene Werte verbleiben natürlich in Textform und werden vom Parser wie 0en behandelt.

	#if ( prerequisites.contains( QRegExp( "([a-zA-Z]+)\\s*[<>=]+" ) ) ) {
		#for ( int k = 0; k < list.count(); ++k ) {
			#// Ersetzen der Fertigkeitsspezialisierungen von dem Format Fertigkeit.Spezialisierung mit Fertigkeitswert, wenn Spezialisierung existiert oder 0, wenn nicht.
			#if ( prerequisites.contains( '.' ) && list.at( k )->type() == cv_AbstractTrait::Skill && list.at( k )->details().count() > 0 ) {
				#QString testSkill = list.at( k )->name() + ".";

				#if ( prerequisites.contains( testSkill ) ) {
					#QString specialisation = prerequisites.right( prerequisites.indexOf( testSkill ) - testSkill.count() + 1 );
					#specialisation = specialisation.left( specialisation.indexOf( ' ' ) );

					#for ( int l = 0; l < list.at( k )->details().count(); l++ ) {
						#// Fertigkeiten mit Spezialisierungsanforderungen werden mit dem Fertigkeitswert ersetzt, wenn Spez existiert, ansonsten mit 0.
						#if ( specialisation == list.at( k )->details().at( l ).name ) {
							#prerequisites.replace( testSkill + specialisation, QString::number( list.at( k )->value() ) );

							#// Wenn alle Worte ersetzt wurden, kann ich aus den Schleifen raus.

							#if ( !prerequisites.contains( QRegExp( "([a-zA-Z]+)\\s*[<>=]+" ) ) ) {
								#return prerequisites;
							#}
						#} else {
							#prerequisites.replace( testSkill + specialisation, "0" );

							#// Wenn alle Worte ersetzt wurden, kann ich aus den Schleifen raus.

							#if ( !prerequisites.contains( QRegExp( "([a-zA-Z]+)\\s*[<>=]+" ) ) ) {
								#return prerequisites;
							#}
						#}
					#}
				#}
			#} else {
				#// Ersetzen von Eigenschaftsnamen mit ihren Werten.
				#prerequisites.replace( list.at( k )->name(), QString::number( list.at( k )->value() ) );

				#// Wenn alle Worte ersetzt wurden, kann ich aus den Schleifen raus.

				#if ( !prerequisites.contains( QRegExp( "([a-zA-Z]+)\\s*[<>=]+" ) ) ) {
					#return prerequisites;
				#}
			#}
		#}
	#} else {
		#qDebug() << Q_FUNC_INFO << "Nicht durch die Schleifen." << name();
	#}
#}


#void Trait::emitTraitChanged() {
	#emit traitChanged( this );
#}