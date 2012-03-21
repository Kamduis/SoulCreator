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
from PySide.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QMessageBox

from src.Config import Config
from src.Widgets.Components.DerangementComboBox import DerangementComboBox
from src.Widgets.Components.Dot import Dot
from src.Debug import Debug




class MoralityWidget(QWidget):
	"""
	@brief Dieses Widget stellt die Moral-Tabelle dar.

	Diese Tabelle zeigt die aktuelle Moralstufe an und bietet Platz für das Eintragen von Geistesstörungen.
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
		# Nur die Spalte mit den Geistesstörungen soll sich strecken dürfen.
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
				box = DerangementComboBox()
				self.__derangementBoxList[Config.moralityTraitMax - i] = box
				self.__layoutTab.addWidget(box, i, 1)

				box.currentIndexChanged[str].connect(self.uniqifyDerangements)
				box.derangementChanged.connect(self.checkSevereDerangement)

			dot.clicked.connect(self.__calcValue)

		self.__character.speciesChanged.connect(self.setMoralityName)
		self.__character.moralityChanged.connect(self.setValue)
		self.valueChanged.connect(self.__character.setMorality)
		self.__character.speciesChanged.connect(self.fillDerangementBoxes)
		self.valueChanged.connect(self.enableDerangementBox)
		self.__character.derangementChanged.connect(self.updateDerangementBoxes)


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


	def fillDerangementBoxes( self, species ):
		"""
		Sorgt dafür, daß die Comboboxen alle für diese Spezies verfügbaren Geistesstörungen enthalten.
		"""

		## Milde Geistesstörungen.
		mild = self.__storage.derangementList(species)
		## Ernste Geistesstörungen.
		severe = []
		for item in mild:
			severe.extend(self.__storage.derangementList(species, item))
		severe.sort()
		## An den Anfang kommt ein leerer String
		mild.insert(0, "")
		#Debug.debug(mild)
		#Debug.debug(severe)
		lostDerangements = []
		for i in range(1, Config.derangementMoralityTraitMax+1)[::-1]:
			## Speichern der alten Auswahl.
			oldSelection = self.__derangementBoxList[i].currentText()
			## Erst löschen
			self.__derangementBoxList[i].clear()
			## Dann wieder füllen
			self.__derangementBoxList[i].addItems(mild)
			self.__derangementBoxList[i].addItems(severe, severe=True)
			## Und wenn möglich, alte Auswahl wiederherstellen.
			oldIndex = self.__derangementBoxList[i].findText(oldSelection)
			if oldIndex < 0:
				lostDerangements.append(oldSelection)
			else:
				self.__derangementBoxList[i].setCurrentIndex(oldIndex)

		#Debug.debug(self.__character.isLoading)
		if lostDerangements and not self.__character.isLoading:
			derangements = ""
			infoText = ""
			if len(lostDerangements) > 1:
				derangements = ", ".join(lostDerangements[:-1])
				derangements = "{} and {}".format(derangements, lostDerangements[-1])
				infoText = self.tr( "The derangements \"{derangements}\" are not available for a {species}. The character lost these deragnements.".format(derangements=derangements, species=species) )
			else:
				derangements = "".join(lostDerangements)
				infoText = self.tr( "The derangement \"{derangements}\" is not available for a {species}. The character lost this deragnement.".format(derangements=derangements, species=species) )
			QMessageBox.information(
				self,
				self.tr( "Lost Derangement" ),
				infoText
			)


	def enableDerangementBox( self, value ):
		"""
		Sorgt dafür, daß die Combobox für die Geistesstörung neben einem leeren Moralpunkt aktiviert und mit den verfügbaren Geistesstörungen gefüllt wird.

		Alle Boxen zeigen alle Geistesstörungen an, aber wenn eine Gewählt wird, die schon anderorts gewählt wurde, wird sie dort abgewählt.
		"""

		#Debug.debug(value)

		for i in range(value+1, Config.derangementMoralityTraitMax+1)[::-1]:
			self.__derangementBoxList[i].setEnabled(True)
		for i in xrange(1, value+1):
			self.__derangementBoxList[i].setCurrentIndex(0)
			self.__derangementBoxList[i].setEnabled(False)


	def uniqifyDerangements(self, text):
		"""
		Eine Geistesstörung darf immer nur in einer ComboBox auftauchen.

		Es werd die oberen doppelt vorkommende Geistesstörung gelöscht.
		"""

		#Debug.debug(text)
		firstOccuranceHappened = False
		for i in range(1, Config.derangementMoralityTraitMax+1):
			if self.__derangementBoxList[i].currentIndex != 0:
				if self.__derangementBoxList[i].currentText() == text and firstOccuranceHappened:
					self.__derangementBoxList[i].setCurrentIndex(0)
				elif self.__derangementBoxList[i].currentText() == text:
					firstOccuranceHappened = True


	def checkSevereDerangement(self, derangement, isSevere, sender):
		"""
		Wird eine schwere Geistesstörung gewählt und ihre Milde version ist nicht gewählt, muß gewarnt werden.
		"""

		if isSevere:
			mildParent = ""
			for item in self.__storage.derangementList(self.__character.species):
				if derangement in self.__storage.derangementList(self.__character.species, item):
					mildParent = item
					break
			mildExists = False
			for i in range(1, Config.derangementMoralityTraitMax+1):
				if self.__derangementBoxList[i].currentText() == mildParent:
					mildExists = True
					break
			if not mildExists:
				#Debug.debug("Milde Verfsion exisitert nicht!")
				QMessageBox.warning(self, self.tr("Warning"), self.tr("{severe} can only be taken, if its mild version {mild} was selected at a higher morality level. Instead of {severe}, {mild} will be selected for this morality level.".format(mild=mildParent, severe=derangement)))
				#Debug.debug(sender)
				sender.setCurrentIndex(sender.findText(mildParent))
				derangement = mildParent

		## Nach der Kontrolle, kann die Geistesstörung gespeichert werden.
		for item in self.__derangementBoxList.items():
			if sender == item[1]:
				#Debug.debug(item[0], derangement)
				self.saveDerangements(moralityValue=item[0], derangement=derangement)
				break


	def saveDerangements( self, moralityValue, derangement ):
		"""
		Speichert die gewählte Geistesstörung im Charakter.
		"""

		self.__character.setDerangement(moralityValue=moralityValue, derangement=derangement)


	def updateDerangementBoxes(self, moralityValue, derangement):
		"""
		Wählt in den derangementBoxen die jeweils übergebenen Geistesstörungen aus.
		"""

		#Debug.debug(derangement, moralityValue)

		self.__derangementBoxList[moralityValue].setCurrentIndex(self.__derangementBoxList[moralityValue].findText(derangement))


