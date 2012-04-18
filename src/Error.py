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

	def __init__(self, msg="", desc="", critical=True):
		super(Err, self).__init__()

		self.obj = QObject()

		# Legt fest, ob es sich bei dieser Ausnahme um eine kritische oder um eine einfache Ausnahme handelt.
		self.critical = critical
		# Kurze Benachrichtigung der Ausnahme
		self.message = msg
		# Ausführliche Beschreibung der ausgelösten Ausnahme.
		self.description = desc




class ErrList(Err):
	"""
	@brief Ausnahme bei Listen.
	"""
	
	def __init__(self):
		super(ErrList, self).__init__()
		
		self.message = self.obj.tr( "Unspecified Problem with a List." ) 
		self.description = self.obj.tr( "An unspecified error occured while handling a List." ) 


class ErrIndexExceedsRange(ErrList):
	"""
	@brief Index überschreitet Listengröße.
	"""

	def __init__(self, idx, listLen ):
		super(ErrList, self).__init__()
		
		self.message = self.obj.tr( "Index exceeds Range of List or Vector." ) 
		self.description = self.obj.tr( "Index {} exceeds List Range of {}.".format(idx, listLen) )


class ErrListLength(ErrList):
	"""
	@brief Listenlänge stimmt nicht mit erwartetem Wert überein.
	"""

	def __init__(self, expected, got ):
		super(ErrListLength, self).__init__()

		txt = "long"
		if got < expected:
			txt = "short"
		self.message = self.obj.tr( "List to {}.".format(txt) ) 
		self.description = self.obj.tr( "Got a List of length {}, but got a length of {}.".format(expected, got) ) 




class ErrFile(Err):
	"""
	@brief Ausnahme im Datei-Management.

	Allgemeine Fehler im Umgang mit Dateien werfen diese Ausnahme.
	"""
	
	def __init__(self, filename = "unknown" ):
		super(ErrFile, self).__init__()

		self.message =self.obj.tr( "Unspecified Problem with a file." )
		self.description =self.obj.tr( "An unspecified error occured while handling file %1".format(filename) )


class ErrFileNotOpened(ErrFile):
	"""
	@brief Datei kann nicht geöffnet werden.

	Das Programm kann die spezifizierte Datei nicht öffnen.
	"""

	def __init__(self, filename = "unknown", lastError = "unknown" ):
		super(ErrFileNotOpened, self).__init__()
		
		self.message = self.obj.tr( "Cannot open File." ) 
		self.description = self.obj.tr( "File {} could not be opened: {}".format(filename,  lastError ) )


class ErrFileNotDeleted(ErrFile):
	"""
	@brief Datei kann nicht gelöscht werden.

	Das Programm kann die spezifizierte Datei nicht löschen.
	"""

	def __init__(self, filename = "unknown" ):
		super(ErrFileNotDeleted, self).__init__()

		self.message = self.obj.tr( "Deletion not successful." ) 
		self.description = self.obj.tr( "File {} could not be deleted.".format(filename ) )




class ErrXml(Err):
	"""
	@brief Ausnahme beim Lesen der XML-Datei

	Treten Fehler beim Lesen der XML-Datei auf, wird diese Ausnahme geworfen.
	"""

	def __init__(self, error = "unknown" ):
		super(ErrXml, self).__init__()

		self.message = self.obj.tr( "XML-Problem." ) 
		self.description = self.obj.tr( "{}".format(error ) )


class ErrXmlParsing(ErrXml):
	"""
	@brief Beim Parsen der XML-Datei trat ein Fehler auf.

	Während das Programm versucht, eine XML-Datei zu parsen, tritt der im Argument spezifizierte Fehler auf.
	"""

	def __init__(self, fileName = "unknown", error = "unknown" ):
		super(ErrXmlParsing, self).__init__()

		self.message = self.obj.tr( "XML-Parsing raised error." ) 
		self.description = self.obj.tr( "While trying to parse the XML-File, the following error was raised: \"{error}\" in file \"{filename}\"".format(filename=fileName, error=error))


class ErrXmlVersion(ErrXml):
	"""
	@brief Die XML-Datei weist die falsche Version auf.
	"""

	def __init__(self, expected = "unknown", got = "unknown" ):
		super(ErrXmlVersion, self).__init__()

		self.message = self.obj.tr( "Wrong XML-Version." ) 
		self.description = self.obj.tr( "Got {} but expected was at least {}".format(got, expected))


class ErrXmlOldVersion(ErrXmlVersion):
	"""
	@brief Die Version der XML-Datei paßt zwar zu diesem Programm, ist aber zu alt.
	"""

	def __init__(self, got="unknown", filename=None ):
		super(ErrXmlOldVersion, self).__init__()

		msg = self.obj.tr( "Wrong file Version." )
		if filename is not None:
			msg = self.obj.tr( "Wrong file Version: {}".format(filename) )
		self.message = msg
		self.description = self.obj.tr( "The file was created to be used with SoulCreator {got}.".format(got=got))
		self.critical = False


class ErrXmlTooOldVersion(ErrXmlVersion):
	"""
	@brief Die Version der XML-Datei paßt zwar zu diesem Programm, ist aber viel zu alt.

	Die Version ist so alt, daß eine Verwendung dieser Ressource nicht empfehlenswert ist.
	"""

	def __init__(self, got="unknown", filename=None ):
		super(ErrXmlTooOldVersion, self).__init__()

		msg = self.obj.tr( "Wrong file Version." )
		if filename is not None:
			msg = self.obj.tr( "Wrong file Version: {}".format(filename) )
		self.message = msg
		self.description = self.obj.tr( "The file was created to be used with SoulCreator {}. This file is not usable with this version of SoulCreator.".format(got))




class ErrSpecies(Err):
	#"""
	#@brief Ausnahme, falls Fehler bei den Spezies auftritt.
	#"""

	def __init__(self ):
		super(ErrSpecies, self).__init__()

		self.message = self.obj.tr( "Problem with species occured." )
		self.description = self.obj.tr( "There is a problem with a character species.")


class ErrSpeciesNotExisting(ErrSpecies):
	#"""
	#@brief Ausnahme, falls eine spezifizierte Spezies nicht existiert.

	#Die erwartete Spezies wurde nicht gefunden.
	#"""

	def __init__(self, species = "unknown" ):
		super(ErrSpeciesNotExisting, self).__init__()

		self.message = self.obj.tr( "Problem with species occured." )
		self.description = self.obj.tr( "Species {} is missing.".format(species))




class ErrTrait(Err):
	"""
	@brief Ausnahme, falls Fehler bei den Eigenschaften auftritt.
	"""

	def __init__(self):
		super(ErrTrait, self).__init__()
		
		self.message = self.obj.tr( "Character Trait Problem" )
		self.description = self.obj.tr( "There is a problem with a character trait." )


class ErrTraitCategory(ErrTrait):
	"""
	@brief Ausnahme, falls eine falsche Kategorie genutzt wird.

	Die Kategorie exitiert nicht oder hat an dieser Stelle keine Gültigkeit.
	"""

	def __init__(self, category):
		super(ErrTraitCategory, self).__init__()

		self.message = self.obj.tr( "Category of a Trait not valid" )
		self.description = self.obj.tr( "The Category {} is not valid at this point.".format( category ))


class ErrTraitType(ErrTrait):
	"""
	@brief Ausnahme, falls ein falscher Typ genutzt wird.
	"""

	def __init__(self, expected, got):
		super(ErrTraitType, self).__init__()

		self.message = self.obj.tr( "Type of a Trait not valid" )
		typ = expected
		if type(expected) == list:
			typ = ", ".join(expected[:-1])
			typ += " or "
			typ += expected[-1]

		self.description = self.obj.tr( "Expected Trait of type {}, but got type {}, which is not valid at this point.".format(typ, got) )


