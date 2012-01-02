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

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFontMetrics, QLabel, QSpinBox

from src.Config import Config
#from src import Error
from src.Widgets.Components.TraitDots import TraitDots
from src.Widgets.Components.Squares import Squares
from src.Debug import Debug




class AdvantagesWidget(QWidget):
	"""
	@brief Dieses Widget zeit die Advantages (Size, Speed, Health etc.) an.
	"""

	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.__character = character
		self.__storage = template

		self.__layout = QVBoxLayout()
		self.setLayout(self.__layout)

		self.__layoutAdvantages = QGridLayout()
		self.__layout.addLayout(self.__layoutAdvantages)

		self.__labelSize = QLabel( self.tr( "Size:" ) )
		self.__labelSizeValue = QLabel()
		self.__labelSizeValue.setNum( 0 )

		self.__labelInitiative = QLabel( self.tr( "Initiative:" ) )
		self.__labelInitiativeValue = QLabel()
		self.__labelInitiativeValue.setNum( 0 )

		self.__labelSpeed = QLabel( self.tr( "Speed:" ) )
		self.__labelSpeedValue = QLabel()
		self.__labelSpeedValue.setNum( 0 )

		self.__labelDefense = QLabel( self.tr( "Defense:" ) )
		self.__labelDefenseValue = QLabel()
		self.__labelDefenseValue.setNum( 0 )

		fontMetrics = QFontMetrics(self.font())
		textRect = fontMetrics.boundingRect("0")

		self.__labelArmor = QLabel( self.tr( "Armor:" ) )
		self.__labelArmorGeneral = QLabel( self.tr( "General" ) )
		self.__labelArmorFirearms = QLabel( self.tr( "Firearms" ) )
		self.__spinBoxArmorGeneral = QSpinBox()
		self.__spinBoxArmorGeneral.setMinimum( 0 )
		self.__spinBoxArmorGeneral.setMaximum( 9 )
		self.__spinBoxArmorGeneral.setMaximumWidth(textRect.width() + Config.spinBoxNoTextWidth);
		self.__spinBoxArmorFirearms = QSpinBox()
		self.__spinBoxArmorFirearms.setMinimum( 0 )
		self.__spinBoxArmorFirearms.setMaximum( 9 )
		self.__spinBoxArmorFirearms.setMaximumWidth(textRect.width() + Config.spinBoxNoTextWidth);

		self.__layoutAdvantages.addWidget( self.__labelSize, 0, 0 )
		self.__layoutAdvantages.addWidget( self.__labelSizeValue, 0, 1 )
		self.__layoutAdvantages.addWidget( self.__labelInitiative, 1, 0 )
		self.__layoutAdvantages.addWidget( self.__labelInitiativeValue, 1, 1 )
		self.__layoutAdvantages.addWidget( self.__labelSpeed, 2, 0 )
		self.__layoutAdvantages.addWidget( self.__labelSpeedValue, 2, 1 )
		self.__layoutAdvantages.addWidget( self.__labelDefense, 3, 0 )
		self.__layoutAdvantages.addWidget( self.__labelDefenseValue, 3, 1 )
		self.__layoutAdvantages.addWidget( self.__labelArmor, 4, 0 )
		self.__layoutAdvantages.addWidget( self.__spinBoxArmorGeneral, 4, 1 )
		self.__layoutAdvantages.addWidget( self.__labelArmorGeneral, 4, 2 )
		self.__layoutAdvantages.addWidget( self.__spinBoxArmorFirearms, 5, 1 )
		self.__layoutAdvantages.addWidget( self.__labelArmorFirearms, 5, 2 )

		self.__labelHealth = QLabel( self.tr( "Health" ) )
		self.__labelHealth.setAlignment( Qt.AlignHCenter )

		self.__layoutHealthDots = QHBoxLayout()

		self.__dotsHealth = TraitDots()
		self.__dotsHealth.setReadOnly( True )

		self.__layoutHealthDots.addStretch()
		self.__layoutHealthDots.addWidget( self.__dotsHealth )
		self.__layoutHealthDots.addStretch()

		self.__layout.addSpacing( Config.traitCategorySpace )

		self.__layout.addWidget( self.__labelHealth )
		self.__layout.addLayout( self.__layoutHealthDots )


		self.__labelWill = QLabel( self.tr( "Willpower" ) )
		self.__labelWill.setAlignment( Qt.AlignHCenter )

		self.__layoutWillDots = QHBoxLayout()

		self.__dotsWill = TraitDots()
		self.__dotsWill.setMaximum( Config.willpowerMax )
		self.__dotsWill.setReadOnly( True )

		self.__layoutWillDots.addStretch()
		self.__layoutWillDots.addWidget( self.__dotsWill )
		self.__layoutWillDots.addStretch()

		self.__layout.addSpacing( Config.traitCategorySpace )

		self.__layout.addWidget( self.__labelWill )
		self.__layout.addLayout( self.__layoutWillDots )


		self.__labelSuper = QLabel( self.tr( "Powerstat" ) )
		self.__labelSuper.setAlignment( Qt.AlignHCenter )

		self.__layoutSuperDots = QHBoxLayout();

		self.__dotsSuper = TraitDots()
		self.__dotsSuper.setMaximum( Config.powerstatMax )
		self.__dotsSuper.setMinimum( Config.powerstatMin )
		# Damit später der Wert stimmt muß ich irgendeinen Wert != 1 geben, sonst wird kein Signal gesandt.
		self.__dotsSuper.setValue( 9 )

		self.__layoutSuperDots.addStretch()
		self.__layoutSuperDots.addWidget( self.__dotsSuper )
		self.__layoutSuperDots.addStretch()

		self.__layout.addSpacing( Config.traitCategorySpace )

		self.__layout.addWidget( self.__labelSuper )
		self.__layout.addLayout( self.__layoutSuperDots )


		self.__labelFuel = QLabel( self.tr( "Fuel" ) )
		self.__labelFuel.setAlignment( Qt.AlignHCenter )

		self.__layoutFuelSquares = QHBoxLayout()

		self.__squaresFuel = Squares()
		self.__squaresFuel.columnMax = 10
		#self.__squaresFuel.maximum = self.__storage.fuelMax( self.__character.species, self.__character.powerstat )
		self.__squaresFuel.maximum = 0

		self.__fuelPerTurn = QLabel( self.tr( "1" ) )
		self.__fuelPerTurn.setAlignment( Qt.AlignCenter )

		self.__layoutFuelSquares.addWidget( self.__squaresFuel )
		self.__layoutFuelSquares.addStretch()
		self.__layoutFuelSquares.addWidget( self.__fuelPerTurn )

		self.__layout.addSpacing( Config.traitCategorySpace )

		self.__layout.addWidget( self.__labelFuel )
		self.__layout.addLayout( self.__layoutFuelSquares )

		self.__layout.addStretch()

	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( writeSize( cv_Species::SpeciesFlag ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( writeInitiative(cv_Species::SpeciesFlag)) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( writeSpeed(cv_Species::SpeciesFlag)) );
	#connect( spinBoxArmorGeneral, SIGNAL(valueChanged(int)), self, SLOT(setArmor()));
	#connect( spinBoxArmorFirearms, SIGNAL(valueChanged(int)), self, SLOT(setArmor()));
	#connect( character, SIGNAL( armorChanged(int,int)), self, SLOT( updateArmor( int, int ) ) );
#// 	connect( character, SIGNAL( traitChanged( cv_Trait ) ), self, SLOT( changeSuper( cv_Trait ) ) );
#// 	connect( dotsSuper, SIGNAL( valueChanged( int ) ), self, SLOT( emitSuperChanged( int ) ) );
#// 	connect( self, SIGNAL( superChanged( cv_Trait ) ), character, SLOT( addTrait( cv_Trait ) ) );
		self.__dotsSuper.valueChanged.connect(self.__character.setPowerstat)
		self.__character.powerstatChanged.connect(self.__dotsSuper.setValue)
		self.__character.powerstatChanged.connect(self.setFuel)
		self.__character.speciesChanged.connect(self.setFuel)
		self.__character.speciesChanged.connect(self.renamePowerstatHeading)
		self.__character.speciesChanged.connect(self.hideSuper)


	def setSize(self, value):
		self.__labelSizeValue.setNum(value)


	def setInitiative(self, value):
		self.__labelInitiativeValue.setNum(value)


	def setSpeed(self, value):
		self.__labelSpeedValue.setNum(value)


	def setDefense(self, value):
		self.__labelDefenseValue.setNum(value)


	def setHealth(self, value):
		self.__dotsHealth.setMaximum(value)
		self.__dotsHealth.setValue(value)


	def setWillpower(self, value):
		self.__dotsWill.setValue(value)


#void AdvantagesWidget::writeSize( int size ) {
	"""
	Schreibe die Größe in das Widget.
	"""
	
	#if ( character.species() == cv_Species::Werewolf ) {
		#QString text = QString::number( calcAdvantages.size( cv_Shape::Hishu ) ) + "/" +
					   #QString::number( calcAdvantages.size( cv_Shape::Dalu ) ) + "/" +
					   #QString::number( calcAdvantages.size( cv_Shape::Gauru ) ) + "/" +
					   #QString::number( calcAdvantages.size( cv_Shape::Urshul ) ) + "/" +
					   #QString::number( calcAdvantages.size( cv_Shape::Urhan ) );
		#labelSizeValue.setText( text );
	#} else {
		#labelSizeValue.setNum( size );
	#}
#}

#void AdvantagesWidget::writeSize( cv_Species::SpeciesFlag species ) {
	"""
	
	"""

	#if ( species == cv_Species::Werewolf ) {
		#QString text = QString::number( calcAdvantages.size( cv_Shape::Hishu ) ) + "/" +
					   #QString::number( calcAdvantages.size( cv_Shape::Dalu ) ) + "/" +
					   #QString::number( calcAdvantages.size( cv_Shape::Gauru ) ) + "/" +
					   #QString::number( calcAdvantages.size( cv_Shape::Urshul ) ) + "/" +
					   #QString::number( calcAdvantages.size( cv_Shape::Urhan ) );
		#labelSizeValue.setText( text );
	#} else {
		#labelSizeValue.setNum( calcAdvantages.size() );
	#}
#}

#void AdvantagesWidget::writeInitiative( int initiative ) {
	"""
	Schreibe die Initiative in das Widget.
	"""

	#if ( character.species() == cv_Species::Werewolf ) {
		#QString text = QString::number( calcAdvantages.initiative( cv_Shape::Hishu ) ) + "/" +
					   #QString::number( calcAdvantages.initiative( cv_Shape::Dalu ) ) + "/" +
					   #QString::number( calcAdvantages.initiative( cv_Shape::Gauru ) ) + "/" +
					   #QString::number( calcAdvantages.initiative( cv_Shape::Urshul ) ) + "/" +
					   #QString::number( calcAdvantages.initiative( cv_Shape::Urhan ) );
		#labelInitiativeValue.setText( text );
	#} else {
		#labelInitiativeValue.setNum( initiative );
	#}
#}

#void AdvantagesWidget::writeInitiative( cv_Species::SpeciesFlag species ) {
	"""

	"""

	#if ( species == cv_Species::Werewolf ) {
		#QString text = QString::number( calcAdvantages.initiative( cv_Shape::Hishu ) ) + "/" +
					   #QString::number( calcAdvantages.initiative( cv_Shape::Dalu ) ) + "/" +
					   #QString::number( calcAdvantages.initiative( cv_Shape::Gauru ) ) + "/" +
					   #QString::number( calcAdvantages.initiative( cv_Shape::Urshul ) ) + "/" +
					   #QString::number( calcAdvantages.initiative( cv_Shape::Urhan ) );
		#labelInitiativeValue.setText( text );
	#} else {
		#labelInitiativeValue.setNum( calcAdvantages.initiative() );
	#}
#}

#void AdvantagesWidget::writeSpeed( int speed ) {
	"""
	Schreibe den Speed in das Widget.
	"""

	#if ( character.species() == cv_Species::Werewolf ) {
		#QString text = QString::number( calcAdvantages.speed( cv_Shape::Hishu ) ) + "/" +
					   #QString::number( calcAdvantages.speed( cv_Shape::Dalu ) ) + "/" +
					   #QString::number( calcAdvantages.speed( cv_Shape::Gauru ) ) + "/" +
					   #QString::number( calcAdvantages.speed( cv_Shape::Urshul ) ) + "/" +
					   #QString::number( calcAdvantages.speed( cv_Shape::Urhan ) );
		#labelSpeedValue.setText( text );
	#} else {
		#labelSpeedValue.setNum( speed );
	#}
#}

#void AdvantagesWidget::writeSpeed( cv_Species::SpeciesFlag species ) {
	"""

	"""

	#if ( species == cv_Species::Werewolf ) {
		#QString text = QString::number( calcAdvantages.speed( cv_Shape::Hishu ) ) + "/" +
					   #QString::number( calcAdvantages.speed( cv_Shape::Dalu ) ) + "/" +
					   #QString::number( calcAdvantages.speed( cv_Shape::Gauru ) ) + "/" +
					   #QString::number( calcAdvantages.speed( cv_Shape::Urshul ) ) + "/" +
					   #QString::number( calcAdvantages.speed( cv_Shape::Urhan ) );
		#labelSpeedValue.setText( text );
	#} else {
		#labelSpeedValue.setNum( calcAdvantages.speed() );
	#}
#}

#void AdvantagesWidget::printHealth( int value ) {
	"""

	"""

	#dotsHealth.setMaximum( value );
	#dotsHealth.setValue( value );
#}

	def hideSuper( self, species ):
		"""

		"""

		if ( species == Config.initialSpecies ):
			self.__labelSuper.setHidden( True )
			self.__dotsSuper.setHidden( True )

			self.__labelFuel.setHidden( True )
			self.__squaresFuel.setHidden( True )
			self.__fuelPerTurn.setHidden( True )
		else:
			self.__labelSuper.setHidden( False )
			self.__dotsSuper.setHidden( False )

			self.__labelFuel.setHidden( False )
			self.__squaresFuel.setHidden( False )
			self.__fuelPerTurn.setHidden( False )


	def renamePowerstatHeading(self, species):
		self.__labelSuper.setText( self.__storage.powerstatName(species) )
		self.__labelFuel.setText( self.__storage.fuelName(species) )


	def setFuel( self ):
		"""
		Diese Funktion paßt das Maximum der Charakterenergie an, wenn sich die Spezies oder der Powerstat-Wert des Charakters ändert.
		"""

		maximum = self.__storage.fuelMax( self.__character.species, self.__character.powerstat )
		self.__squaresFuel.maximum = maximum

		perTurn = self.__storage.fuelPerTurn( self.__character.species, self.__character.powerstat )
		self.__fuelPerTurn.setText( self.tr( "{}/Turn".format( perTurn ) ))


#void AdvantagesWidget::setArmor(){
	"""
	Schreibe die veränderte Rüstung in den Charkater.
	"""
	
	#character.setArmor(spinBoxArmorGeneral.value(), spinBoxArmorFirearms.value());
#}
#void AdvantagesWidget::updateArmor( int general, int firearms ){
	"""
	Schreibe die veränderte Rüstung in das Widget.
	"""
	
	#spinBoxArmorGeneral.setValue(general);
	#spinBoxArmorFirearms.setValue(firearms);
#}





#// void AdvantagesWidget::changeSuper( cv_Trait trait ) {
#// 	if ( trait.type == cv_AbstractTrait::Super ) {
#// 		dotsSuper.setValue( trait.value );
#// 	}
#// }


#// void AdvantagesWidget::emitSuperChanged( int value ) {
#// 	cv_Trait trait;
#// 	trait.name = "Super";
#// 	trait.value = value;trait.type = cv_AbstractTrait::Super;
#// 	trait.category = cv_AbstractTrait::CategoryNo;
#//
#// 	emit superChanged(trait);
#// }


