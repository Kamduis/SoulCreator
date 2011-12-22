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

##include <QDebug>

##include "Exceptions/Exception.h"
#// #include "Config/Config.h"

##include "ReadXml.h"



from __future__ import division, print_function

from PySide.QtCore import QXmlStreamReader, QIODevice

from src.Config import Config
from src.Error import ErrXmlTooOldVersion

##include "CMakeConfig.h"

#// #include "Exceptions/Exception.h"

##include "Config.h"




class ReadXml(QXmlStreamReader):
	"""
	@brief List aus Xml-Dateien.

	Diese Klasse bietet die grundlegendsten Funktionen für das Lesen aus Xml-Dateien.
	"""


	def __init__(self):
		QXmlStreamReader.__init__(self)


	def openFile( self, f ):
		"""
		Öffnet die im Argument übergebe Datei.

		\exception eFileNotOpen Diese Ausnahme wird geworfen, wenn die XML-DaTei nicht geöffnet werden konnte.
		"""

		if not f.open( QIODevice.ReadOnly | QIODevice.Text ) :
			raise eFileNotOpened( f.fileName(), f.errorString() )


	def closeFile(self, f ):
		"""
		Schließt die im Argument übergebe Datei.
		"""

		f.close()


	def readUnknownElement(self):
		"""
		Diese Funktion wird immer dann aufgerufen, wenn ein Zweig mit unbekanntem Namen entsdeckt wird. Diese Funktion marschiert bis zum Ende dieses Zweiges.
		"""
		
		while not self.atEnd():
			self.readNext()

			if self.isEndElement():
				break

			if self.isStartElement():
				#qDebug() << Q_FUNC_INFO << "unbekanntes Element: " << name();
				self.readUnknownElement()


	def checkXmlVersion(self, name, version ):
		if name == Config.programName:
			if version == Config.version():
				return True
			else:
				# Unterschiede in der Minor-Version sind ignorierbar, unterschiede in der Major-Version allerdings nicht.
				splitVersion = version.split(".")

				if( splitVersion[0] == Config.programVersionMajor ):
					raise ErrXmlOldVersion( Config.version(), version )
				else:
					raise ErrXmlTooOldVersion( Config.version(), version )
		else:
			raise ErrXmlVersion( "{} {}".format(Config.programName, Config.version()), "{} {}".format(name, version) )

		return False

