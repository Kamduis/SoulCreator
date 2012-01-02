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
from src.Calc.CalcAdvantages import CalcAdvantages
from src.Widgets.Components.TraitDots import TraitDots
from src.Debug import Debug




class AdvantagesWidget(QWidget):
	"""
	@brief Dieses Widget zeit die Advantages (Size, Speed, Health etc.) an.
	"""

	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.__character = character
		self.__storage = template

		self.__calc = CalcAdvantages( self )

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


	#labelFuel = QLabel( self.tr( "Fuel" ) );
	#labelFuel.setAlignment( Qt::AlignHCenter );

	#QHBoxLayout* layoutFuelSquares = QHBoxLayout();

	#squaresFuel = Squares();
	#squaresFuel.setColumnMax( 10 );
	#squaresFuel.setMaximum( storage.fuelMax( character.species(), character.superTrait() ) );

	#fuelPerTurn = QLabel( self.tr( "1" ) );
	#fuelPerTurn.setAlignment( Qt::AlignCenter );

	#layoutFuelSquares.addWidget( squaresFuel );
	#layoutFuelSquares.addStretch();
	#layoutFuelSquares.addWidget( fuelPerTurn );

	#layout.addSpacing( Config::traitCategorySpace );

	#layout.addWidget( labelFuel );
	#layout.addLayout( layoutFuelSquares );

	#layout.addStretch();

	#connect( calcAdvantages, SIGNAL( sizeChanged( int ) ), self, SLOT( writeSize( int ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( writeSize( cv_Species::SpeciesFlag ) ) );
	#connect( calcAdvantages, SIGNAL( initiativeChanged( int ) ), self, SLOT( writeInitiative( int ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( writeInitiative(cv_Species::SpeciesFlag)) );
	#connect( calcAdvantages, SIGNAL( speedChanged( int ) ), self, SLOT( writeSpeed( int ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( writeSpeed(cv_Species::SpeciesFlag)) );
	#connect( calcAdvantages, SIGNAL( defenseChanged( int ) ), labelDefenseValue, SLOT( setNum( int ) ) );
	#connect( calcAdvantages, SIGNAL( healthChanged( int ) ), self, SLOT( printHealth( int ) ) );
	#connect( calcAdvantages, SIGNAL( willpowerChanged( int ) ), dotsWill, SLOT( setValue( int ) ) );
	#connect( spinBoxArmorGeneral, SIGNAL(valueChanged(int)), self, SLOT(setArmor()));
	#connect( spinBoxArmorFirearms, SIGNAL(valueChanged(int)), self, SLOT(setArmor()));
	#connect( character, SIGNAL( armorChanged(int,int)), self, SLOT( updateArmor( int, int ) ) );
#// 	connect( character, SIGNAL( traitChanged( cv_Trait ) ), self, SLOT( changeSuper( cv_Trait ) ) );
#// 	connect( dotsSuper, SIGNAL( valueChanged( int ) ), self, SLOT( emitSuperChanged( int ) ) );
#// 	connect( self, SIGNAL( superChanged( cv_Trait ) ), character, SLOT( addTrait( cv_Trait ) ) );
	#connect( dotsSuper, SIGNAL( valueChanged( int ) ), character, SLOT( setSuperTrait( int ) ) );
	#connect( character, SIGNAL( superTraitChanged( int ) ), dotsSuper, SLOT( setValue( int ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( hideSuper( cv_Species::SpeciesFlag ) ) );
	#connect( character, SIGNAL( superTraitChanged( int ) ), self, SLOT( setFuelMaximum( int ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( setFuelMaximum( cv_Species::SpeciesFlag ) ) );

	#dotsSuper.setValue( Config::superTraitDefaultValue );
#}


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

#void AdvantagesWidget::hideSuper( cv_Species::SpeciesFlag species ) {
	"""

	"""

	#if ( species == cv_Species::Human ) {
		#labelSuper.setHidden( true );
		#dotsSuper.setHidden( true );

		#labelFuel.setHidden( true );
		#squaresFuel.setHidden( true );
		#fuelPerTurn.setHidden( true );
	#} else {
		#labelSuper.setHidden( false );
		#dotsSuper.setHidden( false );

		#labelFuel.setHidden( false );
		#squaresFuel.setHidden( false );
		#fuelPerTurn.setHidden( false );

		#for ( int i = 0; i < storage.species().count(); ++i ) {
			#if ( cv_Species::toSpecies( storage.species().at( i ).name ) == species ) {
				#labelSuper.setText( storage.species().at( i ).supertrait );
				#labelFuel.setText( storage.species().at( i ).fuel );
			#}
		#}

	#}
#}

#void AdvantagesWidget::setFuelMaximum( cv_Species::SpeciesFlag species ) {
	"""

	"""

	#int maximum = storage.fuelMax( species, character.superTrait() );
	#squaresFuel.setMaximum( maximum );

	#int perTurn = storage.fuelPerTurn( species, character.superTrait() );
	#fuelPerTurn.setText( self.tr( "%1/Turn" ).arg( perTurn ) );
#}

#void AdvantagesWidget::setFuelMaximum( int value ) {
	"""

	"""

	#int maximum = storage.fuelMax( character.species(), value );
	#squaresFuel.setMaximum( maximum );

	#int perTurn = storage.fuelPerTurn( character.species(), value );
	#fuelPerTurn.setText( self.tr( "%1/Turn" ).arg( perTurn ) );
#}


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


