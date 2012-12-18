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
from PyQt4.QtCore import QObject

import src.Calc.Calc as Calc
import src.Config as Config
#import src.Debug as Debug




class CalcAdvantages(QObject):
	"""
	\brief Diese Klasse führt die berechnung der abgeleiteten Eigenschaften durch.

	Die hier deklarierten Berechnungsfunktionen werden zwar bei der Änderung jeder Eigenschaft aufgerufen, aber berechnen die Werte nur, wenn eine Eigenschaft verändert wurde, welche Einfluß auf das Ergebnis nimmt. Sie geben allerdings immer das Ergebnis der berechnung aus. Entweder den neuen Wert, oder den alten Wert, der in dieser Klasse gespeichert wird.

	\todo Diese Klasse so umbennenen, um auszudrücken, daß hier die Werte direkt vom gespeicherten Charakter verwendet werden.
	"""


	sizeChanged = Signal(int)
	initiativeChanged = Signal(int)
	speedChanged = Signal(int)
	defenseChanged = Signal(int)
	healthChanged = Signal(int)
	willpowerChanged = Signal(int)


	def __init__(self, character, parent=None):
		super(CalcAdvantages, self).__init__(parent)

		self.__character = character

		self.__size       = 0
		self.__initiative = 0
		self.__speed      = 0
		self.__defense    = 0
		self.__health     = 0
		self.__willpower  = 0

		self.sizeChanged.connect(self.calcHealth)
		self.sizeChanged.connect(self.calcDefense)


	def calc_size(self):
		"""
		Berechnung der Größe des Charakters.
		"""

		is_large = self.__character.traits["Merit"]["Physical"]["Giant"].totalvalue > 0
		is_small = self.__character.traits["Flaw"]["Physical"]["Dwarf"].totalvalue > 0
		if self.__character.age < Config.AGE_ADULT:
			is_large = self.__character.traits["Merit"]["Physical"]["GiantKid"].totalvalue > 0
			is_small = self.__character.traits["Merit"]["Physical"]["Tiny"].totalvalue > 0

		result = Calc.calc_size( self.__character.age, is_giant=is_large, is_small=is_small )

		if ( self.__size != result ):
			self.__size = result
			self.sizeChanged.emit( result )

		return self.__size


	def calcInitiative(self):
		"""
		Berechnung der Initiative des Charakters.

		\todo Bislang nur von Dexterity, Composure und Fast Reflexes abhängig. Möglicherweise vorhandene Übernatürliche Eigenschaften werden nicht berücksichtigt.
		"""

		result = Calc.calc_initiative(
			self.__character.traits["Attribute"]["Physical"]["Dexterity"].totalvalue,
			self.__character.traits["Attribute"]["Social"]["Composure"].totalvalue,
			self.__character.traits["Merit"]["Physical"]["Fast Reflexes"].totalvalue,
		)

		if ( self.__initiative != result ):
			self.__initiative = result
			self.initiativeChanged.emit( result )

		return self.__initiative


	def calcSpeed(self):
		"""
		Berechnung der Geschwindigkeit des Charakters.

		\todo Bislang nur von Strength und Dexterity abhängig. Möglicherweise vorhandene Übernatürliche Eigenschaften werden nicht berücksichtigt.
		"""

		result = Calc.calc_speed(
			self.__character.traits["Attribute"]["Physical"]["Strength"].totalvalue,
			self.__character.traits["Attribute"]["Physical"]["Dexterity"].totalvalue,
			self.__character.traits["Merit"]["Physical"]["Fleet of Foot"].totalvalue,
		)

		if ( self.__speed != result ):
			self.__speed = result
			self.speedChanged.emit( result )

		return self.__speed


	def calcDefense(self):
		"""
		Berechnung der Defense

		\note Bei Kindern wird pro Punkt Size unter 5 ein weiterer Punkt zur Defense hinzugezählt.

		\todo Bislang nicht von der Spezies abhängig: Tiere sollten stets das größere von Dex und Wits als Defense haben.
		"""

		result = Calc.calc_defense(
			self.__character.traits["Attribute"]["Mental"]["Wits"].totalvalue,
			self.__character.traits["Attribute"]["Physical"]["Dexterity"].totalvalue,
			age=self.__character.age,
			size=self.__size,
		)

		if ( self.__defense != result ):
			self.__defense = result
			self.defenseChanged.emit( result )

		return self.__defense


	def calcHealth(self):
		"""
		Berechnung der Gesundheit.
		"""

		## Bevor ich die Gesundheit ausrechnen kann, muß erst die Größe feststehen.
		size = self.calc_size()

		result = Calc.calc_health(
			self.__character.traits["Attribute"]["Physical"]["Stamina"].totalvalue,
			size,
		)

		if ( self.__health != result ):
			self.__health = result
			self.healthChanged.emit( result )

		return self.__health


	def calcWillpower(self):
		"""
		Berechnung der Willenskraft.
		"""

		result = Calc.calc_willpower(
			self.__character.traits["Attribute"]["Mental"]["Resolve"].totalvalue,
			self.__character.traits["Attribute"]["Social"]["Composure"].totalvalue,
		)

		if ( self.__willpower != result ):
			self.__willpower = result
			self.willpowerChanged.emit( result )

		return self.__willpower
