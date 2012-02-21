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

from PySide.QtCore import Qt, QObject, QFile, QIODevice, QTextStream, QBuffer, QByteArray, QUrl, QRect
from PySide.QtGui import QPainter, QImage, QPalette#, QColor, QPen, QFont, QFontMetrics, QTextDocument
from PySide.QtWebKit import QWebPage

#from src.GlobalState import GlobalState
from src.Config import Config
from src.Error import ErrFileNotOpened
#from src.Random import Random
from src.Datatypes.Identity import Identity
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
		palette = self.__page.palette()
		palette.setBrush(QPalette.Base, Qt.transparent)
		self.__page.setPalette(palette)

		self.__mainFrame = self.__page.mainFrame()

		## Erzeuge für jedes im Charakterbogen vorkommende Bild eine temporäre Datei
		resourceFiles = (
			":sheet/stylesheets/sheet.css",
			":sheet/stylesheets/sheetTemplate.html",
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
		with open(self.__resourceFiles[":sheet/stylesheets/sheetTemplate.html"].name) as f:
			htmlText = f.read()

		htmlText = unicode(htmlText).format(
			stylesheet=QUrl.fromLocalFile(self.__resourceFiles[":sheet/stylesheets/sheet.css"].name).toString(),
			species=self.__character.species.lower(),
			info=self._createInfo(),
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

		tableContents = [
			[
				"Name:", Identity.displayNameDisplay(self.__character.identity.surname, self.__character.identity.firstname, self.__character.identity.nickname),
				"Virtue:", self.__character.virtue,
				"Chronicle:", "",
			],
			[
				"", "",
				"Vice:", self.__character.vice,
				"{}:".format(self.__storage.factionTitle(self.__character.species)), self.__character.faction,
			],
		]
		if self.__character.species != "Human":
			tableContents = [
				[
					tableContents[0][0], tableContents[0][1],
					tableContents[0][2], tableContents[0][3],
					"{}:".format(self.__storage.breedTitle(self.__character.species)), self.__character.breed,
				],
				[
					"Secret Name", self.__character.identity.supername,
					tableContents[1][2], tableContents[1][3],
					tableContents[1][4], tableContents[1][5],
				],
				[
					tableContents[1][0], tableContents[1][1],
					"{}:".format(self.__storage.partyTitle(self.__character.species)), self.__character.party,
					"{}:".format(self.__storage.organisationTitle(self.__character.species)), self.__character.organisation,
				],
			]

			if self.__character.species == "Changeling":
				tableContents[0][4] = "{}:".format(self.__storage.breedTitle(self.__character.species))
				tableContents[0][5] ="{} ({})".format(self.__character.breed, self.__character.kith)
			elif self.__character.species == "Mage":
				tableContents[1][0] = "Shadow Name:"
			elif self.__character.species == "Vampire":
				tableContents[2][0] = "Sire:"
				tableContents[2][1] = ""
			elif self.__character.species == "Werewolf":
				tableContents[1][0] = "Deed Name:"
				tableContents[2][0] = "Totem:"
				tableContents[2][1] = self.__character.companionName

		htmlText = "<table>"
		htmlText += "<colgroup><col width='1*'><col width='2*'><col width='1*'><col width='2*'><col width='1*'><col width='2*'></colgroup>"
		for row in tableContents:
			htmlText += "<tr>"
			for column in row:
				htmlText += u"<td>{}</td>".format(column)
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
		
		scaleFactor = (
			self.__printer.width() / contentsSize.width(),
			self.__printer.height() / contentsSize.height(),
		)
		#self.__painter.scale(scaleFactor[0], scaleFactor[1])
		scale = min(scaleFactor)
		self.__painter.scale(scale, scale)
		self.__painter.setRenderHint ( QPainter.Antialiasing )

		self.__paperSize = (
			self.__printer.width() / scale,
			self.__printer.height() / scale,
		)

		self.__painter.save()

		## Hintergrundbild:
		self._drawBackground()
		posY = 0.01 * self.__paperSize[1]
		width = 0.3 * self.__paperSize[0]
		#if self.__character.species == "Changeling":
			#width = 950
		#elif self.__character.species == "Mage":
			#width = 780
		#elif self.__character.species == "Vampire":
			#posY = -80
			#width = 500
		#elif self.__character.species == "Werewolf":
			#width = 780
		self._drawLogo(posY, width)

		## HTML-Struktur drucken.
		self.__mainFrame.render ( self.__painter )

		self.__painter.restore()
		
		self.__painter.end()

		for tmp in self.__resourceFiles.values():
			os.remove("{}".format(tmp.name))


	def _drawBackground(self):
		"""
		Der Hintergrund für den Charakterbogen wird dargestellt.
		"""

		self.__painter.save()

		rect = QRect(0, 0, self.__paperSize[0], self.__paperSize[1])
		if self.__character.species == "Changeling":
			image = QImage(":sheet/images/sheet/Changeling-Background.jpg")
			self.__painter.drawImage(rect, image)
		elif self.__character.species == "Mage":
			pass
		elif self.__character.species == "Vampire":
			image = QImage(":sheet/images/sheet/Vampire-Background.jpg")
			self.__painter.drawImage(rect, image)
		elif self.__character.species == "Werewolf":
			imageShapes = QImage(":sheet/images/sheet/Werewolf-Shapes.jpg")
			imageShapes = imageShapes.scaledToWidth(self.__paperSize[0])
			rectShapes = QRect(0, 0 - self.__paperSize[1] - imageShapes.height(), self.__paperSize[0], imageShapes.height())
			self.__painter.drawImage(rectShapes, imageShapes)

			## Dieses Bild wird später gezeichnet, damit es nicht von den Gestalten abgeschnitten wird.
			offsetV = 80
			image = QImage(":sheet/images/sheet/Werewolf-Background.png")
			image = image.scaledToHeight(self.__paperSize[1] - imageShapes.height() - offsetV)
			rect = QRect(0 + (self.__paperSize[0] - image.width()) / 2, offsetV, image.width(), image.height())
			self.__painter.drawImage(rect, image)
		else:
			image = QImage(":sheet/images/sheet/WorldOfDarkness-BackgroundL.png")
			image = image.scaledToHeight(self.__paperSize[1])
			rect = QRect(0, 0, image.width(), image.height())
			self.__painter.drawImage(rect, image)

			image = QImage(":sheet/images/sheet/WorldOfDarkness-BackgroundR.png")
			image = image.scaledToHeight(self.__paperSize[1])
			rect = QRect(0, 0, image.width(), image.height())
			self.__painter.drawImage(rect, image)

		self.__painter.restore()


	def _drawLogo(self, offsetV, width, height=None):
		"""
		Zeichnet das Logo auf den Charakterbogen. Das Logo wird auf der Seite immer horizontal zentriert dargestellt.
		"""

		self.__painter.save()

		offsetH = (self.__paperSize[0] - width) / 2

		image = QImage(":sheet/images/sheet/WorldOfDarkness.jpg")
		if self.__character.species == "Changeling":
			image = QImage(":sheet/images/sheet/Changeling.png")
		elif self.__character.species == "Mage":
			image = QImage(":sheet/images/sheet/Mage.png")
		if self.__character.species == "Vampire":
			image = QImage(":sheet/images/sheet/Vampire.png")
		if self.__character.species == "Werewolf":
			image = QImage(":sheet/images/sheet/Werewolf.png")
		else:
			pass

		rect = QRect(offsetH, offsetV, width, image.height() * width / image.width())

		self.__painter.drawImage(rect, image)

		self.__painter.restore()




