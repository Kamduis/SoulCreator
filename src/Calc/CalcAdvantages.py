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

#import traceback

from PySide.QtCore import QObject, Signal
#from PySide.QtGui import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QButtonGroup

from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
#from src.Widgets.Components.CharaTrait import CharaTrait
from src.Debug import Debug




class CalcAdvantages(QObject):
	"""
	\brief Diese Klasse führt die berechnung der abgeleiteten Eigenschaften durch.
 *
 * Die hier deklarierten Berechnungsfunktionen werden zwar bei der Änderung jeder Eigenschaft aufgerufen, aber berechnen die Werte nur, wenn eine Eigenschaft verändert wurde, welche Einfluß auf das Ergebnis nimmt. Sie geben allerdings immer das Ergebnis der berechnung aus. Entweder den neuen Wert, oder den alten Wert, der in dieser Klasse gespeichert wird.
	"""


	sizeChanged = Signal(int)
	initiativeChanged = Signal(int)
	speedChanged = Signal(int)
	defenseChanged = Signal(int)
	healthChanged = Signal(int)
	willpowerChanged = Signal(int)


	def __init__(self, character, parent=None):
		QObject.__init__(self, parent)

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
		self.__meritGiant = self.__character.traits["Merit"]["Physical"]["Giant"]
		self.__meritFleetOfFoot = self.__character.traits["Merit"]["Physical"]["Fleet of Foot"]
		self.__meritFastReflexes = self.__character.traits["Merit"]["Physical"]["Fast Reflexes"]

		self.sizeChanged.connect(self.calcHealth)


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


	def calcSize(self):
		"""
		Berechnung der Größe des Charakters.
		"""

		result = 5
		if self.__character.age < Config.adultAge:
			result -= 1

		if ( self.__meritGiant.value > 0 ):
			result += 1

		if ( self.__size != result ):
			self.__size = result
			self.sizeChanged.emit( result )

		return self.__size


	def calcInitiative(self):
		"""
		Berechnung der Initiative des Charakters.

		\todo Bislang nur von Dexterity, Composure und Fast Reflexes abhängig. Möglicherweise vorhandene Übernatürliche Eigenschaften werden nicht berücksichtigt.
		"""

		result = self.__attrDex.value + self.__attrCom.value + self.__meritFastReflexes.value

		if ( self.__initiative != result ):
			self.__initiative = result
			self.initiativeChanged.emit( result )

		return self.__initiative


	def calcSpeed(self):
		"""
		Berechnung der Geschwindigkeit des Charakters.

		\todo Bislang nur von Strength und Dexterity abhängig. Möglicherweise vorhandene Übernatürliche Eigenschaften werden nicht berücksichtigt.
		"""

		result = self.__attrStr.value + self.__attrDex.value + 5 + self.__meritFleetOfFoot.value;

		if ( self.__speed != result ):
			self.__speed = result
			self.speedChanged.emit( result )

		return self.__speed


	def calcDefense(self):
		"""
		Berechnung der Defense

		\todo Bislang nicht von der Spezies abhängig: Tiere sollten stets das größere von Dex und Wits als Defense haben.
		"""

		result = min( self.__attrWit.value, self.__attrDex.value )

		if ( self.__defense != result ):
			self.__defense = result
			self.defenseChanged.emit( result )

		return self.__defense


	def calcHealth(self):
		"""
		Berechnung der Gesundheit.
		"""

		## Bevor ich die Gesundheit ausrechnen kann, muß erst die Größe feststehen.
		size = self.calcSize()

		result = self.__attrSta.value + size

		#Debug.debug("Berechne {} + {} = {}".format(self.__attrSta.value, size, result))

		if ( self.__health != result ):
			self.__health = result
			self.healthChanged.emit( result )

		return self.__health


	def calcWillpower(self):
		"""
		Berechnung der Willenskraft.
		"""

		result = self.__attrRes.value + self.__attrCom.value

		if ( self.__willpower != result ):
			self.__willpower = result
			self.willpowerChanged.emit( result )

		return self.__willpower


	@staticmethod
	def strength( strength, shape ):
		"""
		Berechnet die Stamina des Charakters abhängig von den unterschiedlichen Gestalten.
		"""

		if shape == Config.shapesWerewolf[1]:
			return strength + 1
		elif shape == Config.shapesWerewolf[2]:
			return strength + 3
		elif shape == Config.shapesWerewolf[3]:
			return strength + 2
		else:
			return strength


	@staticmethod
	def dexterity( dexterity, shape ):
		"""
		Berechnet die Stamina des Charakters abhängig von den unterschiedlichen Gestalten.
		"""

		if shape == Config.shapesWerewolf[2]:
			return dexterity + 1
		elif shape == Config.shapesWerewolf[3] or shape == Config.shapesWerewolf[4]:
			return dexterity + 2
		else:
			return dexterity


	@staticmethod
	def stamina( stamina, shape ):
		"""
		Berechnet die Stamina des Charakters abhängig von den unterschiedlichen Gestalten.
		"""

		if shape == Config.shapesWerewolf[1] or shape == Config.shapesWerewolf[4]:
			return stamina + 1
		elif shape == Config.shapesWerewolf[2] or shape == Config.shapesWerewolf[3]:
			return stamina + 2
		else:
			return stamina


	@staticmethod
	def manipulation( manipulation, shape ):
		"""
		Berechnet die Manipulation des Charakters abhängig von den unterschiedlichen Gestalten.
		"""

		if shape == Config.shapesWerewolf[1]:
			return manipulation - 1
		elif shape == Config.shapesWerewolf[3]:
			return manipulation - 3
		else:
			return manipulation


	@staticmethod
	def size( size, shape ):
		"""
		Berechnet die Größe des Charakters abhängig von den unterschiedlichen Gestalten.
		"""

		if shape == Config.shapesWerewolf[1] or shape == Config.shapesWerewolf[3]:
			return size + 1
		elif shape == Config.shapesWerewolf[2]:
			return size + 2
		elif shape == Config.shapesWerewolf[4]:
			return size - 1
		else:
			return size


	@staticmethod
	def initiative( initiative, shape ):
		"""
		Berechnet die Initiative des Charakters abhängig von den unterschiedlichen Gestalten.
		"""

		if shape == Config.shapesWerewolf[2]:
			return initiative + 1
		elif shape == Config.shapesWerewolf[3] or shape == Config.shapesWerewolf[4]:
			return initiative + 2
		else:
			return initiative


	@staticmethod
	def speed( speed, shape ):
		"""
		Berechnet die Geschwindigkeit des Charakters abhängig von den unterschiedlichen Gestalten.
		"""

		if shape == Config.shapesWerewolf[1]:
			return speed + 1
		elif shape == Config.shapesWerewolf[2]:
			return speed + 4
		elif shape == Config.shapesWerewolf[3]:
			return speed + 7
		elif shape == Config.shapesWerewolf[4]:
			return speed + 5
		else:
			return speed


	@staticmethod
	def health( value, shape ):
		"""
		Berechnet die Geschwindigkeit des Charakters abhängig von den unterschiedlichen Gestalten.
		"""

		if shape == Config.shapesWerewolf[1]:
			return value + 2
		elif shape == Config.shapesWerewolf[2]:
			return value + 4
		elif shape == Config.shapesWerewolf[3]:
			return value + 3
		else:
			return value


