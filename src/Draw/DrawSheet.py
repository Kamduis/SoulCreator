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

import math
import copy

from PySide.QtCore import Qt, QObject, QRectF, QRect
from PySide.QtGui import QColor, QPen, QBrush, QPainter, QImage, QFont, QFontDatabase, QFontMetrics

from src.GlobalState import GlobalState
from src.Config import Config
from src.Error import ErrSpeciesNotExisting
from src.Calc.CalcShapes import CalcShapes
from src.Random import Random
from src.Datatypes.Identity import Identity
from src.Calc.CalcAdvantages import CalcAdvantages
from src.Calc.CalcShapes import CalcShapes
from src.Tools import ImageTools
from src.Debug import Debug




class DrawSheet(QObject):
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

		self.__borderFrameWest = 50
		self.__borderFrameEast = self.__borderFrameWest
		self.__borderFrameNorth = self.__borderFrameWest
		self.__borderFrameSouth = self.__borderFrameWest

		self.__lineWidth = 2.2
		self.__lineWidthBox = 3
		self.__dotDiameterH = 28
		self.__dotDiameterV = self.__dotDiameterH
		self.__dotBigDiameterH = 37
		self.__dotBigDiameterV = self.__dotBigDiameterH
		self.__dotLineWidth = 1.5
		self.__dotSep = 7
		self.__textDotSep = 13
		self.__dotsWidth = 0

		## Die Farbe, mit welcher die Punkte auf dem Charakterbogen ausgefüllt werden.
		self.__colorFill = QColor( "black" )
		self.__colorEmpty = QColor( "white" )
		self.__colorText = QColor( "black" )

		## Schriften sind Abhängig von der Spezies.
		#self.__fontMain = QFont("DejaVu Serif", 31)
		#self.__fontMain = QFont("TeXGyrePagella", 31)
		self.__fontMain = QFont("Linux Libertine O", 31)
		self.__fontMain_small = copy.copy(self.__fontMain)
		self.__fontMain_small.setPointSize(25)
		self.__fontMain_tiny = copy.copy(self.__fontMain)
		self.__fontMain_tiny.setPointSize(18)
		#self.__fontSans = QFont("DejaVu Sans", 31 )
		#self.__fontSans = QFont("TeXGyreHeros", 31 )
		#self.__fontSans_small = copy.copy(self.__fontSans)
		#self.__fontSans_small.setPointSize(25)
		## Mit dieser Schriftart werden Werte eingetragen, die normalerweise der Spier einträgt.
		self.__fontScript = QFont("Blokletters Balpen", 24 )
		self.__headingSep = 12.5
		self.__posSep = 30

		self.__traitMax = self.__storage.maxTrait(self.__character.species, self.__character.powerstat)
		self.__traitMaxStandard = 5


	def print(self):
		"""
		Einstellungen festlegen.
		"""

		if self.__character.species == "Human":
			self.__fontHeading = QFont("Architects Daughter", 40, QFont.Normal )
			self.__fontSubHeading = QFont("Architects Daughter", 35, QFont.Normal )
		elif self.__character.species == "Changeling":
			self.__fontHeading = QFont("Mutlu", 47, QFont.Normal )
			self.__fontSubHeading = QFont("Mutlu", 40, QFont.Normal )
			# Der Rahmen macht es notwendig, daß Wechselbälger einen breiteren Rahmen haben, der für die Charakterwerte nicht zur Verfügung steht.
			self.__borderFrameWest = 172
			self.__borderFrameEast = self.__borderFrameWest
			self.__borderFrameNorth = self.__borderFrameWest
			self.__borderFrameSouth = self.__borderFrameWest
		elif self.__character.species == "Mage":
			self.__fontHeading = QFont("Tangerine", 65, QFont.Normal )
			self.__fontSubHeading = QFont("Tangerine", 56, QFont.Normal )
		elif self.__character.species == "Vampire":
			self.__fontHeading = QFont("Cloister Black", 47, QFont.Bold )
			self.__fontSubHeading = QFont("Cloister Black", 40, QFont.Bold )
			self.__borderFrameWest = 135
			self.__borderFrameEast = 155
			self.__borderFrameNorth = 165
			self.__borderFrameSouth = 270
		elif self.__character.species == "Werewolf":
			self.__fontHeading = QFont("Note this", 47, QFont.Bold )
			self.__fontSubHeading = QFont("Note this", 40, QFont.Bold )
		else:
			#self.__fontHeading = QFont("HVD Edding 780", 44 )	# Tiere
			raise ErrSpeciesNotExisting( self.__character.species )

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

		self.__painter.begin( self.__printer )

		self.__painter.setPen( self.__colorText )
		self.__painter.setBrush( self.__colorFill )

		## Damit der Charakterbogen auf die Seite paßt, muß diese auf die Papiergröße skaliert werden.
		# Die Seitendimensionen werden willkürlich festgelegt und später dann auf das Papier skaliert.
		# DIN A4 => 210 mm Bei 300 dpi wären das 2460.9 Punkte. Das Runden wir auf eine schöne Runde Zahl auf.
		self.__paperWidth_defined = 2500#800
		self.__paperHeight_defined = int(self.__paperWidth_defined * math.sqrt(2))
		self.__paperWidth_real = self.__printer.width()
		self.__paperHeight_real = self.__printer.height()
		#scaleFactor = min(self.__paperWidth_real / self.__paperWidth_defined, self.__paperHeight_real / self.__paperHeight_defined)
		scaleFactorX = self.__paperWidth_real / self.__paperWidth_defined
		scaleFactorY = self.__paperHeight_real / self.__paperHeight_defined
		self.__painter.scale(scaleFactorX, scaleFactorY)

		self.__pageWidth = self.__paperWidth_defined - self.__borderFrameWest - self.__borderFrameEast
		self.__pageHeight = self.__paperHeight_defined - self.__borderFrameNorth - self.__borderFrameSouth

		## Hiermit wird der Seitenrahmen eingehalten.
		self.__painter.translate(self.__borderFrameWest, self.__borderFrameNorth)

		## Grundeinstellungen des Painters sind abgeschlossen. Dies ist der Zusatnd, zu dem wir zurückkehren, wenn wir painter.restore() aufrufen.
		self.__painter.save()

		## Das eigentliche Zeichnen des Charakterbogens.
		self.drawSheet_1()
		if self.__character.species != "Human":
			self.__printer.newPage()
			self.drawSheet_2()

		self.__painter.restore()

		self.__painter.end()


	def drawSheet_1(self):
		"""
		Hier wird gezeichnet.
		"""

		self.__painter.save()

		## Die Breite der Punktwerte hängt vom Eigenschaftshöchstwert für den Charakter ab.
		self.__dotsWidth = self.__traitMax * (self.__dotDiameterH + self.__dotLineWidth)
		self.__dotsWidthStandard = self.__traitMaxStandard * (self.__dotDiameterH + self.__dotLineWidth)

		self._drawBackground()

		if GlobalState.isDevelop:
			self.__drawGrid()

		posX = 0
		posY = 0
		lengthX = 680
		lengthY = 250
		if self.__character.species == "Changeling":
			lengthX = 950
		elif self.__character.species == "Mage":
			lengthX = 780
		elif self.__character.species == "Vampire":
			posY = -80
			lengthX = 500
		elif self.__character.species == "Werewolf":
			lengthX = 780
		self._drawLogo(offsetV=posY, width=lengthX, height=lengthY)

		posY += lengthY + self.__posSep
		lengthY = 150
		if self.__character.species == "Changeling":
			lengthY = 160
		elif self.__character.species == "Mage":
			lengthY = 180
		elif self.__character.species == "Werewolf":
			lengthY = 170
		self._drawInfo(offsetV=posY)

		posY += lengthY + self.__posSep
		lengthY = 200
		if self.__character.species == "Mage":
			lengthY = 220
		elif self.__character.species == "Vampire":
			lengthY = 160
		self._drawAttributes(offsetV=posY)

		posY += lengthY + self.__posSep
		posY_zeile3 = posY
		lengthX = 900
		lengthY = 1900
		if self.__character.species == "Changeling":
			lengthX = 720
			lengthY = 1720
		elif self.__character.species == "Mage":
			lengthX = 840
			lengthY = 1810
		elif self.__character.species == "Vampire":
			lengthX = 720
			lengthY = 1810
		elif self.__character.species == "Werewolf":
			lengthX = 840
			lengthY = 1940
		self._drawSkills(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		if self.__character.species == "Changeling":
			posY += lengthY + self.__posSep
			lengthY = 300
			self._drawSubPowers(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY, short=True)
		elif self.__character.species == "Mage":
			posY += lengthY + self.__posSep
			lengthY = 300
			self._drawMagicalTool(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)
		elif self.__character.species == "Vampire":
			posY += lengthY + self.__posSep
			lengthY = 300
			self._drawVinculi(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		posX += lengthX + self.__posSep
		posX_spalte2 = posX
		posY = posY_zeile3
		lengthX = 800
		if self.__character.species != "Human":
			if self.__character.species == "Changeling":
				lengthX = 750
				lengthY = 500
			elif self.__character.species == "Mage":
				lengthX = 870
				lengthY = 290
			elif self.__character.species == "Vampire":
				lengthX = 750
				lengthY = 430
			elif self.__character.species == "Werewolf":
				lengthX = 830
				lengthY = 230
			self._drawPowers(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)
		posX_spalte3 = posX_spalte2 + lengthX + self.__posSep

		if self.__character.species != "Human":
			posY += lengthY + self.__posSep
		lengthY = 1340
		if self.__character.species == "Changeling":
			lengthY = 970
		elif self.__character.species == "Mage":
			lengthY = 1220
		elif self.__character.species == "Vampire":
			lengthY = 1030
		elif self.__character.species == "Werewolf":
			lengthY = 1040
		self._drawMerits(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		posY += lengthY + self.__posSep
		lengthY = 190
		self._drawFlaws(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		posY += lengthY + self.__posSep
		lengthX = self.__pageWidth - posX
		lengthY = 310
		if self.__character.species == "Changeling":
			lengthY = 350
		elif self.__character.species == "Mage":
			lengthY = 300
		elif self.__character.species == "Vampire":
			lengthY = 400
		elif self.__character.species == "Werewolf":
			lengthY = 390
		self._drawWeapons(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)
		posY_zeile4 = posY + lengthY + self.__posSep

		posX = posX_spalte3
		posY = posY_zeile3
		lengthX = self.__pageWidth - posX
		if self.__character.species != "Werewolf":
			lengthY = 270
			self._drawAdvantages(offsetH=posX, offsetV=posY, width=lengthX)

		if self.__character.species != "Werewolf":
			posY += lengthY + self.__posSep
			lengthY = 295
			if self.__character.species != "Human":
				lengthY = 200
		self._drawHealth(offsetH=posX, offsetV=posY, width=lengthX)

		posY += lengthY + self.__posSep
		lengthY = 295
		if self.__character.species != "Human":
			lengthY = 190
		self._drawWillpower(offsetH=posX, offsetV=posY, width=lengthX)

		if self.__character.species != "Human":
			posY += lengthY + self.__posSep
			lengthY = 140
			self._drawPowerstat(offsetH=posX, offsetV=posY, width=lengthX)

		posY += lengthY + self.__posSep
		if self.__character.species != "Human":
			lengthY = 160
			if self.__character.species == "Mage":
				lengthY = 300
			elif self.__character.species == "Changeling":
				lengthY = 250
			elif self.__character.species == "Vampire":
				lengthY = 280
			elif self.__character.species == "Werewolf":
				lengthY = 170
			self._drawFuel(offsetH=posX, offsetV=posY, width=lengthX)

		if self.__character.species != "Human":
			posY += lengthY + self.__posSep
		self._drawMorality(offsetH=posX, offsetV=posY, width=lengthX)

		posX = 0
		posY = posY_zeile4
		lengthX = 780
		lengthY = self.__pageHeight - posY
		if self.__character.species == "Human":
			#self._drawDerangements(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)
			self._drawInventory(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		posX += lengthX + self.__posSep
		lengthX = 780
		lengthY = self.__pageHeight - posY
		if self.__character.species == "Human":
			self._drawDescription(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		posX += lengthX + self.__posSep
		lengthX = self.__pageWidth - posX
		lengthY = 620
		if self.__character.species == "Human":
			self._drawImage(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

			posY += lengthY + self.__posSep
			lengthY = self.__pageHeight - posY
			self._drawXP(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)
		elif self.__character.species == "Changeling":
			posX = 0
			posY = posY_zeile4
			lengthX = (self.__pageWidth - 2 * posX) / 3
			lengthY = self.__pageHeight - posY
			self._drawBlessing(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

			posX += lengthX + self.__posSep
			lengthY = self.__pageHeight - posY
			self._drawBreedCurse(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

			posX += lengthX + self.__posSep
			lengthX = self.__pageWidth - posX
			lengthY = self.__pageHeight - posY
			self._drawKithAbility(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)
		elif self.__character.species == "Mage":
			posX = 0
			posY = posY_zeile4
			lengthX = (self.__pageWidth - 2 * self.__posSep) / 3
			lengthY = self.__pageHeight - posY
			self.__drawLineBox(self.tr("Active Spells"), offsetH=posX, offsetV=posY, width=lengthX, height=lengthY, description=self.tr("Max: {} +3".format(self.__storage.powerstatName(self.__character.species))))

			posX += lengthX + self.__posSep
			self.__drawLineBox(self.tr("Spells Cast Upon Self"), offsetH=posX, offsetV=posY, width=lengthX, height=lengthY, description=self.tr("Spell Tolerance: Stamina; -1 die per extra spell"))

			posX += lengthX + self.__posSep
			lengthX = self.__pageWidth - posX
			lengthY = lengthY / 2 - self.__posSep / 2
			self._drawNimbus(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)
			
			posY += lengthY + self.__posSep
			lengthY = self.__pageHeight - posY
			self._drawParadoxMarks(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)
		elif self.__character.species == "Vampire":
			posX = 0
			posY = posY_zeile4
			lengthX = (self.__pageWidth - 2 * posX) / 3
			lengthY = self.__pageHeight - posY
			self._drawBreedCurse(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

			posX += lengthX + self.__posSep
			lengthY = self.__pageHeight - posY
			self._drawOrganisationCurse(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)
		elif self.__character.species == "Werewolf":
			posX = 0
			posY = posY_zeile4
			lengthX = self.__pageWidth
			lengthY = self.__pageHeight - posY
			self._drawShapes(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		self.__painter.restore()


	def drawSheet_2(self):
		"""
		Hier wird gezeichnet.
		"""

		self.__painter.save()

		self._drawBackground()

		if GlobalState.isDevelop:
			image  = QImage()
			if ( self.__character.species == "Human" ):
				pass
			elif ( self.__character.species == "Changeling" ):
				image = QImage( ":/characterSheets/images/Charactersheet-Changeling-2.jpg" )
			elif ( self.__character.species == "Mage" ):
				image = QImage( ":/characterSheets/images/Charactersheet-Mage-2.jpg" )
			elif ( self.__character.species == "Vampire" ):
				image = QImage( ":/characterSheets/images/Charactersheet-Vampire-2.jpg" )
			elif ( self.__character.species == "Werewolf" ):
				image = QImage( ":/characterSheets/images/Charactersheet-Werewolf-2.jpg" )
			else:
				raise ErrSpeciesNotExisting( self.__character.species )

			## Damit ich weiß, Wo ich meine Sachen platzieren muß kommt erstmal das Bild dahinter.
			source = QRectF ( 0.0, 0.0, float( image.width() ), float( image.height() ) )
			target = QRectF( 0.0 - self.__borderFrameWest, 0.0 - self.__borderFrameNorth, float( self.__paperWidth_defined ), float( self.__paperHeight_defined ) )
			self.__painter.drawImage(target, image, source)

		if GlobalState.isDevelop:
			self.__drawGrid()

		if self.__character.species != "Changeling":
			posX = 700
			posY = 0
			lengthX = self.__pageWidth - posX
			lengthY = 1000
			if ( self.__character.species == "Changeling" ):
				pass
			elif ( self.__character.species == "Mage" ):
				pass
			elif ( self.__character.species == "Vampire" ):
				posX = 750
				lengthX = self.__pageWidth - posX
			elif ( self.__character.species == "Werewolf" ):
				pass
			self._drawSubPowers(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		posY_zeile3 = 2500
		if ( self.__character.species == "Changeling" ):
			posY_zeile3 = 2200
		elif ( self.__character.species == "Mage" ):
			posY_zeile3 = 2500
		elif ( self.__character.species == "Vampire" ):
			posY_zeile3 = 2200
		elif ( self.__character.species == "Werewolf" ):
			posY_zeile3 = 2500

		posX = 0
		posY = posY_zeile3
		lengthX = 680
		lengthY = self.__pageHeight - posY
		if ( self.__character.species == "Changeling" ):
			lengthX = 680
		elif ( self.__character.species == "Mage" ):
			lengthX = 720
		if ( self.__character.species == "Vampire" ):
			lengthX = 680
		elif ( self.__character.species == "Werewolf" ):
			lengthX = 700
		#self._drawDerangements(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)
		self._drawInventory(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		posX += lengthX + self.__posSep
		lengthX = 720
		if ( self.__character.species == "Changeling" ):
			lengthX = 720
		elif ( self.__character.species == "Mage" ):
			lengthX = 800
		elif ( self.__character.species == "Vampire" ):
			lengthX = 750
		elif ( self.__character.species == "Werewolf" ):
			lengthX = 870
		self._drawDescription(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		posX += lengthX + self.__posSep
		lengthX = self.__pageWidth - posX
		lengthY = 840
		if ( self.__character.species == "Changeling" ):
			lengthY = 840
		elif ( self.__character.species == "Mage" ):
			lengthY = 720
		elif ( self.__character.species == "Vampire" ):
			lengthY = 680
		elif ( self.__character.species == "Werewolf" ):
			lengthY = 710
		self._drawImage(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		posY += lengthY + self.__posSep
		lengthY = self.__pageHeight - posY
		self._drawXP(offsetH=posX, offsetV=posY, width=lengthX, height=lengthY)

		self.__painter.restore()


	def __drawGrid(self):
		"""
		Diese Funktion zeichnet ein Gitter, damit man weiß, an welcher Position man die Einträge platzieren muß.
		"""

		self.__painter.save()

		fontLcl = copy.copy(self.__fontMain)
		fontLcl.setPointSize(20)
		self.__painter.setFont(fontLcl)
		self.__painter.setRenderHint(QPainter.TextAntialiasing)
		self.__painter.save()

		pen = QPen(Qt.DashLine)
		pen.setWidth(2)
		pen.setColor(QColor(255,0,255))
		self.__painter.setPen(pen)

		for i in range(self.__pageWidth)[::50]:
			self.__painter.drawLine(i, 0, i, self.__pageHeight)
		for i in range(self.__pageHeight)[::50]:
			self.__painter.drawLine(0, i, self.__pageWidth, i)

		self.__painter.restore()

		self.__painter.save()

		pen = self.__painter.pen()
		pen.setWidth(3)
		pen.setColor(QColor(0,127,127))
		self.__painter.setPen(pen)
		for i in range(self.__pageWidth)[::500]:
			self.__painter.drawLine(i, 0, i, self.__pageHeight)
			self.__painter.drawText(i+1, 0, 70, 30, Qt.AlignLeft, unicode(i))
		for i in range(self.__pageHeight)[::500]:
			self.__painter.drawLine(0, i, self.__pageWidth, i)
			self.__painter.drawText(1, i, 70, 30, Qt.AlignLeft, unicode(i))

		self.__painter.restore()

		self.__painter.restore()


	def _drawBackground(self):
		"""
		Der Hintergrund für den Charakterbogen wird dargestellt.
		"""

		self.__painter.save()

		rect = QRect(0 - self.__borderFrameWest, 0 - self.__borderFrameNorth, self.__pageWidth + self.__borderFrameWest + self.__borderFrameEast, self.__pageHeight + self.__borderFrameNorth + self.__borderFrameSouth)
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
			imageShapes = imageShapes.scaledToWidth(self.__pageWidth)
			rectShapes = QRect(0 - self.__borderFrameWest, 0 - self.__borderFrameNorth + self.__pageHeight - imageShapes.height(), self.__pageWidth, imageShapes.height())
			self.__painter.drawImage(rectShapes, imageShapes)

			## Dieses Bild wird später gezeichnet, damit es nicht von den Gestalten abgeschnitten wird.
			offsetV = 80
			image = QImage(":sheet/images/sheet/Werewolf-Background.png")
			image = image.scaledToHeight(self.__pageHeight - imageShapes.height() - offsetV)
			rect = QRect(0 - self.__borderFrameWest + (self.__pageWidth - image.width()) / 2, offsetV, image.width(), image.height())
			self.__painter.drawImage(rect, image)
		else:
			rect = QRect(0 - self.__borderFrameWest, 0 - self.__borderFrameNorth, (self.__pageWidth + self.__borderFrameWest + self.__borderFrameEast) / 7, self.__pageHeight + self.__borderFrameNorth + self.__borderFrameSouth)
			image = QImage(":sheet/images/sheet/WorldOfDarkness-BackgroundL.png")
			self.__painter.drawImage(rect, image)
			#self.__drawBB(rect.x(), rect.y(), rect.width(), rect.height())

			rect = QRect(self.__pageWidth + self.__borderFrameWest - (self.__pageWidth + self.__borderFrameWest + self.__borderFrameEast) / 7, 0 - self.__borderFrameNorth, (self.__pageWidth + self.__borderFrameNorth + self.__borderFrameSouth) / 7, self.__pageHeight + self.__borderFrameNorth + self.__borderFrameSouth)
			image = QImage(":sheet/images/sheet/WorldOfDarkness-BackgroundR.png")
			self.__painter.drawImage(rect, image)
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
		elif self.__character.species == "Mage":
			image = QImage(":sheet/images/sheet/Mage.png")
		if self.__character.species == "Vampire":
			image = QImage(":sheet/images/sheet/Vampire.png")
		if self.__character.species == "Werewolf":
			image = QImage(":sheet/images/sheet/Werewolf.png")
		else:
			pass
		self.__painter.drawImage(rect, image)

		self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawInfo(self, offsetV, distanceV=0):
		"""
		Diese Funktion Schreibt Namen, Virtue/Vice etc. in den Kopf des Charakterbogens.

		\param offsetV Vertikaler Abstand zwischen nutzbarer Bildkante und oberkante der BondingBox für die Informationszeilen.
		\param distanceV Vertikaler Abstand zwischen den Zeilen.
		"""

		text = [
			[
				"Name:",
				"",
			],
			[
				"Virtue:",
				"Vice:",
			],
			[
				u"Chronicle:",
				"{}:".format(self.__storage.factionTitle(self.__character.species)),
			],
		]
		textCharacter = [
			[
				Identity.displayNameDisplay(self.__character.identity.surname, self.__character.identity.firstname, self.__character.identity.nickname),
				u"",
			],
			[
				self.__character.virtue,
				self.__character.vice,
			],
			[
				u"",
				self.__character.faction,
			],
		]
		if self.__character.species != "Human":
			text = [
				[
					text[0][0],
					"Secret Name",
					text[0][1],
				],
				[
					text[1][0],
					text[1][1],
					"{}:".format(self.__storage.partyTitle(self.__character.species)),
				],
				[
					"{}:".format(self.__storage.breedTitle(self.__character.species)),
					text[2][1],
					"{}:".format(self.__storage.organisationTitle(self.__character.species)),
				],
			]
			textCharacter = [
				[
					textCharacter[0][0],
					self.__character.identity.supername,
					textCharacter[0][1],
				],
				[
					textCharacter[1][0],
					textCharacter[1][1],
					self.__character.party,
				],
				[
					self.__character.breed,
					textCharacter[2][1],
					self.__character.organisation,
				],
			]

			if self.__character.species == "Changeling":
				text[2][0] = "{}:".format(self.__storage.breedTitle(self.__character.species))
				textCharacter[2][0] ="{} ({})".format(self.__character.breed, self.__character.kith)
			elif self.__character.species == "Mage":
				text[0][1] = "Shadow Name:"

			elif self.__character.species == "Vampire":
				text[0][1] ="Sire:"
				textCharacter[0][1] =""
			elif self.__character.species == "Werewolf":
				text[0][1] = "Deed Name:"
				text[0][2] ="Totem:"
				textCharacter[0][2] = ""

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
				self.__painter.drawText(i * distanceH + width[i] + self.__textDotSep, offsetV - fontSubHeadingHeightDiff + fontScriptHeightDiff - fontScriptHeight + j * (self.__fontSubHeadingHeight + distanceV), distanceH - width[i] - self.__textDotSep, 2 * fontScriptHeight, Qt.AlignLeft | Qt.AlignBottom | Qt.TextWordWrap, textCharacter[i][j])

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

		mainFont = copy.copy(self.__fontMain)
		mainFont.setWeight(QFont.Bold)
		self.__painter.setFont(mainFont)
		fontMetrics = QFontMetrics(self.__painter.font())
		fontHeightDiff = fontSubHeadingMetrics.ascent() - fontMetrics.ascent()

		distanceH = (self.__pageWidth - headingWidth) / 3

		## Bonusattribut erhält einen Extra-Punkt.
		bonusList = self.__storage.bonusTraits(self.__character.species, self.__character.breed)
		bonusTrait = None
		if len(bonusList) > 1:
			for bonus in bonusList:
				if bonus["name"] == self.__character.bonus:
					bonusTrait = bonus
		elif len(bonusList) > 0:
			bonusTrait = bonusList[0]

		i = 0
		for item in Config.attributes:
			j = 0
			for subitem in item[1]:
				attrib = self.__character.traits["Attribute"][item[0]][subitem]
				attributeValue = attrib.value
				if bonusTrait and bonusTrait["type"] == "Attribute" and bonusTrait["name"] == attrib.name:
					attributeValue += 1
				self.__drawTrait(headingWidth + i * distanceH, offsetV - fontSubHeadingHeightDiff + fontHeightDiff + j * self.__fontSubHeadingHeight, width=distanceH, name=attrib.name, value=attributeValue, maxValue=self.__traitMax, align=Qt.AlignRight)
				j += 1
			i += 1

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

		mainFont = copy.copy(self.__fontMain)
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

		fontMetrics = QFontMetrics(self.__painter.font())
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

		self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawPowers(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Bannt die übernatürlichen Kräfte auf den Charakterbogen.

		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox aller Fertigkeiten.
		\param width Die Breite der Spalte.

		\todo Jedes Arcanum sollte mit seiner Rune dargestellt werden.
		"""

		twocolumn = False
		if self.__character.species == "Mage" or self.__character.species == "Werewolf":
			twocolumn = True

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		mainFont = copy.copy(self.__fontMain)
		mainFont.setWeight(QFont.Normal)
		self.__painter.setFont(mainFont)

		self.__drawHeading(offsetH, offsetV, width, self.__storage.powerName(self.__character.species))

		fontMetrics = QFontMetrics(self.__painter.font())
		textHeight = fontMetrics.height() - 3
		numOfTraits = 0
		for item in self.__character.traits["Power"].values():
			for subitem in item.values():
				if subitem.isAvailable and self.__character.species == subitem.species and (subitem.value > 0 or self.__character.species == "Mage" or self.__character.species == "Werewolf"):
					numOfTraits += 1

		traitWidth = width
		if twocolumn:
			traitWidth = width // 2 - self.__dotSep

		i = 0
		j = 0
		secondRow = False
		for item in self.__character.traits["Power"]:
			traits = self.__character.traits["Power"][item].items()
			traits.sort()
			#Debug.debug(traits)
			for subitem in traits:
				if subitem[1].isAvailable and self.__character.species == subitem[1].species and (subitem[1].value > 0 or self.__character.species == "Mage" or self.__character.species == "Werewolf"):
					if twocolumn:
						self.__drawTrait(offsetH + i * (width - traitWidth), offsetV + self.__fontHeadingHeight + j * textHeight, width=traitWidth, name=subitem[1].name, value=subitem[1].value, mirrored=secondRow)
						j += 1
						if j >= numOfTraits // 2:
							i += 1
							j = 0
							secondRow = True
					else:
						self.__drawTrait(offsetH, offsetV + self.__fontHeadingHeight + j * textHeight, width=traitWidth, name=subitem[1].name, value=subitem[1].value)
						j += 1

		## Den freien Platz füllen wir mit leeren Zeilen, die der Spieler dann per Stift ausfüllen kann. Natürlich nur, wenn die Kräfte nicht zweispaltig aufgeführt sind.
		if height and not twocolumn:
			usedSpace = self.__fontHeadingHeight + numOfTraits * textHeight
			while usedSpace < height - (.75 * textHeight):
				self.__drawTrait(offsetH, offsetV + usedSpace, width=width, name="", value=0)
				usedSpace += textHeight

		if not height:
			height = self.__fontHeadingHeight + numOfTraits * textHeight
		self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawSubPowers(self, offsetH=0, offsetV=0, width=None, height=None, short=False):
		"""
		Bannt die übernatürlichen Unterkräfte auf den Charakterbogen.

		\param short Ist dieser Parameter "True" werden nur die Namen der Unterkräfte aufgezählt.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		self.__painter.setFont(self.__fontMain)

		self.__drawHeading(offsetH, offsetV, width, self.__storage.subPowerName(self.__character.species))

		fontMetrics = QFontMetrics(self.__painter.font())
		fontHeight = fontMetrics.height()

		if short:
			listOfSubpowers = []
			for item in self.__character.traits["Subpower"]:
				tmpListOfSubpowers = []
				for trait in self.__character.traits["Subpower"][item].values():
					if trait.value > 0 and trait.species == self.__character.species:
						tmpListOfSubpowers.append(trait.name)
				tmpListOfSubpowers.sort()
				listOfSubpowers.extend(tmpListOfSubpowers)
			self.__painter.drawText(offsetH, offsetV + self.__fontHeadingHeight, width, height - self.__fontHeadingHeight, Qt.AlignLeft | Qt.TextWordWrap, ", ".join(listOfSubpowers))
		else:
			numOfTraits = 0
			for item in self.__character.traits["Subpower"].values():
				for subitem in item.values():
					if subitem.value > 0:
						numOfTraits += 1

			widths = [
				400,
				50,
				50,
				600,
			]
			widths.insert(0, width - sum(widths) - len(widths) * self.__textDotSep)

			i = 0
			for item in self.__character.traits["Subpower"]:
				traits = self.__character.traits["Subpower"][item].items()
				traits.sort()
				#Debug.debug(traits)
				for subitem in traits:
					if subitem[1].isAvailable and subitem[1].value > 0 and subitem[1].species == self.__character.species:
						posY = offsetV + self.__fontHeadingHeight + i * fontHeight
						self.__painter.drawText(offsetH, posY, widths[0], fontHeight, Qt.AlignLeft, subitem[1].name)
						j = 1
						#Debug.debug(self.__storage.traits["Subpower"][item][subitem[0]]["powers"])
						if self.__storage.traits["Subpower"][item][subitem[0]]["powers"]:
							j = 0
							for power in self.__storage.traits["Subpower"][item][subitem[0]]["powers"].items():
								#Debug.debug(subitem[0], power)
								self.__drawTrait(offsetH + self.__textDotSep + widths[0], posY + j * fontHeight, width=widths[1], name=power[0], value=power[1])
								j += 1
						elif self.__character.species == "Werewolf":
							self.__drawTrait(offsetH + self.__textDotSep + widths[0], posY, width=widths[1], name=item, value=int(subitem[1].level))
						self.__painter.drawText(offsetH + 2 * self.__textDotSep + sum(widths[:2]), posY, widths[2], fontHeight, Qt.AlignLeft, self.__storage.traits["Subpower"][item][subitem[0]]["costWill"])
						self.__painter.drawText(offsetH + 3 * self.__textDotSep + sum(widths[:3]), posY, widths[3], fontHeight, Qt.AlignLeft, self.__storage.traits["Subpower"][item][subitem[0]]["costFuel"])
						#self.__painter.save()
						#self.__painter.setFont(self.__fontMain_small)
						self.__painter.drawText(offsetH + 4 * self.__textDotSep + sum(widths[:4]), posY, widths[4], fontHeight, Qt.AlignLeft, self.__storage.traits["Subpower"][item][subitem[0]]["roll"])
						#self.__painter.restore()
						i += j

			### Den freien Platz füllen wir mit leeren Zeilen, die der Spieler dann per Stift ausfüllen kann. Natürlich nur, wenn die Kräfte nicht zweispaltig aufgeführt sind.
			#if height:
				#usedSpace = self.__fontHeadingHeight + numOfTraits * fontHeight
				#while usedSpace < height - (.75 * fontHeight):
					#self.__drawTrait(offsetH, offsetV + usedSpace, width=width, name="", value=0)
					#usedSpace += fontHeight

		if not height:
			height = self.__fontHeadingHeight + numOfTraits * fontHeight
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

		mainFont = copy.copy(self.__fontMain)
		mainFont.setWeight(QFont.Normal)
		self.__painter.setFont(mainFont)

		self.__drawHeading(offsetH, offsetV, width, self.tr("Merits"))

		fontMetrics = QFontMetrics(self.__painter.font())
		textHeight = fontMetrics.height() - 3
		numOfTraits = 0
		for item in self.__character.traits["Merit"].values():
			for subitem in item.values():
				if subitem.value > 0:
					numOfTraits += 1

		j = 0
		for item in self.__character.traits["Merit"]:
			traits = self.__character.traits["Merit"][item].items()
			traits.sort()
			for subitem in traits:
				if (subitem[1].isAvailable and subitem[1].value > 0):
					text = ""
					if subitem[1].custom:
						text = subitem[1].customText
					self.__drawTrait(offsetH, offsetV + self.__fontHeadingHeight + j * textHeight, width=width, name=subitem[1].name, text=text, value=subitem[1].value)
					j += 1

		## Den freien Platz füllen wir mit leeren Zeilen, die der Spieler dann per Stift ausfüllen kann.
		if height:
			usedSpace = self.__fontHeadingHeight + numOfTraits * textHeight
			while usedSpace < height - (.75 * textHeight):
				self.__drawTrait(offsetH, offsetV + usedSpace, width=width, name="", value=0)
				usedSpace += textHeight

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
		text = ", ".join(flaws)

		self.__drawText(
			self.tr("Flaws"),
			text,
			offsetH,
			offsetV,
			width,
			height
		)


	def _drawAdvantages(self, offsetH=0, offsetV=0, width=None):
		"""
		Bannt die Berechneten Werte auf den Charakterbogen.

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

		self.__painter.setFont(self.__fontMain)

		fontMetrics = QFontMetrics(self.__painter.font())
		textHeight = fontMetrics.height() - 3

		generalArmor = 0
		firearmsArmor = 0
		if self.__character.armor["name"] in self.__storage.armor:
			generalArmor = self.__storage.armor[self.__character.armor["name"]]["general"]
			firearmsArmor = self.__storage.armor[self.__character.armor["name"]]["firearms"]

		verticalPos = offsetV
		for item in advantages:
			self.__drawTextWithValue(offsetH, verticalPos, width, item[0], item[1])
			verticalPos += textHeight
		self.__drawTextWithValue(offsetH, verticalPos, width, self.tr("Armor"), "{general}/{firearms}".format(general=generalArmor, firearms=firearmsArmor))
		verticalPos += textHeight

		self.__painter.restore()

		self.__drawBB(offsetH, offsetV, width, verticalPos - offsetV)

		self.__painter.restore()


	def _drawHealth(self, offsetH=0, offsetV=0, width=None):
		"""
		Bannt die Gesundheit auf den Charakterbogen.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox aller Fertigkeiten.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox aller Fertigkeiten.
		\param width Die Breite der Fertigkeits-Spalte.

		\todo Kinder haben andere Wundabzüge.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		self.__drawHeading(offsetH, offsetV, width, self.tr("Health"))
		self.__drawCenterDots(offsetH, offsetV + self.__fontHeadingHeight + self.__textDotSep, width=width, number=self.__calc.calcHealth(), squares=True, big=True)

		dotDiameter = self.__dotBigDiameterH
		number = self.__calc.calcHealth()
		widthDots = number * (dotDiameter + self.__dotLineWidth / 2) + (number - 1) * self.__dotSep

		self.__painter.save()
		self.__painter.setFont(self.__fontMain_tiny)

		fontMetrics = QFontMetrics(self.__painter.font())

		# Die letzten drei Gesundheitsstufen haben Wundabzüge.
		for i in xrange(1, 4):
			modifier = u"−{}".format(4 - i)
			self.__painter.drawText(offsetH + (width - widthDots) / 2 + widthDots - i * (dotDiameter + self.__dotSep), offsetV + self.__fontHeadingHeight + 2 * dotDiameter + self.__dotSep + self.__textDotSep, dotDiameter, fontMetrics.height(), Qt.AlignCenter, modifier)

		self.__painter.restore()

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

		self.__painter.save()
		self.__painter.setFont(self.__fontMain_small)
		text = "per Turn"
		fontMetrics = QFontMetrics(self.__painter.font())
		fontWidth = fontMetrics.boundingRect(text).width()

		self.__painter.drawText(offsetH + width - fontWidth, offsetV + self.__fontHeadingHeight, fontWidth, 2 * fontMetrics.height(), Qt.AlignCenter, "{}\n{}".format(self.__storage.fuelPerTurn(species=self.__character.species, powerstat=self.__character.powerstat), text))
		self.__painter.restore()

		self.__painter.restore()


	def _drawMorality(self, offsetH=0, offsetV=0, width=None):
		"""
		Bannt die Moral auf den Charakterbogen.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox aller Fertigkeiten.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox aller Fertigkeiten.
		\param width Die Breite der Fertigkeits-Spalte.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		self.__drawHeading(offsetH, offsetV, width, self.__storage.moralityName(self.__character.species))

		self.__painter.setFont(self.__fontMain)

		fontMetrics = QFontMetrics(self.__painter.font())
		textHeight = fontMetrics.height() - 3
		textWidth = fontMetrics.boundingRect(unicode(Config.moralityTraitMax)).width()

		self.__painter.save()
		for i in range(1, Config.moralityTraitMax+1)[::-1]:
			#Debug.debug(i)
			lcl_height = offsetV + self.__fontHeadingHeight + (Config.moralityTraitMax-i) * textHeight
			self.__painter.drawText(offsetH, lcl_height, textWidth, textHeight, Qt.AlignRight, unicode(i))
			derangementWidth = 0
			if i in self.__character.derangements:
				self.__painter.drawText(offsetH + textWidth + self.__textDotSep, lcl_height, width - textWidth - self.__textDotSep - self.__dotDiameterH - self.__dotSep, lcl_height, Qt.AlignLeft, self.__character.derangements[i])
				derangementWidth = fontMetrics.boundingRect(self.__character.derangements[i]).width()
			if i <= Config.moralityTraitDefaultValue:
				self.__painter.drawLine(offsetH + textWidth + self.__textDotSep + derangementWidth, lcl_height + fontMetrics.ascent(), offsetH + width - self.__dotDiameterH - self.__dotSep, lcl_height + fontMetrics.ascent())
			self.__painter.save()
			if i <= self.__character.morality:
				self.__painter.setBrush(self.__colorFill)
			else:
				self.__painter.setBrush(self.__colorEmpty)
			self.__painter.drawEllipse(offsetH + width - self.__dotDiameterH, lcl_height + fontMetrics.ascent() - self.__dotDiameterV, self.__dotDiameterH, self.__dotDiameterV)
			self.__painter.restore()
		self.__painter.restore()

		self.__painter.restore()


	def _drawBlessing(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		"""

		self.__drawText(
			self.tr("{} Blessing".format(self.__storage.breedTitle(self.__character.species))),
			self.__storage.breedBlessing(self.__character.species, self.__character.breed),
			offsetH,
			offsetV,
			width,
			height
		)


	def _drawBreedCurse(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		"""

		weaknessText = "Weakness"
		if self.__character.species == "Changeling":
			weaknessText = "Curse"
		self.__drawText(
			self.tr("{} {}".format(self.__storage.breedTitle(self.__character.species), weaknessText)),
			self.__storage.breedCurse(self.__character.species, self.__character.breed),
			offsetH,
			offsetV,
			width,
			height
		)


	def _drawOrganisationCurse(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		"""

		weaknessText = "Weakness"
		self.__drawText(
			self.tr("{} {}".format(self.__storage.organisationTitle(self.__character.species), weaknessText)),
			self.__storage.organisationCurse(self.__character.species, self.__character.organisation),
			offsetH,
			offsetV,
			width,
			height
		)


	def _drawKithAbility(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		"""

		self.__drawText(
			self.tr("Kith Ability"),
			self.__storage.kithAbility(self.__character.breed, self.__character.kith),
			offsetH,
			offsetV,
			width,
			height
		)


	def __drawText(self, heading, text, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Schreibt einen Textblock.

		\param offsetH Der horizontale Abstand zur linken Kante des nutzbaren Charakterbogens.
		\param offsetV Der vertikale Abstand zur Oberkante des nutzbaren Charakterbogens.
		\param width Die Breite.
		\param height Die Höhe.

		\bug Da ich als Argument von self.tr() keine unicode-String nutzen kann, sind manche minus-Zeichen als "-" und nicht als "−" genutzt worden.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth

		self.__painter.setFont(self.__fontMain)

		self.__drawHeading(offsetH, offsetV, width, heading)

		self.__painter.drawText(
			offsetH,
			offsetV + self.__fontHeadingHeight + self.__headingSep,
			width,
			height - self.__fontHeadingHeight - self.__headingSep,
			Qt.AlignLeft | Qt.TextWordWrap,
			text
		)

		self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def __drawLineBox(self, heading, offsetH=0, offsetV=0, width=None, height=None, description=None):
		"""
		Schreibt einen Blick mit Überschrift, einem kurzem erklärenden Text und füllt sie dann mit Linien, um handschriftlich ausgefüllt werden zu können.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth

		self.__painter.setFont(self.__fontMain)

		self.__drawHeading(offsetH, offsetV, width, heading)

		fontMetrics = QFontMetrics(self.__painter.font())
		fontHeight = fontMetrics.height()

		posY = self.__fontHeadingHeight + self.__headingSep

		if description:
			self.__painter.save()
			self.__painter.setFont(self.__fontMain_small)
			fontSmallMetrics = QFontMetrics(self.__painter.font())
			fontSmallHeight = fontSmallMetrics.height()
			self.__painter.drawText(
				offsetH,
				offsetV + posY,
				width,
				fontHeight,
				Qt.AlignHCenter | Qt.TextWordWrap,
				description
			)
			posY += fontSmallHeight
			self.__painter.restore()

		while posY + fontHeight <= height:
			posY += fontHeight
			self.__painter.drawLine(
				offsetH,
				offsetV + posY,
				offsetH + width,
				offsetV + posY
			)

		self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawNimbus(self, offsetH=0, offsetV=0, width=None, height=None):
		self.__drawText(
			self.tr("Nimbus"),
			self.__character.nimbus,
			offsetH,
			offsetV,
			width,
			height
		)


	def _drawParadoxMarks(self, offsetH=0, offsetV=0, width=None, height=None):
		self.__drawText(
			self.tr("Paradox Marks"),
			self.__character.paradoxMarks,
			offsetH,
			offsetV,
			width,
			height
		)


	def _drawShapes(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Zeichnet die Werte aller fünf Gestalten von Werwölfen auf den Charakterbogen.

		\param offsetH Der horizontale Abstand zur linken Kante des nutzbaren Charakterbogens.
		\param offsetV Der vertikale Abstand zur Oberkante des nutzbaren Charakterbogens.
		\param width Die Breite.
		\param height Die Höhe.

		\bug Da ich als Argument von self.tr() keine unicode-String nutzen kann, sind manche minus-Zeichen als "-" und nicht als "−" genutzt worden.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth

		self.__painter.save()

		self.__painter.setFont(self.__fontSubHeading)

		fontSubHeadingMetrics = QFontMetrics(self.__painter.font())
		fontSubHeadingHeight = fontSubHeadingMetrics.height()

		columnWidth = width / 5

		## Name der Gestalten
		i = 0
		for item in Config.shapesWerewolf:
			self.__painter.drawText(offsetH + i * (columnWidth), offsetV, columnWidth, fontSubHeadingHeight, Qt.AlignHCenter, item)
			i += 1

		self.__painter.restore()

		self.__painter.save()

		self.__painter.setFont(self.__fontMain)
		fontMetrics = QFontMetrics(self.__painter.font())
		fontHeight = fontMetrics.height() - 3

		## Attributsänderungen
		shapesAttributes = [
			## Hishu
			[
			],
			## Dalu
			[
				[ u"Strength (+1)", CalcShapes.strength(self.__character.traits["Attribute"]["Physical"]["Strength"].value, Config.shapesWerewolf[1]) ],
				[ u"Stamina (+1)", CalcShapes.stamina(self.__character.traits["Attribute"]["Physical"]["Stamina"].value, Config.shapesWerewolf[1]) ],
				[ u"Manipulation (−1)", CalcShapes.manipulation(self.__character.traits["Attribute"]["Social"]["Manipulation"].value, Config.shapesWerewolf[1]) ],
			],
			## Gauru
			[
				[ u"Strength (+3)", CalcShapes.strength(self.__character.traits["Attribute"]["Physical"]["Strength"].value, Config.shapesWerewolf[2]) ],
				[ u"Dexterity (+1)", CalcShapes.dexterity(self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[2]) ],
				[ u"Stamina (+2)", CalcShapes.stamina(self.__character.traits["Attribute"]["Physical"]["Stamina"].value, Config.shapesWerewolf[2]) ],
			],
			## Urshul
			[
				[ u"Strength (+2)", CalcShapes.strength(self.__character.traits["Attribute"]["Physical"]["Strength"].value, Config.shapesWerewolf[3]) ],
				[ u"Dexterity (+2)", CalcShapes.dexterity(self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[3]) ],
				[ u"Stamina (+2)", CalcShapes.stamina(self.__character.traits["Attribute"]["Physical"]["Stamina"].value, Config.shapesWerewolf[3]) ],
				[ u"Manipulation (−3)", CalcShapes.manipulation(self.__character.traits["Attribute"]["Social"]["Manipulation"].value, Config.shapesWerewolf[3]) ],
			],
			## Urhan
			[
				[ u"Dexterity (+2)", CalcShapes.dexterity(self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[4]) ],
				[ u"Stamina (+1)", CalcShapes.stamina(self.__character.traits["Attribute"]["Physical"]["Stamina"].value, Config.shapesWerewolf[4]) ],
			],
		]

		listLen = []
		i = 0
		for item in shapesAttributes:
			listLen.append(len(item))
			j = 0
			for subitem in item:
				self.__drawTextWithValue(offsetH + self.__textDotSep + i * columnWidth, offsetV + fontSubHeadingHeight + j * fontHeight, columnWidth - 2 * self.__textDotSep, subitem[0], subitem[1])
				j += 1
			i += 1

		generalArmor = 0
		firearmsArmor = 0
		isDedicated = self.__character.armor["dedicated"]
		if self.__character.armor["name"] in self.__storage.armor:
			generalArmor = self.__storage.armor[self.__character.armor["name"]]["general"]
			firearmsArmor = self.__storage.armor[self.__character.armor["name"]]["firearms"]

		## Advantages
		advantages = [
			[ self.tr("Size"), self.__calc.calcSize(), ],
			[ self.tr("Initiative"), self.__calc.calcInitiative(), ],
			[ self.tr("Speed"), self.__calc.calcSpeed(), ],
			[ self.tr("Defense"), self.__calc.calcDefense(), ],
			[ self.tr("Armor"), "{general}/{firearms}".format(general=generalArmor, firearms=firearmsArmor), ],
			[ self.tr("Perception"), u"±0", ],
		]
		daluArmor = "0/0"
		if isDedicated:
			daluArmor = advantages[4][1]
		shapesAdvantages = [
			## Hishu
			advantages,
			## Dalu
			[
				[ advantages[0][0], CalcShapes.size(advantages[0][1], Config.shapesWerewolf[1]), ],
				[ advantages[1][0], CalcShapes.initiative(advantages[1][1], Config.shapesWerewolf[1]), ],
				[ advantages[2][0], CalcShapes.speed(advantages[1][1], Config.shapesWerewolf[1]), ],
				[ advantages[3][0], CalcShapes.defense(self.__character.traits["Attribute"]["Mental"]["Wits"].value, self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[1]), ],
				[ advantages[4][0], daluArmor, ],
				[ advantages[5][0], u"+2", ],
			],
			## Gauru
			[
				[ advantages[0][0], CalcShapes.size(advantages[0][1], Config.shapesWerewolf[2]), ],
				[ advantages[1][0], CalcShapes.initiative(advantages[1][1], Config.shapesWerewolf[2]), ],
				[ advantages[2][0], CalcShapes.speed(advantages[1][1], Config.shapesWerewolf[2]), ],
				[ advantages[3][0], CalcShapes.defense(self.__character.traits["Attribute"]["Mental"]["Wits"].value, self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[2]), ],
				[ advantages[4][0], "1/1", ],
				[ advantages[5][0], u"+3", ],
			],
			## Urshul
			[
				[ advantages[0][0], CalcShapes.size(advantages[0][1], Config.shapesWerewolf[3]), ],
				[ advantages[1][0], CalcShapes.initiative(advantages[1][1], Config.shapesWerewolf[3]), ],
				[ advantages[2][0], CalcShapes.speed(advantages[1][1], Config.shapesWerewolf[3]), ],
				[ advantages[3][0], CalcShapes.defense(self.__character.traits["Attribute"]["Mental"]["Wits"].value, self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[3]), ],
				[ advantages[4][0], "0", ],
				[ advantages[5][0], u"+3", ],
			],
			## Urhan
			[
				[ advantages[0][0], CalcShapes.size(advantages[0][1], Config.shapesWerewolf[4]), ],
				[ advantages[1][0], CalcShapes.initiative(advantages[1][1], Config.shapesWerewolf[4]), ],
				[ advantages[2][0], CalcShapes.speed(advantages[1][1], Config.shapesWerewolf[4]), ],
				[ advantages[3][0], CalcShapes.defense(self.__character.traits["Attribute"]["Mental"]["Wits"].value, self.__character.traits["Attribute"]["Physical"]["Dexterity"].value, Config.shapesWerewolf[4]), ],
				[ advantages[4][0], "0", ],
				[ advantages[5][0], u"+4", ],
			],
		]

		vSpace = fontSubHeadingHeight + max(listLen) * fontHeight + fontHeight

		i = 0
		for item in shapesAdvantages:
			j = 0
			for subitem in item:
				self.__drawTextWithValue(offsetH + self.__textDotSep + i * columnWidth, offsetV + vSpace + j * fontHeight, columnWidth - 2 * self.__textDotSep, subitem[0], subitem[1])
				j += 1
			i += 1

		self.__painter.restore()

		self.__painter.save()

		font = copy.copy(self.__fontMain_small)
		font.setStyle(QFont.StyleItalic)
		self.__painter.setFont(font)

		fontItalicMetrics = QFontMetrics(self.__painter.font())
		fontItalicHeight = fontItalicMetrics.height()

		## Ohne unicode im Argument von self.tr() auch kein unicode "−"!
		comments = [
			## Hishu
			#self.tr("Others suffer {minus}2 to all attempts to detect werewolf nature.".format(minus=u"−")),
			self.tr("Others suffer -2 to all attempts to detect werewolf nature.".format(minus=u"−")),
			## Dalu
			self.tr("Lunacy -4"),
			## Gauru
			self.tr("Full Lunacy\nBite: +2L, Claw: +1L\n-2 to resist Death Rage"),
			## Urshul
			self.tr("Lunacy -2\nBite: +2L"),
			## Urhan
			self.tr("Bite: +2L\nOthers suffer -2 to all attempts to detect werewolf nature."),
		]

		commentBoxHeight = 3 * fontItalicHeight

		vSpace = height - commentBoxHeight

		i = 0
		for item in comments:
			self.__painter.drawText(offsetH + self.__textDotSep + i * columnWidth, offsetV + vSpace, columnWidth - 2 * self.__textDotSep, commentBoxHeight, Qt.AlignHCenter | Qt.AlignBottom | Qt.TextWordWrap, item)
			i += 1

		self.__painter.restore()

		self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawWeapons(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Schreibt die Waffen auf den Charkaterbogen.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox.
		\param width Die Breite der Spalte.
		\param height Die Höhe der Tabelle
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		dmgWidth = 150
		rangesWidth = 210
		capWidth = 125
		strWidth = 95
		sizeWidth = 110
		durabWidth = 170
		colSep = 6
		nameWidth = width - dmgWidth - rangesWidth - capWidth - strWidth - sizeWidth - durabWidth - 5 * colSep

		self.__drawHeading(offsetH, offsetV, nameWidth, self.tr("Weapons"))
		self.__drawSubHeading(offsetH + colSep + nameWidth, offsetV, dmgWidth, self.tr("Dmg."))
		self.__drawSubHeading(offsetH + 2 * colSep + nameWidth + dmgWidth, offsetV, rangesWidth, self.tr("Ranges"))
		self.__drawSubHeading(offsetH + 3 * colSep + nameWidth + dmgWidth + rangesWidth, offsetV, capWidth, self.tr("Cap."))
		self.__drawSubHeading(offsetH + 4 * colSep + nameWidth + dmgWidth + rangesWidth + capWidth, offsetV, strWidth, self.tr("Str."))
		self.__drawSubHeading(offsetH + 5 * colSep + nameWidth + dmgWidth + rangesWidth + capWidth + strWidth, offsetV, sizeWidth, self.tr("Size"))
		self.__drawSubHeading(offsetH + 6 * colSep + nameWidth + dmgWidth + rangesWidth + capWidth + strWidth + sizeWidth, offsetV, durabWidth, self.tr("Durab."))

		self.__painter.save()

		self.__painter.setFont(self.__fontMain)
		fontMetrics = QFontMetrics(self.__painter.font())
		fontHeight = fontMetrics.height()

		#Debug.debug(self.__character.weapons)

		breakLoop = False
		i = 0
		for category in self.__character.weapons:
			for weapon in self.__character.weapons[category]:
				self.__painter.drawText(offsetH, offsetV + self.__fontHeadingHeight + i * fontHeight, nameWidth, fontHeight, Qt.AlignLeft, weapon)

				self.__painter.save()
				self.__painter.setFont(self.__fontMain_small)
				self.__painter.drawText(offsetH + colSep + nameWidth, offsetV + self.__fontHeadingHeight + i * fontHeight, dmgWidth, fontHeight, Qt.AlignHCenter, self.__storage.weapons[category][weapon]["damage"])
				self.__painter.drawText(offsetH + 2 * colSep + nameWidth + dmgWidth, offsetV + self.__fontHeadingHeight + i * fontHeight, rangesWidth, fontHeight, Qt.AlignHCenter, self.__storage.weapons[category][weapon]["ranges"])
				self.__painter.drawText(offsetH + 3 * colSep + nameWidth + dmgWidth + rangesWidth, offsetV + self.__fontHeadingHeight + i * fontHeight, capWidth, fontHeight, Qt.AlignHCenter, self.__storage.weapons[category][weapon]["capacity"])
				self.__painter.drawText(offsetH + 4 * colSep + nameWidth + dmgWidth + rangesWidth + capWidth, offsetV + self.__fontHeadingHeight + i * fontHeight, strWidth, fontHeight, Qt.AlignHCenter, self.__storage.weapons[category][weapon]["strength"])
				self.__painter.drawText(offsetH + 5 * colSep + nameWidth + dmgWidth + rangesWidth + capWidth + strWidth, offsetV + self.__fontHeadingHeight + i * fontHeight, sizeWidth, fontHeight, Qt.AlignHCenter, self.__storage.weapons[category][weapon]["size"])
				self.__painter.drawText(offsetH + 6 * colSep + nameWidth + dmgWidth + rangesWidth + capWidth + strWidth + sizeWidth, offsetV + self.__fontHeadingHeight + i * fontHeight, durabWidth, fontHeight, Qt.AlignHCenter, self.__storage.weapons[category][weapon]["durability"])
				self.__painter.restore()
				i += 1
				if self.__fontHeadingHeight + i * fontHeight > height:
					breakLoop = True
					break
			if breakLoop:
				break

		self.__painter.restore()

		self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawInventory(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Schreibt das Inventar des Charakters nieder

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox.
		\param width Die Breite der Spalte.
		\param height Die Höhe des Kastens.
		"""

		equipment = "; ".join(self.__character.equipment)

		self.__drawText(
			self.tr("Inventory"),
			equipment,
			offsetH,
			offsetV,
			width,
			height
		)


	def _drawDerangements(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Schreibt die Geistesstörungen auf den Charkaterbogen. Allerdings nicht in die Moraltabelle!

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox.
		\param width Die Breite der Spalte.

		\bug Der erklärende Text der Geistesstörungen ist viel zu lang. Diese Funktion wird daher nicht genutzt, und die Geistesstörungen über \ref _drawMorality aufgezählt.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		self.__drawHeading(offsetH, offsetV, width, self.tr("Derangements"))

		self.__painter.setFont(self.__fontMain)
		fontMetrics = QFontMetrics(self.__painter.font())
		fontHeight = fontMetrics.height()

		fontSmallMetrics = QFontMetrics(self.__fontMain_tiny)
		fontSmallHeight = fontSmallMetrics.height()

		keys = [item for item in self.__character.derangements.keys()]
		keys.sort(reverse=True)
		i = 0
		for moralityValue in keys:
			derangement = self.__character.derangements[moralityValue]
			self.__drawTextWithValue(posX=offsetH, posY=offsetV + self.__fontHeadingHeight + i * fontHeight, width=width, text=derangement, value="Morality: {}".format(moralityValue))
			self.__painter.save()
			self.__painter.setFont(self.__fontMain_tiny)
			self.__painter.drawText(offsetH, offsetV + self.__fontHeadingHeight + i * fontHeight + fontHeight, width, 4 * fontHeight, Qt.AlignLeft | Qt.TextWordWrap, self.__storage.derangementDescription(derangement))
			self.__painter.restore()
			i += 4
			if self.__fontHeadingHeight + i * fontHeight + 4 * fontHeight > height:
				break

		self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawDescription(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Schreibt die Beschreibung und die Daten auf den Charkaterbogen.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox.
		\param width Die Breite der Spalte.

		\todo Changelings benötigen noch mehr Hingabe. Bei denen ist ja alles anders.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		self.__drawHeading(offsetH, offsetV, width, self.tr("Description"))

		self.__painter.setFont(self.__fontMain_small)
		fontMetrics = QFontMetrics(self.__painter.font())
		fontHeight = fontMetrics.height()

		text = [
			[ "Birthday:", self.__character.dateBirth.toString(Config.textDateFormat), ],
			[ "Age:", self.__character.age, ],
			[ "Sex:", ImageTools.genderSymbol(self.__character.identity.gender), ],
			[ "Eyes:", self.__character.eyes, ],
			[ "Height:", "{} {}".format(self.__character.height, "m"), ],
			[ "Weight:", "{} {}".format(self.__character.weight, "kg"), ],
			[ "Hair:", self.__character.hair, ],
			[ "Nationality:", self.__character.nationality, ],
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

		additionalSpace = 0
		if self.__character.species == "Werewolf":
			additionalSpace = 3 * fontHeight

		self.__painter.drawText(offsetH, offsetV + self.__fontHeadingHeight, width, height - additionalSpace - (len(text) // 2 + 1) * fontHeight, Qt.AlignLeft | Qt.TextWordWrap, self.__character.description)

		i = 0
		j = 0
		for item in text:
			self.__drawTextWithValue(posX=offsetH + i * (width / 2 + self.__textDotSep), posY=offsetV + height - additionalSpace - (len(text) // 2 - j) * fontHeight, width=width / 2 - self.__textDotSep, text=item[0], value=item[1])
			j += 1
			if j >= len(text) // 2:
				i += 1
				j = 0

		## Jede einzelne Gestalt eines Werwolfs hat eigene Maße
		if self.__character.species == "Werewolf":
			werwolfHeights = CalcShapes.werewolfHeight(height=self.__character.height, strength=self.__character.traits["Attribute"]["Physical"]["Strength"].value, stamina=self.__character.traits["Attribute"]["Physical"]["Stamina"].value)
			werwolfWeights = CalcShapes.werewolfWeight(weight=self.__character.weight, strength=self.__character.traits["Attribute"]["Physical"]["Strength"].value, stamina=self.__character.traits["Attribute"]["Physical"]["Stamina"].value)
			shapeMeasurements = [
				[ "", "Height:", "Weight:", ],
				[ Config.shapesWerewolf[0], "{} {}".format(werwolfHeights[0], "m"), "{} {}".format(werwolfWeights[0], "kg"), ],
				[ Config.shapesWerewolf[1], "{} {}".format(werwolfHeights[1], "m"), "{} {}".format(werwolfWeights[1], "kg"), ],
				[ Config.shapesWerewolf[2], "{} {}".format(werwolfHeights[2], "m"), "{} {}".format(werwolfWeights[2], "kg"), ],
				[ Config.shapesWerewolf[3], "{} {}".format(werwolfHeights[3], "m"), "{} {}".format(werwolfWeights[3], "kg"), ],
				[ Config.shapesWerewolf[4], "{} {}".format(werwolfHeights[4], "m"), "{} {}".format(werwolfWeights[4], "kg"), ],
			]

			i = 0
			posY = offsetV + height - len(shapeMeasurements[0]) * fontHeight
			lengthX = width / len(shapeMeasurements)
			for item in shapeMeasurements:
				posX = offsetH + i * (width / len(shapeMeasurements))
				for j in xrange(len(item)):
					self.__painter.drawText(posX, posY + j * fontHeight, lengthX, fontHeight, Qt.AlignHCenter, item[j])
				i += 1

		self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawImage(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Fügt das Charakterbild ein.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox.
		\param width Die Breite der Spalte.

		\note Das Bild wird stets auf den zur Verfügung stehenden Raum skaliert.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		self.__drawHeading(offsetH, offsetV, width, self.tr("Picture"))

		if self.__character.picture:
			boxRect = QRect(offsetH, offsetV + self.__fontHeadingHeight + self.__headingSep, width, height - self.__fontHeadingHeight - self.__headingSep)
			image = self.__character.picture
			#Debug.debug(image.width(), image.height())
			if True or image.width() > boxRect.width() or image.height() > boxRect.height():
				image = image.scaled(boxRect.width(), boxRect.height(), Qt.KeepAspectRatio)
				#Debug.debug(image.width(), image.height())
			self.__painter.drawPixmap(boxRect.x() + (boxRect.width() - image.width()) / 2, boxRect.y(), image)

		self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawXP(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Fügt den Kasten für die Erfahrungspunkte hinzu.

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox.
		\param width Die Breite der Spalte.
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		halfWidth = width / 2 - self.__posSep / 2
		if self.__character.species == "Mage":
			self.__drawHeading(offsetH, offsetV, halfWidth, self.tr("XP"))
			self.__drawHeading(offsetH + width - halfWidth, offsetV, halfWidth, self.tr("Arcane XP"))
		else:
			self.__drawHeading(offsetH, offsetV, width, self.tr("XP"))

		pen = self.__painter.pen()
		pen.setWidth(self.__lineWidthBox)
		self.__painter.setPen(pen)
		self.__painter.setBrush(self.__colorEmpty)

		if self.__character.species == "Mage":
			self.__painter.drawRect(offsetH, offsetV + self.__fontHeadingHeight + self.__headingSep, halfWidth, height - self.__fontHeadingHeight - self.__headingSep)
			self.__painter.drawRect(offsetH + width - halfWidth, offsetV + self.__fontHeadingHeight + self.__headingSep, halfWidth, height - self.__fontHeadingHeight - self.__headingSep)
		else:
			self.__painter.drawRect(offsetH, offsetV + self.__fontHeadingHeight + self.__headingSep, width, height - self.__fontHeadingHeight - self.__headingSep)

		self.__drawBB(offsetH, offsetV, width, height)

		self.__painter.restore()


	def _drawMagicalTool(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Schreibt das Magisce Werkzeug nieder

		\param offsetH Der horizontale Abstand zwischen der linken Kante des nutzbaren Charakterbogens bis zum linken Rahmen der Boundingbox.
		\param offsetV Der vertikale Abstand zwischen der Oberkante des nutzbaren Charakterbogens bis zum opren Punkt des Boundingbox.
		\param width Die Breite der Spalte.
		\param height Höhe dieser Spalte
		"""

		self.__drawText(
			self.tr("Magical Tool"),
			self.__character.magicalTool,
			offsetH,
			offsetV,
			width,
			height
		)


	def _drawVinculi(self, offsetH=0, offsetV=0, width=None, height=None):
		"""
		Blutsbande
		"""

		self.__painter.save()

		if width == None:
			width = self.__pageWidth / 3

		self.__drawHeading(offsetH, offsetV, width, self.tr("Vinculi"))

		self.__painter.setFont(self.__fontMain)

		fontMetrics = QFontMetrics(self.__painter.font())
		fontHeight = fontMetrics.height()

		i = 0
		for vinculum in self.__character.vinculi:
			self.__drawTrait(
				offsetH,
				offsetV + self.__fontHeadingHeight + self.__headingSep + i * fontHeight,
				width=width,
				name=vinculum.name,
				value=vinculum.value,
				maxValue=Config.vinculumLevelMax
			)
			i += 1

		self.__drawBB(offsetH, offsetV, width, height)

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


	def __drawSubHeading(self, posX, posY, width, text):
		"""
		Zeichnet eine Überschrift in der für die Spezies vorgesehenen Schriftart.

		\param poxX Obere Kante der Boundingbox für die Überschrift.
		\param poxY Linke Kante der Boundingbox für die Überschrift.
		\param width Breite der Überschrift
		\param text Der Text der Überschrift
		\return die Höhe, welche die Überschrift in Anspruch nimmt. Dies ist nützlich, um den Text darunter besser paltzieren zu können.
		"""

		self.__painter.save()

		self.__painter.setFont(self.__fontSubHeading)
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


	def __drawTrait(self, posX, posY, width, align=Qt.AlignLeft, name="", text="", value=0, maxValue=5, mirrored=False):
		"""
		Schreibt eine Eigenschaft mit den Punktwerten.

		posX und posY bestimmen den Punkt der Auflagelinie des Textes.
		"""

		self.__painter.save()

		fontMetrics = QFontMetrics(self.__painter.font())
		textHeight = fontMetrics.height()
		dotsWidth = maxValue * (self.__dotDiameterH + self.__dotLineWidth / 2)
		textWidth = fontMetrics.boundingRect(name).width()

		if mirrored:
			alignMirrored = align
			if align == Qt.AlignLeft:
				alignMirrored = Qt.AlignRight
			if align == Qt.AlignRight:
				alignMirrored = Qt.AlignLeft
			self.__painter.drawText(posX + dotsWidth + self.__dotSep, posY, width - dotsWidth - self.__dotSep, textHeight, alignMirrored, name)
		else:
			self.__painter.drawText(posX, posY, width - dotsWidth - self.__dotSep, textHeight, align, name)

		## Bei linksbündigen Eigenschaften muß eine Linie gezogen werden, damit man weiß, welche Punkte zu welcher Eigenschaft gehören.
		if align == Qt.AlignLeft:
			## Wenn text angegeben wird, wird dieser auf die Linie geschrieben.
			smallWidth = 0
			if text:
				self.__painter.save()
				font = self.__painter.font()
				font.setPointSize(font.pointSize() - 10)
				self.__painter.setFont(font)

				fontMetricsSmall = QFontMetrics(self.__painter.font())
				textWidthSmall = fontMetricsSmall.boundingRect(text).width()

				smallAlign = align
				smallWidth = textWidthSmall
				if textWidthSmall > width - textWidth - dotsWidth - 2 * self.__dotSep:
					smallAlign = align | Qt.TextWordWrap
					smallWidth = width - textWidth - dotsWidth - self.__dotSep
				self.__painter.drawText(posX + textWidth + self.__textDotSep, posY +  fontMetrics.ascent() - fontMetricsSmall.ascent(), smallWidth, 2 * fontMetricsSmall.height(), smallAlign, text)
				self.__painter.restore()

			if smallWidth < width - textWidth - dotsWidth - self.__dotSep:
				self.__painter.save()
				pen = self.__painter.pen()
				pen.setWidthF(self.__lineWidth)
				self.__painter.setPen(pen)
				if mirrored:
					self.__painter.drawLine(posX + dotsWidth + self.__dotSep, posY + fontMetrics.ascent(), posX + width - textWidth - smallWidth - self.__textDotSep, posY +  fontMetrics.ascent())
				else:
					self.__painter.drawLine(posX + textWidth + smallWidth + self.__textDotSep, posY +  fontMetrics.ascent(), posX + width - dotsWidth - self.__textDotSep, posY +  fontMetrics.ascent())
				self.__painter.restore()

		if mirrored:
			self.__drawValueDots(posX, posY + fontMetrics.ascent(), value, maxValue)
		else:
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
		if GlobalState.isDevelop:
			self.__painter.save()

			pen = QPen(Qt.DashDotDotLine)
			pen.setColor(QColor(255,0,0))
			pen.setWidthF(1)
			self.__painter.setPen(pen)
			self.__painter.setBrush(Qt.NoBrush)
			self.__painter.drawRect(posX, posY, width, height)

			self.__painter.restore()



