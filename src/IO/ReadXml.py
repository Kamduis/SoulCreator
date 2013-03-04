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

import src.Config as Config
import src.Error as Error
import src.Debug as Debug




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


	def checkXmlVersion(self, name, version, filename=None, required=False ):
		"""
		Überprüft die Version der XML-Datei. Damit ist die SoulCreator-Version gemeint.

		\param required Für den Betrieb des Programms erfordelriche Dateien sorgen dafür, daß das Programm einen entsprechend ernsten Fehler ausgibt.
		"""

		Debug.debug( "Version of file \"{name_file}\": {name} {version}".format(
			name_file=filename,
			name=name,
			version=version,
		), level=3 )

		if name == Config.PROGRAM_NAME:
			if version == Config.version():
				return
			else:
				# Unterschiede in der Minor-Version sind ignorierbar, Unterschiede in der Major-Version allerdings nicht.
				version_split = version.split(".")
				version_split = [ int(item) for item in version_split ]

				if filename is not None:
					filename = os.path.basename(filename)
				if version_split[0] < Config.PROGRAM_VERSION["major"]:
					raise Error.ErrXmlVersion(
						"XML-file \"{filename}\" was created with {program_name} {file_version} and is incompatible with {program_name} {program_version}.\nLoading of file aborted.".format(
							filename=filename,
							file_version=version,
							program_name=Config.PROGRAM_NAME,
							program_version=Config.version()
						),
						got=version,
						critical=required
					)
				else:
					raise Error.ErrXmlOldVersion(
						"XML-file \"{filename}\" was created with {program_name} {file_version} and may be compatible with {program_name} {program_version}.".format(
							filename=filename,
							file_version=version,
							program_name=Config.PROGRAM_NAME,
							program_version=Config.version()
						),
						got=version,
						critical=required
					)
		else:
			raise Error.ErrXmlVersion(
				got="{} {}".format(name, version),
				expected="{} {}".format(Config.PROGRAM_NAME, Config.version()),
				critical=required
			)

