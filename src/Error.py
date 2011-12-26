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
	#setMessage( self.obj.tr( "Unspecified Problem with a number." ) );
	#setDescription( self.obj.tr( "An unspecified error occured while handling a number or what should at least be a number." ) );
#}

#eNotANumber::eNotANumber() : eNumber() {
	#setMessage( self.obj.tr( "Not a Number." ) );
	#setDescription( self.obj.tr( "While expecting a number, somethin other than a number was given." ) );
#}




class ErrList(Err):
	"""
	@brief Ausnahme bei Listen.
	"""
	
	def __init__(self):
		Error.__init__(self)
		
		self.setMessage( self.obj.tr( "Unspecified Problem with a List." ) )
		self.setDescription( self.obj.tr( "An unspecified error occured while handling a List." ) )


class ErrIndexExceedsRange(ErrList):
	"""
	@brief Index überschreitet Listengröße.
	"""

	def __init__(self, idx, listLen ):
		ErrList.__init__(self)
		
		self.setMessage( self.obj.tr( "Index exceeds Range of List or Vector." ) )
		self.setDescription( self.obj.tr( "Index {} exceeds List Range of {}.".format(idx, listLen) ))


class ErrListLength(ErrList):
	"""
	@brief Listenlänge stimmt nicht mit erwartetem Wert überein.
	"""

	def __init__(self, expected, got ):
		ErrList.__init__(self)

		txt = "long"
		if got < expected:
			txt = "short"
		self.setMessage( self.obj.tr( "List to {}.".format(txt) ) )
		self.setDescription( self.obj.tr( "Got a List of length {}, but got a length of {}.".format(expected, got) ) )




#eDir::eDir( QString dirName ) : Exception() {
	#setMessage( self.obj.tr( "Unspecified Problem with a directory." ) );
	#setDescription( self.obj.tr( "An unspecified error occured while handling directory %1" ).arg( dirName ) );
#}

#eDirNotCreated::eDirNotCreated( QString dirName ) : eDir() {
	#setMessage( self.obj.tr( "Cannot create Directory." ) );
	#setDescription( self.obj.tr( "Directory %1 could not be created" ).arg( dirName ) );
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
	#setMessage( self.obj.tr( "Character Species Problem" ) );
	#setDescription( self.obj.tr( "There is a problem with a character species." ) );
#}

#eSpeciesNotExisting::eSpeciesNotExisting( cv_Species::SpeciesFlag species ) : eSpecies() {
	#setMessage( self.obj.tr( "Character Species Problem" ) );
	#setDescription( self.obj.tr( "Species %1 is missing." ).arg( species ) );
#}

#eSpeciesNotExisting::eSpeciesNotExisting() : eSpecies() {
	#setMessage( self.obj.tr( "Character Species Problem" ) );
	#setDescription( self.obj.tr( "Species is missing." ) );
#}


#eGender::eGender() : Exception() {
	#setMessage( self.obj.tr( "Gender Problem" ) );
	#setDescription( self.obj.tr( "There is a problem with the gender of the character." ) );
#}

#eGenderNotExisting::eGenderNotExisting( cv_Identity::Gender gen ) : eGender() {
	#setMessage( self.obj.tr( "Character Gender Problem" ) );
	#setDescription( self.obj.tr( "Gender %1 does not exist." ).arg( gen ) );
#}


#eTrait::eTrait() : Exception() {
	#setMessage( self.obj.tr( "Character Trait Problem" ) );
	#setDescription( self.obj.tr( "There is a problem with a character trait." ) );
#}

#eTraitNotExisting::eTraitNotExisting() : eTrait() {
	#setMessage( self.obj.tr( "Character Trait Problem" ) );
	#setDescription( self.obj.tr( "Trait is missing." ) );
#}

#eTraitCategory::eTraitCategory( cv_AbstractTrait::Category category ) : eTrait() {
	#setMessage( self.obj.tr( "Category of a Trait not valid" ) );
	#setDescription( self.obj.tr( "The Category %1 is not valid at this point." ).arg( QString::number( category ) ) );
#}

#eTraitType::eTraitType( cv_AbstractTrait::Type type ) : eTrait() {
	#setMessage( self.obj.tr( "Type of a Trait not valid" ) );
	#setDescription( self.obj.tr( "The Type %1 is not valid at this point." ).arg( QString::number( type ) ) );
#}


#ePrint::ePrint() : Exception() {
	#setMessage( self.obj.tr( "Printing Problem" ) );
	#setDescription( self.obj.tr( "There is a problem while trying to print the character sheet." ) );
#}

#eTraitsExceedSheetCapacity::eTraitsExceedSheetCapacity( cv_AbstractTrait::Type type, int maxNumber ) : ePrint() {
	#setMessage( self.obj.tr( "Too many %1 to print on character sheet." ).arg( cv_AbstractTrait::toString( type, true ) ) );
	#setDescription( self.obj.tr( "Trying to print too many %1. The character sheet hat only room for %2" ).arg( cv_AbstractTrait::toString( type, true ) ).arg( maxNumber ) );
#}

#eValueExceedsSheetCapacity::eValueExceedsSheetCapacity( int value, QString name ) : ePrint() {
	#setMessage( self.obj.tr( "A value exceeds the capacity of the Charactersheet." ) );
	#setDescription( self.obj.tr( "The character sheet has no room for %1 %2" ).arg( QString::number( value ) ).arg( name ) );
#}


#eEntry::eEntry() : Exception() {
	#setMessage( self.obj.tr( "Entry Problem." ) );
	#setDescription( self.obj.tr( "There is a problem with an expected Input." ) );
#}

#eUserEntry::eUserEntry() : eEntry() {
	#setMessage( self.obj.tr( "User Entry Problem." ) );
	#setDescription( self.obj.tr( "There is a problem with an expected User Input." ) );
#}

#eMissingUserEntry::eMissingUserEntry() : eUserEntry() {
	#setMessage( self.obj.tr( "Missing User Entry." ) );
	#setDescription( self.obj.tr( "An expected User Input is missing." ) );
#}


#eWerewolfShape::eWerewolfShape() {
	#setMessage( self.obj.tr( "Problem with werewolf shape." ) );
	#setDescription( self.obj.tr( "A Probklem regarding a shape of the werewolf has occured." ) );
#}
#eWerewolfShapeNotExisting::eWerewolfShapeNotExisting( cv_Shape::WerewolfShape shape ): eWerewolfShape() {
	#setMessage( self.obj.tr( "Shape not existing." ) );
	#setDescription( self.obj.tr( "The chosen Shape %1 does not exist." ).arg( shape ) );
#}
#eWerewolfShapeNotExisting::eWerewolfShapeNotExisting( QString shape ): eWerewolfShape() {
	#setMessage( self.obj.tr( "Shape not existing." ) );
	#setDescription( self.obj.tr( "The chosen Shape %1 does not exist." ).arg( shape ) );
#}

