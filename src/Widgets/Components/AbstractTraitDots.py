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

from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import QPoint
from PyQt4.QtGui import QWidget, QColor, QSizePolicy, QPen, QPainter

#from src.Config import Config
#from src.Widgets.TraitLine import TraitLine
#from src.Debug import Debug




class AbstractTraitDots(QWidget):
	"""
	@brief Eine Darstellung von Werten in Form ausgefüllter Punkte.
 
	Ein einfacher ganzzahliger Wert wirden in Form ausgefüllter Punkte dargestellt. Die bis zum Maximalwert übrigen Punkte sind nicht ausgefüllt.
 
	Wird das Widget disabled, wird der Alphakanal genutzt, um die Punkte teilweise durchsichtig zu machen und sie so grau erscheinen zu lassen.
 
	Es besteht die Möglichkeit aus der Menge an Werten zwischen \ref minimum und \ref maximum einige zu verbieten.
	"""

	activated = Signal()
	valueChanged = Signal(int)
	minimumChanged = Signal(int)
	maximumChanged = Signal(int)
	valueClicked = Signal(int)


	def __init__(self, parent=None):
		super(AbstractTraitDots, self).__init__(parent)

		self.__minimum = 0
		self.__maximum = 5
		self.__readOnly = False
		self.__value = 0


		# Es gibt anfangs keine verbotenen Werte, also nur eine leere Liste erstellen
		self.__forbiddenValues = []

		# Standardwerte setzen
		self.setMinimum( 0)
		self.setMaximum( 5)

		# setValue() muß nach dem Füllen der MyAllowedValues-Liste aufgurefen werden, damit die List Einträge besitzt, bevort sie abgefragt wird.
		self.setValue(0)

		# Widget darf nur proportional in seiner Größe verändert werden?
		# Minimalgröße festlegen
		self.__minimumSizeY = 8
		minimumSizeX = self.__minimumSizeY * self.__maximum
		self.setMinimumSize( minimumSizeX, self.__minimumSizeY)
		self.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )

		# Setze Standardfarbe weiß
		self._colorEmpty = QColor( 255, 255, 255 )
		self._colorFull = QColor( 0, 0, 0 )
		self._colorFrame = QColor( 0, 0, 0 )

		self.maximumChanged.connect(self.resetMinimumSize)


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

		windowWidth = self.width() // self.__maximum
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

		for i in xrange(self.__value):
			shiftCenter = dotCenter + QPoint( 0 + dotDiameter * i, 0 )
			painter.drawEllipse( shiftCenter, dotRadius, dotRadius )
	## 		if (v_forbiddenValues.contains(i+1)){
	## 			painter.drawEllipse(shiftCenter, dotRadius/2, dotRadius/2);

		painter.restore()

		painter.setBrush( self._colorEmpty )

		painter.save()

		for i in xrange(self.__value, self.__maximum):
			shiftCenter = dotCenter + QPoint( 0 + dotDiameter * i, 0 )
			painter.drawEllipse( shiftCenter, dotRadius, dotRadius )

			j = i+1
			if ( j in self.__forbiddenValues ):
				dotRadiusHalf = dotRadius / 2
				painter.drawLine( shiftCenter.x() - dotRadiusHalf, shiftCenter.y() - dotRadiusHalf, shiftCenter.x() + dotRadiusHalf, shiftCenter.y() + dotRadiusHalf )
				painter.drawLine( shiftCenter.x() - dotRadiusHalf, shiftCenter.y() + dotRadiusHalf, shiftCenter.x() + dotRadiusHalf, shiftCenter.y() - dotRadiusHalf )


		## 	for (int i = 0; i < v_forbiddenValues.count(); ++i) {
		## 		shiftCenter = dotCenter + QPoint( 0 + dotDiameter * (v_forbiddenValues.at(i) - 1), 0 );
		## ## 		painter.drawLine(shiftCenter.x()-dotDiameter/2, shiftCenter.y()-dotDiameter/2, shiftCenter.x()+dotDiameter/2, shiftCenter.y()+dotDiameter/2);
		## ## 		painter.drawLine(shiftCenter.x()+dotDiameter/2, shiftCenter.y()-dotDiameter/2, shiftCenter.x()-dotDiameter/2, shiftCenter.y()+dotDiameter/2);
		## 		painter.drawEllipse(shiftCenter, dotRadius/2, dotRadius/2);
		## 	}

		painter.restore()


	# Anklicken
	def mousePressEvent( self, event ):
		if ( not self.__readOnly ):
			# Den ursprÜnglichen Wert speichern
			oldValue = self.__value

			# Die Position des Mauszeigers beim Klicken wird errechnet. Dabei soll die Mitte der linken Seite der Position (0, 0) entsprechen.
			mousePoint = event.pos() - self.rect().bottomLeft() - QPoint( 0, self.rect().height() / 2 )

			# Welche Breite haben die Punkte? Das bestimme ich je nachdem, ob das Fenster zu breit ist, sie alle aufzunehmen, oder zu hoch, aus Höhe bzw. Breite.
			windowWidth = self.width() / self.__maximum
			windowHeight = self.height()
			dotDiameter = min( windowWidth, windowHeight )

			# Hierdurch entspricht der neue Wert dem Punkt, auf den geklickt wurde
			newValue = int( mousePoint.x() / dotDiameter ) + 1;

			# Dadurch kann ich aber den Wert 0 nicht erreichen.
			# Also Abfrage einbauen, damit der Wert 0 wird, wenn der Wert bereits 1 war und wieder auf 1 geklickt wird,
			if ( oldValue == 1 and newValue == 1 ):
				self.setValue( 0 )
			else:
				self.setValue( newValue )

			# Signal senden, wenn der neue Wert sich vom alten unterscheidet.
			# Dieses Signal soll nur ausgesendet werden, wenn der User den Wert ändert, nicht wenn programmtechnisch der Wert verändert wird. DafÜr existiert das signal valueChanged( int ).
			if ( self.__value != oldValue ):
				self.valueClicked.emit( oldValue )


	def changeEvent( self, event ):
		self.update()


	def readOnly(self):
		return self.__readOnly

	def setReadOnly( self, sw ):
		"""
		Bestimmt, ob das Widget vom Benutzer direkt verändert werden kann.
		"""
		
		if ( self.__readOnly != sw ):
			self.__readOnly = sw


	def __getValue(self):
		return self.__value

	def setValue( self, value ):
		"""
		Speichert den aktuellen Wert des Widgets.

		Dieser Wert stellt die Zahl der ausgefüllten Punkte dar. Die Gesamtzahl der dargestellten Punkte ist in \ref maximum() gespeichert.

		Soll value auf einen Wert gesetzt werden, der über dem Maximum liegt, wird er nur auf das Maximum gesetzt, soll er unter das Minimum gesetzt werden, wird er auf Minimum gesetzt.

		Soll value auf einen verbotenen Wert gesetzt werden, wird er auf den nächstkleineren, erlaubten Wert gesetzt.
		"""
		
		# Negative Werte werden nicht Übernommen
		if ( value >= 0 ):
			# Reduziere den zu setzenden Wert solange um 1, bis er unter dem Maximum und nicht in der v_forbiddenList liegt.
			# Natürlich wird die Schleife abgebrochen, sollte dadurch der Wert auf 0 sinken.
			if ( value > self.__maximum ):
				value = self.__maximum

			while ( value in self.__forbiddenValues and value > 0 ):
				value -= 1

			# sollte der reduzierte Wert irgendwie unter den Minimalwert fallen, muß er auf eben diesen gesetzt werden, selbst wenn der Minimalwert aufgrund eines Fehlers nicht erlaubt sein sollte.
			if ( value < self.__minimum ):
				value = self.__minimum

			# Signal aussenden, wenn der Wert /verändert/ wurde
			if ( self.__value != value ):
				self.__value = value

				#Debug.debug("Sende Signal valueChanged")
				self.valueChanged.emit( value )

				# neu zeichnen
				self.update()

			# Signal aussenden

	value = property(__getValue, setValue)


	def __getMinimum(self):
		return self.__minimum

	def setMinimum( self, value ):
		"""
		Legt fest, wieviele Punkte mindestens ausgefüllt sein müssen.
		"""
		
		# Negative Werte werden nicht Übernommen
		if ( value >= 0 ):
			self.__minimum = value

			# Ist das neue Minimum größer als das Maximum wird letzteres verändert, um dieses mindestens so groß wie das Minimum zu behalten.
			if ( value > self.__maximum ):
				self.setMaximum( value)

			# Entferne das neue Minimum aus self.__forbiddenList.
			# Diese Liste kann (rein theoretisch) mehrere identische Werte enthalten, also erst alle Duplikate entfernen, dann den verbleibenden Wert.
			if value in self.__forbiddenValues:
				self.__forbiddenValues = list(set(self.__forbiddenValues))
				self.__forbiddenValues.remove(value)

			# Ist das neue Minimum größer als der aktuell angezeigte Wert, muß dieser auf das Minimum gesetzt werden.
			if ( value > self.__value ):
				self.setValue(value)

	minimum = property(__getMinimum, setMinimum)


	def __getMaximum(self):
		return self.__maximum

	def setMaximum( self, value ):
		"""
		Der Maximalwert bestimmt, wieviele Punkte insgesamt angezeigt werden.
		"""
		
		# Negative Werte werden nicht Übernommen
		if ( value >= 0 ):
			# Signal aussenden, wenn der Wert /verändert/ wurde
			if ( value != self.__maximum ):
				# Wert verändern
				self.__maximum = value
				# Signal
				self.maximumChanged.emit( value )
				## neu zeichnen
				self.update()

			# Ist das neue Maximum kleiner als das Minimum wird letzteres verändert, um dieses mindestens so groß wie das Maximum zu behalten.
			if ( value < self.__minimum):
				self.setMinimum( value)

			# Entferne das neue Maximum aus self.__forbiddenList
			# Diese Liste kann (rein theoretisch) mehrere identische Werte enthalten, also das ganze Über eine while-Schleife tun.
			if value in self.__forbiddenValues:
				self.__forbiddenValues = list(set(self.__forbiddenValues))
				self.__forbiddenValues.remove(value)

			## Ist das neue Maximum kleiner als der aktuell angezeigte Wert, muß dieser auf das Maximum gesetzt werden.
			if ( value < self.__value ):
				self.setValue(value)

	maximum = property(__getMaximum, setMaximum)


	# Ändert sich der Maximalwert, ändert sich auch die minimale Breite, die das Widget in Anspruch nicmmt
	def resetMinimumSize( self, sizeX ):
		self.setMinimumWidth( sizeX * self.__minimumSizeY)


	def setForbiddenValues( self, values ):
		"""
		Über diese Funktion wird eine Liste der verbotenen Werte gesetzt.

		Beachtet noch nicht, daß ein aktueller Wert nach einer veränderung der verbotenen Werte erhalten bleibt, obwohl er inzsichen verboten ist.
		"""
		
		self.__forbiddenValues = values

		# Das aktuelle Minimum suchen und eventuell entfernen. Das Minimum muß immer erlaubt sein.
		if self.__minimum in self.__forbiddenValues:
			self.__forbiddenValues.remove(self.__minimum)


	def setAllowedValues( self, values ):
		"""
		Über diese Funktion wird eine Liste der erlaubten Werte gesetzt.
		
		Da es manchmal einfacher ist, erlaubte Werte einzugeben, müssen diese entsprechend Übersetzt werden, ehe sie in die self.__forbiddenList eingesetzt werden.
		"""
		
		# Neue List erstellen und mit den Werten aus dem Argument fÜllen. Aber da Werte kleiner 0 nie erlaubt sind, werden diese garnicht erst übernommen.
		tmpList = values

		for item in tmpList:
			if item < 0:
				tmpList.remove(item)

		# Neue Liste sortieren
		tmpList.sort()

		# Das neue Minimum entspricht dem Wert an Index 0 der Liste
		self.setMinimum( tmpList[0] )

		# Das neue Maximum bleibt unverändert, wenn es größer ist als der größte erlaubte Wert. Es werden alle maximal möglichen Punkte angezeigt, aber sie können eben nicht alle ausgefÜllt werden. Ist es allersdins kleiner wird es auf den größten erlaubten Wert gesetzt.
		if tmpList[-1] > self.__maximum:
			self.setMaximum( tmpList[-1] )

		# Eine Liste beginnt beim Minimalwert und reicht bis zum Maximalwert. Es werden alle Werte verboten, die nicht im Argumetn genannt werden.
		self.__forbiddenValues = range(self.__minimum, self.__maximum + 1)

		for item in tmpList:
			if item in self.__forbiddenValues:
				self.__forbiddenValues.remove(item)


	def addAllowedValue( self, value ):
		"""
		Fügt einen erlaubten Wert hinzu.
		"""
		
		# value aus self.__forbiddenList entfernen.
		if ( value in self.__forbiddenValues ):
			self.__forbiddenValues.remove( value )


	def addForbiddenValue( self, value ):
		"""
		Fügt einen verbotenen Wert hinzu.
		"""

		if ( value in self.__forbiddenValues ):
			self.__forbiddenValues.append( value )

			# Liste wieder sortieren
			self.__forbiddenValues.sort()

	@property
	def forbiddenValues(self):
		return self.__forbiddenValues

