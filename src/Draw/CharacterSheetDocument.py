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

from PySide.QtCore import QFile, QIODevice, QTextStream
from PySide.QtGui import QTextDocument

#from src.Debug import Debug




class CharacterSheetDocument(QTextDocument):
	"""
	@brief Ein TextDocument, welches standardmäßig mit dem Format für die Charkaterbögen geladen wird.
	"""
	
	
	def __init__(self, parent=None):
		QTextDocument.__init__(self, parent)

		## Lade Datei mit Stylesheet-Informationen
		cssFile = QFile(":stylesheets/sheet.css")
		if not cssFile.open(QIODevice.ReadOnly):
			raise ErrFileNotOpened(item, cssFile.errorString())
		cssStream = QTextStream(cssFile)
		cssContent = cssStream.readAll()
		#cssContent = cssFile.readAll()
		cssFile.close()

		#document.addResource(QTextDocument.StyleSheetResource, QUrl("stylesheet.css"), cssContent)
		self.setDefaultStyleSheet(cssContent)

		#htmlHeader = "<html><head><link rel='stylesheet' type='text/css' href='stylesheet.css'></head><body>"
		


