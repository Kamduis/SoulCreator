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
import re

from PySide.QtCore import Qt, QObject, QFile, QIODevice, QTextStream, QBuffer, QByteArray, QUrl, QRect
from PySide.QtGui import QPainter, QImage, QPalette#, QColor, QPen, QFont, QFontMetrics, QTextDocument
from PySide.QtWebKit import QWebPage

#from src.GlobalState import GlobalState
from src.Config import Config
from src.Error import ErrFileNotOpened
#from src.Random import Random
from src.Datatypes.Identity import Identity
from src.Calc.CalcAdvantages import CalcAdvantages
from src.Calc.CalcShapes import CalcShapes
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

		blockHeight = {
			"Human": {
				"inventory": "450px",
				"description": "400px",
			},
			"Changeling": {
				"inventory": "200px",
				"description": "200px",
			},
			"Mage": {
				"inventory": "200px",
				"description": "200px",
			},
			"Vampire": {
				"inventory": "200px",
				"description": "200px",
			},
			"Werewolf": {
				"inventory": "200px",
				"description": "200px",
			},
		}

		curseText = "Weakness"
		if self.__character.species == "Changeling":
			curseText = "Curse"

		htmlText = unicode(htmlText).format(
			info=self._createInfo(),
			attributes=self._createAttributes(),
			skills=self._createSkills(),
			powers=self._createPowers(),
			merits=self._createMerits(),
			flaws=self._createFlaws(),
			advantages=self._createAdvantages(),
			health=self._dotStat(
				self.tr("Health"),
				self.__calc.calcHealth(),
				Config.healthMax[self.__character.species],
				hasTemporary=True
			),
			willpower=self._dotStat(
				self.tr("Willpower"),
				self.__calc.calcWillpower(),
				Config.willpowerMax,
				hasTemporary=True
			),
			powerstat=self._dotStat(
				self.__storage.powerstatName(self.__character.species),
				self.__character.powerstat,
				Config.powerstatMax,
				hasTemporary=False
			),
			fuel=self._createFuel(),
			morality=self._createMorality(),
			weapons=self._createWeapons(),
			goblinContracts=self._createGoblinContracts(),
			magicalTool=self.simpleTextBox(self.__character.magicalTool, title=self.tr("Magical Tool"), species="Mage"),
			vinculi=self._createVinculi(),
			blessing=self.simpleTextBox(
				self.__storage.breedBlessing(self.__character.species, self.__character.breed),
				title=self.tr("{} Blessing".format(self.__storage.breedTitle(self.__character.species)))
			),
			abilityKith=self.simpleTextBox(
				self.__storage.kithAbility(self.__character.breed, self.__character.kith),
				title=self.tr("Kith Ability")
			),
			curseBreed=self.simpleTextBox(
				self.__storage.breedCurse(self.__character.species, self.__character.breed),
				title="{} {}".format(self.__storage.breedTitle(self.__character.species), curseText)
			),
			curseOrganisation=self.simpleTextBox(
				self.__storage.organisationCurse(self.__character.species, self.__character.organisation),
				title="{} {}".format(self.__storage.organisationTitle(self.__character.species), curseText)
			),
			spellsActive=self.userTextBox(
				lines=7,
				title=self.tr("Active Spells"),
				description=self.tr("Max: {} +3".format(self.__storage.powerstatName(self.__character.species)))
			),
			spellsUponSelf=self.userTextBox(
				lines=7,
				title=self.tr("Spells Cast Upon Self"),
				description=self.tr("Spell Tolerance: Stamina; -1 die per extra spell")
			),
			nimbus=self.simpleTextBox(
				self.__character.nimbus,
				title=self.tr("Nimbus")
			),
			paradoxMarks=self.simpleTextBox(
				self.__character.paradoxMarks,
				title=self.tr("Paradox Marks")
			),
			shapes=self._createShapeTable(),
			inventory=self._createInventory(blockHeight[self.__character.species]["inventory"]),
			description=self._createDescription(blockHeight[self.__character.species]["description"]),
			image=self._createImage(),
			rolls=self._createRolls(),
			notes=self.userTextBox(
				lines=3,
				title=self.tr("Notes")
			),
			xp=self._createXp(),
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
				"36%",
				[
					[ "Name:", Identity.displayNameDisplay(self.__character.identity.surname, self.__character.identity.firstname, self.__character.identity.nickname), ],
					[ "", "", ],
				],
			],
			[
				"28%",
				[
					[ "Virtue:", self.__character.virtue, ],
					[ "Vice:", self.__character.vice, ],
				],
			],
			[
				"36%",
				[
					[ "Chronicle:", "", ],
					[ "{}:".format(self.__storage.factionTitle(self.__character.species)), self.__character.faction, ],
				],
			],
		]
		if self.__character.species != "Human":
			tableContents = [
				[
					tableContents[0][0][0][0],
					[
						[ tableContents[0][1][0][0], tableContents[0][1][0][1], ],
						[ "Secret Name:", self.__character.identity.supername, ],
						[ tableContents[0][1][1][0], tableContents[0][1][1][1], ],
					],
				],
				[
					tableContents[1][0][0][0],
					[
						[ tableContents[1][1][0][0], tableContents[1][1][0][1], ],
						[ tableContents[1][1][1][0], tableContents[1][1][1][1], ],
						[ "{}:".format(self.__storage.partyTitle(self.__character.species)), self.__character.party, ],
					],
				],
				[
					tableContents[2][0][0][0],
					[
						[ "{}:".format(self.__storage.breedTitle(self.__character.species)), self.__character.breed, ],
						[ tableContents[2][1][1][0], tableContents[2][1][1][1], ],
						[ "{}:".format(self.__storage.organisationTitle(self.__character.species)), self.__character.organisation, ],
					],
				],
			]

			if self.__character.species == "Changeling":
				tableContents[2][1][0][0] = "{}:".format(self.__storage.breedTitle(self.__character.species))
				tableContents[2][1][0][1] ="{} ({})".format(self.__character.breed, self.__character.kith)
			elif self.__character.species == "Mage":
				tableContents[0][1][1][0] = "Shadow Name:"
			elif self.__character.species == "Vampire":
				tableContents[0][1][2][0] = "Sire:"
				tableContents[0][1][2][1] = ""
			elif self.__character.species == "Werewolf":
				tableContents[0][1][1][0] = "Deed Name:"
				tableContents[0][1][2][0] = "Totem:"
				tableContents[0][1][2][1] = self.__character.companionName

		htmlText = "<table class='fullSpace'><tr>"
		for column in tableContents:
			htmlText += "<td style='width: {}; vertical-align: top;'><table style='width: 100%'>".format(column[0])
			for row in column[1]:
				htmlText += u"<tr><td style='text-align: right; white-space: nowrap;'>{label}</td><td style='width: 100%;'><span class='scriptFont text'>{value}</span></td></tr>".format(label=row[0], value=row[1])
			htmlText += "</table></td>"
		htmlText += "</tr></table>"

		return htmlText


	def _createAttributes(self):
		"""
		Erzeugt die Darstellung der Attribute.
		"""

		tableData = [
			[],
			[],
			[],
		]

		for category in Config.attributes:
			i = 0
			for trait in category[1]:
				tableData[i].append(self.__character.traits["Attribute"][category[0]][trait])
				i += 1

		for i in xrange(len(Config.attributeSorts)):
			tableData[i].insert(0, Config.attributeSorts[i])

		htmlText = u"<table class='fullWidth'>"
		for row in tableData:
			htmlText += u"<tr>"
			htmlText += u"<td style='width: 0%;'><span class='{species}'>{}</span></td>".format(row[0], species=self.__character.species)
			for column in row[1:]:
				htmlText += u"<td style='width: 33%; text-align: right; font-weight: bold;'>{label}</td><td>{value}</td>".format(label=column.name, value=self.valueStyled(column.totalvalue, self.traitMax))
			htmlText += u"</tr>"
		htmlText += u"</table>"

		return htmlText


	def _createSkills(self):
		"""
		Erzeugt die Darstellung der Fertigkeiten und Spezialisierungen.
		"""

		htmlText = u"<table class='fullSpace' style='table-layout: fixed;'>"
		firstRow = True
		for item in self.__character.traits["Skill"]:
			traits = self.__character.traits["Skill"][item].keys()
			traits.sort()
			if not firstRow:
				## Dehnbarer vertikaler Zwischenraum.
				htmlText += u"<tr><td class='layout'></td></tr>"
			firstRow = False
			## Dadurch, daß die Zeile einen Höhe von 0%, aber Inhalt hat, wird sie auf die Höhe des Inhalts gestreckt. Die Verbleibende Höhe wird auf die Zeilen ohne Hlhenangabe, die Platzhalterspalten, aufgeteilt.
			htmlText += u"<tr style='height: 0%'><td class='layout'>"
			htmlText += u"<h2 class='{species}'>{category}</h2>".format(species=self.__character.species.lower(), category=item)
			for subitem in traits:
				trait = self.__character.traits["Skill"][item][subitem]
				#Debug.debug(trait.era, self.__character.era, trait.age, Config.getAge(self.__character.age))
				if (
					(not trait.era or self.__character.era in trait.era) and
					(not trait.age or trait.age == Config.getAge(self.__character.age))
				):
					htmlText += u"<table class='fullWidth'>"
					htmlText += u"<tr>"
					htmlText += u"<td class='nowrap withHRule'>{label}</td>".format(label=trait.name)
					htmlText += u"<td class='hrulefill'><span class='descText'>{additional}</span></td>".format(additional=", ".join(trait.totalspecialties))
					htmlText += u"<td class='nowrap withHRule' style='text-align: right;'>{value}</td>".format(value=self.valueStyled(trait.totalvalue, self.traitMax))
					htmlText += u"</tr>"
					htmlText += u"</table>"
			htmlText += u"</td></tr>"
		htmlText += u"</table>"

		return htmlText


	def _createPowers(self, count=None):
		"""
		Erzeugt die Darstellung der übernatürlichen Kräfte.
		"""

		if self.__character.species not in ( "Human", ):
			if not count:
				countPerSpecies = {
					"Human": 0, # Keine Kräfte
					"Changeling": 8,
					"Mage": 0, # Keine zusätzlichen Kräfte
					"Vampire": 6,
					"Werewolf": 0, # Keine zusätzlichen Kräfte
				}
				if self.__character.species in countPerSpecies.keys():
					count = countPerSpecies[self.__character.species]
				else:
					count = countPerSpecies["Human"]

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

			iteratorGoal = ( ( 0, len(traitList), ), )
			if twocolumn:
				iteratorGoal = (
					( 0, int(math.floor(len(traitList) / 2)), ),
					( int(math.floor(len(traitList) / 2)), len(traitList), ),
				)

			htmlText = u"<h1 class='{species}'>{title}</h1>".format(title=self.__storage.powerName(self.__character.species), species=self.__character.species)

			htmlText += u"<table style='width: 100%'><tr>"
			iterator = 0
			colIterator = 0
			for column in iteratorGoal:
				htmlText += u"<td class='layout'>"
				for i in xrange(column[0], column[1]):
					trait = traitList[i]
					htmlText += u"<table class='fullWidth'>"
					htmlText += u"<tr>"
					labelCol = u"<td class='nowrap withHRule'>{label}</td>".format(label=trait.name)
					ruleCol =u"<td class='hrulefill'><span class='descText'>{additional}</span></td>".format(additional=trait.customText)
					valueCol = u"<td class='nowrap withHRule' style='text-align: right;'>{value}</td>".format(value=self.valueStyled(trait.totalvalue, self.traitMax))
					if colIterator > 0:
						htmlText += valueCol + ruleCol + labelCol
					else:
						htmlText += labelCol + ruleCol + valueCol
					htmlText += u"</tr>"
					htmlText += u"</table>"
					iterator += 1
				htmlText += u"</td>"
				if colIterator < len(iteratorGoal) - 1:
					# Feste Breite
					htmlText += u"<td class='spacer'></td>"
				colIterator += 1
			htmlText += u"</tr></table>"

			freeCount = count - iterator
			if freeCount < 0:
				freeCount = 0
			htmlText += u"<table style='width: 100%'><tr>"
			for column in iteratorGoal:
				htmlText += u"<td class='layout'>"
				for i in xrange(int(math.ceil(freeCount / len(iteratorGoal)))):
					htmlText += u"<table class='fullWidth'>"
					htmlText += u"<tr>"
					htmlText += u"<td class='hrulefill'></td><td class='nowrap withHRule' style='text-align: right;'>{value}</td>".format(value=self.valueStyled(0, self.traitMax))
					htmlText += u"</tr>"
					htmlText += u"</table>"
				htmlText += u"</td>"
			htmlText += u"</tr></table>"

			return htmlText
		else:
			return ""


	def _createMerits(self, count=None):
		"""
		Erzeugt die Darstellung der Merits.
		"""

		if not count:
			countPerSpecies = {
				"Human": 20,
				"Changeling": 20,
				"Mage": 21,
				"Vampire": 26,
				"Werewolf": 20,
			}
			if self.__character.species in countPerSpecies.keys():
				count = countPerSpecies[self.__character.species]
			else:
				count = countPerSpecies["Human"]

		htmlText = u"<h1 class='{species}'>Merits</h1>".format(species=self.__character.species)
		iterator = 0
		for item in self.__character.traits["Merit"]:
			traits = self.__character.traits["Merit"][item].keys()
			traits.sort()
			for subitem in traits:
				trait = self.__character.traits["Merit"][item][subitem]
				if trait.isAvailable and trait.value > 0:
					htmlText += u"<table class='fullWidth'>"
					htmlText += u"<tr>"
					htmlText += u"<td class='nowrap withHRule'>{label}</td>".format(label=trait.name)
					htmlText += u"<td class='hrulefill'><span class='descText'>{additional}</span></td>".format(additional=trait.customText)
					htmlText += u"<td class='nowrap withHRule' style='text-align: right;'>{value}</td>".format(value=self.valueStyled(trait.totalvalue, self.traitMax))
					htmlText += u"</tr>"
					htmlText += u"</table>"
					iterator += 1

		while iterator < count:
			htmlText += u"<table class='fullWidth'><tr>"
			htmlText += u"<td class='hrulefill'></td><td class='nowrap' style='text-align: right;'>{value}</td>".format(value=self.valueStyled(0, self.traitMax))
			htmlText += u"</tr></table>"
			iterator += 1

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

		htmlText = self.simpleTextBox("; ".join(flaws), title=self.tr("Flaws"))

		return "<div style='height: 3.5em'>{}</div>".format(htmlText)


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
				htmlText += u"<table class='fullWidth' style='height: 0%'>"
				htmlText += u"<tr>"
				htmlText += u"<td class='nowrap'>{label}</td>".format(label=item[0])
				htmlText += u"<td class='hrulefill'></td>"
				htmlText += u"<td class='nowrap' style='text-align: right;'>{value}</td>".format(value=item[1])
				htmlText += u"</tr>"
				htmlText += u"</table>"

		return htmlText


	def _dotStat(self, title, value, maxValue, hasTemporary=False):
		htmlText = u"<h1 class='{species}'>{title}</h1>".format(title=title, species=self.__character.species)
		htmlText += u"<table style='width: 100%; table-layout: fixed;'>"
		htmlText += u"<tr>"
		for i in xrange(value):
			htmlText += u"<td class='layout' style='text-align: center; width: {width}%'><span class='bigSymbols'>{}</span></td>".format(self.valueStyled(1), width=100/maxValue)
		for i in xrange(value, maxValue):
			htmlText += u"<td class='layout' style='text-align: center;'><span class='bigSymbols'>{}</span></td>".format(self.valueStyled(0, 1))
		htmlText += u"</tr>"
		if hasTemporary:
			htmlText += u"<tr>"
			for i in xrange(maxValue):
				htmlText += u"<td class='layout' style='text-align: center;'><span class='bigSymbols'>{}</span></td>".format(self.valueStyled(0, 1, squares=True))
			htmlText += u"</tr>"
		htmlText += u"</table>"

		return htmlText


	def _createFuel(self, maxPerRow=10):
		htmlText = u"<h1 class='{species}'>{title}</h1>".format(
			title=self.__storage.fuelName(self.__character.species),
			species=self.__character.species
		)

		htmlText += u"<table><tr><td>"

		htmlText += u"<table class='fullWidth'>"
		htmlText += u"<tr>"

		value = self.__storage.fuelMax(species=self.__character.species, powerstat=self.__character.powerstat)
		while value > maxPerRow:
			value -= maxPerRow
			for i in xrange(maxPerRow):
				htmlText += u"<td class='layout' style='text-align: center;'><span class='bigSymbols'>{}</span></td>".format(self.valueStyled(0, 1, squares=True))
			htmlText += u"</tr><tr>"
		for i in xrange(value):
			htmlText += u"<td class='layout' style='text-align: center;'><span class='bigSymbols'>{}</span></td>".format(self.valueStyled(0, 1, squares=True))
		htmlText += u"</tr>"
		htmlText += u"</table>"

		htmlText += u"</td><td class='spacer'></td><td style='width: 0%'>"

		htmlText += u"<span class='small'><table style='width: 100%'><tr><td class='nowrap' style='text-align: center;'>{perTurn}</td></tr><tr><td class='nowrap' style='text-align: center;'>per Turn</td></tr></table></span>".format(perTurn=self.__storage.fuelPerTurn(species=self.__character.species, powerstat=self.__character.powerstat))

		htmlText += u"</td></tr></table>"

		return htmlText


	def _createMorality(self):
		htmlText = u"<h1 class='{species}'>{title}</h1>".format(title=self.__storage.moralityName(self.__character.species), species=self.__character.species)
		htmlText += u"<table class='fullWidth'>"
		for row in range(self.__character.morality + 1, Config.moralityTraitMax + 1)[::-1]:
			htmlText += u"<tr>"
			htmlText += u"<td style='text-align: center;'>{level}</td><td {hrule}><span class='scriptFont'>{derangement}</span></td><td  class='narrowLine' style='text-align: center;'><span class='bigSymbols'>{value}</span></td>".format(level=row, derangement=self.derangement(row), value=self.valueStyled(0, 1), hrule=self.__derangementPossible(row))
			htmlText += u"</tr>"
		for row in range(1, self.__character.morality + 1)[::-1]:
			htmlText += u"<tr>"
			htmlText += u"<td style='text-align: center;'>{level}</td><td {hrule}></td><td class='narrowLine' style='text-align: center;'><span class='bigSymbols'>{value}</span></td>".format(level=row, value=self.valueStyled(1), hrule=self.__derangementPossible(row))
			htmlText += u"</tr>"
		htmlText += u"</table>"

		return htmlText


	def __derangementPossible(self, level):
		if level <= Config.derangementMoralityTraitMax:
			return "class='hrulefill'"
		else:
			return ""


	def derangement(self, level):
		"""
		Gibt die Geistesstörung des Charakters bei entsprechender Moralstufe zurück. Ist keine Geistesstörung vorhanden, wird ein leerer String zurückgegeben.
		"""

		if level in self.__character.derangements:
			return self.__character.derangements[level]
		else:
			return ""


	def _createWeapons(self, count=5):
		"""
		Die Waffen werden aufgelistet.
		"""

		weaponInfo = (
			"damage",
			"ranges",
			"capacity",
			"strength",
			"size",
			"durability",
		)

		htmlText = u"<table class='fullWidth'>"
		htmlText += u"<tr>"
		htmlText += u"""
			<th class='{species}' style='width: 40%'>{}</th>
			<th class='{species}' style='width: 13%'>{}</th>
			<th class='{species}' style='width: 5%'>{}</th>
			<th class='{species}' style='width: 5%'>{}</th>
			<th class='{species}' style='width: 5%'>{}</th>
			<th class='{species}' style='width: 5%'>{}</th>
			<th class='{species}' style='width: 5%'>{}</th>""".format(
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

		#Debug.debug(htmlText)

		iterator = 0
		for category in self.__character.weapons:
			for weapon in self.__character.weapons[category]:
				htmlText += u"<tr>"
				htmlText += u"<td><span class='scriptFont'>{}</span></td>".format(weapon)
				for column in weaponInfo:
					htmlText += u"<td style='text-align: center;'><span class='scriptFont'>{}</span></td>".format(self.__storage.weapons[category][weapon][column])
				htmlText += u"</tr>"
				iterator += 1

		while iterator < count:
			htmlText += u"<tr class='rowHeight'>"
			## Der Waffenname hat ja auch ein Feld.
			for i in xrange(len(weaponInfo) + 1):
				htmlText += u"<td class='layout' style='vertical-align: bottom;'><table class='underlines fullWidth'><tr style='height: 100%;'>"
				htmlText += u"<td class='hrulefill'></td>"
				htmlText += u"</tr></table></td>"
			htmlText += u"</tr>"
			iterator += 1

		htmlText += u"</table>"

		return htmlText


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
		htmlText = u"<h1 class='{species}'>{title}</h1>".format(title="Vinculi", species=self.__character.species)
		htmlText += u"<table class='fullWidth'>"
		iterator = 0
		for vinculum in [ item for item in self.__character.vinculi if item.value > 0 ]:
			htmlText += u"<tr>"
			htmlText += u"<td class='nowrap withHRule'>{label}</td>".format(label=vinculum.name)
			htmlText += u"<td class='hrulefill'></td>"
			htmlText += u"<td class='nowrap withHRule' style='text-align: right;'>{value}</td>".format(value=self.valueStyled(vinculum.value, Config.vinculumLevelMax))
			htmlText += u"</tr>"
			iterator += 1
		htmlText += u"</table>"

		htmlText += u"<table class='fullWidth'>"
		while iterator < len(self.__character.vinculi):
			htmlText += u"<tr>"
			htmlText += u"<td class='hrulefill'></td>"
			htmlText += u"<td class='nowrap withHRule' style='text-align: right;'>{value}</td>".format(value=self.valueStyled(0, Config.vinculumLevelMax))
			htmlText += u"</tr>"
			iterator += 1
		htmlText += u"</table>"

		return htmlText


	def _createShapeTable(self):
		## Attributsänderungen
		shapesAttributes = {
			"Hishu": (
			),
			"Dalu": (
				( u"Strength (+1)", CalcShapes.strength(self.__character.traits["Attribute"]["Physical"]["Strength"].value, Config.shapesWerewolf[1]) ),
				( u"Stamina (+1)", CalcShapes.stamina(self.__character.traits["Attribute"]["Physical"]["Stamina"].value, Config.shapesWerewolf[1]) ),
				( u"Manipulation (−1)", CalcShapes.manipulation(self.__character.traits["Attribute"]["Social"]["Manipulation"].value, Config.shapesWerewolf[1]) ),
			),
			"Gauru": (
				( u"Strength (+3)", CalcShapes.strength(self.__character.traits["Attribute"]["Physical"]["Strength"].value, Config.shapesWerewolf[2]) ),
				( u"Dexterity (+1)", CalcShapes.dexterity(self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[2]) ),
				( u"Stamina (+2)", CalcShapes.stamina(self.__character.traits["Attribute"]["Physical"]["Stamina"].value, Config.shapesWerewolf[2]) ),
			),
			"Urshul": (
				( u"Strength (+2)", CalcShapes.strength(self.__character.traits["Attribute"]["Physical"]["Strength"].value, Config.shapesWerewolf[3]) ),
				( u"Dexterity (+2)", CalcShapes.dexterity(self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[3]) ),
				( u"Stamina (+2)", CalcShapes.stamina(self.__character.traits["Attribute"]["Physical"]["Stamina"].value, Config.shapesWerewolf[3]) ),
				( u"Manipulation (−3)", CalcShapes.manipulation(self.__character.traits["Attribute"]["Social"]["Manipulation"].value, Config.shapesWerewolf[3]) ),
			),
			"Urhan": (
				( u"Dexterity (+2)", CalcShapes.dexterity(self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[4]) ),
				( u"Stamina (+1)", CalcShapes.stamina(self.__character.traits["Attribute"]["Physical"]["Stamina"].value, Config.shapesWerewolf[4]) ),
			),
		}

		armor = [ 0, 0, ]
		isDedicated = self.__character.armor["dedicated"]
		if self.__character.armor["name"] in self.__storage.armor:
			armor[0] = self.__storage.armor[self.__character.armor["name"]]["general"]
			armor[1] = self.__storage.armor[self.__character.armor["name"]]["firearms"]

		advantages = (
			( self.tr("Size"), self.__calc.calcSize(), ),
			( self.tr("Initiative"), self.__calc.calcInitiative(), ),
			( self.tr("Speed"), self.__calc.calcSpeed(), ),
			( self.tr("Defense"), self.__calc.calcDefense(), ),
			( self.tr("Armor"), "{general}/{firearms}".format(general=armor[0], firearms=armor[1]), ),
			( self.tr("Perception"), u"±0", ),
		)
		daluArmor = "0/0"
		if isDedicated:
			daluArmor = advantages[4][1]
		shapesAdvantages = {
			"Hishu": advantages,
			"Dalu": (
				( advantages[0][0], CalcShapes.size(advantages[0][1], Config.shapesWerewolf[1]), ),
				( advantages[1][0], CalcShapes.initiative(advantages[1][1], Config.shapesWerewolf[1]), ),
				( advantages[2][0], CalcShapes.speed(advantages[1][1], Config.shapesWerewolf[1]), ),
				( advantages[3][0], CalcShapes.defense(self.__character.traits["Attribute"]["Mental"]["Wits"].value, self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[1]), ),
				( advantages[4][0], daluArmor, ),
				( advantages[5][0], u"+2", ),
			),
			"Gauru": (
				( advantages[0][0], CalcShapes.size(advantages[0][1], Config.shapesWerewolf[2]), ),
				( advantages[1][0], CalcShapes.initiative(advantages[1][1], Config.shapesWerewolf[2]), ),
				( advantages[2][0], CalcShapes.speed(advantages[1][1], Config.shapesWerewolf[2]), ),
				( advantages[3][0], CalcShapes.defense(self.__character.traits["Attribute"]["Mental"]["Wits"].value, self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[2]), ),
				( advantages[4][0], "1/1", ),
				( advantages[5][0], u"+3", ),
			),
			"Urshul": (
				( advantages[0][0], CalcShapes.size(advantages[0][1], Config.shapesWerewolf[3]), ),
				( advantages[1][0], CalcShapes.initiative(advantages[1][1], Config.shapesWerewolf[3]), ),
				( advantages[2][0], CalcShapes.speed(advantages[1][1], Config.shapesWerewolf[3]), ),
				( advantages[3][0], CalcShapes.defense(self.__character.traits["Attribute"]["Mental"]["Wits"].value, self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[3]), ),
				( advantages[4][0], "0", ),
				( advantages[5][0], u"+3", ),
			),
			"Urhan": (
				( advantages[0][0], CalcShapes.size(advantages[0][1], Config.shapesWerewolf[4]), ),
				( advantages[1][0], CalcShapes.initiative(advantages[1][1], Config.shapesWerewolf[4]), ),
				( advantages[2][0], CalcShapes.speed(advantages[1][1], Config.shapesWerewolf[4]), ),
				( advantages[3][0], CalcShapes.defense(self.__character.traits["Attribute"]["Mental"]["Wits"].value, self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[4]), ),
				( advantages[4][0], "0", ),
				( advantages[5][0], u"+4", ),
			),
		}

		## Ohne unicode im Argument von self.tr() auch kein unicode "−"!
		comments = {
			"Hishu": (
				self.tr("Others suffer -2 to all attempts to detect werewolf nature."),
			),
			"Dalu": (
				self.tr("Lunacy -4"),
			),
			"Gauru": (
				self.tr("Full Lunacy<br>Bite: +2L, Claw: +1L<br>-2 to resist Death Rage"),
			),
			"Urshul": (
				self.tr("Lunacy -2<br>ite: +2L"),
			),
			"Urhan": (
				self.tr("Bite: +2L<br>Others suffer -2 to all attempts to detect werewolf nature."),
			),
		}

		htmlText = "<table style='width: 100%'><tr>"
		iterator = 0
		for shape in Config.shapesWerewolf:
			if iterator > 0:
				htmlText += "<td class='layout spacer'><!--Fixed horizontal space--></td>"
			htmlText += "<td class='layout' style='width: {}%'>".format((100 / len(Config.shapesWerewolf)) - 1)
			htmlText += "<h2 class='{species}'>{title}</h2>".format(title=shape, species=self.__character.species)
			htmlText += "<table style='width: 100%'>"
			for row in shapesAttributes[shape]:
				htmlText += "<tr><td class='layout'><table style='width: 100%'><tr>"
				htmlText += u"<td class='nowrap withHRule'>{label}</td>".format(label=row[0])
				htmlText += u"<td class='hrulefill'></td>"
				htmlText += u"<td class='nowrap withHRule' style='text-align: right;'><span class='scriptFont'>{value}</span></td>".format(value=row[1])
				htmlText += "</tr></table></td></tr>"
			htmlText += "</table>"
			htmlText += "</td>"
			iterator += 1
		htmlText += "</tr><tr>"
		for shape in Config.shapesWerewolf:
			htmlText += "<td class='layout'><div class='spacer'></div></td>"
		htmlText += "</tr><tr>"
		iterator = 0
		for shape in Config.shapesWerewolf:
			if iterator > 0:
				htmlText += "<td class='layout spacer'><!--Fixed horizontal space--></td>"
			htmlText += "<td class='layout'>"
			htmlText += "<table style='width: 100%'>"
			for row in shapesAdvantages[shape]:
				htmlText += "<tr><td class='layout'><table style='width: 100%'><tr>"
				htmlText += u"<td class='nowrap withHRule'>{label}</td>".format(label=row[0])
				htmlText += u"<td class='hrulefill'></td>"
				htmlText += u"<td class='nowrap withHRule' style='text-align: right;'><span class='scriptFont'>{value}</span></td>".format(value=row[1])
				htmlText += "</tr></table></td></tr>"
			htmlText += "</table>"
			htmlText += "</td>"
			iterator += 1
		htmlText += "</tr><tr>"
		for shape in Config.shapesWerewolf:
			htmlText += "<td class='layout'><div class='spacer'></div></td>"
		htmlText += "</tr><tr>"
		iterator = 0
		for shape in Config.shapesWerewolf:
			if iterator > 0:
				htmlText += "<td class='layout spacer'><!--Fixed horizontal space--></td>"
			htmlText += "<td class='layout'>"
			htmlText += "<table style='width: 100%'>"
			for row in comments[shape]:
				htmlText += "<tr><td style='text-align: center; font-style: italic;'><span class='small' style=' line-height: 1em;'>{}</span></td></tr>".format(row)
			htmlText += "</table>"
			htmlText += "</td>"
			iterator += 1
		htmlText += "</tr></table>"


		return htmlText


	def _createInventory(self, height=293):
		#u"<div style='height:{height}; overflow:hidden;'>{text}</div>".format(text=self.simpleTextBox("; ".join(self.__character.equipment), title=self.tr("Inventory")), height="{}px".format(heightInventory))
		
		htmlText = text=self.simpleTextBox("; ".join(self.__character.equipment), title=self.tr("Inventory"))

		htmlText += u"<dl>"
		for typ in self.__character.extraordinaryItems:
			equipment = "; ".join(self.__character.extraordinaryItems[typ])
			htmlText += u"<dt><span class='scriptFont text'>{}</span></dt><dd><span class='scriptFont text'>{}</span><dd>".format(typ, equipment)
		htmlText += u"</dl>"

		return htmlText


	def _createDescription(self, height=220):
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
			dataTable[0][1] = "{} ({})".format(dataTable[0][1], self.__character.age)
			dataTable[1][1] = "{} ({})".format(self.__character.dateBecoming.toString(Config.textDateFormat), self.__character.ageBecoming)
		if self.__character.species == "Changeling":
			dataTable[1][0] = "Taken:"
		elif self.__character.species == "Mage":
			dataTable[1][0] = "Awakening:"
		elif self.__character.species == "Vampire":
			dataTable[1][0] = "Embrace:"
		elif self.__character.species == "Werewolf":
			dataTable[1][0] = "First Change:"
			# Größe und Gewicht löschen
			del dataTable[4:6]

		htmlText = u"<table class='fullSpace'><tr style ='height: 100%;'><td class='layout'>"

		description = re.search(r".*\<body[^\>]*\>\n*(.*)\</body\>", self.__character.description, flags=re.MULTILINE | re.DOTALL)
		## description.group(0) zeigt den gesamten ursprünglichen string.
		description = description.group(1)
		htmlText += u"<div style='height:{height}; overflow:hidden;'>{text}</div>".format(text=self.simpleTextBox(description, title=self.tr("Description")), height="{}".format(height))

		htmlText += u"""</td>
		</tr>
		<tr>
		<td class='layout'></td>
		</tr>
		<tr>
		<td class='layout' style='height: 10%'>"""

		htmlText += u"<table class='fullWidth'><tr>"
		for column in dataTable:
			htmlText += u"<td class='layout' style='width: {}%;'><table class='fullWidth'>".format(100 / len(dataTable))
			for row in column:
				htmlText += u"<tr>"
				htmlText += u"<td>{label}</td><td class='hfill' style='text-align: right;'><span class='scriptFont'>{value}</span></td>".format(label=row[0], value=row[1])
				htmlText += u"</tr>"
			htmlText += u"</table></td>"
		htmlText += u"</tr></table>"

		htmlText += u"</td></tr></table>"

		return htmlText


	def _createImage(self, height=190):
		htmlText = u"<h1 class='{species}'>{title}</h1>".format(title=self.tr("Picture"), species=self.__character.species)

		if self.__character.picture:
			imageData = QByteArray()
			imageBuffer = QBuffer(imageData)
			imageBuffer.open(QIODevice.WriteOnly)
			self.__character.picture.save(imageBuffer, Config.pictureFormat)	# Schreibt das Bild in ein QByteArray im angegebenen Bildformat.
			imageData = imageData.toBase64()

			htmlText += u"<p style='text-align: center;'><img src='data:image/{form};base64,{image}' style='max-width:100%; max-height:{height}px;'></p>".format(image=imageData, form=Config.pictureFormat, height=height)

		return htmlText


	def _createRolls(self, height=190):
		htmlText = u"<h1 class='{species}'>{title}</h1>".format(title=self.tr("Rolls"), species=self.__character.species)

		specialBonus = ""
		if self.__character.species == "Werewolf" and self.__character.breed == "Irraka":
			specialBonus = "+ 2"

		rolls = {
			"Werewolf": (
				( "Shapeshifting", "Stamina + Survival + Primal Urge", ),
				( "Stepping Sideways", "Intelligence + Presence + Primal Urge", ),
				( "Dual Senses", "Wits + Empathy + Primal Urge{}".format(specialBonus), ),
				( "Sense Twilight Spirit", "Wits + Occult + Primal Urge{}".format(specialBonus), ),
			),
		}

		htmlText += "<table style='width: 100%'>"
		for roll in rolls[self.__character.species]:
			htmlText += "<tr><td class='layout'><table style='width: 100%'><tr>"
			htmlText += "<td class='nowrap withHRule'>{desc}</td>".format(desc=roll[0])
			htmlText += "<td class='hrulefill'></td>"
			htmlText += "<td class='nowrap withHRule' style='text-align: right;'>{dice}</td>".format(dice=roll[1])
			htmlText += "</tr></table></td></tr>"
		htmlText += "</table>"

		return htmlText


	def _createXp(self):
		xpColumns = (
			"XP",
		)
		if self.__character.species == "Mage":
			xpColumns = (
				"XP",
				self.tr("Arcane XP"),
			)
		htmlText = u""
		for column in xpColumns:
			htmlText += u"<table style='width: {}%'>".format(100 / len(xpColumns))
			htmlText += u"<tr><td><h1 class='{species}'>{title}</h1></td></tr>".format(title=column, species=self.__character.species)
			htmlText += u"<tr style='height: 3em;'><td class='box'></td></tr>"
			htmlText += u"</table>"

		return htmlText


	def simpleTextBox(self, text, title=None, species=None):
		"""
		\param species Wird in diesem Argument eine Spezies angegeben, wird nur dann ein Wert zurückgegeben, wenn die Spezies mit der Charakterspezies übereinstimmt.
		"""
		
		if self.__isForSpecies(species):
			htmlText = u""
			if title:
				htmlText += u"<h1 class='{species}'>{title}</h1>".format(title=title, species=self.__character.species)
			htmlText += u"<span class='scriptFont text'><p>{}</p></span>".format(text)
			return htmlText
		else:
			return ""


	def userTextBox(self, lines, title=None, description=None, species=None):
		"""
		Eine Box mit einer angebenen Anzahl an Linien, in welche der Spieler auf dem ausgedruckten Bogen Dinge eingeben kann.
		"""
		
		if self.__isForSpecies(species):
			htmlText = u""
			if title:
				htmlText += u"<h1 class='{species}'>{title}</h1>".format(title=title, species=self.__character.species)
			if description:
				htmlText += u"<p style='text-align: center;'><span class='small'>{}</span></p>".format(description)
			htmlText += u"<table style='width: 100%'>"
			for i in xrange(lines):
				htmlText += "<tr class='rowHeight'><td class='hrulefill'></td></tr>"
			htmlText += u"</table>"
			return htmlText
		else:
			return ""


	def __isForSpecies(self, species=None):
		if species is None or species == self.__character.species:
			return True
		else:
			return False


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

		text = u"<span class='dots'>{}</span>".format(text)
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
			image = QImage(":sheet/images/species/Mage/Background.jpg")
			self.__painter.drawImage(rect, image)
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
		#scale = min(scaleFactor)
		scale = scaleFactor[0]
		self.__painter.scale(scale, scale)
		self.__painter.setRenderHint ( QPainter.Antialiasing )

		self.__paperSize = (
			self.__printer.width() / scale,
			self.__printer.height() / scale,
		)
		#self.__paperSize = (
			#self.__printer.width() / scaleFactor[0],
			#self.__printer.height() / scaleFactor[1],
		#)

		self.__painter.save()

		## Hintergrundbild:
		self._drawBackground()
		#posY = 0.01 * self.__paperSize[1]
		posY = 0
		width = 0.33 * self.__paperSize[0]
		if self.__character.species == "Changeling":
			posY = 0.035 * self.__paperSize[1]
			width = 0.35 * self.__paperSize[0]
		elif self.__character.species == "Mage":
			posY = 0.01 * self.__paperSize[1]
			width = 0.33 * self.__paperSize[0]
		elif self.__character.species == "Vampire":
			posY = 0
			width = 0.25 * self.__paperSize[0]
		elif self.__character.species == "Werewolf":
			posY = 0.01 * self.__paperSize[1]
			width = 0.33 * self.__paperSize[0]
		self._drawLogo(posY, width)

		## HTML-Struktur drucken.
		self.__mainFrame.render ( self.__painter )

		self.__painter.restore()

		self.__painter.end()

		for tmp in self.__persistentResourceFiles.values():
			os.remove("{}".format(tmp.name))




