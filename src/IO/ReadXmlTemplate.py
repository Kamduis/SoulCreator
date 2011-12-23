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

#import traceback

from PySide.QtCore import QObject, QFile

from src.Config import Config
from src import Error
from ReadXml import ReadXml
from src.Storage.StorageTemplate import StorageTemplate
from src.Datatypes.cv_Species import cv_Species
from src.Datatypes.Traits.cv_AbstractTrait import cv_AbstractTrait
from src.Debug import Debug




class ReadXmlTemplate(QObject, ReadXml):
	"""
	@brief Liest die Eigenschaften aus den beigefügten xml-Dateien.

	Diese Klasse dient dazu einen möglichst simplen Zugriff auf die Eigenschaften der WoD-Charaktere zu bieten. Dazu werden die Eigenschaften und all ihre Zusatzinformationen aus den xml-Dateien gelesen und in Listen gespeichert.
	"""

	# \todo Hier kann ich Listen verwenden.
	templateFile_base = "resources/xml/base.xml"
	templateFile_human = "resources/xml/human.xml"
	templateFile_changeling = "resources/xml/changeling.xml"
	templateFile_mage = "resources/xml/mage.xml"
	templateFile_vampire = "resources/xml/vampire.xml"
	templateFile_werewolf = "resources/xml/werewolf.xml"

#//const QString ReadXmlTemplate::templateFile = test.dat"

#// QList< cv_Trait > ReadXmlTemplate::traitList

#// QList<cv_Species> ReadXmlTemplate::speciesList


	def __init__(self, parent=None):
		QObject.__init__(self, parent)
		ReadXml.__init__(self)
		
		self.storage = StorageTemplate()

		# \todo Hier kann ich Listen verwenden.
		self.__file_base = QFile( self.templateFile_base );
		self.__file_human = QFile( self.templateFile_human );
		self.__file_changeling = QFile( self.templateFile_changeling );
		self.__file_mage = QFile( self.templateFile_mage );
		self.__file_vampire = QFile( self.templateFile_vampire );
		self.__file_werewolf = QFile( self.templateFile_werewolf );


	def read(self):
		"""
		Diese Methode startet den Lesevorgang.
		"""
		
		self.__process( self.__file_base )
		self.__process( self.__file_human )
		self.__process( self.__file_changeling )
		self.__process( self.__file_mage )
		self.__process( self.__file_vampire )
		self.__process( self.__file_werewolf )


	def __process(self, device ):
		"""
		Arbeitet den Leseprozeß ab.
		"""

		Debug.debug("Lese aus Datei: {}".format(device.fileName()))
		self.readXml( device )


	def readXml(self, device ):
		"""
		Die erste Ebene in der Abarbeitung des XML-Baumes. Kontrolliert, ob es sich um eine Zuässige Template-Datei für dieses Programm handelt und gibt dann die Leseoperation an readSoulCreator() weiter.

		\exception ErrXmlVersion Die XML-DaTei hat die falsche Version.

		\todo Momentan wird trotz Argument immer nur die basis-Datei abgearbeitet.
		"""
    
		self.openFile( device )
		self.setDevice( device )

		while( not self.atEnd() ):
			self.readNext()

			if self.isStartElement():
				elementName = self.name()
				elementVersion = self.attributes().value( "version" )

				try:
					self.checkXmlVersion( elementName, elementVersion )
					self.readSoulCreator()
				except Error.ErrXmlOldVersion as e:
					raise Error.ErrXmlOldVersion( e.message(), e.description() )
					self.readSoulCreator()


		if( self.hasError() ):
			Debug.debug("Error!")
			raise Error.ErrXmlParsing( device.fileName(), self.errorString() )

		self.closeFile( self.__file_base )


	def readSoulCreator(self):
		while( not self.atEnd() ):
			self.readNext()

			if self.isEndElement():
				break

			if( self.isStartElement() ):
				Debug.debug("Element {} gefunden.".format(self.name()))
				if( self.name() == "traits" ):
					speciesFlag = self.attributes().value( "species" )
					Debug.debug("Spezies {} gefunden.".format(speciesFlag))
					if( speciesFlag in cv_Species.Species ):
						species = cv_Species()
						species.name = speciesFlag
						species.morale = self.attributes().value( "morale" )
						species.supertrait = self.attributes().value( "supertrait" )
						species.fuel = self.attributes().value( "fuel" )

						# Füge die gerade in der xml-Datei gefundene Spezies einer Liste zu, die später zur Auswahl verwendet werden wird.
						self.storage.appendSpecies( species )

						self.readTree( speciesFlag )
				elif( self.name() == "creation" ):
					speciesFlag = self.attributes().value( "species" )
					Debug.debug("Spezies {} gefunden.".format(speciesFlag))
					if( speciesFlag in cv_Species.Species ):
						self.readCreationTree( speciesFlag );
				else:
					Debug.debug("Finde Element {}".format(self.name()))
					self.readUnknownElement()


	def readTree( self, sp ):
		while( not self.atEnd() ):
			self.readNext()

			if self.isEndElement():
				break

			if( self.isStartElement() ):
				typ = self.name()

				if( typ in cv_AbstractTrait.Typ ):
					#Debug.debug("Typ {} gefunden.".format(typ))
					# Virtues und Vices haben keine Kategorie, also darf ich dort auch nicht so tief den Baum hinuntersteigen. Bei allen anderen aber muß ich erst die Kategorie einlesen.
					if( typ == "Virtue" or
							typ == "Vice" or
							typ == "Breed" or
							typ == "Faction" ):
						#self.readTraits( sp, typ, None )
						self.readUnknownElement()
					elif( typ == "Super" ):
						#self.readSuperTrait( sp )
						self.readUnknownElement()
					else:
						#self.readTraits( sp, typ )
						self.readUnknownElement()
				else:
					self.readUnknownElement()


#void ReadXmlTemplate::readSuperTrait( cv_Species::Species sp ) {
	#while( !atEnd() ) {
		#readNext();

		#if( isEndElement() )
			#break;

		#if( isStartElement() ) {
			#if( name() == "supertrait" ) {
				#cv_SuperEffect superEffect;
				#superEffect.species = sp;
				#superEffect.fuelMax = attributes().value( "fuelMax" ).toString().toInt();
				#superEffect.fuelPerTurn = attributes().value( "fuelPerTurn" ).toString().toInt();
				#superEffect.traitMax = attributes().value( "traitMax" ).toString().toInt();
				#superEffect.value = readElementText().toInt();

				#storage->appendSuperEffect( superEffect );
			#} else
				#readUnknownElement();
		#}
	#}
#}


#void ReadXmlTemplate::readTraits( cv_Species::Species sp, cv_AbstractTrait::Type a ) {

	#while( !atEnd() ) {
		#readNext();

		#if( isEndElement() )
			#break;

		#if( isStartElement() ) {
			#QString elementName = name().toString();
			#cv_AbstractTrait::Category category = cv_AbstractTrait::toCategory( elementName );

			#readTraits( sp, a, category );
		#}
	#}
#}

	#def readTraits( self, sp, a, b=None ):
		#if( a == "Breed" or
				#a == "Faction" or
				#a == "Power"
		#):
			#titleName = self.attributes().value( "name" )
			#title = cv_SpeciesTitle( cv_SpeciesTitle::toTitle( cv_AbstractTrait::toString( a ) ), titleName, sp );

			#Debug.debug(title.title)
	#// 		qDebug() << Q_FUNC_INFO << title.title << title.name << title.species;

			#storage->appendTitle( title );
		#}

		#while( !atEnd() ) {
			#readNext();

			#if( isEndElement() )
				#break;

			#if( isStartElement() ) {
				#if( name() == "trait" ) {
					#cv_Trait trait = storeTraitData( sp, a, b );
					#// Alle Eigenschaften können 0 als Wert haben, auch wenn dies nicht in den XML-Dateien steht.

					#if( !trait.possibleValues().isEmpty() ) {
						#trait.addPossibleValue( 0 );
					#}

					#storage->appendTrait( trait );
				#} else {
					#readUnknownElement();
				#}
			#}
		#}
	#}

#cv_Trait ReadXmlTemplate::storeTraitData( cv_Species::Species sp, cv_AbstractTrait::Type a, cv_AbstractTrait::Category b ) {
	#// Es besteht die Möglichkeit, daß einzelne Eigenschaften in mehreren XML-DAteien auftauchen. Beispiel: Fertigkeit mit Spezialisierungen speziell für eine Spezies.
	#// Momentan löse ich das Problem nicht hier beim Einlesen, sondern bei der Ausgabe in Storage.cpp
#// 	QString specialtyName;

	#cv_Trait trait;
	#trait.setSpecies( sp );
	#trait.setType( a );
	#trait.setCategory( b );
	#// Keinefalls darf ich zulassen, daß dieser Wert uninitialisiert bleibt, sonst führt das zu Problemen.
	#trait.setValue( 0 );

	#if( isStartElement() ) {
		#trait.setName( attributes().value( "name" ).toString() );
#// 		qDebug() << Q_FUNC_INFO << trait.name;
		#trait.setEra( cv_Trait::toEra( attributes().value( "era" ).toString() ) );
		#trait.setAge( cv_Trait::toAge( attributes().value( "age" ).toString() ) );
		#trait.setCustom( attributes().value( "custom" ).toString() == QString( "true" ) );

#// 		if (trait.custom){
#// 			qDebug() << Q_FUNC_INFO << trait.name << "ist besonders!";
#// 		}

		#while( !atEnd() ) {
			#readNext();

			#if( isEndElement() ) {
				#break;
			#}

			#if( isStartElement() ) {
				#if( name() == "specialty" ) {
					#QString specialtyName = readElementText();
					#cv_TraitDetail traitDetail;
					#traitDetail.name = specialtyName;
					#traitDetail.value = false;
#// 					traitDetail.species = sp;
					#trait.addDetail( traitDetail );
				#} else if( name() == "value" ) {
					#int value = readElementText().toInt();
					#trait.addPossibleValue( value );
				#} else if( name() == "prerequisite" ) {
					#QString text = readElementText();
#// 					trait.v_prerequisites.append( text );
					#trait.setPrerequisites( text );
				#} else if( name() == "bonus" ) {	// Es können Bonuseigenschaften vergeben werden.
#// 					qDebug() << Q_FUNC_INFO << "Im Bonus-Zweig!";
					#readBonusTraits( sp, trait.name() );
				#} else {
					#readUnknownElement();
				#}
			#}
		#}
	#}

	#return trait;
#}


#void ReadXmlTemplate::readBonusTraits( cv_Species::Species sp, QString nameDependant ) {
	#while( !atEnd() ) {
		#readNext();

		#if( isEndElement() )
			#break;

		#if( isStartElement() ) {
			#// Es können Bonuseiegnschaften verschiedener Typen gewährt werden.
			#cv_AbstractTrait::Type type = cv_AbstractTrait::toType( name().toString() );

			#if( type != cv_AbstractTrait::TypeNo ) {
				#readBonusTraits( sp, type, nameDependant );
			#} else {
				#readUnknownElement();
			#}
		#}
	#}
#}

#void ReadXmlTemplate::readBonusTraits( cv_Species::Species sp, cv_AbstractTrait::Type tp, QString nameDep ) {
	#while( !atEnd() ) {
		#readNext();

		#if( isEndElement() )
			#break;

		#if( isStartElement() ) {
			#if( name() == "trait" ) {
				#QString name = attributes().value( "name" ).toString();

				#Trait* lcl_trait1 = new Trait( name, 0, sp, tp );

				#storage->appendTraitBonus( lcl_trait1, nameDep );

				#readUnknownElement();
			#} else {
				#readUnknownElement();
			#}
		#}
	#}
#}


	def	readCreationTree( self, sp ):
		while( not self.atEnd() ):
			self.readNext()

			if( self.isEndElement() ):
				break

			if( self.isStartElement() ):
				typ = self.name()
				if( typ in cv_AbstractTrait.Typ ):
					points = self.readCreationPoints()
					self.storage.appendCreationPoints( sp, typ, points )
				else:
					self.readUnknownElement()


	def readCreationPoints(self):
		resultList = []

		while( not self.atEnd() ):
			self.readNext()

			if( self.isEndElement() ):
				break

			if( self.isStartElement() ):
				if( self.name() == "points" ):
					resultList.append( self.attributes().value( "value" ) )
					self.readUnknownElement()
				else:
					self.readUnknownElement()

		return resultList

