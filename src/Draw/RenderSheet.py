# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) Victor von Rhein, 2011, 2012

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http:##www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

import os
import tempfile
import math
#import copy

from PySide.QtCore import QObject, QFile, QIODevice, QTextStream, QBuffer, QByteArray, QUrl
from PySide.QtGui import QPainter, QImage#, QColor, QPen, QFont, QFontMetrics, QTextDocument
from PySide.QtWebKit import QWebPage

#from src.GlobalState import GlobalState
from src.Config import Config
from src.Error import ErrFileNotOpened
#from src.Random import Random
#from src.Datatypes.Identity import Identity
from src.Calc.CalcAdvantages import CalcAdvantages
#from src.Calc.CalcShapes import CalcShapes
#from src.Draw.CharacterSheetDocument import CharacterSheetDocument
#from src.Tools import ImageTools
from src.Debug import Debug




class RenderSheet(QObject):
	"""
	\brief Führt das Drucken des Charakters aus.

	Mit Hilfe dieser Klasse können die Charakterwerte auf Papier gebannt werden.
	"""

	def __init__(self, template, character, printer, parent=None):
		QObject.__init__(self, parent)

		self.__storage = template
		self.__character = character
		self.__calc = CalcAdvantages(self.__character)

		self.__painter = QPainter()
		self.__printer = printer

		#self.__htmlFileLike = None

		self.__page = QWebPage(self)
		self.__mainFrame = self.__page.mainFrame()
		
		## Erzeuge für jedes im Charakterbogen vorkommende Bild eine temporäre Datei
		resourceFiles = (
			":characterSheets/stylesheets/sheet.css",
			":characterSheets/stylesheets/sheetTemplate.html",
			":sheet/images/sheet/WorldOfDarkness.jpg",
		)
		self.__resourceFiles = {}
		for resFile in resourceFiles:
			qrcFile = QFile(resFile)
			if not qrcFile.open(QIODevice.ReadOnly):
				raise ErrFileNotOpened(resFile, qrcFile.errorString())
			fileContent = qrcFile.readAll()
			qrcFile.close()
			fileLike = tempfile.NamedTemporaryFile(delete=False)
			fileLike.write(fileContent)
			fileLike.seek(0)
			fileLike.close()
			self.__resourceFiles[resFile] = fileLike

		self.__mainFrame.loadFinished.connect(self.__renderPdf)


	def createSheets(self):
		"""
		Erzeugt den Charakterbogen.
		"""

		htmlText = ""
		with open(self.__resourceFiles[":characterSheets/stylesheets/sheetTemplate.html"].name) as f:
			htmlText = f.read()

		htmlText = htmlText.format(
			stylesheet=QUrl.fromLocalFile(self.__resourceFiles[":characterSheets/stylesheets/sheet.css"].name).toString(),
			species=self.__character.species.lower(),
			logo=QUrl.fromLocalFile(self.htmlImage(":sheet/images/sheet/WorldOfDarkness.jpg")).toString(),
			logoWidth="100px",
			#info=self._createInfo(),
			info="",
			attributes=self._createAttributes(),
			skills=self._createSkills(),
		)

		#Debug.debug(htmlText)

		self.__mainFrame.setHtml(htmlText)
		#Debug.debug(QUrl.fromLocalFile(self.__htmlFileLike.name))

		##Das Rendern in PDF wird durch das Signal ausgelöst, welches gesendet wird, sobald der HTML-Text fertig geladen ist.


	def _createInfo(self):
		"""
		Erzeugt die Darstellung der Informationen.
		"""

		htmlText = "<table>"
		for category in Config.attributes:
			htmlText += "<tr>"
			htmlText += "<td><span id='{species}'>{category}</span></td>".format(species=self.__character.species, category=category[0])
			for attribute in category[1]:
				trait = self.__character.traits["Attribute"][category[0]][attribute]
				htmlText += "<td>{}</td><td>{}</td>".format(trait.name, trait.totalvalue)
			htmlText += "</tr>"
		htmlText += "</table>"

		return htmlText


	def _createAttributes(self):
		"""
		Erzeugt die Darstellung der Fertigkeiten.
		"""

		htmlText = "<table>"
		for category in Config.attributes:
			htmlText += "<tr>"
			htmlText += "<td><span id='{species}'>{category}</span></td>".format(species=self.__character.species, category=category[0])
			for attribute in category[1]:
				trait = self.__character.traits["Attribute"][category[0]][attribute]
				htmlText += "<td>{}</td><td>{}</td>".format(trait.name, trait.totalvalue)
			htmlText += "</tr>"
		htmlText += "</table>"

		return htmlText


	def _createSkills(self):
		"""
		Erzeugt die Darstellung der Attribute.
		"""

		htmlText = ""
		for item in self.__character.traits["Skill"]:
			traits = self.__character.traits["Skill"][item].keys()
			traits.sort()
			htmlText += "<h2 class='{species}'>{category}</h2>".format(species=self.__character.species.lower(), category=item)
			htmlText += "<table>"
			for subitem in traits:
				trait = self.__character.traits["Skill"][item][subitem]
				if (
					(not trait.era or trait.era == self.__character.era) and
					(not trait.age or trait.age == Config.getAge(self.__character.age))
				):
					htmlText += "<tr>"
					htmlText += "<td>{}</td><td>{}</td>".format(trait.name, trait.totalvalue)
					htmlText += "</tr>"
			htmlText += "</table>"

		return htmlText


	def htmlImage(self, imagePath):
		return "{}".format(self.__resourceFiles[imagePath].name)


	def __renderPdf(self, status=None):
		"""
		Wandelt das Html-Layout in pdf-Format um.
		"""

		#Debug.debug("Status ist {}".format(status))

		contentsSize = self.__mainFrame.contentsSize()
		#Debug.debug(contentsSize)
		self.__page.setViewportSize ( contentsSize )

		self.__painter.begin(self.__printer)
		
		self.__paperWidth_defined = contentsSize.width()
		#self.__paperHeight_defined = int(self.__paperWidth_defined * math.sqrt(2))
		#self.__paperHeight_defined = contentsSize.height()
		self.__paperWidth_real = self.__printer.width()
		self.__paperHeight_real = self.__printer.height()
		
		scaleFactor = (
			self.__paperWidth_real / self.__paperWidth_defined,
			#self.__paperHeight_real / self.__paperHeight_defined,
		)
		#self.__painter.scale(scaleFactor[0], scaleFactor[1])
		self.__painter.scale(scaleFactor[0], scaleFactor[0])
		self.__painter.setRenderHint ( QPainter.Antialiasing )
		self.__mainFrame.render ( self.__painter )
		
		#Debug.debug(self.__mainFrame.renderTreeDump())
		
		self.__painter.end()

		#for tmp in self.__resourceFiles.values():
			#os.remove("{}".format(tmp.name))

		#if self.__htmlFileLike:
			#os.remove(self.__htmlFileLike.name)




