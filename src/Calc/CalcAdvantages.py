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
		self.__speed = 0;
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

	#QList< cv_AbstractTrait::Type > types;
	#types.append( cv_AbstractTrait::Attribute );
	#types.append( cv_AbstractTrait::Merit );

	#QList< Trait* > list;

	#bool stopLoop = false;

	#for ( int i = 0; i < types.count(); ++i ) {
		#list = character.traits( types.at( i ) );

		#for ( int j = 0; j < list.count(); ++j ) {
			#if ( types.at( i ) == cv_AbstractTrait::Attribute ) {
				#if ( list.at( j ).name() == "Wits" ) {
					#attrWit = list.at( j );
				#} else if ( list.at( j ).name() == "Resolve" ) {
					#attrRes = list.at( j );
				#} else if ( list.at( j ).name() == "Strength" ) {
					#attrStr = list.at( j );
				#} else if ( list.at( j ).name() == "Dexterity" ) {
					#attrDex = list.at( j );
				#} else if ( list.at( j ).name() == "Stamina" ) {
					#attrSta = list.at( j );
				#} else if ( list.at( j ).name() == "Composure" ) {
					#attrCom = list.at( j );
				#}

				#if ( attrWit != 0 && attrRes != 0 && attrStr != 0 && attrDex != 0 && attrSta != 0 && attrCom != 0 ) {
					#break;
				#}
			#} else if ( types.at( i ) == cv_AbstractTrait::Merit ) {
				#if ( list.at( j ).name() == "Giant" ) {
					#meritGiant = list.at( j );
				#} else if ( list.at( j ).name() == "Fast Reflexes" ) {
					#meritFastReflexes = list.at( j );
				#} else if ( list.at( j ).name() == "Fleet of Foot" ) {
					#meritFleetOfFoot = list.at( j );
				#}

				#if ( meritGiant != 0 && meritFleetOfFoot != 0 && meritFastReflexes != 0 ) {
					#break;
				#}
			#}
		#}
	#}

	#connect( attrWit, SIGNAL( valueChanged( int ) ), this, SLOT( calcInitiative() ) );
	#connect( attrWit, SIGNAL( valueChanged( int ) ), this, SLOT( calcDefense() ) );
	#connect( attrRes, SIGNAL( valueChanged( int ) ), this, SLOT( calcWillpower() ) );
	#connect( attrStr, SIGNAL( valueChanged( int ) ), this, SLOT( calcSpeed() ) );
	#connect( attrDex, SIGNAL( valueChanged( int ) ), this, SLOT( calcSpeed() ) );
	#connect( attrDex, SIGNAL( valueChanged( int ) ), this, SLOT( calcInitiative() ) );
	#connect( attrDex, SIGNAL( valueChanged( int ) ), this, SLOT( calcDefense() ) );
	#connect( attrSta, SIGNAL( valueChanged( int ) ), this, SLOT( calcHealth() ) );
	#connect( attrCom, SIGNAL( valueChanged( int ) ), this, SLOT( calcWillpower() ) );
	#connect( meritGiant, SIGNAL( valueChanged( int ) ), this, SLOT( calcSize() ) );
	#connect( meritFastReflexes, SIGNAL( valueChanged( int ) ), this, SLOT( calcInitiative() ) );
	#connect( meritFleetOfFoot, SIGNAL( valueChanged( int ) ), this, SLOT( calcSpeed() ) );
	#connect( this, SIGNAL( sizeChanged( int ) ), this, SLOT( calcHealth() ) );
#}


#int CalcAdvantages::strength( int str, cv_Shape::WerewolfShape shape ) {
	"""
	"""
	
	#switch ( shape ) {
		#case cv_Shape::ShapeNo:
			#return str;
		#case cv_Shape::Hishu:
			#return str;
		#case cv_Shape::Dalu:
			#return str + 1;
		#case cv_Shape::Gauru:
			#return str + 3;
		#case cv_Shape::Urshul:
			#return str + 2;
		#case cv_Shape::Urhan:
			#return str;
		#default:
			#throw eWerewolfShapeNotExisting( shape );
	#}
#}

#int CalcAdvantages::dexterity( int dex, cv_Shape::WerewolfShape shape ) {
	"""
	"""

	#switch ( shape ) {
		#case cv_Shape::ShapeNo:
			#return dex;
		#case cv_Shape::Hishu:
			#return dex;
		#case cv_Shape::Dalu:
			#return dex;
		#case cv_Shape::Gauru:
			#return dex + 1;
		#case cv_Shape::Urshul:
			#return dex + 2;
		#case cv_Shape::Urhan:
			#return dex + 2;
		#default:
			#throw eWerewolfShapeNotExisting( shape );
	#}
#}

#int CalcAdvantages::stamina( int sta, cv_Shape::WerewolfShape shape ) {
	"""
	"""

	#switch ( shape ) {
		#case cv_Shape::ShapeNo:
			#return sta;
		#case cv_Shape::Hishu:
			#return sta;
		#case cv_Shape::Dalu:
			#return sta + 1;
		#case cv_Shape::Gauru:
			#return sta + 2;
		#case cv_Shape::Urshul:
			#return sta + 2;
		#case cv_Shape::Urhan:
			#return sta + 1;
		#default:
			#throw eWerewolfShapeNotExisting( shape );
	#}
#}

#int CalcAdvantages::manipulation( int man, cv_Shape::WerewolfShape shape ) {
	"""
	"""

	#switch ( shape ) {
		#case cv_Shape::ShapeNo:
			#return man;
		#case cv_Shape::Hishu:
			#return man;
		#case cv_Shape::Dalu:
			#return man - 1;
		#case cv_Shape::Gauru:
			#return man;
		#case cv_Shape::Urshul:
			#return man - 3;
		#case cv_Shape::Urhan:
			#return man;
		#default:
			#throw eWerewolfShapeNotExisting( shape );
	#}
#}


#int CalcAdvantages::size( cv_Shape::WerewolfShape shape ) const {
	"""
	Berechnet die Größe des Charakters abhängig von den unterschiedlichen Gestalten.
	
	\note Es wird auf das Ergebnis der Funktion calcSize() zurückgegriffen, welche bei jeder Veränderung einer Eigenschaft, die Auswirkung auf die Size haben kann, aufgerufen wird.
	"""

	#switch ( shape ) {
		#case cv_Shape::ShapeNo:
			#return v_size;
		#case cv_Shape::Hishu:
			#return v_size;
		#case cv_Shape::Dalu:
			#return v_size + 1;
		#case cv_Shape::Gauru:
			#return v_size + 2;
		#case cv_Shape::Urshul:
			#return v_size + 1;
		#case cv_Shape::Urhan:
			#return v_size - 1;
		#default:
			#throw eWerewolfShapeNotExisting( shape );
	#}
#}

#int CalcAdvantages::initiative( cv_Shape::WerewolfShape shape ) const {
	"""
	Berechnet die Initiative des Charakters abhängig von den unterschiedlichen Gestalten.
	
	\note Es wird auf das Ergebnis der Funktion calcInitiativa() zurückgegriffen, welche bei jeder Veränderung einer Eigenschaft, die Auswirkung auf die Initiative haben kann, aufgerufen wird.
	"""

	#switch ( shape ) {
		#case cv_Shape::ShapeNo:
			#return v_initiative;
		#case cv_Shape::Hishu:
			#return v_initiative;
		#case cv_Shape::Dalu:
			#return v_initiative;
		#case cv_Shape::Gauru:
			#return v_initiative + 1;
		#case cv_Shape::Urshul:
			#return v_initiative + 2;
		#case cv_Shape::Urhan:
			#return v_initiative + 2;
		#default:
			#throw eWerewolfShapeNotExisting( shape );
	#}
#}

#int CalcAdvantages::speed( cv_Shape::WerewolfShape shape ) const {
	"""
	Berechnet die Geschwindigkeit des Charakters abhängig von den unterschiedlichen Gestalten.
	
	\note Es wird auf das Ergebnis der Funktion calcSpeed() zurückgegriffen, welche bei jeder Veränderung einer Eigenschaft, die Auswirkung auf diee Eigenschaft haben kann, aufgerufen wird.
	"""

	#switch ( shape ) {
		#case cv_Shape::ShapeNo:
			#return v_speed;
		#case cv_Shape::Hishu:
			#return v_speed;
		#case cv_Shape::Dalu:
			#return v_speed + 1;
		#case cv_Shape::Gauru:
			#return v_speed + 4;
		#case cv_Shape::Urshul:
			#return v_speed + 7;
		#case cv_Shape::Urhan:
			#return v_speed + 5;
		#default:
			#throw eWerewolfShapeNotExisting( shape );
	#}
#}

#int CalcAdvantages::defense() const {
	"""
	Gibt die berechnete Defense des Charakters aus.
	"""

	#return v_defense;
#}

#int CalcAdvantages::health() const {
	"""
	Gibt die berechnete Gesundheit des Charakters aus.
	"""

	#return v_health;
#}

#int CalcAdvantages::willpower() const {
	"""
	Gibt die berechnete Willenskraft des Charakters aus.
	"""

	#return v_willpower;
#}


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


	def calcInitiative(self):
		"""
		Berechnung der Initiative des Charakters.

		\todo Bislang nur von Dexterity, Composure und Fast Reflexes abhängig.
		"""

		result = self.__attrDex.value + self.__attrCom.value + self.__meritFastReflexes.value

		if ( self.__initiative != result ):
			self.__initiative = result
			self.initiativeChanged.emit( result )


	def calcSpeed(self):
		"""
		Berechnung der Geschwindigkeit des Charakters.

		\todo Bislang nur von Strength und Dexterity abhängig.
		"""

		result = self.__attrStr.value + self.__attrDex.value + 5 + self.__meritFleetOfFoot.value;

		if ( self.__speed != result ):
			self.__speed = result
			self.speedChanged.emit( result )


	def calcDefense(self):
		"""
		Berechnung der Defense

		\todo Bislang nicht von der Spezies abhängig. Tiere haben stets das größere von Dex und Wits als Defense.
		"""

		result = min( self.__attrWit.value, self.__attrDex.value )

		if ( self.__defense != result ):
			self.__defense = result
			self.defenseChanged.emit( result )


	def calcHealth(self):
		"""
		Berechnung der Gesundheit.
		"""

		result = self.__attrSta.value + self.__size

		if ( self.__health != result ):
			self.__health = result
			self.healthChanged.emit( result )


	def calcWillpower(self):
		"""
		Berechnung der Willenskraft.

		\note der Übergebene Wert wird ignoriert. Stattdessen wird alles was man braucht direkt aus dem Charakterspeicher genommen.
		"""

		result = self.__attrRes.value + self.__attrCom.value

		if ( self.__willpower != result ):
			self.__willpower = result
			self.willpowerChanged.emit( result )


