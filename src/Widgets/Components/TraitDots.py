# -*- coding: utf-8 -*-

"""
# Copyright

Copyright (C) 2012 by Victor
victor@caern.de

# License

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import QPoint
from PyQt4.QtGui import QColor, QPainter, QPen

from src.Config import Config
from src.Widgets.Components.AbstractTraitDots import AbstractTraitDots
#from src.Debug import Debug




class TraitDots(AbstractTraitDots):
	"""
	@brief Diese Punkte können neben dem Wert auch den Bonuswert einer Eigenschaft anzeigen, indem ein farblich anders gekennzeichneter Punkt den Bonuswert markiert.
	"""

	bonusValueChanged = Signal(int)
	totalvalueChanged = Signal(int)


	def __init__(self, parent=None):
		super(TraitDots, self).__init__(parent)

		self.__bonusValue = 0


	# Das automatisch ausgelöste paintEvent, das das Widget bei jeder Fensterveränderung neu zeichnet.
	def paintEvent( self, event ):
		# Wenn das Widget disabled ist, muß ich den Alphakanal meiner Farben verändern.
		frameWidth = 16
		dotCenter = QPoint( 0, 0 )
		shiftCenter = dotCenter
		
		# Damit der Rahmen nicht irgendwie abgeschnitten wird, muß der Kreis entsprechend kleiner sein.
		dotRadius = 100
		framePen = QPen()
		framePen.setWidth(frameWidth )
		framePen.setColor( self._colorFrame )

		dotDiameter = 2 * dotRadius + frameWidth

		painter = QPainter( self )

		windowWidth = self.width() // self.maximum
		windowHeight = float( self.height() )
		side = min( windowWidth, windowHeight )

		painter.setRenderHint( QPainter.Antialiasing )

		if ( not self.isEnabled() ):
			painter.setOpacity( .5 )

		painter.translate( side / 2, self.height() / 2 )

		painter.scale( side / dotDiameter, side / dotDiameter )

		painter.setPen( framePen )
		painter.setBrush( self._colorFull )

		painter.save()

		for i in range(self.value):
			shiftCenter = dotCenter + QPoint( 0 + dotDiameter * i, 0 )
			painter.drawEllipse( shiftCenter, dotRadius, dotRadius )
	## 		if (v_forbiddenValues.contains(i+1)){
	## 			painter.drawEllipse(shiftCenter, dotRadius/2, dotRadius/2);

		painter.restore()

		painter.setBrush( QColor(Config.bonusColor) )

		painter.save()

		for i in range(self.value, self.value + self.__bonusValue):
			shiftCenter = dotCenter + QPoint( 0 + dotDiameter * i, 0 )
			painter.drawEllipse( shiftCenter, dotRadius, dotRadius )

		painter.restore()

		painter.setBrush( self._colorEmpty )

		painter.save()

		for i in range(self.value + self.__bonusValue, self.maximum):
			shiftCenter = dotCenter + QPoint( 0 + dotDiameter * i, 0 )
			painter.drawEllipse( shiftCenter, dotRadius, dotRadius )

			j = i+1
			if ( j in self.forbiddenValues ):
				dotRadiusHalf = dotRadius / 2
				painter.drawLine( shiftCenter.x() - dotRadiusHalf, shiftCenter.y() - dotRadiusHalf, shiftCenter.x() + dotRadiusHalf, shiftCenter.y() + dotRadiusHalf )
				painter.drawLine( shiftCenter.x() - dotRadiusHalf, shiftCenter.y() + dotRadiusHalf, shiftCenter.x() + dotRadiusHalf, shiftCenter.y() - dotRadiusHalf )

		painter.restore()


	def __getBonusValue(self):
		"""
		Bonus-Wert, der manchen Eigenschaften zugesprochen wird.
		"""

		return self.__bonusValue

	def setBonusValue(self, value):
		if self.__bonusValue != value:
			self.__bonusValue = value
			self.bonusValueChanged.emit(value)
			self.totalvalueChanged.emit(self.value + value)

	bonusValue = property(__getBonusValue, setBonusValue)

