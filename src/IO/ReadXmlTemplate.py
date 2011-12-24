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
from src.Debug import Debug




class ReadXmlTemplate(QObject, ReadXml):
	"""
	@brief Liest die Eigenschaften aus den beigefügten xml-Dateien.

	Diese Klasse dient dazu einen möglichst simplen Zugriff auf die Eigenschaften der WoD-Charaktere zu bieten. Dazu werden die Eigenschaften und all ihre Zusatzinformationen aus den xml-Dateien gelesen und in Listen gespeichert.
	"""

	__templateFiles = (
		"resources/xml/base.xml",
		"resources/xml/human.xml",
		"resources/xml/changeling.xml",
		"resources/xml/mage.xml",
		"resources/xml/vampire.xml",
		"resources/xml/werewolf.xml",
	)


	__types = (
		"Attribute",
		"Skill",
		"Merit",
		"Derangement",
		"Flaw",
		"Super",
		"Power",
	)


	def __init__(self, parent=None):
		QObject.__init__(self, parent)
		ReadXml.__init__(self)
		
		self.storage = StorageTemplate()


	def read(self):
		"""
		Diese Methode startet den Lesevorgang.
		"""
		
		for item in self.__templateFiles:
			#Debug.debug("Lese aus Datei: {}".format(item))
			f = QFile(item)
			self.readXml( f )
			self.closeFile( f )


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
			#Debug.debug("Error!")
			raise Error.ErrXmlParsing( device.fileName(), self.errorString() )


	def readSoulCreator(self):
		"""
		Die zweite Ebene des XML-Baumes wird einegelesen. Es wird gespeichert, für welche Spezies dieser Zweig vorgesehen ist. Daraufhin wird die Arbeit an readTree() weitergegeben.
		
		\exception ErrXmlError Ist das XML_Dokument fehlerhaft, wird diese Exception mit dem passenden Fehlertext geworfen.
		"""
		
		while( not self.atEnd() ):
			self.readNext()

			if self.isEndElement():
				break

			if( self.isStartElement() ):
				elementName = self.name()
				#Debug.debug("Element {} gefunden.".format(elementName))
				if( elementName == "traits" ):
					speciesData = [
						self.attributes().value( "species" ),
						self.attributes().value( "morale" ),
						self.attributes().value( "supertrait" ),
						self.attributes().value( "fuel" ),
					]
					#Debug.debug("Spezies {} gefunden.".format(speciesData[0]))

					# Füge die gerade in der xml-Datei gefundene Spezies einer Liste zu, die später zur Auswahl verwendet werden wird.
					self.storage.appendSpecies( speciesData )

					self.readTree( speciesData[0] )
				elif( elementName == "creation" ):
					speciesFlag = self.attributes().value( "species" )
					#Debug.debug("Erschaffungspunkte für Spezies {} gefunden.".format(speciesFlag))
					self.readCreationTree( speciesFlag )
				else:
					self.readUnknownElement()


	def readTree( self, species ):
		"""
		Hier wird der cv_TRait::Type der Eigenschaftengruppe ausgelesen und danach entschieden, an welche Funktion weitergesprungen werden soll.
		
		- Virtues und Vices werden mit cv_AbstractTrait::CategoryNo bewertet (sie sind weder mental noch physisch oder sozial). Sie werden daraufhin mit der Funktion readTraits(cv_Species::Species sp, cv_AbstractTrait::Type a, cv_AbstractTrait::Category b) weitergelesen.
		
		- Alle anderen Eigenschaften werden mit der Funktion readTraits(cv_Species::Species sp, cv_AbstractTrait::Type a) weitergelesen.
		"""
		
		while( not self.atEnd() ):
			self.readNext()

			if self.isEndElement():
				break

			if( self.isStartElement() ):
				typ = self.name()

				if( typ == "Virtue" or typ == "Vice" ):
					self.readCharacteristics( species, typ )
				elif(typ == "Breed" or
						typ == "Faction" ):
					self.readGroups( species, typ, None )
				elif( typ == "Super" ):
					self.readSuperTrait( species )
				elif( typ in self.__types):
					#self.readUnknownElement()
					self.readTraits( species, typ )
				else:
					self.readUnknownElement()


	def readCharacteristics( self, species, typ, category=None ):
		"""
		Liest die Charakteristiken ein.

		- Tugenden
		- Laster
		"""

		while( not self.atEnd() ):
			self.readNext()

			if self.isEndElement():
				break

			if( self.isStartElement() ):
				elementName = self.name()
				if( elementName == "trait" ):
					#Debug.debug("Lese {} ein.".format(elementName))

					traitData = {
						"name": self.attributes().value( "name" ),
						"species": species,
						"age": self.attributes().value( "age" ),
					}

					self.storage.appendTrait( typ, category, traitData );
					self.readUnknownElement()
				else:
					self.readUnknownElement()


	def readGroups( self, species, typ, category=None ):
		"""
		Liest die verschiedenen Gruppierungsnamen der einzelnen Spezies ein.
		"""

		if( typ == "Breed" or
				typ == "Faction"
		):
			group = self.attributes().value( "name" )

			self.storage.appendTitle( species, typ, group )

		while( not self.atEnd() ):
			self.readNext()

			if self.isEndElement():
				break

			if( self.isStartElement() ):
				elementName = self.name()
				if( elementName == "trait" ):
					title = self.attributes().value( "name" )
					self.storage.appendTitle( species, typ, group, title )

					# Damit weitergesucht wird.
					self.readGroupInfo(species, title)
				else:
					self.readUnknownElement()


	def readGroupInfo( self, species, breed ):
		"""
		Einzelne Gruppen bieten noch zusätzliche Informationen wie beispielsweise die Bonuseigenschaften der Vampir-Clans etc. Die Ermittlung dieser informationen beginnt hier.
		"""

		while( not self.atEnd() ):
			self.readNext()

			if self.isEndElement():
				break

			if( self.isStartElement() ):
				name = self.name()
				if( name == "bonus" ):
					self.readBonusTraits(species, breed)
				else:
					self.readUnknownElement()

		


	def readBonusTraits( self, species, breed ):
		"""
		Es werden die Bonus-Eigenschaften ausgelesen.
		"""

		while( not self.atEnd() ):
			self.readNext()

			if( self.isEndElement() ):
				break

			if( self.isStartElement() ):
				# Es können Bonuseiegnschaften verschiedener Typen gewährt werden.
				traitTyp = self.name()
				self.readBonusTraitsDetails( species, breed, traitTyp )



	def readBonusTraitsDetails(self, species, breed, typ):
		"""
		Die tatsächlichen Eigenscahften werden in dieser Funktion ermittelt.
		"""

		while( not self.atEnd() ):
			self.readNext()

			if( self.isEndElement() ):
				break

			if( self.isStartElement() ):
				if( self.name() == "trait" ):
					traitName = self.attributes().value( "name" )
					traitData = {
						"name": traitName,
						"typ": typ,
					}
					self.storage.appendBonusTrait( species, breed, traitData )
					self.readUnknownElement()
				else:
					self.readUnknownElement()


	def readSuperTrait( self, species ):
		"""
		Lese die Informationen über die Auswirkungen der Supereigenschaft aus den Template-Dateien.
		"""

		while( not self.atEnd() ):
			self.readNext()

			if( self.isEndElement() ):
				break

			if( self.isStartElement() ):
				if( self.name() == "supertrait" ):
					superEffectData = {
						"fuelMax": int(self.attributes().value( "fuelMax" )),
						"fuelPerTurn": int(self.attributes().value( "fuelPerTurn" )),
						"traitMax": int(self.attributes().value( "traitMax" )),
						"value": int(self.readElementText()),
					}
					self.storage.appendSuperEffect( species, superEffectData )
				else:
					self.readUnknownElement()


	def readTraits( self, species, typ ):
		"""
		Lese die Eigenschaften aus den Template-Dateien.

		Hier wird die Kategorie bestimmt und dann an eine Funktion übergeben, die den nächsten Schritt im XML-Baum geht.
		"""

		while( not self.atEnd() ):
			self.readNext()

			if( self.isEndElement() ):
				break

			if( self.isStartElement() ):
				category = self.name()

				self.readTraitData( species, typ, category );


	def readTraitData( self, species, typ, category ):
		"""
		Nächster Schritt beim Einlesen der Eigenschaften.
		"""

		while( not self.atEnd() ):
			self.readNext()

			if self.isEndElement():
				break

			if( self.isStartElement() ):
				if( self.name() == "trait" ):
					traitData = {
						"name": self.attributes().value( "name" ),
						"species": species,
						"age": self.attributes().value( "age" ),
						"era": self.attributes().value( "era" ),
						"value": [0],
					}

					#Debug.debug("Lese {} ein.".format(traitData["name"]))
					#cv_Trait trait = storeTraitData( sp, a, b );
					#// Alle Eigenschaften können 0 als Wert haben, auch wenn dies nicht in den XML-Dateien steht.

					#if( !trait.possibleValues().isEmpty() ) {
						#trait.addPossibleValue( 0 );
					#}

					self.readTraitInformation( species, typ, category, traitData )
				else:
					self.readUnknownElement()


	def readTraitInformation( self, species, typ, category, traitData ):
		"""
		Nun werden die zusätzlichen Informationen (Spezialisierungen, Voraussetzungen etc.) ausgelesen.
		"""

		traitInfo = traitData

		while( not self.atEnd() ):
			self.readNext()

			if self.isEndElement():
				break

			if( self.isStartElement() ):
				name = self.name()
				if( name == "specialty" or name == "prerequisite" ):
					if name not in traitInfo:
						traitInfo.setdefault(name,[])
					traitInfo[name].append(self.readElementText())
				elif( name == "value" ):
					if name not in traitInfo:
						traitInfo.setdefault(name,[])
					val = int(self.readElementText())
					if val not in traitInfo[name]:
						traitInfo[name].append(val)
				else:
					self.readUnknownElement()

		self.storage.appendTrait( typ, category, traitInfo )


	def readCreationTree( self, sp ):
		"""
		Ab hier werden die Erschaffungspunkte ausgelesen.
		"""
		
		while( not self.atEnd() ):
			self.readNext()

			if( self.isEndElement() ):
				break

			if( self.isStartElement() ):
				typ = self.name()
				if( typ in self.__types ):
					points = self.readCreationPoints()
					self.storage.appendCreationPoints( sp, typ, points )
				else:
					self.readUnknownElement()


	def readCreationPoints(self):
		"""
		Diese Funktion liest die einzelnenen Erschaffungspunkte aus, hängt sie an eine Liste an und übergibt sie an die aufrufende Funktion.
		"""

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

