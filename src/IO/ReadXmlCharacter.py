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
#from PySide.QtGui import QColor

from src.Config import Config
from src.IO.ReadXml import ReadXml
from src.Error import ErrXmlOldVersion
from src.Debug import Debug




class ReadXmlCharacter(QObject, ReadXml):
	"""
	@brief Liest die gespeicherten Charakterwerte in das Programm.

	Diese Klasse dient dazu, einen auf Datenträger gespeicherten Charakter wieder in das Programm zu laden.
	"""

	def __init__(self, character, parent=None):
		QObject.__init__(self, parent)
		ReadXml.__init__(self)

		self.__character = character


#QList< cv_Trait > ReadXmlCharacter::traitList;

#ReadXmlCharacter::ReadXmlCharacter() : QObject(), ReadXml() {
	#storage = new StorageTemplate();
	#character = StorageCharacter::getInstance();
#}


	def read( self, f ):
		"""
		Startet den Lesevorgang.
		"""
		
		## Wir erzeugen eine neue Trait-Liste aus der aktuellen Trait-Liste des Charakters. Diese wird dann entsprechend des gespeicherten Datei verändert und dann in den Charakter geschrieben. Damit sende ich nur ein Signal, daß die Eigenschaften verändert würden.
		#self.__traits = self.__character.traits

		self.openFile( f )
		self.setDevice( f )

		while ( not self.atEnd() ):
			self.readNext()

			if ( self.isStartElement() ):
				elementName = self.name()
				#Debug.debug("Lese Element {} aus.".format(elementName))
				elementVersion = self.attributes().value( "version" )

				try:
					self.checkXmlVersion( elementName, elementVersion )
					self.readSoulCreator()
				except ErrXmlOldVersion as e:
					MessageBox.exception( self, e.message(), e.description() )
					readSoulCreator()

		if ( self.hasError() ):
			Debug.debug("Error!")
			raise ErrXmlError( f.fileName(), self.errorString() )

		## Die möglicherweise veränderten Eigenschaften müssen wieder in den Charakter-Speicher geschrieben werden.
		#self.__character.traits = self.__traits

		self.closeFile( f )


	def readSoulCreator(self):
		"""
		Es wird zwischen den einzelnen Eigenscahften unterschieden und je nach Typ unterschiedlich eingelesen.
		"""
		
		while ( not self.atEnd() ):
			self.readNext()

			if ( self.isEndElement() ):
				break

			if ( self.isStartElement() ):
				elementName = self.name()
				#Debug.debug("Lese Element {} aus.".format(elementName))

				if ( elementName == "species" ):
					self.__character.species = self.readElementText()
				elif ( elementName == "identities" ):
					self.readIdentities()
				elif ( elementName == "age" ):
					self.__character.age = int(self.readElementText())
				elif ( elementName == "virtue" ):
					self.__character.virtue = self.readElementText()
				elif ( elementName == "vice" ):
					self.__character.vice = self.readElementText()
				elif ( elementName == "breed" ):
					self.__character.breed = self.readElementText()
				elif ( elementName == "faction" ):
					self.__character.faction = self.readElementText()
				elif ( elementName == "superTrait" ):
					self.__character.superTrait = int(self.readElementText())
				elif ( elementName == "morality" ):
					self.__character.morality = int(self.readElementText())
				elif ( elementName == "armor" ):
					txt = self.readElementText()
					self.__character.armor = [int(n) for n in txt.split(Config.sepChar)]
				elif ( elementName == "era" ):
					self.__character.era = self.readElementText()
				elif ( elementName in Config.typs ):
					self.readTraitCategories( elementName )
				#elif ( elementName != cv_AbstractTrait::toXmlString( cv_AbstractTrait::TypeNo ) ) {
	#// 				qDebug() << Q_FUNC_INFO << elementName << "!";
					#readTraits( cv_AbstractTrait::toType( elementName ) );
				else:
					self.readUnknownElement()


	def readIdentities(self):
		"""
		Liest die Identitäten des Charakters.
		
		\todo Derzeit kann nur eine identität eingelesen werden, da das Programm nur eine Identitöät unterstüzt.
		"""
		
		while ( not self.atEnd() ):
			self.readNext()

			if ( self.isEndElement() ):
				break

			if ( self.isStartElement() ):
				elementName = self.name()

				if ( elementName == "identity" ):
					self.__character.identities[0].forenames = self.attributes().value( "forenames" ).split(" ")
					self.__character.identities[0].surename = self.attributes().value( "surename" )
					self.__character.identities[0].honorname = self.attributes().value( "honorname" )
					self.__character.identities[0].nickname = self.attributes().value( "nickname" )
					self.__character.identities[0].supername = self.attributes().value( "supername" )
					self.__character.identities[0].gender = self.attributes().value( "gender" )

					self.readUnknownElement()
				else:
					self.readUnknownElement()


	def readTraitCategories( self, typ ):
		"""
		Liest die Kategorie der Eigenschaft aus und ruft die Funktion auf, welche die tatsächliche Eigenschaftsdaten ausliest.
		"""
		
		while ( not self.atEnd() ):
			self.readNext()

			if ( self.isEndElement() ):
				break

			if ( self.isStartElement() ):
				elementName = self.name()
				#Debug.debug("Lese Element {} aus.".format(elementName))
				self.readTraits( typ, elementName )


	def readTraits( self, typ, category ):
		"""
		Liest die Daten der einzelnen Eigenschaften aus dem gespeicherten Charakter aus.
		"""
		
		while ( not self.atEnd() ):
			self.readNext()

			if ( self.isEndElement() ):
				break

			if ( self.isStartElement() ):
				elementName = self.name()
				#Debug.debug("Lese Element {} aus.".format(elementName))

				#if ( typ == cv_AbstractTrait::Derangement && elementName == "derangement" ) {
					#cv_Derangement derangement;
					#derangement.setName(attributes().value( "name" ).toString());
					#derangement.setType(type);
					#derangement.setCategory(category);
					#derangement.setMorality(attributes().value( "morality" ).toString().toInt());

					#character.addDerangement( derangement );

					#while ( !atEnd() ) {
						#readNext();

						#if ( self.isEndElement() )
							#break;

						#if ( self.isStartElement() ):
							#readUnknownElement();
						#}
					#}
				if ( elementName == "trait" ):
					itemExists = False
					for item in self.__character.traits[typ][category]:
						traitName = self.attributes().value( "name" )
						traitCustomText = self.attributes().value( "customText" )
						if item.name == traitName:
							# Wenn eine Eigenschaft mit Zusatztext bereits im Speicher existiert, muß weitergesucht werden, bis eine Eigenscahft gleichen namens mit identischem oder ohne Zusatztext gefunden wurde.
							if item.customText and item.customText != traitCustomText:
								continue

							item.value = int(self.attributes().value( "value" ))
							#Debug.debug("Ändere Eigenschaft {} zu {}".format(item.name, item.value))
							# Zusatztext
							item.customText = traitCustomText
							self.readSpecialties(item)
							itemExists = True
							break

					# Wenn die Eigenscahft ncht schon im Charakter-Speicher existiert (also in den Template-Dateien vorkam), wird sie ignoriert.
					if not itemExists:
						self.readUnknownElement()

					#if ( customText.isEmpty() ) {
	#// 					trait.custom = false;
						#trait.setCustomText( "" );
					#} else {
	#// 					qDebug() << Q_FUNC_INFO << customText;
	#// 					trait.custom = true;
						#trait.setCustomText( customText );
					#}

					#character.modifyTrait( trait );
				else:
					self.readUnknownElement()


	def readSpecialties( self, trait ):
		"""
		Liest die Spezialisierungen der auszulesenen Eigenscahft aus.
		"""

		while ( not self.atEnd() ):
			self.readNext()

			if ( self.isEndElement() ):
				break

			if ( self.isStartElement() ):
				elementName = self.name()
				#Debug.debug("Lese Element {} aus.".format(elementName))

				if ( elementName == "specialties" ):
					txt = self.readElementText()
					trait.specialties = [n for n in txt.split(Config.sepChar)]
				else:
					self.readUnknownElement()


