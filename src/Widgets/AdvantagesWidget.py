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

from PySide.QtCore import Qt, Signal
from PySide.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFontMetrics, QLabel, QSpinBox

from src.Config import Config
#from src import Error
from src.Calc.CalcAdvantages import CalcAdvantages
from src.Calc.CalcShapes import CalcShapes
from src.Widgets.Components.TraitDots import TraitDots
from src.Widgets.Components.Squares import Squares
from src.Debug import Debug

from ui.ui_AdvantagesWidget import Ui_AdvantagesWidget




class AdvantagesWidget(QWidget):
	"""
	@brief Dieses Widget zeit die Advantages (Size, Speed, Health etc.) an.
	"""


	sizeChanged = Signal(int)
	initiativeChanged = Signal(int)
	speedChanged = Signal(int)
	defenseChanged = Signal(int)
	healthChanged = Signal(int)


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.ui = Ui_AdvantagesWidget()
		self.ui.setupUi(self)

		self.__character = character
		self.__storage = template

		fontMetrics = QFontMetrics(self.font())
		textRect = fontMetrics.boundingRect("0")

		self.ui.spinBox_armorGeneral.setMaximumWidth(textRect.width() + Config.spinBoxNoTextWidth)
		self.ui.spinBox_armorFirearms.setMaximumWidth(self.ui.spinBox_armorGeneral.maximumWidth())

		self.ui.dots_health.setReadOnly( True )

		self.ui.dots_willpower.setMaximum( Config.willpowerMax )
		self.ui.dots_willpower.setReadOnly( True )

		self.ui.dots_powerstat.setMaximum( Config.powerstatMax )
		self.ui.dots_powerstat.setMinimum( Config.powerstatMin )
		# Damit später der Wert stimmt muß ich irgendeinen Wert != 1 geben, sonst wird kein Signal gesandt.
		self.ui.dots_powerstat.setValue( 9 )

		self.ui.squares_fuel.columnMax = 10

		self.__character.speciesChanged.connect(self.setShapeSize)
		self.sizeChanged.connect(self.setShapeSize)
		self.__character.speciesChanged.connect(self.setShapeInitiaitve)
		self.initiativeChanged.connect(self.setShapeInitiaitve)
		self.__character.speciesChanged.connect(self.setShapeSpeed)
		self.speedChanged.connect(self.setShapeSpeed)
		self.__character.speciesChanged.connect(self.setShapeDefense)
		self.__character.traits["Attribute"]["Mental"]["Wits"].valueChanged.connect(self.setShapeDefense)
		self.__character.traits["Attribute"]["Physical"]["Dexterity"].valueChanged.connect(self.setShapeDefense)
		self.__character.speciesChanged.connect(self.setShapeHealth)
		self.healthChanged.connect(self.setShapeHealth)
		self.ui.spinBox_armorGeneral.valueChanged.connect(self.saveArmor)
		self.ui.spinBox_armorFirearms.valueChanged.connect(self.saveArmor)
		self.__character.armorChanged.connect(self.updateArmor)
##// 	connect( character, SIGNAL( traitChanged( cv_Trait ) ), self, SLOT( changeSuper( cv_Trait ) ) );
##// 	connect( dotsSuper, SIGNAL( valueChanged( int ) ), self, SLOT( emitSuperChanged( int ) ) );
##// 	connect( self, SIGNAL( superChanged( cv_Trait ) ), character, SLOT( addTrait( cv_Trait ) ) );
		self.ui.dots_powerstat.valueChanged.connect(self.__character.setPowerstat)
		self.__character.powerstatChanged.connect(self.ui.dots_powerstat.setValue)
		self.__character.powerstatChanged.connect(self.setFuel)
		self.__character.speciesChanged.connect(self.setFuel)
		self.__character.speciesChanged.connect(self.renamePowerstatHeading)
		self.__character.speciesChanged.connect(self.hideSuper)


	def setSize(self, value):
		if self.ui.label_size.text() != unicode(value):
			self.ui.label_size.setText(unicode(value))
			self.sizeChanged.emit(value)


	def setInitiative(self, value):
		if self.ui.label_initiative.text() != unicode(value):
			self.ui.label_initiative.setText(unicode(value))
			self.initiativeChanged.emit(value)


	def setSpeed(self, value):
		if self.ui.label_speed.text() != unicode(value):
			self.ui.label_speed.setText(unicode(value))
			self.speedChanged.emit(value)


	def setDefense(self, value):
		if self.ui.label_defense.text() != unicode(value):
			self.ui.label_defense.setNum(value)
			self.defenseChanged.emit(value)


	def setHealth(self, value):
		if self.ui.dots_health.value() != value:
			self.ui.dots_health.setMaximum(value)
			self.ui.dots_health.setValue(value)
			self.healthChanged.emit(value)


	def setWillpower(self, value):
		self.ui.dots_willpower.setValue(value)


	def setShapeSize(self):
		if self.__character.species == "Werewolf":
			size = int(self.ui.label_size.text())
			self.ui.label_sizeShapes.setHidden(False)
			self.ui.label_sizeShapes.setText(", {}, {}, {}, {}".format(
				CalcShapes.size(size, Config.shapesWerewolf[1]),
				CalcShapes.size(size, Config.shapesWerewolf[2]),
				CalcShapes.size(size, Config.shapesWerewolf[3]),
				CalcShapes.size(size, Config.shapesWerewolf[4]),
			))
		else:
			self.ui.label_sizeShapes.setHidden(True)


	def setShapeInitiaitve(self):
		if self.__character.species == "Werewolf":
			value = int(self.ui.label_initiative.text())
			self.ui.label_initiativeShapes.setHidden(False)
			self.ui.label_initiativeShapes.setText(", {}, {}, {}, {}".format(
				CalcShapes.initiative(value, Config.shapesWerewolf[1]),
				CalcShapes.initiative(value, Config.shapesWerewolf[2]),
				CalcShapes.initiative(value, Config.shapesWerewolf[3]),
				CalcShapes.initiative(value, Config.shapesWerewolf[4]),
			))
		else:
			self.ui.label_initiativeShapes.setHidden(True)


	def setShapeSpeed(self):
		if self.__character.species == "Werewolf":
			value = int(self.ui.label_speed.text())
			self.ui.label_speedShapes.setHidden(False)
			self.ui.label_speedShapes.setText(", {}, {}, {}, {}".format(
				CalcShapes.speed(value, Config.shapesWerewolf[1]),
				CalcShapes.speed(value, Config.shapesWerewolf[2]),
				CalcShapes.speed(value, Config.shapesWerewolf[3]),
				CalcShapes.speed(value, Config.shapesWerewolf[4]),
			))
		else:
			self.ui.label_speedShapes.setHidden(True)


	def setShapeDefense(self):
		if self.__character.species == "Werewolf":
			wits = self.__character.traits["Attribute"]["Mental"]["Wits"].value
			dexterity = self.__character.traits["Attribute"]["Physical"]["Dexterity"].value
			self.ui.label_defenseShapes.setHidden(False)
			self.ui.label_defenseShapes.setText(", {}, {}, {}, {}".format(
				CalcShapes.defense(wits, dexterity, Config.shapesWerewolf[1]),
				CalcShapes.defense(wits, dexterity, Config.shapesWerewolf[2]),
				CalcShapes.defense(wits, dexterity, Config.shapesWerewolf[3]),
				CalcShapes.defense(wits, dexterity, Config.shapesWerewolf[4]),
			))
		else:
			self.ui.label_defenseShapes.setHidden(True)


	def setShapeHealth(self):
		if self.__character.species == "Werewolf":
			value = self.ui.dots_health.value()
			self.ui.label_healthShapes.setHidden(False)
			self.ui.label_healthShapes.setText("{}, {}, {}, {}".format(
				CalcShapes.health(value, Config.shapesWerewolf[1]),
				CalcShapes.health(value, Config.shapesWerewolf[2]),
				CalcShapes.health(value, Config.shapesWerewolf[3]),
				CalcShapes.health(value, Config.shapesWerewolf[4]),
			))
		else:
			self.ui.label_healthShapes.setHidden(True)


	def hideSuper( self, species ):
		"""
		Verbirgt die übernatürlichen Eigenschaften, falls ein Mensch gewählt wird.
		"""

		if ( species == Config.initialSpecies ):
			self.ui.label_powerstat.setHidden( True )
			self.ui.dots_powerstat.setHidden( True )

			self.ui.label_fuel.setHidden( True )
			self.ui.squares_fuel.setHidden( True )
			self.ui.label_fuelPerTurn.setHidden( True )
		else:
			self.ui.label_powerstat.setHidden( False )
			self.ui.dots_powerstat.setHidden( False )

			self.ui.label_fuel.setHidden( False )
			self.ui.squares_fuel.setHidden( False )
			self.ui.label_fuelPerTurn.setHidden( False )


	def renamePowerstatHeading(self, species):
		"""
		Benennt die Übernatürlichen Eigenschaften je nach Spezies um.
		"""
		
		self.ui.label_powerstat.setText( self.__storage.powerstatName(species) )
		self.ui.label_fuel.setText( self.__storage.fuelName(species) )


	def setFuel( self ):
		"""
		Diese Funktion paßt das Maximum der Charakterenergie an, wenn sich die Spezies oder der Powerstat-Wert des Charakters ändert.
		"""

		maximum = self.__storage.fuelMax( self.__character.species, self.__character.powerstat )
		self.ui.squares_fuel.maximum = maximum

		perTurn = self.__storage.fuelPerTurn( self.__character.species, self.__character.powerstat )
		self.ui.label_fuelPerTurn.setText( self.tr( "{}/Turn".format( perTurn ) ))


	def saveArmor(self):
		"""
		Schreibe die veränderte Rüstung in den Charkater.
		"""

		armor = [
			self.ui.spinBox_armorGeneral.value(),
			self.ui.spinBox_armorFirearms.value(),
		]
		self.__character.armor = armor

	def updateArmor( self, armor ):
		"""
		Schreibe die veränderte Rüstung in das Widget.
		"""

		self.ui.spinBox_armorGeneral.setValue(armor[0])
		self.ui.spinBox_armorFirearms.setValue(armor[1])

