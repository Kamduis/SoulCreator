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

from PySide.QtCore import Qt, QObject, QRectF, QRect
from PySide.QtGui import QColor, QPen, QBrush, QPainter, QImage, QFont, QFontDatabase, QFontMetrics

from src.GlobalState import GlobalState
from src.Config import Config
from src.Error import ErrSpeciesNotExisting
from src.Random import Random
from src.Datatypes.Identity import Identity
from src.Calc.CalcAdvantages import CalcAdvantages
from src.Debug import Debug




class DrawSheet(QObject):
	"""
	\brief Führt das Drucken des Charakters aus.

	Mit Hilfe dieser Klasse können die Charakterwerte auf Papier gebannt werden.

	\todo Bei Werwölfen wird die Rites-Kraft noch nicht beim Zeichnen der Kräfte unter Renown berücksichtigt.
	"""

	def __init__(self, template, character, printer, parent=None):
		QObject.__init__(self, parent)

		self.__storage = template
		self.__character = character
		self.__calc = CalcAdvantages(self.__character)

		self.__painter = QPainter()
		self.__printer = printer

		self.__borderFrameX = 15
		self.__borderFrameY = self.__borderFrameX

		self.__lineWidth = .75
		self.__dotDiameterH = 9
		self.__dotDiameterV = self.__dotDiameterH
		self.__dotBigDiameterH = 12
		self.__dotBigDiameterV = self.__dotBigDiameterH
		self.__dotLineWidth = .5
		self.__dotSep = 2
		self.__textDotSep = 4
		self.__dotsWidth = 0

		## Die Farbe, mit welcher die Punkte auf dem Charakterbogen ausgefüllt werden.
		self.__colorFill = QColor( 0, 0, 0 )
		self.__colorEmpty = QColor( 255, 255, 255 )
		self.__colorText = QColor( 0, 0, 0 )

		## Schriften sind Abhängig von der Spezies.
		self.__fontMain = QFont("TeX Gyre Pagella", 10)
		self.__fontSans = QFont("TeX Gyre Heros" )
		self.__headingSep = 4

		self.__traitMax = self.__storage.maxTrait(self.__character.species, self.__character.powerstat)
		self.__traitMaxStandard = 5


	def print(self):
		"""
		Hier wird gezeichnet und gedruckt.
		"""
		
		if self.__character.species == "Human":
			self.__fontHeading = QFont("ArchitectsDaughter", 13 )
			self.__fontSubHeading = QFont("ArchitectsDaughter", 11 )
		elif self.__character.species == "Changeling":
			self.__fontHeading = QFont("Mutlu", 15 )
			self.__fontSubHeading = QFont("Mutlu", 13 )
			# Der Rahmen macht es notwendig, daß Wechselbälger einen breiteren Rahmen haben, der für die Charakterwerte nicht zur Verfügung steht.
			self.__borderFrameX = 55
			self.__borderFrameY = self.__borderFrameX
		elif self.__character.species == "Mage":
			self.__fontHeading = QFont("Tangerine", 17 )
			self.__fontSubHeading = QFont("Tangerine", 15 )
		elif self.__character.species == "Vampire":
			self.__fontHeading = QFont("Cloister Black", 15 )
			self.__fontSubHeading = QFont("Cloister Black", 13 )
			self.__borderFrameX = 44
			self.__borderFrameY = 53
		elif self.__character.species == "Werewolf":
			self.__fontHeading = QFont("Note this", 15 )
			self.__fontSubHeading = QFont("Note this", 13 )
		else:
			#self.__fontHeading = QFont("HVD Edding 780", 14 )	# Tiere
			raise ErrSpeciesNotExisting( character.species )
		self.__fontScript = QFont("Blokletters Balpen", 6 )

		## Die Schrifthöhe muß bei einigen Schriftarten Manuell festgelegt werden, damit Überschneidungen möglich sind.
		fontHeadingMetrics = QFontMetrics(self.__fontHeading)
		self.__fontHeadingHeight = fontHeadingMetrics.height()
		self.__fontHeadingHeightAscent = fontHeadingMetrics.ascent()
		fontSubHeadingMetrics = QFontMetrics(self.__fontHeading)
		self.__fontSubHeadingHeight = fontSubHeadingMetrics.height()
		self.__fontSubHeadingHeightAscent = fontHeadingMetrics.ascent()
		if self.__character.species == "Changeling":
			self.__fontHeadingHeight *= .5
			self.__fontHeadingHeightAscent *= .5
			self.__fontSubHeadingHeight *= .5
			self.__fontSubHeadingHeightAscent *= .5
		else:
			self.__fontHeadingHeight *= .7
			self.__fontHeadingHeightAscent *= .7
			self.__fontSubHeadingHeight *= .7
			self.__fontSubHeadingHeightAscent *= .7

		self.__pageWidth = self.__printer.width() - 2 * self.__borderFrameX
		self.__pageHeight = self.__printer.height() - 2 * self.__borderFrameY

		self.__painter.begin( self.__printer )

		self.__painter.setPen( self.__colorText )
		self.__painter.setBrush( self.__colorFill )

		image  = QImage( ":/characterSheets/images/Charactersheet-Human.jpg" )
		if ( self.__character.species == "Human" ):
			pass
		elif ( self.__character.species == "Changeling" ):
			image = QImage( ":/characterSheets/images/Charactersheet-Changeling-1.jpg" )
		elif ( self.__character.species == "Mage" ):
			image = QImage( ":/characterSheets/images/Charactersheet-Mage-1.jpg" )
		elif ( self.__character.species == "Vampire" ):
			image = QImage( ":/characterSheets/images/Charactersheet-Vampire-1.jpg" )
		elif ( self.__character.species == "Werewolf" ):
			image = QImage( ":/characterSheets/images/Charactersheet-Werewolf-1.jpg" )
		else:
			raise ErrSpeciesNotExisting( self.__character.species )

		## Grundeinstellungen des Painters sind abgeschlossen. Dies ist der Zusatnd, zu dem wir zurückkehren, wenn wir painter.restore() aufrufen.
		self.__painter.save()

		if GlobalState.isDebug:
			## Damit ich weiß, Wo ich meine Sachen platzieren muß kommt erstmal das Bild dahinter.
			source = QRectF ( 0.0, 0.0, float( image.width() ), float( image.height() ) )
			target = QRectF( 0.0, 0.0, float( self.__printer.width() ), float( self.__printer.height() ) )
			self.__painter.drawImage(target, image, source)

		## Hiermit wird der Seitenrahmen eingehalten.
		self.__painter.translate(self.__borderFrameX, self.__borderFrameY)

		## Die Breite der Punktwerte hängt vom Eigenschaftshöchstwert für den Charakter ab.
		self.__dotsWidth = self.__traitMax * (self.__dotDiameterH + self.__dotLineWidth)
		self.__dotsWidthStandard = self.__traitMaxStandard * (self.__dotDiameterH + self.__dotLineWidth)
		
		self.__painter.save()

		self._drawBackground()

		if GlobalState.isDebug:
			self.__drawGrid()

		lengthX = 220
		if self.__character.species == "Changeling":
			lengthX = 300
		elif self.__character.species == "Vampire":
			lengthX = 160
		self._drawLogo(offsetV=0, width=lengthX, height=80)

		posY = 80
		if self.__character.species == "Changeling":
			posY = 75
		self._drawInfo(offsetV=posY)

		self._drawAttributes(offsetV=140)

		lengthX = 300
		lengthY = 580
		if self.__character.species == "Changeling":
			lengthX = 230
			lengthY = 550
		elif self.__character.species == "Vampire":
			lengthX = 230
			lengthY = 580
		self._drawSkills(offsetH=0, offsetV=210, width=lengthX, height=lengthY)

		posX = 310
		lengthX = 300
		if self.__character.species == "Changeling":
			posX = 240
			posY = 210
			lengthX = 240
		elif self.__character.species == "Vampire":
			posX = 240
			posY = 210
			lengthX = 240
		if self.__character.species != "Human":
			self._drawPowers(offsetH=posX, offsetV=posY, width=lengthX, height=180)

		posY = 210
		lengthY = 400
		if self.__character.species == "Changeling":
			posY = 400
			lengthY = 290
		elif self.__character.species == "Vampire":
			posY = 400
			lengthY = 320
		self._drawMerits(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		posY = 620
		if self.__character.species == "Changeling":
			posY = 700
		elif self.__character.species == "Vampire":
			posY = 730
		self._drawFlaws(offsetH=posX, offsetV=posY, width=lengthX, height=60)

		posX = 570
		lengthX = 193
		if self.__character.species == "Changeling":
			posX = 490
			lengthX = 193
		elif self.__character.species == "Vampire":
			posX = 490
			lengthX = 210
		self._drawAdvantages(offsetH=posX, offsetV=210, width=lengthX)

		posY = 320
		if self.__character.species == "Changeling":
			posY = 300
		elif self.__character.species == "Vampire":
			posY = 300
		self._drawHealth(offsetH=posX, offsetV=posY, width=lengthX)

		posY = 400
		if self.__character.species == "Changeling":
			posY = 360
		elif self.__character.species == "Vampire":
			posY = 360
		self._drawWillpower(offsetH=posX, offsetV=posY, width=lengthX)

		if self.__character.species == "Changeling" or self.__character.species == "Vampire":
			self._drawPowerstat(offsetH=posX, offsetV=420, width=lengthX)
			self._drawFuel(offsetH=posX, offsetV=470, width=lengthX)

		posY = 490
		if self.__character.species == "Changeling":
			posY = 570
		elif self.__character.species == "Vampire":
			posY = 610
		self._drawMorality(offsetH=posX, offsetV=posY, width=lengthX, species=self.__character.species)

		self.__painter.restore()

		self.__painter.restore()

		self.__painter.end()


	def __drawGrid(self):
		"""
		Diese Funktion zeichnet ein Gitter, damit man weiß, an welcher Position man die Einträge platzieren muß.
		"""

		self.__painter.save()

		fontLcl = self.__fontSans
		fontLcl.setPointSize(4)
		self.__painter.setFont(fontLcl)
		self.__painter.setRenderHint(QPainter.TextAntialiasing)
		self.__painter.save()
		
		pen = QPen(Qt.DashLine)
		pen.setColor(QColor(0,0,255))
		self.__painter.setPen(pen)
		
		for i in range(self.__pageWidth)[::10]:
			self.__painter.drawLine(i, 0, i, self.__pageHeight)
		for i in range(self.__pageHeight)[::10]:
			self.__painter.drawLine(0, i, self.__pageWidth, i)

		self.__painter.restore()

		self.__painter.save()

		self.__painter.setPen(QColor(0,127,127))
		for i in range(self.__pageWidth)[::100]:
			self.__painter.drawLine(i, 0, i, self.__pageHeight)
			self.__painter.drawText(i+1, 0, 10, 10, Qt.AlignLeft, unicode(i))
		for i in range(self.__pageHeight)[::100]:
			self.__painter.drawLine(0, i, self.__pageWidth, i)
			self.__painter.drawText(1, i, 10, 10, Qt.AlignLeft, unicode(i))

		self.__painter.restore()

		self.__painter.restore()


	def _drawBackground(self):
		"""
		Der Hintergrund für den Charakterbogen wird dargestellt.
		"""

		self.__painter.save()

		rect = QRect(0 - self.__borderFrameX, 0 - self.__borderFrameY, self.__pageWidth + 2 * self.__borderFrameX, self.__pageHeight + 2 * self.__borderFrameY)
		if self.__character.species == "Changeling":
			image = QImage(":sheet/images/sheet/Changeling-Rahmen.jpg")
			self.__painter.drawImage(rect, image)
		elif self.__character.species == "Mage":
			#image = QImage(":sheet/images/sheet/WorldOfDarkness.jpg")
			pass
		if self.__character.species == "Vampire":
			image = QImage(":sheet/images/sheet/Vampire-Rahmen.jpg")
			self.__painter.drawImage(rect, image)
		else:
			rect = QRect(0 - self.__borderFrameX, 0 - self.__borderFrameY, (self.__pageWidth + 2 * self.__borderFrameX) / 7, self.__pageHeight + 2 * self.__borderFrameY)
			image = QImage(":sheet/images/sheet/WorldOfDarkness-SeitenrandL-gray.png")
			self.__painter.drawImage(rect, image)
			#if GlobalState.isDebug:
				#self.__drawBB(rect.x(), rect.y(), rect.width(), rect.height())

			rect = QRect(self.__pageWidth + self.__borderFrameX - (self.__pageWidth + 2 * self.__borderFrameX) / 7, 0 - self.__borderFrameY, (self.__pageWidth + 2 * self.__borderFrameX) / 7, self.__pageHeight + 2 * self.__borderFrameY)
			image = QImage(":sheet/images/sheet/WorldOfDarkness-SeitenrandR-gray.png")
			self.__painter.drawImage(rect, image)
			#if GlobalState.isDebug:
				#self.__drawBB(rect.x(), rect.y(), rect.width(), rect.height())

		self.__painter.restore()


	def _drawLogo(self, offsetV, width, height):
		"""
		Zeichnet das Logo auf den Charakterbogen. Das Logo wird auf der Seite immer horizontal zentriert dargestellt.

		\param offsetV Obere Kante des Logos.
		\param width Breite des Logos.
		\param height Höhe des Logos.
		"""

		self.__painter.save()

		offsetH = (self.__pageWidth - width) / 2

		rect = QRect(offsetH, offsetV, width, height)
		image = QImage(":sheet/images/sheet/WorldOfDarkness.jpg")
		if self.__character.species == "Changeling":
			image = QImage(":sheet/images/sheet/Changeling.png")
			pass
		elif self.__character.species == "Mage":
			#image = QImage(":sheet/images/sheet/WorldOfDarkness.jpg")
			pass
		if self.__character.species == "Vampire":
			image = QImage(":sheet/images/sheet/Vampire.png")
		if self.__character.species == "Werewolf":
			#image = QImage(":sheet/images/sheet/WorldOfDarkness.jpg")
			pass
		else:
			pass
		self.__painter.drawImage(rect, image)

		if GlobalState.isDebug:
			self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawInfo(self, offsetV, distanceV=0):
		"""
		Diese Funktion Schreibt Namen, Virtue/Vice etc. in den Kopf des Charakterbogens.

		\param offsetV Vertikaler Abstand zwischen nutzbarer Bildkante und oberkante der BondingBox für die Informationszeilen.
		\param distanceV Vertikaler Abstand zwischen den Zeilen.
		"""

		text = [
			[ u"Name:", u"Concept:", ],
			[ u"Virute:", u"Vice:", ],
			[ u"Chronicle:", u"Faction:", ],
		]
		textCharacter = [
			[ Identity.displayNameDisplay(self.__character.identities[0].surename, self.__character.identities[0].firstname, self.__character.identities[0].nickname), u"", ],
			[ self.__character.virtue, self.__character.vice, ],
			[ u"", u"", ],
		]
		if self.__character.species == "Changeling":
			text = [
				[ text[0][0], text[0][1], u"", ],
				[ text[1][0], text[1][1], u"Motley:", ],
				[ self.__storage.breedTitle(self.__character.species), u"Kith:", self.__storage.factionTitle(self.__character.species), ],
			]
			textCharacter = [
				[ textCharacter[0][0], textCharacter[0][1], u"", ],
				[ textCharacter[1][0], textCharacter[1][1], u"", ],
				[ self.__character.breed, u"", self.__character.faction, ],
			]
		elif self.__character.species == "Vampire":
			text = [
				[ text[0][0], text[0][1], u"Sire:", ],
				[ text[1][0], text[1][1], u"Coterie:", ],
				[ self.__storage.breedTitle(self.__character.species), u"Bloodline:", self.__storage.factionTitle(self.__character.species), ],
			]
			textCharacter = [
				[ textCharacter[0][0], textCharacter[0][1], u"", ],
				[ textCharacter[1][0], textCharacter[1][1], u"", ],
				[ self.__character.breed, u"", self.__character.faction, ],
			]

		self.__painter.save()

		self.__painter.setFont(self.__fontSubHeading)

		fontSubHeadingMetrics = QFontMetrics(self.__painter.font())
		fontSubHeadingHeight = fontSubHeadingMetrics.height()
		fontSubHeadingHeightDiff = (fontSubHeadingMetrics.ascent() - self.__fontSubHeadingHeightAscent)

		distanceH = self.__pageWidth / 3

		width = []
		for i in xrange(len(text)):
			subWidth = []
			for j in xrange(len(text[i])):
				textWidth = fontSubHeadingMetrics.boundingRect(text[i][j]).width()
				self.__painter.drawText(i * distanceH, offsetV - fontSubHeadingHeightDiff + j * (self.__fontSubHeadingHeight + distanceV), textWidth, fontSubHeadingHeight, Qt.AlignLeft, text[i][j])
				subWidth.append(textWidth)
			width.append(max(subWidth))

		self.__painter.restore()
		
		self.__painter.save()
		
		self.__painter.setFont(self.__fontScript)
		fontScriptMetrics = QFontMetrics(self.__painter.font())
		fontScriptHeight = fontScriptMetrics.height()
		fontScriptHeightDiff = fontSubHeadingMetrics.ascent() - fontScriptMetrics.ascent()

		for i in xrange(len(textCharacter)):
			for j in xrange(len(textCharacter[i])):
				textWidth = fontScriptMetrics.boundingRect(textCharacter[i][j]).width()
				self.__painter.drawText(i * distanceH + width[i], offsetV - fontSubHeadingHeightDiff + fontScriptHeightDiff + j * (self.__fontSubHeadingHeight + distanceV), textWidth, fontScriptHeight, Qt.AlignLeft, textCharacter[i][j])

		if GlobalState.isDebug:
			self.__drawBB(0, offsetV, self.__pageWidth, len(text[0]) * self.__fontSubHeadingHeight + (len(text[0]) - 1) * distanceV)

		self.__painter.restore()


	def _drawAttributes(self, offsetV=0):
		"""
		Diese Funktion Zeichnet die Attribute

		\param offsetV Vertikaler Abstand zwischen Bildkante und Boundingbox des Attributsblocks.
		"""

		self.__painter.save()
		
		self.__painter.setFont(self.__fontSubHeading)
		fontSubHeadingMetrics = QFontMetrics(self.__painter.font())
		fontSubHeadingHeight = fontSubHeadingMetrics.height()
		fontSubHeadingHeightDiff = (fontSubHeadingMetrics.ascent() - self.__fontSubHeadingHeightAscent)
		
		textwidthArray = []
		for item in Config.attributeSorts:
			textwidthArray.append(fontSubHeadingMetrics.boundingRect(item).width())
		headingWidth = max(textwidthArray)

		for i in xrange(len(Config.attributeSorts)):
			self.__painter.drawText(0, offsetV - fontSubHeadingHeightDiff + i * self.__fontSubHeadingHeight, headingWidth, fontSubHeadingHeight, Qt.AlignRight, Config.attributeSorts[i])

		self.__painter.restore()

		self.__painter.save()

		mainFont = self.__fontMain
		mainFont.setWeight(QFont.Bold)
		self.__painter.setFont(mainFont)
		fontMetrics = QFontMetrics(self.__painter.font())
		fontHeight = fontMetrics.height()
		fontHeightDiff = fontSubHeadingMetrics.ascent() - fontMetrics.ascent()

		distanceH = (self.__pageWidth - headingWidth) / 3

		i = 0
		for item in Config.attributes:
			j = 0
			for subitem in item[1]:
				attrib = self.__character.traits["Attribute"][item[0]][subitem]
				self.__drawTrait(headingWidth + i * distanceH, offsetV - fontSubHeadingHeightDiff + fontHeightDiff + j * self.__fontSubHeadingHeight, width=distanceH, name=attrib.name, value=attrib.value, maxValue=self.__traitMax, align=Qt.AlignRight)
				j += 1
			i += 1

		if GlobalState.isDebug:
			self.__drawBB(0, offsetV, self.__pageWidth, len(Config.attributeSorts) * self.__fontHeadingHeight)

		self.__painter.restore()


	def _drawSkills(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Bannt die Fertigkeiten auf den Charakterbogen.

		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox aller Fertigkeiten.
		\param distanceV Der vertikale Zwischenraum zwischen den einzelnen Fertigkeitskategorien.
		\param width Die Breite der Fertigkeits-Spalte.
		\param height Die Höhe, auf welche die Fertigkeitsspalte gestreckt werden soll der Fertigkeits-Spalte.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		mainFont = self.__fontMain
		mainFont.setWeight(QFont.Normal)
		self.__painter.setFont(mainFont)

		traitCount = 0
		traitsToDisplay = {}
		for item in self.__character.traits["Skill"]:
			traitsToDisplay.setdefault(item,[])
			traits = self.__character.traits["Skill"][item].keys()
			traits.sort()
			for subitem in traits:
				trait = self.__character.traits["Skill"][item][subitem]
				if (
					(not trait.era or trait.era == self.__character.era) and
					(not trait.age or trait.age == Config.getAge(self.__character.age))
				):
					traitsToDisplay[item].append(trait)
					traitCount += 1

		fontMetrics = QFontMetrics(self.__fontMain)
		if height:
			textHeight = height - len(Config.mainCategories) * self.__fontHeadingHeight - (len(Config.mainCategories) - 1) * self.__headingSep
			textHeight /= traitCount
		else:
			textHeight = fontMetrics.height() * .7

		# Warnung, hier muß darauf geachtet werden, daß dies auch die Schriftart/-größe der Überschrift ist.
		fontHeadingMetrics = QFontMetrics(self.__fontHeading)
		fontHeadingHeight = fontHeadingMetrics.height()

		i = 0
		j = 0
		## Die Verwendung von Config.mainCategories garantiert die richtige Reihenfolge der Kategorien.
		for item in Config.mainCategories:
			self.__drawHeading(offsetH, offsetV + i * (self.__fontHeadingHeight + self.__headingSep) + j * textHeight, width, item)
			for subitem in traitsToDisplay[item]:
				self.__drawTrait(offsetH, offsetV + self.__fontHeadingHeight + i * (self.__fontHeadingHeight + self.__headingSep) + j * textHeight, width=width, name=subitem.name, value=subitem.value, maxValue=self.__traitMax, text=", ".join(subitem.specialties))
				j += 1
			i += 1

		if GlobalState.isDebug:
			self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawPowers(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Bannt die übernatürlichen Kräfte auf den Charakterbogen.

		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox aller Fertigkeiten.
		\param width Die Breite der Spalte.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		mainFont = self.__fontMain
		mainFont.setWeight(QFont.Normal)
		self.__painter.setFont(mainFont)

		self.__drawHeading(offsetH, offsetV, width, self.__storage.powerName(self.__character.species, "power"))

		fontMetrics = QFontMetrics(self.__painter.font())
		textHeight = fontMetrics.height() - 3
		numOfTraits = 0
		if height:
			for item in self.__character.traits["Power"].values():
				for subitem in item.values():
					if subitem.value > 0:
						numOfTraits += 1
			if numOfTraits < 1:
				numOfTraits = 1
			textHeightCalculated = (height - self.__fontHeadingHeight) / numOfTraits
			if textHeightCalculated < textHeight:
				textHeight = textHeightCalculated

		j = 0
		for item in self.__character.traits["Power"]:
			traits = self.__character.traits["Power"][item].values()
			traits.sort()
			for subitem in traits:
				if (subitem.isAvailable and subitem.value > 0):
					self.__drawTrait(offsetH, offsetV + self.__fontHeadingHeight + j * textHeight, width=width, name=subitem.name, value=subitem.value)
					j += 1
			if numOfTraits < 1:
				numOfTraits = j

		if GlobalState.isDebug:
			if not height:
				height = self.__fontHeadingHeight + numOfTraits * textHeight
			self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawMerits(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Bannt die Merits auf den Charakterbogen.

		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox aller Fertigkeiten.
		\param width Die Breite der Merit-Spalte.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		mainFont = self.__fontMain
		mainFont.setWeight(QFont.Normal)
		self.__painter.setFont(mainFont)

		self.__drawHeading(offsetH, offsetV, width, self.tr("Merits"))

		fontMetrics = QFontMetrics(self.__painter.font())
		textHeight = fontMetrics.height() - 3
		numOfTraits = 0
		if height:
			for item in self.__character.traits["Merit"].values():
				for subitem in item.values():
					if subitem.value > 0:
						numOfTraits += 1
			if numOfTraits < 1:
				numOfTraits = 1
			textHeightCalculated = (height - self.__fontHeadingHeight) / numOfTraits
			if textHeightCalculated < textHeight:
				textHeight = textHeightCalculated

		j = 0
		for item in self.__character.traits["Merit"]:
			traits = self.__character.traits["Merit"][item].values()
			traits.sort()
			for subitem in traits:
				if (subitem.isAvailable and subitem.value > 0):
					self.__drawTrait(offsetH, offsetV + self.__fontHeadingHeight + j * textHeight, width=width, name=subitem.name, value=subitem.value)
					j += 1
			if numOfTraits < 1:
				numOfTraits = j

		if GlobalState.isDebug:
			if not height:
				height = self.__fontHeadingHeight + numOfTraits * textHeight
			self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawFlaws(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Bannt die Nachteile auf den Charakterbogen.

		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox aller Fertigkeiten.
		\param width Die Breite der Merit-Spalte.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		mainFont = self.__fontMain
		mainFont.setWeight(QFont.Normal)
		self.__painter.setFont(mainFont)

		fontMetrics = QFontMetrics(self.__painter.font())
		textHeight = fontMetrics.height() - 3

		self.__drawHeading(offsetH, offsetV, width, self.tr("Flaws"))

		flaws = []
		for item in self.__character.traits["Flaw"]:
			traits = self.__character.traits["Flaw"][item].values()
			traits.sort()
			for subitem in traits:
				if (subitem.isAvailable and subitem.value > 0):
					text = subitem.name
					if subitem.customText:
						text += " ({})".format(subitem.customText)
					flaws.append(text)
		flawsLine = ", ".join(flaws)
		rect = QRect(offsetH, offsetV + self.__fontHeadingHeight, width, height)
		self.__painter.drawText(rect, Qt.AlignLeft | Qt.TextWordWrap, flawsLine)

		if GlobalState.isDebug:
			self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawAdvantages(self, offsetH=0, offsetV=0, width=None):
		"""
		Bannt die Berechneten Werte, Moral und Powerstat sowie die Energie auf den Charakterbogen.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox aller Fertigkeiten.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox aller Fertigkeiten.
		\param width Die Breite der Fertigkeits-Spalte.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		advantages = [
			[ self.tr("Size"), self.__calc.calcSize(), ],
			[ self.tr("Initiative"), self.__calc.calcInitiative(), ],
			[ self.tr("Speed"), self.__calc.calcSpeed(), ],
			[ self.tr("Defense"), self.__calc.calcDefense(), ],
			#[ self.tr("Health"), self.__calc.calcHealth(), ],
			#[ self.tr("Willpower"), self.__calc.calcWillpower(), ],
		]

		self.__painter.save()

		font = self.__fontMain
		self.__painter.setFont(font)

		fontMetrics = QFontMetrics(self.__fontMain)
		textHeight = fontMetrics.height() - 3

		verticalPos = offsetV
		for item in advantages:
			self.__drawTextWithValue(offsetH, verticalPos, width, item[0], item[1])
			verticalPos += textHeight
		self.__drawTextWithValue(offsetH, verticalPos, width, self.tr("Armor"), "{general}/{firearms}".format(general=self.__character.armor[0], firearms=self.__character.armor[0]))
		verticalPos += textHeight

		self.__painter.restore()

		if GlobalState.isDebug:
			self.__drawBB(offsetH, offsetV, width, verticalPos - offsetV)

		self.__painter.restore()


	def _drawHealth(self, offsetH=0, offsetV=0, width=None):
		"""
		Bannt die Gesundheit auf den Charakterbogen.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox aller Fertigkeiten.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox aller Fertigkeiten.
		\param width Die Breite der Fertigkeits-Spalte.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		self.__drawHeading(offsetH, offsetV, width, self.tr("Health"))
		self.__drawCenterDots(offsetH, offsetV + self.__fontHeadingHeight + self.__textDotSep, width=width, number=self.__calc.calcHealth(), squares=True, big=True)

		self.__painter.restore()


	def _drawWillpower(self, offsetH=0, offsetV=0, width=None):
		"""
		Bannt die Willenskraft auf den Charakterbogen.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox aller Fertigkeiten.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox aller Fertigkeiten.
		\param width Die Breite der Fertigkeits-Spalte.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		self.__drawHeading(offsetH, offsetV, width, self.tr("Willpower"))
		self.__drawCenterDots(offsetH, offsetV + self.__fontHeadingHeight + self.__textDotSep, width=width, number=self.__calc.calcWillpower(), maxNumber=Config.willpowerMax, squares=True, big=True)

		self.__painter.restore()


	def _drawPowerstat(self, offsetH=0, offsetV=0, width=None):
		"""
		Bannt den Powerstat (Wyrd, Gnosis etc.) auf den Charakterbogen.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox.
		\param width Die Breite der Spalte.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		self.__drawHeading(offsetH, offsetV, width, self.__storage.powerstatName(self.__character.species))
		self.__drawCenterDots(offsetH, offsetV + self.__fontHeadingHeight + self.__textDotSep, width=width, number=self.__character.powerstat, maxNumber=Config.powerstatMax, big=True)

		self.__painter.restore()


	def _drawFuel(self, offsetH=0, offsetV=0, width=None):
		"""
		Bannt den Energievorrat (Glamour, Mana etc.) auf den Charakterbogen.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox.
		\param width Die Breite der Spalte.
		"""

		self.__painter.save()

		self.__painter.setFont(self.__fontMain)

		if width == None:
			width = self.__pageWidth / 3

		self.__drawHeading(offsetH, offsetV, width, self.__storage.fuelName(self.__character.species))

		self.__drawSquares(offsetH, offsetV + self.__fontHeadingHeight + self.__textDotSep, number=self.__storage.fuelMax(species=self.__character.species, powerstat=self.__character.powerstat), perRow=10, big=True)

		text = "per Turn"
		fontMetrics = QFontMetrics(self.__painter.font())
		fontWidth = fontMetrics.boundingRect(text).width()

		self.__painter.drawText(offsetH + width - fontWidth, offsetV + self.__fontHeadingHeight, fontWidth, 2 * fontMetrics.height(), Qt.AlignCenter, "{}\n{}".format(self.__storage.fuelPerTurn(species=self.__character.species, powerstat=self.__character.powerstat), text))

		self.__painter.restore()


	def _drawMorality(self, offsetH=0, offsetV=0, width=None, species=Config.initialSpecies):
		"""
		Bannt die Moral auf den Charakterbogen.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox aller Fertigkeiten.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox aller Fertigkeiten.
		\param width Die Breite der Fertigkeits-Spalte.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		self.__drawHeading(offsetH, offsetV, width, self.__storage.moralityName(species))

		font = self.__fontMain
		self.__painter.setFont(font)

		fontMetrics = QFontMetrics(self.__painter.font())
		textHeight = fontMetrics.height() - 3
		textWidth = fontMetrics.boundingRect(unicode(Config.moralityTraitMax)).width()

		self.__painter.save()
		for i in xrange(Config.moralityTraitMax):
			lcl_height = offsetV + self.__fontHeadingHeight + (i+1) * textHeight
			self.__painter.drawText(offsetH, lcl_height - textHeight, textWidth, textHeight, Qt.AlignRight, unicode(Config.moralityTraitMax-i))
			if (Config.moralityTraitMax - i) <= Config.moralityTraitDefaultValue:
				self.__painter.drawLine(offsetH + textWidth, lcl_height, offsetH + width - self.__dotDiameterH - self.__dotSep, lcl_height)
			self.__painter.save()
			if (Config.moralityTraitMax - i) <= self.__character.morality:
				self.__painter.setBrush(self.__colorFill)
			else:
				self.__painter.setBrush(self.__colorEmpty)
			self.__painter.drawEllipse(offsetH + width - self.__dotDiameterH, lcl_height - self.__dotDiameterV, self.__dotDiameterH, self.__dotDiameterV)
			self.__painter.restore()
		self.__painter.restore()

		self.__painter.restore()


	def __drawHeading(self, posX, posY, width, text):
		"""
		Zeichnet eine Überschrift in der für die Spezies vorgesehenen Schriftart.

		\param poxX Obere Kante der Boundingbox für die Überschrift.
		\param poxY Linke Kante der Boundingbox für die Überschrift.
		\param width Breite der Überschrift
		\param text Der Text der Überschrift
		\return die Höhe, welche die Überschrift in Anspruch nimmt. Dies ist nützlich, um den Text darunter besser paltzieren zu können.
		"""

		self.__painter.save()

		self.__painter.setFont(self.__fontHeading)
		fontMetrics = QFontMetrics(self.__painter.font())
		fontHeight = fontMetrics.height()# Tatsächliche Höhe der Schrift

		## Differenz der tatsächlichen Höhe der Schrift, und der Höhe für die Platz reserviert werden soll.
		heightDiff = (fontHeight - self.__fontHeadingHeight)

		if self.__character.species == "Human":
			imageRect = QRect(posX, posY, width, self.__fontHeadingHeight)
			image = QImage(":sheet/images/sheet/WorldOfDarkness-BalkenOben.png")
			rnd = Random.random(1)
			if rnd == 0:
				image = image.mirrored(True, False)
			self.__painter.drawImage(imageRect, image)

		self.__painter.drawText(posX, posY - heightDiff / 2, width, fontHeight, Qt.AlignCenter, text)

		self.__painter.restore()


	def __drawValueDots(self, posX, posY, value=0, maxValue=5):
		"""
		Zeichnet die Punkte für den Eigenschaftswert. Übersteigt value den Wert von maxValue, werden nur maxValue Punkte dargestellt.
		"""

		if value > maxValue:
			value = maxValue

		self.__painter.save()

		pen = self.__painter.pen()
		pen.setWidthF(self.__dotLineWidth)
		self.__painter.setPen(pen)

		self.__painter.save()

		self.__painter.setBrush(self.__colorFill)

		for i in xrange(value):
			self.__painter.drawEllipse(posX + i * self.__dotDiameterH, posY - self.__dotDiameterV, self.__dotDiameterH, self.__dotDiameterV)

		self.__painter.restore()

		self.__painter.save()

		self.__painter.setBrush(self.__colorEmpty)

		for i in range(value, maxValue):
			self.__painter.drawEllipse(posX + i * self.__dotDiameterH, posY - self.__dotDiameterV, self.__dotDiameterH, self.__dotDiameterV)

		self.__painter.restore()

		self.__painter.restore()


	def __drawTrait(self, posX, posY, width, align=Qt.AlignLeft, name="", text="", value=0, maxValue=5):
		"""
		Schreibt eine Eigenschaft mit den Punktwerten.

		posX und posY bestimmen den Punkt der Auflagelinie des Textes.
		"""

		self.__painter.save()

		fontMetrics = QFontMetrics(self.__painter.font())
		textHeight = fontMetrics.height()
		dotsWidth = maxValue * (self.__dotDiameterH + self.__dotLineWidth / 2)
		textWidth = fontMetrics.boundingRect(name).width()

		self.__painter.drawText(posX, posY, width - dotsWidth - self.__dotSep, textHeight, align, name)

		## Bei linksbündigen Eigenschaften muß eine Linie gezogen werden, damit man weiß, welche Punkte zu welcher Eigenschaft gehören.
		if align == Qt.AlignLeft:
			## Wenn text angegeben wird, wird dieser auf die Linie geschrieben.
			smallWidth = 0
			if text:
				self.__painter.save()
				font = self.__painter.font()
				font.setPointSize(font.pointSize() - 4)
				self.__painter.setFont(font)

				fontMetricsSmall = QFontMetrics(self.__painter.font())
				textWidthSmall = fontMetricsSmall.boundingRect(text).width()

				smallAlign = align
				smallWidth = textWidthSmall
				if textWidthSmall > width - textWidth - dotsWidth - self.__dotSep:
					smallAlign = align | Qt.TextWordWrap
					smallWidth = width - textWidth - dotsWidth - self.__dotSep
				self.__painter.drawText(posX + textWidth, posY +  fontMetrics.ascent() - fontMetricsSmall.ascent(), smallWidth, 2 * fontMetricsSmall.height(), smallAlign, text)
				self.__painter.restore()

			if smallWidth < width - textWidth - dotsWidth - self.__dotSep:
				self.__painter.save()
				pen = self.__painter.pen()
				pen.setWidthF(self.__lineWidth)
				self.__painter.setPen(pen)
				self.__painter.drawLine(posX + textWidth + smallWidth, posY +  fontMetrics.ascent(), posX + width - dotsWidth - self.__textDotSep, posY +  fontMetrics.ascent())
				self.__painter.restore()
		
		self.__drawValueDots(posX + width - dotsWidth, posY + fontMetrics.ascent(), value, maxValue)

		self.__painter.restore()


	def __drawTextWithValue(self, posX, posY, width, text="", value=0):
		"""
		Schreibt einen Text und hinter einer Abstandslinie den zugehörigen Wert.

		\param posX Linke Kante der Zeile.
		\param posY Oberkante des Textes.
		"""

		self.__painter.save()

		fontMetrics = QFontMetrics(self.__painter.font())
		textHeight = fontMetrics.height()
		textWidth = fontMetrics.boundingRect(text).width()
		valueWidth = fontMetrics.boundingRect(unicode(value)).width()

		self.__painter.drawText(posX, posY, textWidth, textHeight, Qt.AlignLeft, text)

		self.__painter.save()
		pen = self.__painter.pen()
		pen.setWidthF(self.__lineWidth)
		self.__painter.setPen(pen)
		self.__painter.drawLine(posX + textWidth, posY + fontMetrics.ascent(), posX + width - valueWidth, posY + fontMetrics.ascent())
		self.__painter.restore()

		self.__painter.drawText(posX + width - valueWidth, posY, valueWidth, textHeight, Qt.AlignRight, unicode(value))

		self.__painter.restore()


	def __drawCenterDots(self, posX, posY, width, number=0, maxNumber=None, squares=False, big=False):
		"""
		Zeichnet Punkte über Kästchen. Diese werden Mittig in der angegebenen Breite ausgerichtet.
		"""

		if maxNumber == None:
			maxNumber = number

		if big:
			dotDiameter = self.__dotBigDiameterH
		else:
			dotDiameter = self.__dotDiameterH

		self.__painter.save()

		pen = self.__painter.pen()
		pen.setWidthF(self.__dotLineWidth)
		self.__painter.setPen(pen)

		self.__painter.save()

		widthDots = maxNumber * (dotDiameter + self.__dotLineWidth / 2) + (number - 1) * self.__dotSep

		self.__painter.setBrush(self.__colorFill)

		for i in xrange(number):
			self.__painter.drawEllipse(posX + i * (dotDiameter + self.__dotSep) + (width - widthDots) / 2, posY, dotDiameter, dotDiameter)

		self.__painter.restore()

		self.__painter.save()

		self.__painter.setBrush(self.__colorEmpty)

		for i in xrange(number, maxNumber):
			self.__painter.drawEllipse(posX + i * (dotDiameter + self.__dotSep) + (width - widthDots) / 2, posY, dotDiameter, dotDiameter)

		self.__painter.restore()

		if squares:
			self.__painter.save()

			self.__painter.setBrush(self.__colorEmpty)

			for i in xrange(maxNumber):
				self.__painter.drawRect(posX + i * (dotDiameter + self.__dotSep) + (width - widthDots) / 2, posY + dotDiameter + self.__dotSep, dotDiameter, dotDiameter)

			self.__painter.restore()

		self.__painter.restore()


	def __drawSquares(self, posX, posY, number=0, perRow=1, squares=False, big=False):
		"""
		Kästchen. Die Kästchen werden in mehreren Reihen angeordnet.

		\param perRow Wieviele Kästchen pro Reihe gezeichnet werden.
		"""

		if big:
			squareSide = self.__dotBigDiameterH
		else:
			squareSide = self.__dotDiameterH

		self.__painter.save()

		pen = self.__painter.pen()
		pen.setWidthF(self.__dotLineWidth)
		self.__painter.setPen(pen)

		widthSquares = number * (squareSide + self.__dotLineWidth / 2) + (number - 1) * self.__dotSep

		self.__painter.setBrush(self.__colorEmpty)

		i = 0
		numOfSquares = 0
		stopLoop = False
		while True:
			for j in xrange(perRow):
				self.__painter.drawRect(posX + j * (squareSide + self.__dotSep), posY + self.__dotSep + i * (squareSide + self.__dotSep), squareSide, squareSide)
				numOfSquares += 1
				if numOfSquares >= number:
					stopLoop = True
					break
			if stopLoop:
				break
			i += 1

		self.__painter.restore()


	def __drawBB(self, posX, posY, width, height):
		self.__painter.save()

		pen = QPen(Qt.DashDotDotLine)
		pen.setColor(QColor(255,0,0))
		pen.setWidthF(1)
		self.__painter.setPen(pen)
		self.__painter.setBrush(Qt.NoBrush)
		self.__painter.drawRect(posX, posY, width, height)

		self.__painter.restore()



