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

from PySide.QtCore import Qt, QPoint, Signal
from PySide.QtGui import QWidget, QColor, QSizePolicy, QPen, QBrush, QPainter

#from src.Config import Config
#from src.Widgets.TraitLine import TraitLine
from src.Debug import Debug




class Dot(QWidget):
	"""
	@brief Ein simpler Punkt, der beim Klicken seine Farbe ändert.
	"""


	changed = Signal(bool)
	clicked = Signal(bool)


	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		# Widget darf nur proportional in seiner Größe verändert werden?
		# Minimalgröße festlegen
		self.__minimumSizeY = 8
		minimumSizeX = self.__minimumSizeY
		self.setMinimumSize( minimumSizeX, self.__minimumSizeY)
		self.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )

		self.__value = False

		# Setze Standardfarbe weiß
		self.__colorEmpty = QColor( 255, 255, 255 )
		self.__colorFull = QColor( 0, 0, 0 )
		self.__colorFrame = QColor( 0, 0, 0 )

		self.changed.connect(self.update)


	# Das automatisch ausgelöste paintEvent, das das Widget bei jeder Fensterveränderung neu zeichnet.
	def paintEvent( self, event ):
		# Wenn das Widget disabled ist, muß ich den Alphakanal meiner Farben verändern.
		frameWidth = 16
		dotCenter = QPoint( 0, 0 )
		color = self.__colorEmpty
		if self.__value:
			color = self.__colorFull
		
		# Damit der Rahmen nicht irgendwie abgeschnitten wird, muß der Kreis entsprechend kleiner sein.
		dotRadius = 100
		framePen = QPen( QBrush( Qt.OpaqueMode ), frameWidth )
		framePen.setColor( self.__colorFrame )

		dotDiameter = 2 * dotRadius + frameWidth

		painter = QPainter( self )

		windowWidth = self.width()
		windowHeight = float( self.height() )
		side = min( windowWidth, windowHeight )

		painter.setRenderHint( QPainter.Antialiasing )

		if ( not self.isEnabled() ):
			painter.setOpacity( .5 )

		painter.translate( side / 2, self.height() / 2 )

		painter.scale( side / dotDiameter, side / dotDiameter )

		painter.setPen( framePen )
		painter.setBrush( color )

		painter.save()

		painter.drawEllipse( dotCenter, dotRadius, dotRadius )

		painter.restore()


	# Anklicken
	def mousePressEvent( self, event ):
		self.value = not self.__value
		self.update()
		self.clicked.emit(self.value)

			## Die Position des Mauszeigers beim Klicken wird errechnet. Dabei soll die Mitte der linken Seite der Position (0, 0) entsprechen.
			#mousePoint = event.pos() - self.rect().bottomLeft() - QPoint( 0, self.rect().height() / 2 )

			## Welche Breite haben die Punkte? Das bestimme ich je nachdem, ob das Fenster zu breit ist, sie alle aufzunehmen, oder zu hoch, aus Höhe bzw. Breite.
			#windowWidth = self.width() / self.__maximum
			#windowHeight = self.height()
			#dotDiameter = min( windowWidth, windowHeight )

			## Hierdurch entspricht der neue Wert dem Punkt, auf den geklickt wurde
			#newValue = int( mousePoint.x() / dotDiameter ) + 1;

			## Dadurch kann ich aber den Wert 0 nicht erreichen.
			## Also Abfrage einbauen, damit der Wert 0 wird, wenn der Wert bereits 1 war und wieder auf 1 geklickt wird,
			#if ( oldValue == 1 and newValue == 1 ):
				#self.setValue( 0 )
			#else:
				#self.setValue( newValue )

			## Signal senden, wenn der neue Wert sich vom alten unterscheidet.
			## Dieses Signal soll nur ausgesendet werden, wenn der User den Wert ändert, nicht wenn programmtechnisch der Wert verändert wird. DafÜr existiert das signal valueChanged( int ).
			#if ( self.__value != oldValue ):
				#self.valueClicked.emit( oldValue )


	def changeEvent( self, event ):
		self.update()


	def __getValue(self):
		return self.__value

	def __setValue( self, value ):
		"""
		Ändert den aktuellen Wert des Widgets.
		"""

		if self.__value != value:
			self.__value = value
			#Debug.debug("Ändere Wert auf {}".format(value))
			self.changed.emit(value)

	value = property(__getValue, __setValue)



