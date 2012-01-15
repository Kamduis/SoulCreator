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

from PySide.QtCore import Qt, Signal
from PySide.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QComboBox

from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
from src.Widgets.Components.Dot import Dot
from src.Debug import Debug




class MoralityWidget(QWidget):
	"""
	@brief Dieses Widget stellt die Moral-Tabelle dar.

	Diese Tabelle zeigt die aktuelle Moralstufe an und bietet Platz für das Eintragen von Geistesstörungen.

	\todo wenn die Spezies verändert wird, müssen auch die Verfügbaren Geistesstörungen verändert werden.

	\todo Ich bin mit den Geistesstörungen noch nicht gänzlich zufrieden. Es besteht die Gefahr, daß einzelne Geistesstörungen immer und immer wieder zu dem Charkater hinzugefügt werden und dementsprechend das Programm und den gespeicherten Charakter aufblähen können.
	"""


	valueChanged = Signal(int)


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.__character = character
		self.__storage = template

		self.__value = 0

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__layoutHeading = QHBoxLayout()
		self.__layout.addLayout(self.__layoutHeading)

		self.__labelHeading = QLabel("Test")
		self.__labelHeading.setAlignment(Qt.AlignHCenter)

		self.__layoutHeading.addStretch()
		self.__layoutHeading.addWidget(self.__labelHeading)
		self.__layoutHeading.addStretch()

		self.__layoutTab = QGridLayout()
		# Nur die Spalte mit den GEistesstörungen soll sich strecken dürfen.
		self.__layoutTab.setColumnStretch(1, 1)
		self.__layout.addLayout(self.__layoutTab)

		self.__dotList = {}
		self.__derangementBoxList = {}

		for i in xrange(Config.moralityTraitMax):
			label = QLabel("{}".format(Config.moralityTraitMax - i))
			label.setAlignment(Qt.AlignRight)
			self.__layoutTab.addWidget(label, i, 0)

			dot = Dot()
			# Den Punkt zu einer Liste hinzufügen, um später zu sehen, welcher Punkt den Wert änderte.
			self.__dotList[Config.moralityTraitMax - i] = dot
			self.__layoutTab.addWidget(dot, i, 2)

			if i >= Config.moralityTraitMax - Config.derangementMoralityTraitMax:
				box = QComboBox()
				self.__derangementBoxList[Config.moralityTraitMax - i] = box
				self.__layoutTab.addWidget(box, i, 1)

				box.currentIndexChanged[str].connect(self.uniqifyDerangements)
				box.currentIndexChanged[str].connect(self.saveDerangements)
				self.__character.derangementChanged.connect(self.updateDerangementBoxes)

			dot.clicked.connect(self.__calcValue)

		self.__character.speciesChanged.connect(self.setMoralityName)
		self.__character.moralityChanged.connect(self.setValue)
		self.valueChanged.connect(self.__character.setMorality)
		self.valueChanged.connect(self.enableDerangementBox)

		#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( updateDerangements( cv_Species::SpeciesFlag ) ) );
		#connect( character, SIGNAL( moralityChanged( int ) ), this, SLOT( setValue( int ) ) );
		#connect( this, SIGNAL( valueChanged( int ) ), character, SLOT( setMorality( int ) ) );
		#connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( drawValue( int ) ) );
		#connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( disableDerangements( int ) ) );

		#setValue( Config::moralityTraitDefaultValue );


	def __getValue(self):
		return self.__value

	def setValue( self, value ):
		if ( self.__value != value ):
			self.__value = value
			self.__drawValue(value)
			#Debug.debug(value)
			self.valueChanged.emit( value )

	value = property(__getValue, setValue)


	def __calcValue(self, value):
		"""
		Berechnet aus dem angeklickten Punkt, welchen Wert die Moral jetzt hat.
		"""
		
		#Debug.debug(self.__dotList)
		# Ist der Wert True, suche ich nach dem höchsten wahren Punkt und mache alle kleineren auch wahr.
		# Ist der Wert False, suche ich nach dem niedrigesten False punkt, und mache die höheren alle False.
		if value:
			dotsTrue = []
			for i in xrange(1, self.__layoutTab.rowCount()+1):
				if self.__dotList[i].value:
					dotsTrue.append(i)
			maxValue = max(dotsTrue)
			#Debug.debug(dotsTrue)
			for i in xrange(1, maxValue):
				self.__dotList[i].value = True
				#Debug.debug("{}: {} (Maximalwert {})".format(i, self.__dotList[i].value, maxValue))
			self.value = maxValue
		else:
			dotsFalse = []
			for i in xrange(1, self.__layoutTab.rowCount()+1):
				if not self.__dotList[i].value:
					dotsFalse.append(i)
			minValue = min(dotsFalse)
			if minValue == self.value and minValue != 1:
				self.__dotList[minValue].value = True
			else:
				for i in xrange(minValue+1, self.__layoutTab.rowCount()+1):
					self.__dotList[i].value = False
					#Debug.debug("{}: {} (Maximalwert {})".format(i, self.__dotList[i].value, minValue))
				# Intuitiverweise will man die Moral auf den Wert setzen, auf den man klickt. Aber das gilt nicht, wenn man auf den untersten Punkt klickt.
				if minValue == 1:
					self.__dotList[minValue].value = False
					self.value = 0
				else:
					self.value = minValue



	def __drawValue( self, value ):
		"""
		Ändert sich der Wert des Widgets, wird hierüber die passende Anzahl an Punkten schwarz ausgemalt.
		"""

		if value > 0:
			for i in xrange(value, len(self.__dotList)+1):
				self.__dotList[i].value = False
			for i in xrange(1, value+1):
				self.__dotList[i].value = True
		else:
			for i in xrange(1, len(self.__dotList)+1):
				self.__dotList[i].value = False


	def setMoralityName( self, species ):
		"""
		Setzt die Überschrift dieses Widgets auf einen neuen Namen. Der name hängt von der Spezies ab.
		"""

		self.__labelHeading.setText("<b>{}</b>".format(self.__storage.moralityName(species)))


	def enableDerangementBox( self, value ):
		"""
		Sorgt dafür, daß die Combobox für die Geistesstörung neben einem leeren Moralpunkt aktiviert und mit den verfügbaren Geistesstörungen gefüllt wird.

		Alle Boxen zeigen alle Geistesstörungen an, aber wenn eine Gewählt wird, die schon anderorts gewählt wurde, wird sie dort abgewählt.
		"""

		## Milde Geistesstörungen.
		mild = self.__storage.derangements(self.__character.species)
		## An den Anfang kommt ein leerer String
		mild.insert(0, "")
		for i in range(value+1, Config.derangementMoralityTraitMax+1)[::-1]:
			#Debug.debug(i)
			self.__derangementBoxList[i].setEnabled(True)
			##Debug.debug(self.__storage.derangements())
			self.__derangementBoxList[i].addItems(mild)
		for i in xrange(1, value+1):
			self.__derangementBoxList[i].setEnabled(False)
			self.__derangementBoxList[i].clear()


	def uniqifyDerangements(self, text):
		"""
		Eine Geistesstörung darf immer nur in einer ComboBox auftauchen.

		Es werd die oberen doppelt vorkommende Geistesstörung gelöscht.
		"""

		firstOccuranceHappened = False
		for i in range(1, Config.derangementMoralityTraitMax+1):
			if self.__derangementBoxList[i].currentIndex != 0:
				if self.__derangementBoxList[i].currentText() == text and firstOccuranceHappened:
					self.__derangementBoxList[i].setCurrentIndex(0)
				elif self.__derangementBoxList[i].currentText() == text:
					firstOccuranceHappened = True


	def updateDerangementBoxes(self, moralityValue, derangement):
		"""
		Wählt in den derangementBoxen die jeweils übergebenen Geistesstörungen aus.

		\bug aus irgendeinem grund nimmt moralityValue manchmal den Wert -1 an. Weiß aber nicht, woher.
		"""

		#Debug.debug(derangement, moralityValue)

		self.__derangementBoxList[moralityValue].setCurrentIndex(self.__derangementBoxList[moralityValue].findText(derangement))


	def saveDerangements( self ):
		"""
		Speichert die gewählte Geistesstörung im Charakter.

		\todo Wenn ich weiß bei welcher Moral die Geistesstörungen platziert werden, kann ich auch beim ändern des INdex einer Geistesstörungsbox diese direkt im Charakter ändern, ohne alle löschen und neu abarbeiten zu müssen.
		"""

		derangementMapping = {}

		isDerangementPresent = False
		for i in range(1, Config.derangementMoralityTraitMax+1):
			if self.__derangementBoxList[i].currentIndex != 0:
				self.__character.setDerangement(derangement=self.__derangementBoxList[i].currentText(), moralityValue=i)


