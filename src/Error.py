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

	def __getMessage(self):
		"""
		Erlaubt das Auslesen der Standardnachricht.
		"""
		
		return self.__message

	def __setMessage(self, txt):
		"""
		Setzt die Kurznachricht über die Ausnahme.
		"""
		
		self.__message = txt

	message = property(__getMessage, __setMessage)

		
	def __getDescription(self):
		"""
		Erlaubt das Auslesen einer ausfühlrichen Beschreibung der ausgelösten Ausnahme.
		"""
		
		return self.__description

	def __setDescription(self, txt):
		"""
		Setzt die ausfühlriche Beschreibung der Ausnahme.
		"""
		
		self.__description = txt



#eNumber::eNumber() : Exception() {
	#"""
	#@brief Ausnahme bei Zahlen.
	#"""
	
	#message = self.obj.tr( "Unspecified Problem with a number." )
	#description = self.obj.tr( "An unspecified error occured while handling a number or what should at least be a number." )
#}

#eNotANumber::eNotANumber() : eNumber() {
	#"""
	#@brief Ausnahme beim Fehlen einer Zahl.

	#Es wird eine Zahl erwartet, abe rkeine Zahl übergeben.
	#"""

	#message = self.obj.tr( "Not a Number." )
	#description = self.obj.tr( "While expecting a number, somethin other than a number was given." )
#}




class ErrList(Err):
	"""
	@brief Ausnahme bei Listen.
	"""
	
	def __init__(self):
		Err.__init__(self)
		
		self.message = self.obj.tr( "Unspecified Problem with a List." ) 
		self.description = self.obj.tr( "An unspecified error occured while handling a List." ) 


class ErrIndexExceedsRange(ErrList):
	"""
	@brief Index überschreitet Listengröße.
	"""

	def __init__(self, idx, listLen ):
		ErrList.__init__(self)
		
		self.message = self.obj.tr( "Index exceeds Range of List or Vector." ) 
		self.description = self.obj.tr( "Index {} exceeds List Range of {}.".format(idx, listLen) )


class ErrListLength(ErrList):
	"""
	@brief Listenlänge stimmt nicht mit erwartetem Wert überein.
	"""

	def __init__(self, expected, got ):
		ErrList.__init__(self)

		txt = "long"
		if got < expected:
			txt = "short"
		self.message = self.obj.tr( "List to {}.".format(txt) ) 
		self.description = self.obj.tr( "Got a List of length {}, but got a length of {}.".format(expected, got) ) 




#eDir::eDir( QString dirName ) : Exception() {
	#"""
	#@brief Ausnahme im Verzeichnis-Management.

	#Allgemeine Fehler im Umgang mit Verzeichnissen werfen diese Ausnahme.
	#"""

	#message = self.obj.tr( "Unspecified Problem with a directory." )
	#description = self.obj.tr( "An unspecified error occured while handling directory %1" ).arg( dirName )
#}

#eDirNotCreated::eDirNotCreated( QString dirName ) : eDir() {
	#"""
	#@brief Verzeichnis kann nicht angelegt werden.
	#"""

	#message = self.obj.tr( "Cannot create Directory." )
	#description = self.obj.tr( "Directory %1 could not be created" ).arg( dirName )
#}




class ErrFile(Err):
	"""
	@brief Ausnahme im Datei-Management.

	Allgemeine Fehler im Umgang mit Dateien werfen diese Ausnahme.
	"""
	
	def __init__(self, filename = "unknown" ):
		Err.__init__(self)

		self.message =self.obj.tr( "Unspecified Problem with a file." )
		self.description =self.obj.tr( "An unspecified error occured while handling file %1".format(filename) )


class ErrFileNotOpened(ErrFile):
	"""
	@brief Datei kann nicht geöffnet werden.

	Das Programm kann die spezifizierte Datei nicht öffnen.
	"""

	def __init__(self, filename = "unknown", lastError = "unknown" ):
		ErrFile.__init__(self)
		
		self.message = self.obj.tr( "Cannot open File." ) 
		self.description = self.obj.tr( "File {} could not be opened: {}".format(filename,  lastError ) )


class ErrFileNotDeleted(ErrFile):
	"""
	@brief Datei kann nicht gelöscht werden.

	Das Programm kann die spezifizierte Datei nicht löschen.
	"""

	def __init__(self, filename = "unknown" ):
		ErrFile.__init__(self)

		self.message = self.obj.tr( "Deletion not successful." ) 
		self.description = self.obj.tr( "File {} could not be deleted.".format(filename ) )




class ErrXml(Err):
	"""
	@brief Ausnahme beim Lesen der XML-Datei

	Treten Fehler beim Lesen der XML-Datei auf, wird diese Ausnahme geworfen.
	"""

	def __init__(self, error = "unknown" ):
		Err.__init__(self)

		self.message = self.obj.tr( "XML-Problem." ) 
		self.description = self.obj.tr( "{}".format(error ) )


class ErrXmlParsing(ErrXml):
	"""
	@brief Beim Parsen der XML-Datei trat ein Fehler auf.

	Während das Programm versucht, eine XML-Datei zu parsen, tritt der im Argument spezifizierte Fehler auf.
	"""

	def __init__(self, fileName = "unknown", error = "unknown" ):
		ErrXml.__init__(self)

		self.message = self.obj.tr( "XML-Parsing raised error." ) 
		self.description = self.obj.tr( "While trying to parse the XML-File, the following error was raised: \"{error}\" in file \"{filename}\"".format(filename=fileName, error=error))


class ErrXmlVersion(ErrXml):
	"""
	@brief Die XML-Datei weist die falsche Version auf.
	"""

	def __init__(self, expected = "unknown", got = "unknown" ):
		ErrXml.__init__(self)

		self.message = self.obj.tr( "Wrong XML-Version." ) 
		self.description = self.obj.tr( "Got {} but expected was {}".format(got, expected))


class ErrXmlOldVersion(ErrXmlVersion):
	"""
	@brief Die Version der XML-Datei paßt zwar zu diesem programm, ist aber zu alt.
	"""

	def __init__(self, expected = "unknown", got = "unknown" ):
		ErrXmlVersion.__init__(self)

		self.message = self.obj.tr( "Old Version." ) 
		self.description = self.obj.tr( "Got {} but expected was {}".format(got, expected))


class ErrXmlTooOldVersion(ErrXmlOldVersion):
	"""
	@brief Die Version der XML-Datei paßt zwar zu diesem Programm, ist aber viel zu alt.

	Die Version ist so alt, daß eine Verwendung dieser Ressource nicht empfehlenswert ist.
	"""

	def __init__(self, expected = "unknown", got = "unknown" ):
		ErrXmlOldVersion.__init__(self)

		self.message = self.obj.tr( "Too old Version." ) 
		self.description = self.obj.tr( "Got {} but expected was {}".format(got, expected))




class ErrSpecies(Err):
	#"""
	#@brief Ausnahme, falls Fehler bei den Spezies auftritt.
	#"""

	def __init__(self ):
		Err.__init__(self)

		self.message = self.obj.tr( "Problem with species occured." )
		self.description = self.obj.tr( "There is a problem with a character species.")


class ErrSpeciesNotExisting(ErrSpecies):
	#"""
	#@brief Ausnahme, falls eine spezifizierte Spezies nicht existiert.

	#Die erwartete Spezies wurde nicht gefunden.
	#"""

	def __init__(self, species = "unknown" ):
		ErrSpecies.__init__(self)

		self.message = self.obj.tr( "Problem with species occured." )
		self.description = self.obj.tr( "Species {} is missing.".format(species))




#eGender::eGender() : Exception() {
	#"""
	#@brief Ausnahme, falls Fehler bei den Geschlechtern auftritt.
	#"""

	#message = self.obj.tr( "Gender Problem" )
	#description = self.obj.tr( "There is a problem with the gender of the character." )
#}

#eGenderNotExisting::eGenderNotExisting( cv_Identity::Gender gen ) : eGender() {
	#"""
	#@brief Ausnahme, falls das spezifizierte Geschlecht nicht existiert.
	#"""

	#message = self.obj.tr( "Character Gender Problem" )
	#description = self.obj.tr( "Gender %1 does not exist." ).arg( gen )
#}


class ErrTrait(Err):
	"""
	@brief Ausnahme, falls Fehler bei den Eigenschaften auftritt.
	"""

	def __init__(self):
		Err.__init__(self)
		
		self.message = self.obj.tr( "Character Trait Problem" )
		self.description = self.obj.tr( "There is a problem with a character trait." )


#eTraitNotExisting::eTraitNotExisting() : eTrait() {
	#"""
	#@brief Ausnahme, falls eine spezifizierte Eigenscahft nicht existiert.

	#Die erwartete Charaktereigenschaft wurde nicht gefunden.
	#"""

	#message = self.obj.tr( "Character Trait Problem" )
	#description = self.obj.tr( "Trait is missing." )
#}

class ErrTraitCategory(ErrTrait):
	"""
	@brief Ausnahme, falls eine falsche Kategorie genutzt wird.

	Die Kategorie exitiert nicht oder hat an dieser Stelle keine Gültigkeit.
	"""

	def __init__(self, category):
		self.message = self.obj.tr( "Category of a Trait not valid" )
		self.description = self.obj.tr( "The Category {} is not valid at this point.".format( category ))


class ErrTraitType(ErrTrait):
	"""
	@brief Ausnahme, falls ein falscher Typ genutzt wird.
	"""

	def __init__(self, expected, got):
		ErrTrait.__init__(self)

		self.message = self.obj.tr( "Type of a Trait not valid" )
		typ = expected
		if type(expected) == list:
			typ = ", ".join(expected[:-1])
			typ += " or "
			typ += expected[-1]

		self.description = self.obj.tr( "Expected Trait of type {}, but got type {}, which is not valid at this point.".format(typ, got) )


#ePrint::ePrint() : Exception() {
	#"""
	#@brief Ausnahme, falls beim Audrucken ein Fehler entsteht.

	#Ein unspezifizierter Fehler beim Ausdruck ist aufgetreten.
	#"""

	#message = self.obj.tr( "Printing Problem" )
	#description = self.obj.tr( "There is a problem while trying to print the character sheet." )
#}

#eTraitsExceedSheetCapacity::eTraitsExceedSheetCapacity( cv_AbstractTrait::Type type, int maxNumber ) : ePrint() {
	#"""
	#@brief Ausnahme, falls zu viele Eigenschaften gedruckt werden sollen.

	#Aufgrund vorgefertigter Charakterbögen können je nach Typ nur eine gewissen Anzahl der entsprechenden Eigenschaften darauf aufgebracht werden. Stehen im Generator mehr dieser Eigenschaften, als gedruckt werden können, tritt diese Ausnahme auf.
	#"""

	#message = self.obj.tr( "Too many %1 to print on character sheet." ).arg( cv_AbstractTrait::toString( type, true ) )
	#description = self.obj.tr( "Trying to print too many %1. The character sheet hat only room for %2" ).arg( cv_AbstractTrait::toString( type, true ) ).arg( maxNumber )
#}

#eValueExceedsSheetCapacity::eValueExceedsSheetCapacity( int value, QString name ) : ePrint() {
	#"""
	#@brief Ausnahme, falls ein zu großer Wert auf den Charakterbogen gedruckt werden soll.

	#Aufgrund vorgefertigter Charakterbögen können gewisse Teiel des charkaters nicht in beliebiger Höhe dargestellt werden.
	#"""

	#message = self.obj.tr( "A value exceeds the capacity of the Charactersheet." )
	#description = self.obj.tr( "The character sheet has no room for %1 %2" ).arg( QString::number( value ) ).arg( name )
#}


#eEntry::eEntry() : Exception() {
	#"""
	#@brief Ausnahme, falls Fehler bei einer Eingabe auftreten.

	#Falsche oder Fehlende Eingabe führt zu dieser Ausnahme.
	#"""

	#message = self.obj.tr( "Entry Problem." )
	#description = self.obj.tr( "There is a problem with an expected Input." )
#}

#eUserEntry::eUserEntry() : eEntry() {
	#"""
	#@brief Ausnahme, falls Fehler bei einer Benutzereingabe auftreten.
	#"""

	#message = self.obj.tr( "User Entry Problem." )
	#description = self.obj.tr( "There is a problem with an expected User Input." )
#}

#eMissingUserEntry::eMissingUserEntry() : eUserEntry() {
	#"""
	#@brief Ausnahme, falls Fehler bei einer Benutzereingabe auftreten.
	
	#Fehlende Benutzereingabe führt zu dieser Ausnahme.
	#"""

	#message = self.obj.tr( "Missing User Entry." )
	#description = self.obj.tr( "An expected User Input is missing." )
#}


#eWerewolfShape::eWerewolfShape() {
	#"""
	#@brief Ausnahme, falls Fehler Bei den Gestalten der Werwölfe auftritt.
	#"""

	#message = self.obj.tr( "Problem with werewolf shape." )
	#description = self.obj.tr( "A Probklem regarding a shape of the werewolf has occured." )
#}
#eWerewolfShapeNotExisting::eWerewolfShapeNotExisting( cv_Shape::WerewolfShape shape ): eWerewolfShape() {
	#"""
	#@brief Ausnahme, falls eine ungültige Werwolf-Gestalt gewählt wird.
	#"""

	#message = self.obj.tr( "Shape not existing." )
	#description = self.obj.tr( "The chosen Shape %1 does not exist." ).arg( shape )
#}
#eWerewolfShapeNotExisting::eWerewolfShapeNotExisting( QString shape ): eWerewolfShape() {
	#"""
	#
	#"""

	#message = self.obj.tr( "Shape not existing." )
	#description = self.obj.tr( "The chosen Shape %1 does not exist." ).arg( shape )
#}

