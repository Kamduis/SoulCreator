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

from src.Config import Config
import src.Error as Error
from src.Debug import Debug

## Fallback to normal ElementTree, sollte lxml nicht installiert sein.
lxmlLoadad = False
try:
	from lxml import etree
	#Debug.debug("Running with lxml.etree")
	lxmlLoadad = True
except ImportError:
	try:
		# Python 2.5
		import xml.etree.cElementTree as etree
		Debug.debug("running with cElementTree on Python 2.5+")
	except ImportError:
		try:
			# Python 2.5
			import xml.etree.ElementTree as etree
			Debug.debug("running with ElementTree on Python 2.5+")
		except ImportError:
			Debug.debug("Failed to import ElementTree from any known place")




class ReadXml(object):
	"""
	@brief Liest aus Xml-Dateien.

	Diese Klasse bietet die grundlegendsten Funktionen für das Lesen aus XML-Dateien.
	"""


	def __init__(self):
		pass


	def checkXmlVersion(self, name, version ):
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
				if( splitVersion[0] != Config.programVersionMajor or splitVersion[1] < 7):
					raise Error.ErrXmlTooOldVersion( version )
				else:
					raise Error.ErrXmlOldVersion( version )
		else:
			raise Error.ErrXmlVersion( "{} {}".format(Config.programName, Config.version()), "{} {}".format(name, version) )

