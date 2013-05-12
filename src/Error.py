# -*- coding: utf-8 -*-

"""
# Copyright

Copyright (C) 2012 by Victor
victor@caern.de

# License

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from PyQt4.QtCore import QObject

import src.Config as Config




class Err(Exception):
	"""
	@brief Basisklasse für die Ausnahmebehandlung

	Diese Klasse liegt allen eigenen Ausnahmebehandlungen zugrunde.

	\param critical (bool) Kritische Fehler führen zu einem Abbruch des Programms.
	"""

	def __init__( self, text=None, critical=False ):
		super().__init__()

		self.obj = QObject()

		if text is None:
			text = self.obj.tr( "Unknown generic Exception." )

		# Kurze Benachrichtigung der Ausnahme
		self.text = text
		self.critical = critical


	def __str__(self):
		return self.text




#class ErrList(Err):
	#"""
	#@brief Ausnahme bei Listen.
	#"""
	
	#def __init__(self):
		#super(ErrList, self).__init__()
		
		#self.message = self.obj.tr( "Unspecified Problem with a List." ) 
		#self.description = self.obj.tr( "An unspecified error occured while handling a List." ) 


#class ErrIndexExceedsRange(ErrList):
	#"""
	#@brief Index überschreitet Listengröße.
	#"""

	#def __init__(self, idx, listLen ):
		#super(ErrList, self).__init__()
		
		#self.message = self.obj.tr( "Index exceeds Range of List or Vector." ) 
		#self.description = self.obj.tr( "Index {} exceeds List Range of {}.".format(idx, listLen) )


#class ErrListLength(ErrList):
	#"""
	#@brief Listenlänge stimmt nicht mit erwartetem Wert überein.
	#"""

	#def __init__(self, expected, got ):
		#super(ErrListLength, self).__init__()

		#txt = "long"
		#if got < expected:
			#txt = "short"
		#self.message = self.obj.tr( "List to {}.".format(txt) ) 
		#self.description = self.obj.tr( "Got a List of length {}, but got a length of {}.".format(expected, got) ) 




class ErrFile(Err):
	"""
	@brief Ausnahme im Datei-Management.

	Allgemeine Fehler im Umgang mit Dateien werfen diese Ausnahme.
	"""
	
	def __init__(self, text=None, filename=None ):

		if text is None:
			text = self.obj.tr( "Unknown exception while handling a file." )

			if filename is not None:
				text = self.obj.tr( "Unknown exception while handling file \"{}\".".format( filename ) )

		super().__init__( text=text )

		self.filename = filename


class ErrFileNotOpened(ErrFile):
	"""
	@brief Datei kann nicht geöffnet werden.

	Das Programm kann die spezifizierte Datei nicht öffnen.
	"""

	def __init__(self, text=None, filename=None ):

		if text is None:
			text = self.obj.tr( "Could not open file." )

			if filename is not None:
				text = self.obj.tr( "Could not open file \"{}\".".format( filename ) )

		super().__init__( text=text, filename=filename )


#class ErrFileNotDeleted(ErrFile):
	#"""
	#@brief Datei kann nicht gelöscht werden.

	#Das Programm kann die spezifizierte Datei nicht löschen.
	#"""

	#def __init__(self, filename = "unknown" ):
		#super(ErrFileNotDeleted, self).__init__()

		#self.message = self.obj.tr( "Deletion not successful." ) 
		#self.description = self.obj.tr( "File {} could not be deleted.".format(filename ) )




class ErrXml(Err):
	"""
	@brief Ausnahme beim Umgang mit XML.
	"""

	def __init__(self, text=None, critical=False ):
		super().__init__( text=text, critical=critical )

		if text is None:
			text = self.obj.tr( "Unknown exception while handling XML." )
			self.text = text


class ErrXmlParsing(ErrXml):
	"""
	@brief Beim Parsen einer XML-Datei trat ein Fehler auf.

	Während das Programm versucht, eine XML-Datei zu parsen, tritt der im Argument spezifizierte Fehler auf.
	"""

	def __init__(self, text=None, critical=False ):
		super().__init__( text=text, critical=critical )

		if text is None:
			text = self.obj.tr( "Unknown exception while parsing XML." )
			self.text = text



class ErrXmlVersion(ErrXml):
	"""
	@brief Die XML-Datei weist die falsche Version auf.
	"""

	def __init__(self, text=None, got=None, expected=None, critical=False ):
		super().__init__( text=text, critical=critical )

		if text is None:
			text = self.obj.tr( "Wrong version number of XML-string." )

			if got is not None:
				if expected is not None:
					text += " " + self.obj.tr( "Got version {} but expected was {}.".format( got, expected ) )
				else:
					text += " " + self.obj.tr( "Got version {}.".format( got ) )

			self.text = text

		self.got = got
		self.expected = expected


class ErrXmlOldVersion(ErrXmlVersion):
	"""
	@brief Die Version der XML-Datei paßt zwar zu diesem Programm, ist aber zu alt.
	"""

	def __init__(self, text=None, got=None, critical=False ):
		super().__init__( text=text, got=got, critical=critical )

		if text is None:
			text = self.obj.tr( "Old Version of XML-string." )

			if got is not None:
				text += " " + self.obj.tr( "Was created for {} {}.".format( Config.PROGRAM_NAME, got ) )

			self.text = text




class ErrSpecies(Err):
	#"""
	#@brief Ausnahme, falls Fehler bei den Spezies auftritt.
	#"""

	def __init__(self, text=None, critical=False ):
		super().__init__( text=text, critical=critical )
		
		if text is None:
			text = self.obj.tr( "Unknown error with character species." )

			self.text = text


class ErrSpeciesNotExisting(ErrSpecies):
	"""
	@brief Ausnahme, falls eine spezifizierte Spezies nicht existiert.

	Die erwartete Spezies wurde nicht gefunden.
	"""

	def __init__(self, text=None, species=None, critical=False ):
		super().__init__( text=text, critical=critical )

		if text is None:
			text = self.obj.tr( "Species does not exist." )

			if species is not None:
				text = self.obj.tr( "Species \"{}\" does not exist.".format( species ) )

			self.text = text





class ErrTrait(Err):
	"""
	@brief Ausnahme, falls Fehler bei den Eigenschaften auftritt.
	"""

	def __init__(self, text=None, critical=False ):
		super().__init__( text=text, critical=critical )

		if text is None:
			text = self.obj.tr( "Unknown error with character trait." )

			self.text = text


#class ErrTraitCategory(ErrTrait):
	#"""
	#@brief Ausnahme, falls eine falsche Kategorie genutzt wird.

	#Die Kategorie exitiert nicht oder hat an dieser Stelle keine Gültigkeit.
	#"""

	#def __init__(self, category):
		#super(ErrTraitCategory, self).__init__()

		#self.message = self.obj.tr( "Category of a Trait not valid" )
		#self.description = self.obj.tr( "The Category {} is not valid at this point.".format( category ))


class ErrTraitType(ErrTrait):
	"""
	@brief Ausnahme, falls ein falscher Typ genutzt wird.
	"""

	def __init__(self, text=None, got=None, expected=None, critical=False ):
		super().__init__( text=text, critical=critical )

		if text is None:
			text = self.obj.tr( "Type of character trait is not valid." )

			if got is not None:
				if expected is not None:
					expected_text = "{} or {}".format( ", ".join( expected[:-1], expected[-1] ) )
					text += self.obj.tr( "Got {} but expected {}.".format( got, expected_text ) )
				else:
					text += self.obj.tr( "Got {}.".format( got ) )

			self.text = text


#class ErrTraitPrerequisite(ErrTrait):
	#"""
	#Ungültige Voraussetzung für die Eigenschaft.
	#"""

	#def __init__(self, trait):
		#super().__init__()

		#self.message = self.obj.tr( "Prerequisit of a Trait not valid" )
		#self.description = self.obj.tr( "Some or all prerequisites of the trait \"{}\" is not valid.".format( trait ))
