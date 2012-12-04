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




import os

from src.Config import Config
import src.Error as Error
#from src.Debug import Debug




class ReadXml(object):
	"""
	@brief Liest aus Xml-Dateien.

	Diese Klasse bietet die grundlegendsten Funktionen für das Lesen aus XML-Dateien.
	"""


	def __init__(self):
		pass


	def getElementAttribute(self, element, attribute):
		"""
		Gibt den Wert des Attributs aus oder, sollte es nicht esxistieren, einen leeren String.
		"""

		if attribute in element.attrib:
			return element.attrib[attribute]
		else:
			return ""


	def checkXmlVersion(self, name, version, filename=None ):
		"""
		Überprüft die Version der XML-Datei. Damit ist die SoulCreator-Version gemeint.
		"""

		if name == Config.programName:
			if version == Config.version():
				return
			else:
				# Unterschiede in der Minor-Version sind ignorierbar, Unterschiede in der Major-Version allerdings nicht.
				splitVersion = version.split(".")
				splitVersion = [int(item) for item in splitVersion]

				## Es ist darauf zu achten, daß Charaktere bis Version 0.6 nicht mit SoulCreator 0.7 und neuer geladen werden können.
				if filename is not None:
					filename = os.path.basename(filename)
				if( splitVersion[0] != Config.programVersionMajor or splitVersion[1] < 7):
					raise Error.ErrXmlTooOldVersion( version, filename )
				else:
					raise Error.ErrXmlOldVersion( version, filename )
		else:
			raise Error.ErrXmlVersion( "{} {}".format(Config.programName, Config.version()), "{} {}".format(name, version) )

