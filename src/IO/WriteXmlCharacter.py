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

from PySide.QtCore import QObject, QXmlStreamWriter, QIODevice
#from PySide.QtGui import QColor

from src.Config import Config
from src.Error import ErrTraitType, ErrTraitCategory
from src.Debug import Debug




class WriteXmlCharacter(QObject, QXmlStreamWriter):
	"""
	@brief Liest die Eigenschaften aus den beigefügten xml-Dateien.

	Diese Klasse dient dazu einen möglichst simplen Zugriff auf die Eigenschaften der WoD-Charaktere zu bieten. Dazu werden die Eigenschaften und all ihre Zusatzinformationen aus den xml-Dateien gelesen und in Listen gespeichert.

	Es wird nur in die Datei geschrieben, was auch wirklich benötigt wird (Speicherplatz sparen).
	"""

	def __init__(self, character, parent=None):
		QObject.__init__(self, parent)
		QXmlStreamWriter.__init__(self)
		
		self.__character = character

		self.setAutoFormatting( True )


	def write( self, f ):
		"""
		Schreibt die veränderten Charakteristika in die Datei.
		"""
		
		#Debug.debug("Speicherversuch")

		f.open( QIODevice.WriteOnly )
		self.setDevice( f )

		self.writeStartDocument()
		self.writeStartElement( Config.programName )
		self.writeAttribute( "version", Config.version() )
		self.writeTextElement( "species", self.__character.species )
		self.writeStartElement( "identities" )
		self.writeStartElement( "identity" )
		self.writeAttribute( "forenames", " ".join(self.__character.identities[0].forenames) )
		self.writeAttribute( "surename", self.__character.identities[0].surename )
		self.writeAttribute( "honorname", self.__character.identities[0].honorname )
		self.writeAttribute( "nickname", self.__character.identities[0].nickname )
		self.writeAttribute( "supername", self.__character.identities[0].supername )
		self.writeAttribute( "gender", self.__character.identities[0].gender )
		self.writeEndElement()
		self.writeEndElement()
		self.writeTextElement( "age", unicode(self.__character.age) )
		self.writeTextElement( "virtue", self.__character.virtue )
		self.writeTextElement( "vice", self.__character.vice )
		self.writeTextElement( "breed", self.__character.breed )
		self.writeTextElement( "faction", self.__character.faction )
		self.writeTextElement( "powerstat", unicode( self.__character.powerstat ) )
		self.writeTextElement( "morality", unicode( self.__character.morality ) )
		self.writeTextElement( "armor", Config.sepChar.join( unicode(n) for n in self.__character.armor ) )
		self.writeTextElement( "era", self.__character.era )

		self.writeCharacterTraits()

		#writeCharacterDerangements();

		self.writeEndElement()
		self.writeEndDocument()

		f.close()


	def writeCharacterTraits(self):
		"""
		Schreibt die veränderten Eigenschaften in die Datei.
		"""
		
		for item in self.__character.traits:
			startElementWritten_item = False
			for subitem in self.__character.traits[item]:
				startElementWritten_subitem = False
				for subsubitem in self.__character.traits[item][subitem].values():
					## Eigenschaften müssen nur dann gespeichert werden, wenn ihr Wert != 0 ist und sie für die aktuell gewählte Spezies zur Verfügung stehen.
					if ( subsubitem.value != 0 and (not subsubitem.species or subsubitem.species == self.__character.species) ):
						## Soabld die erste Eigenschaft mit einem Wert != 0 auftaucht, muß das Startelement geschrieben werden.
						if not startElementWritten_item:
							try:
								self.writeStartElement( item )
							except ErrTraitType as e:
								Debug.debug(e.message())
							startElementWritten_item = True
						if not startElementWritten_subitem:
							try:
								self.writeStartElement( "Category" )
								self.writeAttribute("name", subitem)
							except ErrTraitCategory as e:
								Debug.debug(e.message)
							startElementWritten_subitem = True

						self.writeStartElement( "trait" )
						self.writeAttribute( "name", subsubitem.name )
						self.writeAttribute( "value", unicode( subsubitem.value ) )
						# Zusatztext
						if subsubitem.custom:
							self.writeAttribute( "customText", unicode( subsubitem.customText ) )
						# Spezialisierungen
						if subsubitem.specialties:
							self.writeTextElement( "specialties", Config.sepChar.join( unicode(n) for n in subsubitem.specialties ) )

	#// 					qDebug() << Q_FUNC_INFO << list.at( k ).name << list.at( k ).custom;

						#if ( list.at( k ).custom() ) {
							#writeAttribute( "custom", list.at( k ).customText() );
						#}

						self.writeEndElement()
				# Das Endelement taucht natürlich nur auf, wenn auch ein zugehöriges Startelement existiert.
				if startElementWritten_subitem:
					self.writeEndElement()
			# Das Endelement taucht natürlich nur auf, wenn auch ein zugehöriges Startelement existiert.
			if startElementWritten_item:
				self.writeEndElement()


	def writeCharacterDerangements(self):
		"""
		Schreibt die Geistesstörungen in die Datei.
		"""
		
		pass
		#QList< cv_Derangement* > list;

		#try {
			#writeStartElement( cv_AbstractTrait.toXmlString( cv_AbstractTrait.Derangement ) );
		#} except ( eTraitType &e ) {
			#qDebug() << Q_FUNC_INFO << e.message();
		#}

		#// Liste der Kategorien ist je nach Typ unterschiedlich
		#QList< cv_AbstractTrait.Category > category;

		#category = cv_AbstractTrait.getCategoryList( cv_AbstractTrait.Derangement );

		#for ( int j = 0; j < category.count(); ++j ) {
			#list = self.__character.derangements( category.at( j ) );

			#qDebug() << Q_FUNC_INFO << list.count();

			#try {
				#writeStartElement( cv_AbstractTrait.toXmlString( category.at( j ) ) );
			#} except ( eTraitCategory &e ) {
				#qDebug() << Q_FUNC_INFO << e.message();
			#}

			#for ( int k = 0; k < list.count(); ++k ) {
	#// 					qDebug() << Q_FUNC_INFO << list.at( k ).name;
				#writeStartElement( "derangement" );
				#writeAttribute( "name", list.at( k ).name() );
				#writeAttribute( "morality", QString.number( list.at( k ).morality() ) );

				#writeEndElement();
			#}

			#writeEndElement();
		#}

		#writeEndElement();
	#}

