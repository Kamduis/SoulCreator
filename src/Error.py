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




class Err(Exception):
	"""
	@brief Basisklasse für die Ausnahmebehandlung

	Diese Klasse liegt allen Ausnahmebehandlungen zugrunde.
	"""

	def __init__(self, msg="", desc=""):
		Exception.__init__(self)

		self.obj = QObject()

		self.__message = msg
		self.__description = desc

	def message(self):
		return self.__message

	def setMessage(self, txt):
		self.__message = txt

		
	def description(self):
		return self.__description

	def setDescription(self, txt):
		self.__description = txt



#eNumber::eNumber() : Exception() {
	#setMessage( QObject::tr( "Unspecified Problem with a number." ) );
	#setDescription( QObject::tr( "An unspecified error occured while handling a number or what should at least be a number." ) );
#}

#eNotANumber::eNotANumber() : eNumber() {
	#setMessage( QObject::tr( "Not a Number." ) );
	#setDescription( QObject::tr( "While expecting a number, somethin other than a number was given." ) );
#}


#eList::eList() : Exception() {
	#setMessage( QObject::tr( "Unspecified Problem with a List or Vector." ) );
	#setDescription( QObject::tr( "An unspecified error occured while handling a List or Vector." ) );
#}

#eIndexExceedsRange::eIndexExceedsRange( int idx, int range ) : eList() {
	#setMessage( QObject::tr( "Index exceeds Range of List or Vector." ) );
	#setDescription( QObject::tr( "Index %1 exceeds List Range of %2." ).arg( idx ).arg( range ) );
#}


#eDir::eDir( QString dirName ) : Exception() {
	#setMessage( QObject::tr( "Unspecified Problem with a directory." ) );
	#setDescription( QObject::tr( "An unspecified error occured while handling directory %1" ).arg( dirName ) );
#}

#eDirNotCreated::eDirNotCreated( QString dirName ) : eDir() {
	#setMessage( QObject::tr( "Cannot create Directory." ) );
	#setDescription( QObject::tr( "Directory %1 could not be created" ).arg( dirName ) );
#}




class ErrFile(Err):
	"""
	@brief Ausnahme im Datei-Management.

	Allgemeine Fehler im Umgang mit Dateien werfen diese Ausnahme.
	"""
	
	def __init__(self, filename = "unknown" ):
		Err.__init__(self)

		self.setMessage(self.obj.tr( "Unspecified Problem with a file." ))
		self.setDescription(self.obj.tr( "An unspecified error occured while handling file %1".format(filename) ))


class ErrFileNotOpened(ErrFile):
	"""
	@brief Datei kann nicht geöffnet werden.

	Das Programm kann die spezifizierte Datei nicht öffnen.
	"""

	def __init__(self, filename = "unknown", lastError = "unknown" ):
		ErrFile.__init__(self)
		
		self.setMessage( self.obj.tr( "Cannot open File." ) )
		self.setDescription( self.obj.tr( "File {} could not be opened: {}".format(filename,  lastError ) ))


class ErrFileNotDeleted(ErrFile):
	"""
	@brief Datei kann nicht gelöscht werden.

	Das Programm kann die spezifizierte Datei nicht löschen.
	"""

	def __init__(self, filename = "unknown" ):
		ErrFile.__init__(self)

		self.setMessage( self.obj.tr( "Deletion not successful." ) )
		self.setDescription( self.obj.tr( "File {} could not be deleted.".format(filename ) ))




class ErrXml(Err):
	"""
	@brief Ausnahme beim Lesen der XML-Datei

	Treten Fehler beim Lesen der XML-Datei auf, wird diese Ausnahme geworfen.
	"""

	def __init__(self, error = "unknown" ):
		Err.__init__(self)

		self.setMessage( self.obj.tr( "XML-Problem." ) )
		self.setDescription( self.obj.tr( "{}".format(error ) ))


class ErrXmlParsing(ErrXml):
	"""
	@brief Beim Parsen der XML-Datei trat ein Fehler auf.

	Während das Programm versucht, eine XML-Datei zu parsen, tritt der im Argument spezifizierte Fehler auf.
	"""

	def __init__(self, fileName = "unknown", error = "unknown" ):
		ErrXml.__init__(self)

		self.setMessage( self.obj.tr( "XML-Parsing raised error." ) )
		self.setDescription( self.obj.tr( "While trying to parse the XML-File, the following error was raised: \"{error}\" in file \"{filename}\"".format(filename=fileName, error=error)))


class ErrXmlVersion(ErrXml):
	"""
	@brief Die XML-Datei weist die falsche Version auf.
	"""

	def __init__(self, expected = "unknown", got = "unknown" ):
		ErrXml.__init__(self)

		self.setMessage( self.obj.tr( "Wrong XML-Version." ) )
		self.setDescription( self.obj.tr( "Got {} but expected was {}".format(got, expected)))


class ErrXmlOldVersion(ErrXmlVersion):
	"""
	@brief Die Version der XML-Datei paßt zwar zu diesem programm, ist aber zu alt.
	"""

	def __init__(self, expected = "unknown", got = "unknown" ):
		ErrXmlVersion.__init__(self)

		self.setMessage( self.obj.tr( "Old Version." ) )
		self.setDescription( self.obj.tr( "Got {} but expected was {}".format(got, expected)))


class ErrXmlTooOldVersion(ErrXmlOldVersion):
	"""
	@brief Die Version der XML-Datei paßt zwar zu diesem Programm, ist aber viel zu alt.

	Die Version ist so alt, daß eine Verwendung dieser Ressource nicht empfehlenswert ist.
	"""

	def __init__(self, expected = "unknown", got = "unknown" ):
		ErrXmlOldVersion.__init__(self)

		self.setMessage( self.obj.tr( "Too old Version." ) )
		self.setDescription( self.obj.tr( "Got {} but expected was {}".format(got, expected)))


#eSpecies::eSpecies() : Exception() {
	#setMessage( QObject::tr( "Character Species Problem" ) );
	#setDescription( QObject::tr( "There is a problem with a character species." ) );
#}

#eSpeciesNotExisting::eSpeciesNotExisting( cv_Species::SpeciesFlag species ) : eSpecies() {
	#setMessage( QObject::tr( "Character Species Problem" ) );
	#setDescription( QObject::tr( "Species %1 is missing." ).arg( species ) );
#}

#eSpeciesNotExisting::eSpeciesNotExisting() : eSpecies() {
	#setMessage( QObject::tr( "Character Species Problem" ) );
	#setDescription( QObject::tr( "Species is missing." ) );
#}


#eGender::eGender() : Exception() {
	#setMessage( QObject::tr( "Gender Problem" ) );
	#setDescription( QObject::tr( "There is a problem with the gender of the character." ) );
#}

#eGenderNotExisting::eGenderNotExisting( cv_Identity::Gender gen ) : eGender() {
	#setMessage( QObject::tr( "Character Gender Problem" ) );
	#setDescription( QObject::tr( "Gender %1 does not exist." ).arg( gen ) );
#}


#eTrait::eTrait() : Exception() {
	#setMessage( QObject::tr( "Character Trait Problem" ) );
	#setDescription( QObject::tr( "There is a problem with a character trait." ) );
#}

#eTraitNotExisting::eTraitNotExisting() : eTrait() {
	#setMessage( QObject::tr( "Character Trait Problem" ) );
	#setDescription( QObject::tr( "Trait is missing." ) );
#}

#eTraitCategory::eTraitCategory( cv_AbstractTrait::Category category ) : eTrait() {
	#setMessage( QObject::tr( "Category of a Trait not valid" ) );
	#setDescription( QObject::tr( "The Category %1 is not valid at this point." ).arg( QString::number( category ) ) );
#}

#eTraitType::eTraitType( cv_AbstractTrait::Type type ) : eTrait() {
	#setMessage( QObject::tr( "Type of a Trait not valid" ) );
	#setDescription( QObject::tr( "The Type %1 is not valid at this point." ).arg( QString::number( type ) ) );
#}


#ePrint::ePrint() : Exception() {
	#setMessage( QObject::tr( "Printing Problem" ) );
	#setDescription( QObject::tr( "There is a problem while trying to print the character sheet." ) );
#}

#eTraitsExceedSheetCapacity::eTraitsExceedSheetCapacity( cv_AbstractTrait::Type type, int maxNumber ) : ePrint() {
	#setMessage( QObject::tr( "Too many %1 to print on character sheet." ).arg( cv_AbstractTrait::toString( type, true ) ) );
	#setDescription( QObject::tr( "Trying to print too many %1. The character sheet hat only room for %2" ).arg( cv_AbstractTrait::toString( type, true ) ).arg( maxNumber ) );
#}

#eValueExceedsSheetCapacity::eValueExceedsSheetCapacity( int value, QString name ) : ePrint() {
	#setMessage( QObject::tr( "A value exceeds the capacity of the Charactersheet." ) );
	#setDescription( QObject::tr( "The character sheet has no room for %1 %2" ).arg( QString::number( value ) ).arg( name ) );
#}


#eEntry::eEntry() : Exception() {
	#setMessage( QObject::tr( "Entry Problem." ) );
	#setDescription( QObject::tr( "There is a problem with an expected Input." ) );
#}

#eUserEntry::eUserEntry() : eEntry() {
	#setMessage( QObject::tr( "User Entry Problem." ) );
	#setDescription( QObject::tr( "There is a problem with an expected User Input." ) );
#}

#eMissingUserEntry::eMissingUserEntry() : eUserEntry() {
	#setMessage( QObject::tr( "Missing User Entry." ) );
	#setDescription( QObject::tr( "An expected User Input is missing." ) );
#}


#eWerewolfShape::eWerewolfShape() {
	#setMessage( QObject::tr( "Problem with werewolf shape." ) );
	#setDescription( QObject::tr( "A Probklem regarding a shape of the werewolf has occured." ) );
#}
#eWerewolfShapeNotExisting::eWerewolfShapeNotExisting( cv_Shape::WerewolfShape shape ): eWerewolfShape() {
	#setMessage( QObject::tr( "Shape not existing." ) );
	#setDescription( QObject::tr( "The chosen Shape %1 does not exist." ).arg( shape ) );
#}
#eWerewolfShapeNotExisting::eWerewolfShapeNotExisting( QString shape ): eWerewolfShape() {
	#setMessage( QObject::tr( "Shape not existing." ) );
	#setDescription( QObject::tr( "The chosen Shape %1 does not exist." ).arg( shape ) );
#}

