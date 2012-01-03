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

from PySide.QtCore import Qt, QObject, QRectF
from PySide.QtGui import QColor, QPen, QBrush, QPainter, QImage, QFont, QFontDatabase, QFontMetrics

#from src.Config import Config
from src.Error import ErrSpeciesNotExisting
from src.Datatypes.Identity import Identity
from src.Debug import Debug




class DrawSheet(QObject):
	"""
	\brief Führt das Drucken des Charakters aus.

	Mit Hilfe dieser Klasse können die Charakterwerte auf Papier gebannt werden.

	\todo Bei Werwölfen wird die Rites-Kraft noch nicht beim Zeichnen der Kräfte unter Renown berücksichtigt.
	"""

	def __init__(self, character, printer, parent=None):
		QObject.__init__(self, parent)

		self.__character = character

		self.__painter = QPainter()
		self.__printer = printer

		self.__dotDiameterH = 9
		self.__dotDiameterV = self.__dotDiameterH
	#v_textHeight = 0;
	#v_textDotsHeightDifference = 0;
		## Die Farbe, mit welcher die Punkte auf dem Charakterbogen ausgefüllt werden.
		self.__colorFill = QColor( 0, 0, 0 )
		self.__colorEmpty = QColor( 255, 255, 255 )
		self.__colorText = QColor( 255, 0, 0 )

		## Schriften sind Abhängig von der Spezies.
		self.__fontMain = QFont("TeX Gyre Pagella")
		self.__fontSans = QFont("TeX Gyre Heros" )
		self.__fontHeading = QFont("TeX Gyre Heros", 13 )
		if self.__character.species == "Human":
			self.__fontHeading = QFont("ArchitectsDaughter", 11 )
		elif self.__character.species == "Changeling":
			self.__fontHeading = QFont("Mutlu", 13 )
		elif self.__character.species == "Mage":
			self.__fontHeading = QFont("Tangerine", 15 )
		elif self.__character.species == "Vampire":
			self.__fontHeading = QFont("Cloister Black", 13 )
		elif self.__character.species == "Werewolf":
			self.__fontHeading = QFont("Note this", 13 )
		else:
			#self.__fontHeading = QFont("HVD Edding 780", 14 )	# Tiere
			raise ErrSpeciesNotExisting( character.species )
		self.__fontScript = QFont("Blokletters Balpen", 6 )

		#calcAdvantages = new CalcAdvantages( this );


	def print(self):
		"""
		Hier wird gezeichnet und gedruckt.
		"""
		
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
			raise ErrSpeciesNotExisting( character.species )

		## Grundeinstellungen des Painters sind abgeschlossen. Dies ist der Zusatnd, zu dem wir zurückkehren, wenn wir painter.restore() aufrufen.
		self.__painter.save()

		## Damit ich weiß, Wo ich meine Sachen platzieren muß kommt erstmal das Bild dahinter.
		source = QRectF ( 0.0, 0.0, float( image.width() ), float( image.height() ) )
		target = QRectF( 0.0, 0.0, float( self.__printer.width() ), float( self.__printer.height() ) )
		self.__painter.drawImage(target, image, source)

		self.drawGrid()

		self.drawInfo(offsetH=23, offsetV=118, distanceH=255, distanceV=19)

		self.drawAttributes(offsetH=23, offsetV=180, distanceV=18)

		self.__painter.restore()

		self.__painter.end()


	def drawGrid(self):
		"""
		Diese Funktion zeichnet ein Gitter, damit man weiß, an welcher Position man die Einträge platzieren muß.
		"""

		pageWidth = self.__printer.width()
		pageHeight = self.__printer.height()

		self.__painter.save()

		fontLcl = self.__fontSans
		fontLcl.setPointSize(4)
		self.__painter.setFont(fontLcl)
		self.__painter.setRenderHint(QPainter.TextAntialiasing)
		self.__painter.save()
		
		pen = QPen(Qt.DashLine)
		pen.setColor(QColor(0,0,255))
		self.__painter.setPen(pen)
		
		for i in range(pageWidth)[::10]:
			self.__painter.drawLine(i, 0, i, pageHeight)
		for i in range(pageHeight)[::10]:
			self.__painter.drawLine(0, i, pageWidth, i)

		self.__painter.restore()

		self.__painter.save()

		self.__painter.setPen(QColor(0,127,127))
		for i in range(pageWidth)[::100]:
			self.__painter.drawLine(i, 0, i, pageHeight)
			self.__painter.drawText(i+1, 0, 10, 10, Qt.AlignLeft, unicode(i))
		for i in range(pageHeight)[::100]:
			self.__painter.drawLine(0, i, pageWidth, i)
			self.__painter.drawText(1, i, 10, 10, Qt.AlignLeft, unicode(i))

		self.__painter.restore()

		self.__painter.restore()


	def drawInfo(self, offsetH=0, offsetV=0, distanceH=0, distanceV=0):
		"""
		Diese Funktion Schreibt Namen, Virtue/Vice etc. in den Kopf des Charakterbogens.

		\param offsetH Horizontaler Abstand zwischen Bildkante und der rechten Kante des Platzes für den Namen.
		\param offsetV Vertikaler Abstand zwischen Bildkante und dem Platz für den Namen.
		\param distanceH Horizontaler Abstand zwischen den Zeilen.
		\param distanceV Vertikaler Abstand zwischen den Spalten.
		"""

		text = [
			[ u"Name:", u"Concept:", ],
			[ u"Virute:", u"Vice:", ],
			[ u"Chronicle:", u"Faction:", ],
		]
		
		self.__painter.save()
		self.__painter.setFont(self.__fontHeading)

		fontMetrics = QFontMetrics(self.__painter.font())

		width = []
		for i in xrange(len(text)):
			subWidth = []
			for j in xrange(len(text[i])):
				self.__painter.drawText(offsetH + i * distanceH, offsetV + j * distanceV, text[i][j])
				subWidth.append(fontMetrics.boundingRect(text[i][j]).width())
			width.append(max(subWidth))

		self.__painter.restore()
		
		self.__painter.save()
		
		self.__painter.setFont(self.__fontScript)

		text = [
			[ Identity.displayNameDisplay(self.__character.identities[0].surename, self.__character.identities[0].firstname, self.__character.identities[0].nickname), u"", ],
			[ self.__character.virtue, self.__character.vice, ],
			[ u"", u"", ],
		]

		for i in xrange(len(text)):
			for j in xrange(len(text[i])):
				var = self.__character
				self.__painter.drawText(offsetH + i * distanceH + width[i], offsetV + j * distanceV, text[i][j])

		self.__painter.restore()


	def drawAttributes(self, offsetH=0, offsetV=0, distanceV=0):
		"""
		Diese Funktion Zeichnet die Attribute

		\param offsetH Horizontaler Abstand zwischen Bildkante und der rechten Kante des Platzes für den Namen.
		\param offsetV Vertikaler Abstand zwischen Bildkante und dem Platz für den Namen.
		\param distanceV Vertikaler Abstand zwischen den Spalten.
		"""

		self.__painter.save()
		self.__painter.setFont(self.__fontHeading)

		text = [ u"Power", u"Finesse", u"Resistance", ]

		fontMetrics = QFontMetrics(self.__painter.font())
		textwidthArray = []
		for item in text:
			textwidthArray.append(fontMetrics.boundingRect("Resistance").width())
		textwidth = max(textwidthArray)
		height = fontMetrics.height()
		baseline = offsetV - fontMetrics.ascent()

		for i in xrange(len(text)):
			for j in xrange(len(text[i])):
				self.__painter.drawText(offsetH, baseline + i * distanceV, textwidth, height, Qt.AlignRight, text[i])

		self.__painter.restore()

		self.__painter.save()
		self.__painter.setFont(self.__fontMain)
		fontMetrics = QFontMetrics(self.__painter.font())
		height = fontMetrics.height()
		baseline = offsetV - fontMetrics.ascent()

		widthLeft = self.__printer.width() - offsetH - textwidth

		distanceH = widthLeft // 3

		sep = 4

		i = 0
		for item in self.__character.traits["Attribute"]:
			j = 0
			for subitem in self.__character.traits["Attribute"][item]:
				# Schreibe Attributsname
				self.__painter.drawText(offsetH + i * distanceH, baseline + j * distanceV, distanceH, height, Qt.AlignRight, subitem.name)
				# Male Punkte aus
				for k in xrange(subitem.value):
					self.__painter.drawEllipse(offsetH + (i+1) * distanceH + sep + k * self.__dotDiameterH, offsetV - self.__dotDiameterV + j * distanceV, self.__dotDiameterH, self.__dotDiameterV)
				## \todo die "5" muß mit dem Maximalen für den Charakter möglichen Wert ersetzt werden.
				self.__painter.save()
				self.__painter.setBrush(self.__colorEmpty)
				self.__painter.setOpacity(.5)
				for k in range(subitem.value, 5):
					self.__painter.drawEllipse(offsetH + (i+1) * distanceH + sep + k * self.__dotDiameterH, offsetV - self.__dotDiameterV + j * distanceV, self.__dotDiameterH, self.__dotDiameterV)
				self.__painter.restore()
				j += 1
			i += 1

		self.__painter.restore()

	## Der horizontale Radius eines Punkts auf dem Charakterbogen.
	#v_dotDiameterH = target.width() * 0.01156;
	## Der vertikale Radius eines Punkts auf dem Charakterbogen.
	#v_dotDiameterV = target.height() * 0.0082;

	## Die Schrifthöhe auf dem Charakterbogen.
	#v_textHeight = target.height() * 0.0182;
	## Die Differenz in der Ausgangshöhe zwischen dem Schrifttext und den Punkten.
	#v_textDotsHeightDifference = target.height() * 0.002;

	#qreal dotSizeFactor = 1.27;

	#qreal offsetHInfo = target.width() * 0.34;
	#qreal offsetVInfo = target.height() * 0.09;
	#qreal distanceHInfo = target.width() * 0.3;
	#qreal distanceVInfo = target.height() * 0.019;
	#qreal textWidthInfo = target.width() * 0.215;

	#qreal offsetHAttributes = target.width() * 0.36;
	#qreal offsetVAttributes = target.height() * 0.152;
	#qreal distanceHAttributes = target.width() * 0.2764;
	#qreal distanceVAttributes = target.height() * 0.0158;

	#qreal offsetHSkills = target.width() * 0.338;
	#qreal offsetVSkills = target.height() * 0.235;
	#qreal distanceVSkills = target.height() * 0.01795;
	#qreal distanceVCat = target.height() * 0.1735;
	#qreal textWidthSkills = target.width() * 0.23;

	#int maxMerits = 17;
	#qreal offsetHMerits = target.width() * 0.66;
	#qreal offsetVMerits = offsetVSkills;
	#qreal distanceVMerits = target.height() * 0.0178;
	#qreal textWidthMerits = target.width() * 0.247;

	#qreal offsetHFlaws = target.width() * 0.413;
	#qreal offsetVFlaws = target.height() * 0.565;
	#qreal textWidthFlaws = target.width() * 0.306;

	#int maxPowers = 0;
	#qreal offsetHPowers = 0;
	#qreal offsetVPowers = 0;
	#qreal distanceHPowers = 0;
	#qreal distanceVPowers = 0;
	#qreal textWidthPowers = 0;

	#qreal offsetHAdvantages = target.width() * 0.84;
	#qreal offsetVAdvantages = target.height() * 0.2119;
	#qreal distanceHAdvantages = 0;	// Nur für Werwölfe mit mehreren Gestalten interessant.
	#qreal distanceVAdvantages = target.height() * 0.022;
	#qreal textWidthAdvantages = target.width() * 0.174;

	#qreal offsetHHealth = target.width() * 0.766;
	#qreal offsetVHealth = target.height() * 0.3532;
	#qreal distanceHHealth = target.width() * 0.017;

	#qreal offsetHWillpower = target.width() * 0.77503;
	#qreal offsetVWillpower = target.height() * 0.4145;
	#qreal distanceHWillpower = distanceHHealth;

	#qreal offsetHSuper = 0;
	#qreal offsetVSuper = 0;
	#qreal distanceHSuper = 0;

	#qreal offsetHFuel = 0;
	#qreal offsetVFuel = 0;
	#qreal distanceHFuel = 0;
	#qreal squareSizeFuel = 0;

	#qreal offsetHFuelPerTurn = 0;
	#qreal offsetVFuelPerTurn = 0;
	#qreal distanceHFuelPerTurn = 0;

	#qreal offsetHMorality = target.width() * 0.9565;
	#qreal offsetVMorality = target.height() * 0.608;
	#qreal distanceVMorality = target.height() * 0.0144;
	#qreal textWidthMorality = target.width() * 0.187;

	#if ( character.species() == cv_Species::Human ) {
		#// Werte bleiben, wie sie zuvor definiert wurden.
	#} else if ( character.species() == cv_Species::Changeling ) {
		#offsetHInfo = target.width() * 0.352;
		#offsetVInfo = target.height() * 0.116;
		#distanceHInfo = target.width() * 0.286;
		#distanceVInfo = target.height() * 0.019;
		#textWidthInfo = target.width() * 0.218;

		#offsetHAttributes = target.width() * 0.352;
		#offsetVAttributes = target.height() * 0.177;
		#distanceHAttributes = target.width() * 0.257;
		#distanceVAttributes = target.height() * 0.016;

		#offsetHSkills = target.width() * 0.2955;
		#offsetVSkills = target.height() * 0.261;
		#distanceVCat = target.height() * 0.1665;
		#textWidthSkills = target.width() * 0.14;

		#maxMerits = 14;
		#offsetHMerits = target.width() * 0.6085;
		#offsetVMerits = target.height() * 0.4255;
		#textWidthMerits = target.width() * 0.237;

		#offsetHFlaws = target.width() * 0.367;
		#offsetVFlaws = target.height() * 0.69;
		#textWidthFlaws = target.width() * 0.303;

		#offsetHAdvantages = target.width() * 0.79;
		#offsetVAdvantages = target.height() * 0.237;

		#offsetHHealth = target.width() * 0.686;
		#offsetVHealth = target.height() * 0.3725;

		#offsetHWillpower = target.width() * 0.7255;
		#offsetVWillpower = target.height() * 0.4275;

		#offsetHSuper = target.width() * 0.73015;
		#offsetVSuper = target.height() * 0.4887;
		#distanceHSuper = target.width() * 0.016;

		#offsetHFuel = target.width() * 0.861;
		#offsetVFuel = target.height() * 0.544;
		#distanceHFuel = target.width() * 0.0032;
		#squareSizeFuel = target.width() * 0.014;

		#offsetHFuelPerTurn = target.width() * 0.865;
		#offsetVFuelPerTurn = target.height() * 0.527;
		#distanceHFuelPerTurn = target.height() * 0.045;

		#offsetHMorality = target.width() * 0.909;
		#offsetVMorality = target.height() * 0.716;
		#distanceVMorality = target.height() * 0.0143;

		#maxPowers = 8;
		#offsetHPowers = offsetHMerits;
		#offsetVPowers = offsetVSkills;
		#distanceVPowers = distanceVMerits;
		#textWidthPowers = textWidthMerits;
	#} else if ( character.species() == cv_Species::Mage ) {
		#offsetHInfo = target.width() * 0.35;
		#offsetVInfo = target.height() * 0.087;
		#distanceHInfo = target.width() * 0.315;
		#distanceVInfo = target.height() * 0.019;
		#textWidthInfo = target.width() * 0.255;

		#offsetHAttributes = target.width() * 0.341;
		#offsetVAttributes = target.height() * 0.158;
		#distanceHAttributes = target.width() * 0.2865;
		#distanceVAttributes = target.height() * 0.016;

		#offsetHSkills = target.width() * 0.2995;
		#offsetVSkills = target.height() * 0.2405;
		#distanceVCat = target.height() * 0.1787;
		#textWidthSkills = target.width() * 0.186;

		#maxMerits = 17;
		#offsetHMerits = target.width() * 0.642;
		#offsetVMerits = target.height() * 0.344;
		#textWidthMerits = target.width() * 0.268;

		#offsetHFlaws = target.width() * 0.37;
		#offsetVFlaws = target.height() * 0.67;
		#textWidthFlaws = target.width() * 0.33;

		#offsetHAdvantages = target.width() * 0.83;
		#offsetVAdvantages = target.height() * 0.215;

		#offsetHHealth = target.width() * 0.749;
		#offsetVHealth = target.height() * 0.351;

		#offsetHWillpower = target.width() * 0.766;
		#offsetVWillpower = target.height() * 0.4067;

		#offsetHSuper = target.width() * 0.771;
		#offsetVSuper = target.height() * 0.4695;
		#distanceHSuper = target.width() * 0.016;

		#offsetHFuel = target.width() * 0.8945;
		#offsetVFuel = target.height() * 0.5215;
		#distanceHFuel = target.width() * 0.0032;
		#squareSizeFuel = target.width() * 0.014;

		#offsetHFuelPerTurn = target.width() * 0.915;
		#offsetVFuelPerTurn = target.height() * 0.5045;
		#distanceHFuelPerTurn = target.height() * 0.045;

		#offsetHMorality = target.width() * 0.9575;
		#offsetVMorality = target.height() * 0.695;
		#distanceVMorality = target.height() * 0.0143;
		#textWidthMorality = target.width() * 0.205;

		#maxPowers = 10;
		#offsetHPowers = target.width() * 0.469;
		#offsetVPowers = offsetVSkills;
		#distanceHPowers = target.width() * 0.1245;
		#distanceVPowers = target.height() * 0.0143;
	#} else if ( character.species() == cv_Species::Vampire ) {
		#offsetHInfo = target.width() * 0.361;
		#offsetVInfo = target.height() * 0.115;
		#distanceHInfo = target.width() * 0.29;
		#distanceVInfo = target.height() * 0.019;
		#textWidthInfo = target.width() * 0.228;

		#offsetHAttributes = target.width() * 0.3555;
		#offsetVAttributes = target.height() * 0.194;
		#distanceHAttributes = target.width() * 0.2565;
		#distanceVAttributes = target.height() * 0.0157;

		#offsetHSkills = target.width() * 0.2895;
		#offsetVSkills = target.height() * 0.28;
		#distanceVCat = target.height() * 0.1703;
		#textWidthSkills = target.width() * 0.14;

		#maxMerits = 14;
		#offsetHMerits = target.width() * 0.591;
		#offsetVMerits = target.height() * 0.4444;
		#textWidthMerits = target.width() * 0.2275;

		#offsetHFlaws = target.width() * 0.365;
		#offsetVFlaws = target.height() * 0.71;
		#textWidthFlaws = target.width() * 0.29;

		#offsetHAdvantages = target.width() * 0.79;
		#offsetVAdvantages = target.height() * 0.255;

		#offsetHHealth = target.width() * 0.668;
		#offsetVHealth = target.height() * 0.392;

		#offsetHWillpower = target.width() * 0.7178;
		#offsetVWillpower = target.height() * 0.448;

		#offsetHSuper = target.width() * 0.723;
		#offsetVSuper = target.height() * 0.506;
		#distanceHSuper = target.width() * 0.016;

		#offsetHFuel = target.width() * 0.8441;
		#offsetVFuel = target.height() * 0.5605;
		#distanceHFuel = target.width() * 0.00315;
		#squareSizeFuel = target.width() * 0.014;

		#offsetHFuelPerTurn = target.width() * 0.867;
		#offsetVFuelPerTurn = target.height() * 0.541;
		#distanceHFuelPerTurn = target.height() * 0.045;

		#offsetHMorality = target.width() * 0.9103;
		#offsetVMorality = target.height() * 0.735;
		#distanceVMorality = target.height() * 0.0143;
		#textWidthMorality = target.width() * 0.21;

		#maxPowers = 8;
		#offsetHPowers = offsetHMerits;
		#offsetVPowers = offsetVSkills;
		#distanceVPowers = distanceVMerits;
		#textWidthPowers = textWidthMerits;
	#} else if ( character.species() == cv_Species::Werewolf ) {
		#offsetHInfo = target.width() * 0.345;
		#offsetVInfo = target.height() * 0.085;
		#distanceHInfo = target.width() * 0.32;
		#distanceVInfo = target.height() * 0.019;
		#textWidthInfo = target.width() * 0.255;

		#offsetHAttributes = target.width() * 0.285;
		#offsetVAttributes = target.height() * 0.146;
		#distanceHAttributes = target.width() * 0.235;
		#distanceVAttributes = target.height() * 0.016;

		#offsetHSkills = target.width() * 0.299;
		#offsetVSkills = target.height() * 0.24;
		#distanceVCat = target.height() * 0.1734;
		#textWidthSkills = target.width() * 0.17;

		#maxMerits = 13;
		#offsetHMerits = target.width() * 0.642;
		#offsetVMerits = target.height() * 0.342;
		#textWidthMerits = target.width() * 0.268;

		#offsetHFlaws = target.width() * 0.37;
		#offsetVFlaws = target.height() * 0.595;
		#textWidthFlaws = target.width() * 0.332;

		#offsetHAdvantages = target.width() * 0.2;
		#offsetVAdvantages = target.height() * 0.83;
		#distanceHAdvantages = target.width() * 0.196;
		#distanceVAdvantages = target.height() * 0.017;

		#offsetHHealth = target.width() * 0.749;
		#offsetVHealth = target.height() * 0.244;

		#offsetHWillpower = target.width() * 0.766;
		#offsetVWillpower = target.height() * 0.3073;

		#offsetHSuper = target.width() * 0.771;
		#offsetVSuper = target.height() * 0.3715;
		#distanceHSuper = target.width() * 0.016;

		#offsetHFuel = target.width() * 0.8945;
		#offsetVFuel = target.height() * 0.433;
		#distanceHFuel = target.width() * 0.0032;
		#squareSizeFuel = target.width() * 0.014;

		#offsetHFuelPerTurn = target.width() * 0.915;
		#offsetVFuelPerTurn = target.height() * 0.415;
		#distanceHFuelPerTurn = target.height() * 0.045;

		#offsetHMorality = target.width() * 0.9555;
		#offsetVMorality = target.height() * 0.6144;
		#distanceVMorality = target.height() * 0.0143;
		#textWidthMorality = target.width() * 0.205;

		#maxPowers = 5;
		#offsetHPowers = target.width() * 0.469;
		#offsetVPowers = offsetVSkills;
		#distanceHPowers = target.width() * 0.1245;
		#distanceVPowers = target.height() * 0.0143;
	#} else {
		#throw eSpeciesNotExisting( character.species() );
	#}

	#// Die Schriftart einstellen.
	#QFont characterFont = Config::exportFont;

	#characterFont.setPointSize( v_textHeight*Config::textSizeFactorPrintNormal );

		##painter.setFont( characterFont )
		#painter.setFont( QFont("ArchitectsDaughter" ))
		#Debug.debug(painter.font())

##// 	qDebug() << Q_FUNC_INFO << "Punktradius" << v_dotDiameterH << v_dotDiameterV;

		#painter.save()

		#painter.drawImage( target, image, source )
		#text = u"Dies ist ein ganz normaler Testsatz, in dem ich auch ein paar Umlaute wie beispielsweise ÄÖÜßäöü é unterbringen will."
		#painter.drawText(10, 10, text)

		#painter.restore()

		#painter.setFont( QFont("HVD Edding 780" ))
		#painter.save()
		#painter.drawText(10, 20, text)

	#drawInfo( &painter, offsetHInfo, offsetVInfo, distanceHInfo, distanceVInfo, textWidthInfo );
	#drawAttributes( &painter, offsetHAttributes, offsetVAttributes, distanceHAttributes, distanceVAttributes );
	#drawSkills( &painter, offsetHSkills, offsetVSkills, distanceVSkills, distanceVCat, textWidthSkills );
	#drawMerits( &painter, offsetHMerits, offsetVMerits, distanceVMerits, textWidthMerits, maxMerits );
	#drawFlaws( &painter, offsetHFlaws, offsetVFlaws, textWidthFlaws );
	#drawAdvantages( &painter, offsetHAdvantages, offsetVAdvantages, distanceVAdvantages, textWidthAdvantages, character.species(), distanceHAdvantages );
	#drawHealth( &painter, offsetHHealth, offsetVHealth, distanceHHealth, dotSizeFactor );
	#drawWillpower( &painter, offsetHWillpower, offsetVWillpower, distanceHWillpower, dotSizeFactor );
	#drawMorality( &painter, offsetHMorality, offsetVMorality, distanceVMorality, textWidthMorality );

	#if ( character.species() != cv_Species::Human ) {
		#drawPowers( &painter, offsetHPowers, offsetVPowers, distanceVPowers, textWidthPowers, maxPowers, character.species(), distanceHPowers );

		#// Werwölfe haben zusätzlich zu Renown auch noch Rites.
		#if ( character.species() == cv_Species::Werewolf ) {
			#drawPowers( &painter, offsetHMerits, offsetVPowers + target.height() * 0.058, distanceVPowers, textWidthPowers, maxPowers, character.species(), 0 );
		#}

		#drawSuper( &painter, offsetHSuper, offsetVSuper, distanceHSuper, dotSizeFactor );
		#drawFuelMax( &painter, offsetHFuel, offsetVFuel, distanceHFuel, squareSizeFuel );
		#drawFuelPerTurn( &painter, offsetHFuelPerTurn, offsetVFuelPerTurn, distanceHFuelPerTurn );
	#}



#void DrawSheet::drawInfo( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH, qreal distanceV, qreal textWidth ) {
	#// Der Name braucht mehr vertikalen Raum, da er sehr lang sein kann.
	#QRect textRect( offsetH - textWidth, offsetV - v_textHeight + distanceV*0, textWidth, 2*v_textHeight );
	#painter.drawText( textRect, Qt::AlignLeft | Qt::AlignBottom | Qt::TextWordWrap, cv_Name::displayNameDisplay( character.identities().at( 0 ).sureName, character.identities().at( 0 ).firstName(), character.identities().at( 0 ).nickName ) );

	#//Virtue
	#textRect = QRect( offsetH + distanceH - textWidth, offsetV + distanceV * 0, textWidth, v_textHeight );
	#painter.drawText( textRect, Qt::AlignLeft | Qt::AlignBottom | Qt::TextWordWrap, character.virtue() );
	#//Vice
	#textRect = QRect( offsetH + distanceH - textWidth, offsetV + distanceV * 1, textWidth, v_textHeight );
	#painter.drawText( textRect, Qt::AlignLeft | Qt::AlignBottom | Qt::TextWordWrap, character.vice() );

	#if ( character.species() != cv_Species::Human ) {
		#if ( character.species() == cv_Species::Mage || character.species() == cv_Species::Werewolf ) {
			#// Name unter übernatürlichen
			#qreal lcl_textWidth = textWidth * .75;

			#if ( character.species() == cv_Species::Werewolf ) {
				#lcl_textWidth = textWidth * .8;
			#}

			#textRect = QRect( offsetH - lcl_textWidth, offsetV + distanceV * 1, lcl_textWidth, v_textHeight );

			#painter.drawText( textRect, Qt::AlignLeft | Qt::AlignBottom | Qt::TextWordWrap, character.identities().at( 0 ).supernaturalName );
		#}
	#}

	#qreal lcl_textWidth = textWidth;

	#if ( character.species() == cv_Species::Changeling ) {
		#lcl_textWidth = textWidth * .95;
	#} else if ( character.species() == cv_Species::Vampire ) {
		#lcl_textWidth = textWidth * .85;
	#} else if ( character.species() == cv_Species::Werewolf ) {
		#lcl_textWidth = textWidth * .95;
	#}

	#// Breed
	#textRect = QRect( offsetH + distanceH * 2 - lcl_textWidth, offsetV, lcl_textWidth, v_textHeight );

	#painter.drawText( textRect, Qt::AlignLeft | Qt::AlignBottom | Qt::TextWordWrap, character.breed() );

	#qreal lcl_vSep = distanceV;

	#if ( character.species() == cv_Species::Vampire ) {
		#lcl_vSep = 2 * distanceV;
	#}

	#// Faction
	#textRect = QRect( offsetH + distanceH * 2 - lcl_textWidth, offsetV + lcl_vSep, lcl_textWidth, v_textHeight );

	#painter.drawText( textRect, Qt::AlignLeft | Qt::AlignBottom | Qt::TextWordWrap, character.faction() );
#}

#void DrawSheet::drawAttributes( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH, qreal distanceV ) {
	#QList< cv_AbstractTrait::Category > category = cv_AbstractTrait::getCategoryList( cv_AbstractTrait::Attribute );

	#QList< Trait* > list;

	#for ( int i = 0; i < category.count(); ++i ) {
		#// Bei Werwölfen ist der Abstand zwischen den Kategorien nicht identisch.
		#if ( character.species() == cv_Species::Werewolf && i > 1 ) {
			#distanceH *= 1.164;
		#}

		#list = character.traits( cv_AbstractTrait::Attribute, category.at( i ) );

		#for ( int j = 0; j < list.count(); ++j ) {
			#for ( int k = 0; k < list.at( j ).value(); ++k ) {
				#// Punkte malen.
				#QRectF dotsRect( offsetH + distanceH*i + v_dotDiameterH*k, offsetV + distanceV*j, v_dotDiameterH, v_dotDiameterV );
				#painter.drawEllipse( dotsRect );
			#}
		#}
	#}
#}

#void DrawSheet::drawSkills( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceV, qreal distanceVCat, qreal textWidth ) {
	#QList< cv_AbstractTrait::Category > categories = cv_AbstractTrait::getCategoryList( cv_AbstractTrait::Skill );

	#QList< Trait* > list;

	#for ( int i = 0; i < categories.count(); ++i ) {
		#list = character.traits( cv_AbstractTrait::Skill, categories.at( i ) );

		#for ( int j = 0; j < list.count(); ++j ) {
			#for ( int k = 0; k < list.at( j ).value(); ++k ) {
				#// Punkte malen.
				#QRectF dotsRect( offsetH + v_dotDiameterH*k, offsetV + distanceV*j + distanceVCat*i, v_dotDiameterH, v_dotDiameterV );
				#painter.drawEllipse( dotsRect );
			#}

			#if ( !list.at( j ).details().isEmpty() ) {
				#QString specialities;

				#for ( int k = 0; k < list.at( j ).details().count(); ++k ) {
					#// Spezialisierungen hinzufügen
					#specialities.append( list.at( j ).details().at( k ).name );

					#if ( k < list.at( j ).details().count() - 1 ) {
						#specialities.append( ", " );
					#}
				#}

				#// Spezialisierungen schreiben.
				#painter.save();

				#QFont lclFont = painter.font();

				#lclFont.setPointSize( v_textHeight*Config::textSizeFactorPrintSmall );

				#painter.setFont( lclFont );

				#// Wird ein bißchen nach oben verschoben, damit der Name schön über dem Strich steht.
				#QRect textRect( offsetH - textWidth, offsetV + distanceV*j + distanceVCat*i, textWidth, v_textHeight );

#// 				painter.drawRect( textRect );
				#painter.drawText( textRect, Qt::AlignLeft | Qt::AlignTop | Qt::TextWordWrap, specialities );

				#painter.restore();
			#}
		#}
	#}
#}


#void DrawSheet::drawMerits( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceV, qreal textWidth, int maxNumber ) {
	#QList< Trait* > listToUse;

	#try {
		#listToUse = getTraits( cv_AbstractTrait::Merit, maxNumber );
	#} catch ( eTraitsExceedSheetCapacity &e ) {
		#listToUse = getTraits( cv_AbstractTrait::Merit, maxNumber, true );
		#emit enforcedTraitLimits( cv_AbstractTrait::Merit );
	#}

	#for ( int j = 0; j < listToUse.count(); ++j ) {
		#for ( int k = 0; k < listToUse.at( j ).value(); ++k ) {
			#// Punkte malen.
			#QRectF dotsRect( offsetH + v_dotDiameterH*k, offsetV + distanceV*j, v_dotDiameterH, v_dotDiameterV );
			#painter.drawEllipse( dotsRect );
		#}

		#QString name = listToUse.at( j ).name();

		#QString customText = listToUse.at( j ).customText();

		#// Namen
		#QRect textRect( offsetH - textWidth, offsetV - v_textDotsHeightDifference + distanceV*j, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignLeft | Qt::AlignTop | Qt::TextWordWrap, name );

		#// Zusatztext

		#if ( !customText.isEmpty() ) {
			#painter.save();

			#QFont lclFont = painter.font();
			#lclFont.setPointSize( v_textHeight*Config::textSizeFactorPrintSmall );

			#painter.setFont( lclFont );
			#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, customText + " " );
			#painter.restore();
		#}
	#}
#}

#void DrawSheet::drawFlaws( QPainter* painter, qreal offsetH, qreal offsetV, qreal textWidth ) {
	#QList< cv_AbstractTrait::Category > category = cv_AbstractTrait::getCategoryList( cv_AbstractTrait::Flaw );

	#QList< Trait* > list;
	#QStringList stringList;

	#for ( int i = 0; i < category.count(); ++i ) {
		#list = character.traits( cv_AbstractTrait::Flaw, category.at( i ) );

		#for ( int j = 0; j < list.count(); ++j ) {
			#if ( list.at( j ).value() > 0 ) {
				#QString lcl_text = list.at( j ).name();

				#if ( list.at( j ).custom() ) {
					#lcl_text += " (" + list.at( j ).customText() + ")";
				#}

				#stringList.append( lcl_text );
			#}
		#}
	#}

	#QString text = stringList.join( ", " );

	#qreal lcl_textHeight = 3 * v_textHeight;

	#if ( character.species() != cv_Species::Human ) {
		#lcl_textHeight = 2 * v_textHeight;
	#}

	#QRect textRect( offsetH, offsetV, textWidth, lcl_textHeight );

	#painter.drawText( textRect, Qt::AlignLeft | Qt::AlignTop | Qt::TextWordWrap, text );
#}

#void DrawSheet::drawAdvantages( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceV, qreal textWidth, cv_Species::SpeciesFlag species,
								#qreal distanceH ) {
	#QRect textRect;

	#// Werwölfe haben mehrere Gestalten und für jede davon auch berechnete Werte

	#if ( species == cv_Species::Werewolf ) {
		#// Size
		#textRect = QRect( offsetH - textWidth, offsetV, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.size( cv_Shape::Hishu ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 1, offsetV, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.size( cv_Shape::Dalu ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 2, offsetV, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.size( cv_Shape::Gauru ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 3, offsetV, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.size( cv_Shape::Urshul ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 4, offsetV, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.size( cv_Shape::Urhan ) ) );

		#// Initiative
		#textRect = QRect( offsetH - textWidth, offsetV + distanceV * 1, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.initiative( cv_Shape::Hishu ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 1, offsetV + distanceV * 1, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.initiative( cv_Shape::Dalu ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 2, offsetV + distanceV * 1, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.initiative( cv_Shape::Gauru ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 3, offsetV + distanceV * 1, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.initiative( cv_Shape::Urshul ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 4, offsetV + distanceV * 1, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.initiative( cv_Shape::Urhan ) ) );

		#// Speed
		#textRect = QRect( offsetH - textWidth, offsetV + distanceV * 2, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.speed( cv_Shape::Hishu ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 1, offsetV + distanceV * 2, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.speed( cv_Shape::Dalu ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 2, offsetV + distanceV * 2, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.speed( cv_Shape::Gauru ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 3, offsetV + distanceV * 2, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.speed( cv_Shape::Urshul ) ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 4, offsetV + distanceV * 2, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.speed( cv_Shape::Urhan ) ) );

		#// Defense
		#textRect = QRect( offsetH - textWidth, offsetV + distanceV * 3, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.defense() ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 1, offsetV + distanceV * 3, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.defense() ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 2, offsetV + distanceV * 3, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.defense() ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 3, offsetV + distanceV * 3, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.defense() ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 4, offsetV + distanceV * 3, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.defense() ) );

		#// Armor
		#textRect = QRect( offsetH - textWidth, offsetV + distanceV * 4, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( character.armorGeneral() ) + "/" + QString::number( character.armorFirearms() ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 1, offsetV + distanceV * 4, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( character.armorGeneral() ) + "/" + QString::number( character.armorFirearms() ) );
		#textRect = QRect( offsetH - textWidth + distanceH * 2, offsetV + distanceV * 4, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, "1/1" );
#// 		textRect = QRect( offsetH - textWidth + distanceH * 3, offsetV + distanceV * 3, textWidth, v_textHeight );
#// 		painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.defense() ) );
#// 		textRect = QRect( offsetH - textWidth + distanceH * 4, offsetV + distanceV * 3, textWidth, v_textHeight );
#// 		painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.defense() ) );
	#} else {
		#// Size
		#QRect textRect = QRect( offsetH - textWidth, offsetV, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.size() ) );

		#// Initiative
		#textRect = QRect( offsetH - textWidth, offsetV + distanceV * 1, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.initiative() ) );

		#// Speed
		#textRect = QRect( offsetH - textWidth, offsetV + distanceV * 2, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.speed() ) );

		#// Defense
		#textRect = QRect( offsetH - textWidth, offsetV + distanceV * 3, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages.defense() ) );

		#// Armor
		#textRect = QRect( offsetH - textWidth, offsetV + distanceV * 4, textWidth, v_textHeight );
		#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( character.armorGeneral() ) + "/" + QString::number( character.armorFirearms() ) );
	#}

	#// Armor
#}

#void DrawSheet::drawHealth( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH, qreal dotSizeFactor ) {
	#int health = calcAdvantages.health();

	#for ( int i = 0; i < health; ++i ) {
		#QRect dotsRect = QRect( offsetH + distanceH * i, offsetV, v_dotDiameterH * dotSizeFactor, v_dotDiameterV * dotSizeFactor );
		#painter.drawEllipse( dotsRect );
	#}
#}

#void DrawSheet::drawWillpower( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH, qreal dotSizeFactor ) {
	#int willpower = calcAdvantages.willpower();

	#for ( int i = 0; i < willpower; ++i ) {
		#QRect dotsRect = QRect( offsetH + distanceH * i, offsetV, v_dotDiameterH * dotSizeFactor, v_dotDiameterV * dotSizeFactor );
		#painter.drawEllipse( dotsRect );
	#}
#}

#void DrawSheet::drawMorality( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceV, qreal textWidth, qreal dotSizeFactor ) {
	#int value = character.morality();

	#for ( int i = 0; i < value; ++i ) {
		#QRect dotsRect = QRect( offsetH, offsetV - distanceV * i, v_dotDiameterH * dotSizeFactor, v_dotDiameterV * dotSizeFactor );
		#painter.drawEllipse( dotsRect );
	#}

	#QList< cv_Derangement >* list = character.derangements();

	#for ( int i = value; i < Config::derangementMoralityTraitMax; ++i ) {
		#for ( int j = 0; j < list.count(); ++j ) {
			#if ( list.at( j ).morality() == i + 1 ) {
				#QRect textRect = QRect( offsetH - textWidth, offsetV + v_dotDiameterV * dotSizeFactor + v_textDotsHeightDifference - distanceV * i - v_textHeight, textWidth, v_textHeight );
#// 				painter.drawRect( textRect );
				#painter.drawText( textRect, Qt::AlignLeft | Qt::AlignBottom, list.at( j ).name() );

				#break;
			#}
		#}
	#}
#}

#void DrawSheet::drawPowers( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceV, qreal textWidth, int maxNumber, cv_Species::SpeciesFlag species, qreal distanceH ) {
	#QList< Trait* > listToUse;

	#try {
		#listToUse = getTraits( cv_AbstractTrait::Power, maxNumber );
	#} catch ( eTraitsExceedSheetCapacity &e ) {
		#listToUse = getTraits( cv_AbstractTrait::Power, maxNumber, true );
		#emit enforcedTraitLimits( cv_AbstractTrait::Power );
	#}

	#qDebug() << Q_FUNC_INFO << listToUse.count();

	#if ( species == cv_Species::Mage || ( species == cv_Species::Werewolf && distanceH != 0 ) ) {
		#// Bei Magiern und Werwölfen sind alle Kräfte schon auf dem Charakterbogen, also muß ich aufpassen, daß sie in der richtigen Reihenfolge an der richtigen Stelle auftauchen, auch wenn einige im Charkater fehlen.
		#StorageTemplate storage;
		#QList< Trait* > list = storage.traits( cv_AbstractTrait::Power, species );

		#// Bei den Werwölfen müssen die Rites gesondert behandelt werden.
		#if ( species == cv_Species::Werewolf ) {
			#list.removeLast();
		#}

		#qreal half = ceil( static_cast<qreal>( list.count() ) / 2 );

		#qDebug() << Q_FUNC_INFO << "Die halbe Anzahl an Powers ist:" << half;

		#for ( int i = 0; i < half; ++i ) {
			#for ( int k = 0; k < listToUse.count(); ++k ) {
				#if ( listToUse.at( k ).name() == list.at( i ).name() ) {
					#for ( int j = 0; j < listToUse.at( k ).value(); ++j ) {
						#// Punkte malen.
						#QRectF dotsRect( offsetH + v_dotDiameterH*j, offsetV + distanceV*i, v_dotDiameterH, v_dotDiameterV );
						#painter.drawEllipse( dotsRect );
					#}

					#break;
				#}
			#}
		#}

		#for ( int i = half; i < list.count(); ++i ) {
			#for ( int k = 0; k < listToUse.count(); ++k ) {
				#if ( listToUse.at( k ).name() == list.at( i ).name() ) {
					#for ( int j = 0; j < listToUse.at( k ).value(); ++j ) {
						#// Punkte malen.
						#QRectF dotsRect( offsetH + distanceH - v_dotDiameterH*j, offsetV + distanceV*( i - half ), v_dotDiameterH, v_dotDiameterV );
						#painter.drawEllipse( dotsRect );
					#}
					#break;
				#}
			#}
		#}
	#} else if ( species == cv_Species::Werewolf ) {
		#// Die Rites werden anders gezeichnet
		#for ( int k = 0; k < listToUse.last().value(); ++k ) {
			#// Punkte malen.
			#QRectF dotsRect( offsetH + v_dotDiameterH*k, offsetV, v_dotDiameterH, v_dotDiameterV );
			#painter.drawEllipse( dotsRect );
		#}
	#} else {
		#for ( int j = 0; j < listToUse.count(); ++j ) {
			#for ( int k = 0; k < listToUse.at( j ).value(); ++k ) {
				#// Punkte malen.
				#QRectF dotsRect( offsetH + v_dotDiameterH*k, offsetV + distanceV*j, v_dotDiameterH, v_dotDiameterV );
				#painter.drawEllipse( dotsRect );
			#}

			#QString name = listToUse.at( j ).name();
			#QString customText = listToUse.at( j ).customText();

			#// Namen
			#QRect textRect( offsetH - textWidth, offsetV - v_textDotsHeightDifference + distanceV*j, textWidth, v_textHeight );
			#painter.drawText( textRect, Qt::AlignLeft | Qt::AlignTop | Qt::TextWordWrap, name );

			#// Zusatztext

			#if ( !customText.isEmpty() ) {
				#painter.save();

				#QFont lclFont = painter.font();
				#lclFont.setPointSize( v_textHeight*Config::textSizeFactorPrintSmall );

				#painter.setFont( lclFont );
				#painter.drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, customText + " " );
				#painter.restore();
			#}
		#}
	#}
#}


#void DrawSheet::drawSuper( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH, qreal dotSizeFactor ) {
	#int value = character.superTrait();

	#for ( int i = 0; i < value; ++i ) {
		#QRect dotsRect = QRect( offsetH + distanceH * i, offsetV, v_dotDiameterH * dotSizeFactor, v_dotDiameterV * dotSizeFactor );
		#painter.drawEllipse( dotsRect );
	#}
#}

#void DrawSheet::drawFuelMax( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH, qreal widthPerSquare ) {
	#StorageTemplate storage;
	#int value = storage.fuelMax( character.species(), character.superTrait() );

	#if ( value > 20 ) {
		#QString fuel;

		#for ( int i = 0; i < storage.species().count(); ++i ) {
			#if ( cv_Species::toSpecies( storage.species().at( i ).name ) == character.species() ) {
				#fuel = storage.species().at( i ).fuel;
				#break;
			#}
		#}

		#throw eValueExceedsSheetCapacity( value, fuel );
	#}

	#painter.save();

	#painter.setOpacity( 0.5 );

	#for ( int i = 0; i < 20 - value; ++i ) {
		#QRect fuelRect = QRect( offsetH - ( widthPerSquare + distanceH ) * i, offsetV, -widthPerSquare, widthPerSquare );
#// 		painter.drawLine( fuelRect.bottomLeft(), fuelRect.topRight() );
#// 		painter.drawLine( fuelRect.topLeft(), fuelRect.bottomRight() );
		#painter.drawRect( fuelRect );
	#}

	#painter.restore();
#}

#void DrawSheet::drawFuelPerTurn( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH ) {
	#StorageTemplate storage;
	#int value = storage.fuelPerTurn( character.species(), character.superTrait() );

	#QRect textRect = QRect( offsetH, offsetV, distanceH, v_textHeight );
	#painter.drawText( textRect, Qt::AlignHCenter | Qt::AlignBottom, QString::number( value ) );
#// 	painter.drawRect(textRect);
#}






#QList< Trait* > DrawSheet::getTraits( cv_AbstractTrait::Type type, int maxNumber, bool enforceTraitLimits ) {
	"""
	Mit dieser Hilfsfunktion für drawMerits() werden die passenden Merits aus dem Charakter geholt.
	
	Diese globale Variable legt fest, ob bei einer Überschreitung der Eigenschaftshöchstwerte eine Ausnahme geworfen wird (false/Standardverhalten), oder die Grenzen einfach fest durchgesetzt werden.

	\param enforceTraitLimits Wird dieser Schalter auf true gesetzt (standardmäßig ist er false), werden die Grenzen für die maximale Anzahl durchgesetzt, auch wenn dadurch nicht alle Eigenschaften des Charakters auf Papier gebannt werden.
	"""
	
	#QList< cv_AbstractTrait::Category > category;
	#category.append( cv_AbstractTrait::CategoryNo );

#// 	if ( type == cv_AbstractTrait::Merit ) {
#// 		category.append( cv_AbstractTrait::getCategoryList( cv_AbstractTrait::Merit ) );
#// 	}
	#category.append( cv_AbstractTrait::getCategoryList( type ) );

	#QList< Trait* > list;
	#QList< Trait* > listToUse;

	#int iter = 0;

	#for ( int i = 0; i < category.count(); ++i ) {
		#list = character.traits( type, category.at( i ) );

		#for ( int j = 0; j < list.count(); ++j ) {
			#if ( list.at( j ).value() > 0 ) {
				#iter++;

				#listToUse.append( list.at( j ) );
			#}

			#// Sobald keine Eigenschaften mehr auf den Charakterbogen passen, hören wir auf, weitere hinzuzuschreiben. Das gilt natürlich nur, wenn maxNumber größer als 0 ist.
			#if ( maxNumber > 0 && iter > maxNumber ) {
				#if ( enforceTraitLimits ) {
					#break;
				#} else {
					#throw eTraitsExceedSheetCapacity( type, maxNumber );
				#}
			#}
		#}
	#}

	#return listToUse;
#}