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
from src.Tools import ImageTools
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

		## Erzeuge Temporäre DAteien, ums sie in HTML laden zu können.
		persistentResourceFiles = (
			":sheet/stylesheets/sheet.css",
		)
		self.__persistentResourceFiles = {}
		for resFile in persistentResourceFiles:
			qrcFile = QFile(resFile)
			if not qrcFile.open(QIODevice.ReadOnly):
				raise ErrFileNotOpened(resFile, qrcFile.errorString())
			fileContent = qrcFile.readAll()
			qrcFile.close()
			fileLike = tempfile.NamedTemporaryFile(delete=False)
			fileLike.write(fileContent)
			fileLike.seek(0)
			fileLike.close()
			self.__persistentResourceFiles[resFile] = fileLike

		htmlTemplates = {
			0: ":sheet/stylesheets/sheetTemplate.html",
			"Human": ":sheet/stylesheets/sheetTemplate-Human.html",
			"Changeling": ":sheet/stylesheets/sheetTemplate-Changeling.html",
			"Mage": ":sheet/stylesheets/sheetTemplate-Mage.html",
			"Vampire": ":sheet/stylesheets/sheetTemplate-Vampire.html",
			"Werewolf": ":sheet/stylesheets/sheetTemplate-Werewolf.html",
		}
		self.__htmlTemplates = {}
		for species in htmlTemplates.items():
			qrcFile = QFile(species[1])
			if not qrcFile.open(QIODevice.ReadOnly):
				raise ErrFileNotOpened(resFile, qrcFile.errorString())
			textStream = QTextStream(qrcFile)
			fileContent = textStream.readAll()
			qrcFile.close()
			self.__htmlTemplates[species[0]] = fileContent

		self.traitMax = self.__storage.maxTrait(self.__character.species, self.__character.powerstat)

		self.__mainFrame.loadFinished.connect(self.__renderPdf)


	def createSheets(self):
		"""
		Erzeugt den Charakterbogen.
		"""

		htmlText = self.__htmlTemplates[0]

		htmlText = htmlText.format(
			stylesheet=QUrl.fromLocalFile(self.__persistentResourceFiles[":sheet/stylesheets/sheet.css"].name).toString(),
			body=self.__htmlTemplates[self.__character.species],
		)

		htmlText = unicode(htmlText).format(
			info=self._createInfo(),
			attributes=self._createAttributes(),
			skills=self._createSkills(),
			powers=self._createPowers(),
			merits=self._createMerits(),
			flaws=self._createFlaws(),
			advantages=self._createAdvantages(),
			weapons=self._createWeapons(),
			goblinContracts=self._createGoblinContracts(),
			magicalTool=self.simpleTextBox(self.__character.magicalTool, title=self.tr("Magical Tool"), species="Mage"),
			vinculi=self._createVinculi(),
			inventory=self.simpleTextBox("; ".join(self.__character.equipment), title=self.tr("Inventory")),
			description=self._createDescription(),
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
				[ "Name:", Identity.displayNameDisplay(self.__character.identity.surname, self.__character.identity.firstname, self.__character.identity.nickname), ],
				[ "Virtue:", self.__character.virtue, ],
				[ "Chronicle:", "", ],
			],
			[
				[ "", "", ],
				[ "Vice:", self.__character.vice, ],
				[ "{}:".format(self.__storage.factionTitle(self.__character.species)), self.__character.faction, ],
			],
		]
		if self.__character.species != "Human":
			tableContents = [
				[
					[ tableContents[0][0][0], tableContents[0][0][1], ],
					[ tableContents[0][1][0], tableContents[0][1][1], ],
					[ "{}:".format(self.__storage.breedTitle(self.__character.species)), self.__character.breed, ],
				],
				[
					[ "Secret Name:", self.__character.identity.supername, ],
					[ tableContents[1][1][0], tableContents[1][1][1], ],
					[ tableContents[1][2][0], tableContents[1][2][1], ],
				],
				[
					[ tableContents[1][0][0], tableContents[1][0][1], ],
					[ "{}:".format(self.__storage.partyTitle(self.__character.species)), self.__character.party, ],
					[ "{}:".format(self.__storage.organisationTitle(self.__character.species)), self.__character.organisation, ],
				],
			]

			if self.__character.species == "Changeling":
				tableContents[0][2][0] = "{}:".format(self.__storage.breedTitle(self.__character.species))
				tableContents[0][2][1] ="{} ({})".format(self.__character.breed, self.__character.kith)
			elif self.__character.species == "Mage":
				tableContents[1][0][0] = "Shadow Name:"
			elif self.__character.species == "Vampire":
				tableContents[2][0][0] = "Sire:"
				tableContents[2][0][1] = ""
			elif self.__character.species == "Werewolf":
				tableContents[1][0][0] = "Deed Name:"
				tableContents[2][0][0] = "Totem:"
				tableContents[2][0][1] = self.__character.companionName

		htmlText = "<table class='fullWidth'>"
		for row in tableContents:
			htmlText += "<tr>"
			for column in row:
				htmlText += u"<td align='right'>{label}</td><td style='width: 25%;'><span id='scriptFont'>{value}</span></td>".format(label=column[0], value=column[1])
			htmlText += "</tr>"
		htmlText += "</table>"

		return htmlText


	def _createAttributes(self):
		"""
		Erzeugt die Darstellung der Fertigkeiten.
		"""

		htmlText = u"<table class='fullWidth'>"
		for category in Config.attributes:
			htmlText += u"<tr>"
			htmlText += u"<td><span id='{species}'>{category}</span></td>".format(species=self.__character.species, category=category[0])
			for attribute in category[1]:
				trait = self.__character.traits["Attribute"][category[0]][attribute]
				htmlText += u"<td style='width: 33%; text-align: right;'>{label}</td><td  style='text-align: right;'>{value}</td>".format(label=trait.name, value=self.valueStyled(trait.totalvalue, self.traitMax))
			htmlText += u"</tr>"
		htmlText += u"</table>"

		return htmlText


	def _createSkills(self):
		"""
		Erzeugt die Darstellung der Fertigkeiten und Spezialisierungen.
		"""

		htmlText = u""
		for item in self.__character.traits["Skill"]:
			traits = self.__character.traits["Skill"][item].keys()
			traits.sort()
			htmlText += u"<h2 class='{species}'>{category}</h2>".format(species=self.__character.species.lower(), category=item)
			#htmlText += u"<dl class='dottedList'>"
			for subitem in traits:
				trait = self.__character.traits["Skill"][item][subitem]
				if (
					(not trait.era or trait.era == self.__character.era) and
					(not trait.age or trait.age == Config.getAge(self.__character.age))
				):
					htmlText += u"<table class='fullWidth'>"
					htmlText += u"<tr>"
					htmlText += u"<td class='nowrap'>{label}</td>".format(label=trait.name)
					htmlText += u"<td style='width: 100%;'><span id='specialties'>{specialties}</span></td>".format(specialties=", ".join(trait.totalspecialties))
					htmlText += u"<td class='nowrap' style='text-align: right;'>{value}</td>".format(value=self.valueStyled(trait.totalvalue, self.traitMax))
					htmlText += u"</tr>"
					htmlText += u"</table>"
					#htmlText += u"<dt>{label}<span id='{specialties}'>{specialties}</span></dt><dd>{value}</dd>".format(label=trait.name, specialties=", ".join(trait.totalspecialties), value=self.valueStyled(trait.totalvalue, self.traitMax))
			#htmlText += u"</dl>"

		return htmlText


	def _createPowers(self):
		"""
		Erzeugt die Darstellung der übernatürlichen Kräfte.
		"""

		if self.__character.species not in ( "Human", ):
			twocolumn = False
			if self.__character.species in ( "Mage", "Werewolf", ):
				twocolumn = True

			traitList = []
			for item in self.__character.traits["Power"]:
				traits = self.__character.traits["Power"][item].keys()
				traits.sort()
				for key in traits:
					trait = self.__character.traits["Power"][item][key]
					if trait.isAvailable and self.__character.species == trait.species and (trait.value > 0 or self.__character.species in ( "Mage", "Werewolf", )):
						traitList.append(trait)

			iteratorGoal = ( len(traitList), )
			columnWidth = "100%"
			if twocolumn:
				iteratorGoal = (
					( 0, int(math.floor(len(traitList) / 2)), ),
					( int(math.floor(len(traitList) / 2)), len(traitList), ),
				)
				columnWidth = "50%"

			htmlText = u"<h1 class='{species}'>{title}</h1>".format(title=self.__storage.powerName(self.__character.species), species=self.__character.species)

			htmlText += u"<table style='width: {};'><tr>".format(columnWidth)
			for column in iteratorGoal:
				htmlText += u"<td>".format(columnWidth)
				for i in xrange(column[0], column[1]):
					trait = traitList[i]
					htmlText += u"<table class='fullWidth'>"
					htmlText += u"<tr>"
					htmlText += u"<td class='nowrap'>{label}</td>".format(label=trait.name)
					htmlText += u"<td style='width: 100%;'><span id='specialties'>{specialties}</span></td>".format(specialties=trait.customText)
					htmlText += u"<td class='nowrap' style='text-align: right;'>{value}</td>".format(value=self.valueStyled(trait.totalvalue, self.traitMax))
					htmlText += u"</tr>"
					htmlText += u"</table>"
				htmlText += u"</td>"
			htmlText += u"</tr></table>"

			return htmlText
		else:
			return ""


	def _createMerits(self):
		"""
		Erzeugt die Darstellung der Merits.
		"""

		htmlText = u"<h1 class='{species}'>Merits</h1>".format(species=self.__character.species)
		for item in self.__character.traits["Merit"]:
			traits = self.__character.traits["Merit"][item].keys()
			traits.sort()
			for subitem in traits:
				trait = self.__character.traits["Merit"][item][subitem]
				if trait.isAvailable and trait.value > 0:
					htmlText += u"<table class='fullWidth'>"
					htmlText += u"<tr>"
					htmlText += u"<td class='nowrap'>{label}</td>".format(label=trait.name)
					htmlText += u"<td style='width: 100%;'><span id='specialties'>{specialties}</span></td>".format(specialties=trait.customText)
					htmlText += u"<td class='nowrap' style='text-align: right;'>{value}</td>".format(value=self.valueStyled(trait.totalvalue, self.traitMax))
					htmlText += u"</tr>"
					htmlText += u"</table>"

		return htmlText


	def _createFlaws(self):
		"""
		Erzeugt die Darstellung der Merits.
		"""

		flaws = []
		for item in self.__character.traits["Flaw"]:
			traits = self.__character.traits["Flaw"][item].values()
			traits.sort()
			for subitem in traits:
				if subitem.isAvailable and subitem.value > 0:
					text = subitem.name
					if subitem.customText:
						text += " ({})".format(subitem.customText)
					flaws.append(text)

		return self.simpleTextBox("; ".join(flaws), title=self.tr("Flaws"))


	def _createAdvantages(self):
		"""
		Erzeugt die Darstellung der berechneten Werte.
		"""

		htmlText = u""
		if self.__character.species != "Werewolf":
			armor = [ 0, 0 ]
			if self.__character.armor["name"] in self.__storage.armor:
				armor[0] = self.__storage.armor[self.__character.armor["name"]]["general"]
				armor[1] = self.__storage.armor[self.__character.armor["name"]]["firearms"]

			advantages = (
				( self.tr("Size"), self.__calc.calcSize(), ),
				( self.tr("Initiative"), self.__calc.calcInitiative(), ),
				( self.tr("Speed"), self.__calc.calcSpeed(), ),
				( self.tr("Defense"), self.__calc.calcDefense(), ),
				( self.tr("Armor"), "{general}/{firearms}".format(general=armor[0], firearms=armor[1]), ),
			)

			for item in advantages:
				htmlText += u"<table class='fullWidth'>"
				htmlText += u"<tr>"
				htmlText += u"<td style='width: 100%;'>{label}</td>".format(label=item[0])
				htmlText += u"<td class='nowrap' style='text-align: right;'>{value}</td>".format(value=item[1])
				htmlText += u"</tr>"
				htmlText += u"</table>"

		## ((Name, Wert, Max, Kreise /und/ Quadrate, verbotene Spezies))
		energy = (
			( self.tr("Health"), self.__calc.calcHealth(), Config.healthMax, True, (), ),
			( self.tr("Willpower"), self.__calc.calcWillpower(), Config.willpowerMax, True, (), ),
			( self.__storage.powerstatName(self.__character.species), self.__character.powerstat, Config.powerstatMax, False, ("Human"), ),
		)

		for item in energy:
			if self.__character.species not in item[4]:
				htmlText += u"<h1 class='{species}'>{title}</h1>".format(title=item[0], species=self.__character.species)
				htmlText += u"<table class='fullWidth'>"
				htmlText += u"<tr>"
				for i in xrange(item[1]):
					htmlText += u"<td style='text-align: center;'>{}</td>".format(self.valueStyled(1))
				for i in xrange(item[1], item[2]):
					htmlText += u"<td style='text-align: center;'>{}</td>".format(self.valueStyled(0, 1))
				htmlText += u"</tr>"
				if item[3]:
					htmlText += u"<tr>"
					for i in xrange(item[2]):
						htmlText += u"<td style='text-align: center;'>{}</td>".format(self.valueStyled(0, 1, squares=True))
					htmlText += u"</tr>"
				htmlText += u"</table>"

		maxPerRow = 10

		if self.__character.species not in ( "Human", ):
			htmlText += u"<h1 class='{species}'>{title}</h1>".format(title=self.__storage.fuelName(self.__character.species), species=self.__character.species)
			htmlText += u"<table class='fullWidth'>"
			htmlText += u"<tr>"
			value = self.__storage.fuelMax(species=self.__character.species, powerstat=self.__character.powerstat)
			while value > maxPerRow:
				value -= maxPerRow
				for i in xrange(maxPerRow):
					htmlText += u"<td style='text-align: center;'>{}</td>".format(self.valueStyled(0, 1, squares=True))
				htmlText += u"</tr><tr>"
			for i in xrange(value):
				htmlText += u"<td style='text-align: center;'>{}</td>".format(self.valueStyled(0, 1, squares=True))
			htmlText += u"</tr>"
			htmlText += u"</table>"

		htmlText += u"<h1 class='{species}'>{title}</h1>".format(title=self.__storage.moralityName(self.__character.species), species=self.__character.species)
		htmlText += u"<table class='fullWidth'>"
		for row in range(self.__character.morality + 1, Config.moralityTraitMax + 1)[::-1]:
			htmlText += u"<tr>"
			htmlText += u"<td style='text-align: center;'>{level}</td><td>{derangement}</td><td style='text-align: center;'>{value}</td>".format(level=row, derangement=self.derangement(row), value=self.valueStyled(0, 1))
			htmlText += u"</tr>"
		for row in range(1, self.__character.morality + 1)[::-1]:
			htmlText += u"<tr>"
			htmlText += u"<td style='text-align: center;'>{level}</td><td></td><td style='text-align: center;'>{value}</td>".format(level=row, value=self.valueStyled(1))
			htmlText += u"</tr>"
		htmlText += u"</table>"

		return htmlText


	def _createWeapons(self):
		"""
		Die Waffen werden aufgelistet.
		"""

		htmlText = u"<table class='fullWidth'>"
		htmlText += u"<tr>"
		htmlText += u"<th id='{species}'>{}</th><th id='{species}'>{}</th><th id='{species}'>{}</th><th id='{species}'>{}</th><th id='{species}'>{}</th><th id='{species}'>{}</th><th id='{species}'>{}</th>".format(
			self.tr("Weapon"),
			self.tr("Dmg."),
			self.tr("Ranges"),
			self.tr("Cap."),
			self.tr("Str."),
			self.tr("Size"),
			self.tr("Durab."),
			species=self.__character.species,
		)
		htmlText += u"</tr>"
		for category in self.__character.weapons:
			for weapon in self.__character.weapons[category]:
				htmlText += u"<tr>"
				htmlText += u"<td>{}</td><td style='text-align: center;'>{}</td><td style='text-align: center;'>{}</td><td style='text-align: center;'>{}</td><td style='text-align: center;'>{}</td><td style='text-align: center;'>{}</td><td style='text-align: center;'>{}</td>".format(
					weapon,
					self.__storage.weapons[category][weapon]["damage"],
					self.__storage.weapons[category][weapon]["ranges"],
					self.__storage.weapons[category][weapon]["capacity"],
					self.__storage.weapons[category][weapon]["strength"],
					self.__storage.weapons[category][weapon]["size"],
					self.__storage.weapons[category][weapon]["durability"],
				)
				htmlText += u"</tr>"
		htmlText += u"</table>"

		return htmlText


	def derangement(self, level):
		"""
		Gibt die Geistesstörung des Charakters bei entsprechender Moralstufe zurück. Ist keine Geistesstörung vorhanden, wird ein leerer String zurückgegeben.
		"""

		if level in self.__character.derangements:
			return self.__character.derangements[level]
		else:
			return ""


	def _createGoblinContracts(self):
		if self.__character.species == "Changeling":
			listOfSubpowers = []
			for item in self.__character.traits["Subpower"]:
				tmpListOfSubpowers = []
				for trait in self.__character.traits["Subpower"][item].values():
					if trait.value > 0 and trait.species == self.__character.species:
						tmpListOfSubpowers.append(trait.name)
				tmpListOfSubpowers.sort()
				listOfSubpowers.extend(tmpListOfSubpowers)

			return self.simpleTextBox("; ".join(listOfSubpowers), title=self.tr("Goblin Contracts"))
		else:
			return ""


	def _createVinculi(self):
		if self.__character.species == "Vampire":
			htmlText = u"<h1 class='{species}'>{title}</h1>".format(title=self.tr("Vinculi"), species=self.__character.species)
			htmlText += u"<table class='fullWidth'>"
			for vinculum in self.__character.vinculi:
				htmlText += u"<tr><td style='width: 100%;'>{name}</td><td>{value}</td></tr>".format(name=vinculum.name, value=self.valueStyled(vinculum.value, Config.vinculumLevelMax))
			htmlText += u"</table>"
			return htmlText
		else:
			return ""


	def _createDescription(self):
		dataTable = [
			[
				[ "Birthday:", self.__character.dateBirth.toString(Config.textDateFormat), ],
				[ "Age:", self.__character.age, ],
				[ "Sex:", ImageTools.genderSymbol(self.__character.identity.gender), ],
				[ "Eyes:", self.__character.eyes, ],
			],
			[
				[ "Height:", "{} {}".format(self.__character.height, "m"), ],
				[ "Weight:", "{} {}".format(self.__character.weight, "kg"), ],
				[ "Hair:", self.__character.hair, ],
				[ "Nationality:", self.__character.nationality, ],
			],
		]
		if self.__character.species != "Human":
			text[0][1] = "{} ({})".format(text[0][1], self.__character.age)
			text[1][1] = "{} ({})".format(self.__character.dateBecoming.toString(Config.textDateFormat), self.__character.ageBecoming)
		if self.__character.species == "Changeling":
			text[1][0] = "Taken:"
		elif self.__character.species == "Mage":
			text[1][0] = "Awakening:"
		elif self.__character.species == "Vampire":
			text[1][0] = "Embrace:"
		elif self.__character.species == "Werewolf":
			text[1][0] = "First Change:"
			# Größe und Gewicht löschen
			del text[4:6]

		htmlText = self.simpleTextBox(self.__character.description, title=self.tr("Description"))

		htmlText += u"<table><tr>"
		for column in dataTable:
			htmlText += u"<td><table>"
			for row in column:
				htmlText += u"<tr>"
				htmlText += u"<td>{label}</td><td style='text-align: right;'>{value}</td>".format(label=row[0], value=row[1])
				htmlText += u"</tr>"
			htmlText += u"</table></td>"
		htmlText += u"</tr></table>"

		return htmlText


	def simpleTextBox(self, text, title=None, species=None):
		if species is None or species == self.__character.species:
			htmlText = u""
			if title:
				htmlText += u"<h1 class='{species}'>{title}</h1>".format(title=title, species=self.__character.species)
			htmlText += u"<p>{}</p>".format(text)
			return htmlText
		else:
			return ""


	def htmlImage(self, imagePath):
		return "{}".format(self.__persistentResourceFiles[imagePath].name)


	def valueStyled(self, value, maxValue=None, squares=False):
		"""
		Gibt den übergebenen Wert in stilisierter Form aus: Als gefüllte Punkte.

		\note Ist maxValue kleiner als value, wird nur maxValue berücksichtigt.
		"""

		charEmpty = u"○"
		charFull = u"●"
		if squares:
			charEmpty = u"□"
			charFull = u"▣"

		if not maxValue:
			maxValue = value
		text = u""
		for filled in xrange(min(value, maxValue)):
			text += charFull
		for empty in xrange(min(value, maxValue), maxValue):
			text += charEmpty

		return text


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
			rect = QRect(0, 0, image.width() * self.__paperSize[1] / image.height(), self.__paperSize[1])
			self.__painter.drawImage(rect, image)

			image = QImage(":sheet/images/sheet/WorldOfDarkness-BackgroundR.png")
			rect = QRect(self.__paperSize[0] - rect.width(), 0, rect.width(), rect.height())
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
		#scale = scaleFactor[0]
		self.__painter.scale(scale, scale)
		self.__painter.setRenderHint ( QPainter.Antialiasing )

		self.__paperSize = (
			self.__printer.width() / scale,
			self.__printer.height() / scale,
		)

		self.__painter.save()

		## Hintergrundbild:
		self._drawBackground()
		#posY = 0.01 * self.__paperSize[1]
		posY = 0
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

		for tmp in self.__persistentResourceFiles.values():
			os.remove("{}".format(tmp.name))




