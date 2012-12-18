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
#from PyQt4.QtGui import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QButtonGroup

import src.Calc.Calc as Calc
import src.Config as Config
#from src import Error
#from ReadXml import ReadXml
#from src.Widgets.Components.CharaTrait import CharaTrait
#import src.Debug as Debug




class CalcAdvantages(QObject):
	"""
	\brief Diese Klasse führt die berechnung der abgeleiteten Eigenschaften durch.

	Die hier deklarierten Berechnungsfunktionen werden zwar bei der Änderung jeder Eigenschaft aufgerufen, aber berechnen die Werte nur, wenn eine Eigenschaft verändert wurde, welche Einfluß auf das Ergebnis nimmt. Sie geben allerdings immer das Ergebnis der berechnung aus. Entweder den neuen Wert, oder den alten Wert, der in dieser Klasse gespeichert wird.

	\todo Die eigentlichen Berechnungen in Calc durchführen und diese Klasse umbennenen, um auszudrücken, daß hier die Werte direkt vom gespeicherten Charakter verwendet werden.
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

		self.__size = 0
		self.__initiative = 0
		self.__speed = 0
		self.__defense = 0
		self.__health = 0
		self.__willpower = 0

		self.__attrWit = self.__character.traits["Attribute"]["Mental"]["Wits"]
		self.__attrRes = self.__character.traits["Attribute"]["Mental"]["Resolve"]
		self.__attrStr = self.__character.traits["Attribute"]["Physical"]["Strength"]
		self.__attrDex = self.__character.traits["Attribute"]["Physical"]["Dexterity"]
		self.__attrSta = self.__character.traits["Attribute"]["Physical"]["Stamina"]
		self.__attrCom = self.__character.traits["Attribute"]["Social"]["Composure"]
		self.__meritFleetOfFoot = self.__character.traits["Merit"]["Physical"]["Fleet of Foot"]
		self.__meritFastReflexes = self.__character.traits["Merit"]["Physical"]["Fast Reflexes"]
		self.__giantTrait = self.__character.traits["Merit"]["Physical"]["Giant"]
		self.__giantTraitKid = self.__character.traits["Merit"]["Physical"]["GiantKid"]
		self.__smallTrait = self.__character.traits["Flaw"]["Physical"]["Dwarf"]
		self.__smallTraitKid = self.__character.traits["Merit"]["Physical"]["Tiny"]

		self.sizeChanged.connect(self.calcHealth)
		self.sizeChanged.connect(self.calcDefense)


	#@property
	#def size(self):
		#return self.__size


	#@property
	#def initiative(self):
		#return self.__initiative


	#@property
	#def speed(self):
		#return self.__speed


	#@property
	#def defense(self):
		#"""
		#Gibt die berechnete Defense des Charakters aus.
		#"""

		#return self.__defense


	#@property
	#def health(self):
		#"""
		#Gibt die berechnete Gesundheit des Charakters aus.
		#"""

		#return self.__health


	#@property
	#def willpower(self):
		#"""
		#Gibt die berechnete Willenskraft des Charakters aus.
		#"""

		#return self.__willpower


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

		result = Calc.calc_initiative( self.__attrDex.totalvalue, self.__attrCom.totalvalue, self.__meritFastReflexes.totalvalue )

		if ( self.__initiative != result ):
			self.__initiative = result
			self.initiativeChanged.emit( result )

		return self.__initiative


	def calcSpeed(self):
		"""
		Berechnung der Geschwindigkeit des Charakters.

		\todo Bislang nur von Strength und Dexterity abhängig. Möglicherweise vorhandene Übernatürliche Eigenschaften werden nicht berücksichtigt.
		"""

		result = Calc.calc_speed( self.__attrStr.totalvalue, self.__attrDex.totalvalue, self.__meritFleetOfFoot.totalvalue )

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

		result = Calc.calc_defense( self.__attrWit.totalvalue, self.__attrDex.totalvalue, age=self.__character.age, size=self.__size )

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

		result = Calc.calc_health( self.__attrSta.totalvalue, size )

		if ( self.__health != result ):
			self.__health = result
			self.healthChanged.emit( result )

		return self.__health


	def calcWillpower(self):
		"""
		Berechnung der Willenskraft.
		"""

		result = Calc.calc_willpower( self.__attrRes.totalvalue, self.__attrCom.totalvalue )

		if ( self.__willpower != result ):
			self.__willpower = result
			self.willpowerChanged.emit( result )

		return self.__willpower


	@staticmethod
	def calculateSpiritRank(power, finesse, resistance):
		"""
		Berechnet den Rang eines Geistes aus dessen Attributen.
		"""
		
		result = power + finesse + resistance

		rank = 1
		if result > 25:
			rank = 5
		elif result > 19:
			rank = 4
		elif result > 13:
			rank = 3
		elif result > 7:
			rank = 2

		return rank
