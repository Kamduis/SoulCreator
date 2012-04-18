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

import math

from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import QRect
from PyQt4.QtGui import QWidget, QPainter, QPen, QColor

#from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
#from src.Widgets.Components.CharaTrait import CharaTrait
#from src.Debug import Debug




class Squares(QWidget):
	"""
	@brief Darstellung von ankreuzbaren Quadraten.

	Ein einfacher ganzzahliger Wert wirden in Form angekreuzter Quadrate dargestellt. Die bis zum Maximalwert übrigen Quadrate sind nicht ausgefüllt.

	Wird das Widget disabled, wird der Alphakanal genutzt, um die Quadrate teilweise durchsichtig zu machen und sie so grau erscheinen zu lassen.
	"""


	valueChanged = Signal(int)
	maximumChanged = Signal(int)
	minimumChanged = Signal(int)
	columnMaxChanged = Signal(int)
	clicked = Signal(int)


	def __init__(self, parent=None):
		super(Squares, self).__init__(parent)

		#self.__character = character
		#self.__storage = template

		self.__minimum = 0
		self.__maximum = 5
		self.__columnMax = 10
		self.__readOnly = False
		self.__value = 0

	#// Standardwerte setzen
	#setMinimum( 0 );
	#setMaximum( 10 );
	#setValue( 0 );

		# Widget darf nur proportional in seiner Größe verändert werden?
		# Minimalgröße festlegen
		self.__minimumSizeY = 10
		self.resetMinimumSize()
		#self.setMinimumSize(50, 10);
		#self.setSizePolicy( QSizePolicy.MinimumExpanding, QSizePolicy.Preferred )

		# Setze Standardfarbe weiß
		self.__colorEmpty = QColor( 255, 255, 255 )
		self.__colorFrame = QColor( 0, 0, 0 )

		self.maximumChanged.connect(self.resetMinimumSize)
		self.columnMaxChanged.connect(self.resetMinimumSize)


	def paintEvent( self, event ):
		"""
		Das automatisch ausgelöste paintEvent, das das Widget bei jeder Fensterveränderung neu zeichnet.
		"""

		if self.__maximum > 0:
			frameWidth = 1
			separatorWidth = 1

			# Damit der Rahmen nicht irgendwie abgeschnitten wird, muß das Quadrat entsprechend kleiner sein.
			squareSideLength = 10
			framePen = QPen( frameWidth )
			framePen.setColor( self.__colorFrame )

			squareSideLengthPlus = squareSideLength + 2 * frameWidth

			painter = QPainter( self )

			windowWidth = self.width() / min( self.__maximum, self.__columnMax )
			windowHeight = self.__maximum / self.__columnMax
			windowHeight = math.ceil( windowHeight )
			windowHeight = self.height() / windowHeight
			side = min( windowWidth, windowHeight )

			painter.setRenderHint( QPainter.Antialiasing )

			# Wenn das Widget disabled ist, muß ich den Alphakanal meiner Farben verändern.
			if ( not self.isEnabled() ):
				painter.setOpacity( .5 )

			#painter.translate( float( windowWidth ), float( windowHeight ) )

			painter.scale( side / squareSideLengthPlus, side / squareSideLengthPlus )
			painter.setPen( framePen )
			painter.setBrush( self.__colorEmpty )

			painter.save()

			squareColumnIter = 0
			squareLineIter = 0
			squareCount = 0
			for squareCount in xrange (self.__maximum):
				square = QRect(
					( squareSideLength + separatorWidth ) * squareColumnIter + frameWidth * ( squareColumnIter + 1 ),
					( squareSideLength + separatorWidth ) * squareLineIter + frameWidth * ( squareLineIter + 1 ), squareSideLength, squareSideLength
				)
				painter.drawRect( square )

				# Wir zeichnen die ausgekreuzten Quadrate
				if (self.__value > (self.__columnMax * squareLineIter + squareColumnIter)):
					painter.drawLine(square.bottomLeft(), square.topRight())
					painter.drawLine(square.topLeft(), square.bottomRight())

				squareColumnIter += 1

				if ( squareColumnIter >= self.__columnMax ):
					squareColumnIter = 0
					squareLineIter += 1

			painter.restore()


	def mousePressEvent( self, event ):
		if ( not self.__readOnly and self.__maximum > 0 ):
			# Den ursprÜnglichen Wert speichern
			oldValue = self.__value

			# Die Position des Mauszeigers beim Klicken wird errechnet. Dabei soll die Mitte der linken Seite der Position (0, 0) entsprechen.
	#// 		QPointF mousePoint = event.pos() - rect().bottomLeft() - QPoint( 0, rect().height() / 2 );
			mousePoint = event.pos() - self.rect().topLeft()

			# Größe der Quadrate
			squareSide = self.width() / min( self.__maximum, self.__columnMax ) 

			# Hierdurch entspricht der neue Wert dem Punkt, auf den geklickt wurde
			value = int( mousePoint.x() / squareSide ) + 1;
			value += int( mousePoint.y() / squareSide ) * self.__columnMax

			# Dadurch kann ich aber den Wert 0 nicht erreichen.
			# Also Abfrage einbauen, damit der Wert 0 wird, wenn der Wert bereits 1 war und wieder auf 1 geklickt wird.
			if ( oldValue == 1 and value == 1 ):
				self.value = 0
			else:
				self.value = value

			# Signal senden, wenn der neue Wert sich vom alten unterscheidet.
			# Dieses Signal soll nur ausgesendet werden, wenn der User den Wert ändert, nicht wenn programmtechnisch der Wert verändert wird. Dafür existiert das signal valueChanged( int ).
			if ( self.__value != oldValue ):
				self.clicked.emit( self.__value )


	def changeEvent( self, event ):
		self.update()


	def __getReadOnly(self):
		return self.__readOnly

	def __setReadOnly( self, sw ):
		if ( self.__readOnly != sw ):
			self.__readOnly = sw

	readOnly = property(__getReadOnly, __setReadOnly)


	def __getValue(self):
		return self.__value

	def __setValue( self, value ):
		# Negative Werte werden nicht Übernommen
		if ( value >= 0 ):
			if ( value > self.__maximum ):
				value = self.__maximum
			elif ( value < self.__minimum):
				value = self.__minimum

			# Signal aussenden, wenn der Wert /verändert/ wurde
			if ( self.__value != value ):
				self.__value = value

				self.valueChanged.emit( value )

				# neu zeichnen
				self.update()

			#emit activated( newValue )

	value = property(__getValue, __setValue)


	def __getMaximum(self):
		return self.__maximum

	def __setMaximum( self, value ):
		# Negative Werte werden nicht Übernommen
		if ( value >= 0 ):
			# Signal aussenden, wenn der Wert \emph{verändert} wurde.
			if ( self.__maximum != value ):
				self.__maximum = value
				self.maximumChanged.emit( value )
				# neu zeichnen
				self.update()

			# Ist das neue Maximum kleiner als das Minimum wird letzteres verändert, um dieses mindestens so groß wie das Maximum zu behalten.
			if ( value < self.__minimum):
				self.setMinimum( value )

			# Ist das neue Maximum kleiner als der aktuell angezeigte Wert, muß dieser auf das Maximum gesetzt werden.
			if ( value < self.__value ):
				self.value = value

	maximum = property(__getMaximum, __setMaximum)

	def __getMinimum(self):
		return self.__minimum

	def __setMinimum( self, value ):
		# Negative Werte werden nicht Übernommen
		if ( value >= 0 ):
			# Signal aussenden, wenn der Wert \emph{verändert} wurde.
			if ( self.__minimum != value ):
				self.__minimum = value
				self.minimumChanged.emit( value )
				# neu zeichnen
				self.update()

			# Ist das neue Minimum größer als das Maximum wird letzteres verändert, um dieses mindestens so groß wie das Minimum zu behalten.
			if ( value > self.__maximum ):
				self.setMaximum( value )

			# Ist das neue Minimum größer als der aktuell angezeigte Wert, muß dieser auf das Minimum gesetzt werden.
			if ( value > self.__value ):
				self.value = value

	minimum = property(__getMinimum, __setMinimum)
	
	def __getColumnMax(self):
		return self.__columnMax

	def __setColumnMax( self, value ):
		if ( self.__columnMax != value ):
			if ( value > 1 ):
				self.__columnMax = value
			else:
				self.__columnMax = 1

			self.columnMaxChanged.emit( value )

	columnMax = property(__getColumnMax, __setColumnMax)


#QColor Squares::colorEmpty() const {
	#return v_colorEmpty;
#}

#void Squares::setColorEmpty( const QColor & color ) {
	#v_colorEmpty = color;

	#// Neu zeichnen
	#update();
#}

#QColor Squares::colorFrame() const {
	#return v_colorFrame;
#}

#void Squares::setColorFrame( const QColor & color ) {
	#v_colorFrame
	#= color;

	#// Neu zeichnen
	#update();
#}


	def resetMinimumSize(self):
		"""
		Ändert sich der Maximalwert, ändert sich auch die minimale Breite, die das Widget in Anspruch nicmmt
		"""

		countX = min( self.__maximum, self.__columnMax )
		self.setMinimumWidth( countX * self.__minimumSizeY )

		countYdouble = self.__maximum / self.__columnMax
		countYdouble = math.ceil( countYdouble )
		countY = int( countYdouble )
		self.setMinimumHeight( self.__minimumSizeY * countY )



