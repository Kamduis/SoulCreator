/**
 * \file
 * \author Victor von Rhein <victor@caern.de>
 *
 * \section License
 *
 * Copyright (C) 2011 by Victor von Rhein
 *
 * This file is part of SoulCreator.
 *
 * SoulCreator is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SoulCreator is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <QDialog>
#include <QDebug>

// #include "Datatypes/cv_Trait.h"
// #include "Exceptions/Exception.h"
#include "Config/Config.h"

#include "AdvantagesWidget.h"


AdvantagesWidget::AdvantagesWidget( QWidget *parent ) : QWidget( parent )  {
	calcAdvantages = new CalcAdvantages( this );
	storage = new StorageTemplate( this );
	character = StorageCharacter::getInstance();

	layout = new QVBoxLayout( this );
	layout->setMargin( 0 );

	advantagesLayout = new QGridLayout();
// 	advantagesLayout->setColumnMinimumWidth( 1, 0 );

	setLayout( layout );

	layout->addLayout( advantagesLayout );

	QLabel* labelSize = new QLabel( tr( "Size:" ) );
	labelSizeValue = new QLabel( this );
	labelSizeValue->setNum( 0 );

	QLabel* labelInitiative = new QLabel( tr( "Initiative:" ) );
	labelInitiativeValue = new QLabel( this );
	labelInitiativeValue->setNum( 0 );

	QLabel* labelSpeed = new QLabel( tr( "Speed:" ) );
	labelSpeedValue = new QLabel( this );
	labelSpeedValue->setNum( 0 );

	QLabel* labelDefense = new QLabel( tr( "Defense:" ) );
	QLabel* labelDefenseValue = new QLabel( this );
	labelDefenseValue->setNum( 0 );

	QFontMetrics fontMetrics = QFontMetrics(this->font());
	QRect textRect = fontMetrics.boundingRect("0");

	QLabel* labelArmor = new QLabel( tr( "Armor:" ) );
	QLabel* labelArmorGeneral = new QLabel( tr( "General" ) );
	QLabel* labelArmorFirearms = new QLabel( tr( "Firearms" ) );
	spinBoxArmorGeneral = new QSpinBox( this );
	spinBoxArmorGeneral->setMinimum( 0 );
	spinBoxArmorGeneral->setMaximum( 9 );
	spinBoxArmorGeneral->setMaximumWidth(textRect.width() + Config::spinBoxNoTextWidth);
	spinBoxArmorFirearms = new QSpinBox( this );
	spinBoxArmorFirearms->setMinimum( 0 );
	spinBoxArmorFirearms->setMaximum( 9 );
	spinBoxArmorFirearms->setMaximumWidth(textRect.width() + Config::spinBoxNoTextWidth);

	advantagesLayout->addWidget( labelSize, 0, 0 );
	advantagesLayout->addWidget( labelSizeValue, 0, 1 );
	advantagesLayout->addWidget( labelInitiative, 1, 0 );
	advantagesLayout->addWidget( labelInitiativeValue, 1, 1 );
	advantagesLayout->addWidget( labelSpeed, 2, 0 );
	advantagesLayout->addWidget( labelSpeedValue, 2, 1 );
	advantagesLayout->addWidget( labelDefense, 3, 0 );
	advantagesLayout->addWidget( labelDefenseValue, 3, 1 );
	advantagesLayout->addWidget( labelArmor, 4, 0 );
	advantagesLayout->addWidget( spinBoxArmorGeneral, 4, 1 );
	advantagesLayout->addWidget( labelArmorGeneral, 4, 2 );
	advantagesLayout->addWidget( spinBoxArmorFirearms, 5, 1 );
	advantagesLayout->addWidget( labelArmorFirearms, 5, 2 );

	QLabel* labelHealth = new QLabel( tr( "Health" ) );
	labelHealth->setAlignment( Qt::AlignHCenter );

	QHBoxLayout* layoutHealthDots = new QHBoxLayout();

	dotsHealth = new TraitDots( );
	dotsHealth->setReadOnly( true );

	layoutHealthDots->addStretch();
	layoutHealthDots->addWidget( dotsHealth );
	layoutHealthDots->addStretch();

	layout->addSpacing( Config::traitCategorySpace );

	layout->addWidget( labelHealth );
	layout->addLayout( layoutHealthDots );


	QLabel* labelWill = new QLabel( tr( "Willpower" ) );
	labelWill->setAlignment( Qt::AlignHCenter );

	QHBoxLayout* layoutWillDots = new QHBoxLayout();

	TraitDots* dotsWill = new TraitDots( );
	dotsWill->setMaximum( Config::superTraitMax );
	dotsWill->setReadOnly( true );

	layoutWillDots->addStretch();
	layoutWillDots->addWidget( dotsWill );
	layoutWillDots->addStretch();

	layout->addSpacing( Config::traitCategorySpace );

	layout->addWidget( labelWill );
	layout->addLayout( layoutWillDots );


	labelSuper = new QLabel( tr( "Super" ) );
	labelSuper->setAlignment( Qt::AlignHCenter );

	QHBoxLayout* layoutSuperDots = new QHBoxLayout();

	dotsSuper = new TraitDots( );
	dotsSuper->setMaximum( Config::superTraitMax );
	dotsSuper->setMinimum( Config::superTraitMin );
	// Damit später der Wert stimmt muß ich irgendeinen Wert != 1 geben, sonst wird kein Signal gesandt.
	dotsSuper->setValue( 9 );

	layoutSuperDots->addStretch();
	layoutSuperDots->addWidget( dotsSuper );
	layoutSuperDots->addStretch();

	layout->addSpacing( Config::traitCategorySpace );

	layout->addWidget( labelSuper );
	layout->addLayout( layoutSuperDots );


	labelFuel = new QLabel( tr( "Fuel" ) );
	labelFuel->setAlignment( Qt::AlignHCenter );

	QHBoxLayout* layoutFuelSquares = new QHBoxLayout();

	squaresFuel = new Squares();
	squaresFuel->setColumnMax( 10 );
	squaresFuel->setMaximum( storage->fuelMax( character->species(), character->superTrait() ) );

	fuelPerTurn = new QLabel( tr( "1" ) );
	fuelPerTurn->setAlignment( Qt::AlignCenter );

	layoutFuelSquares->addWidget( squaresFuel );
	layoutFuelSquares->addStretch();
	layoutFuelSquares->addWidget( fuelPerTurn );

	layout->addSpacing( Config::traitCategorySpace );

	layout->addWidget( labelFuel );
	layout->addLayout( layoutFuelSquares );

	layout->addStretch();

	connect( calcAdvantages, SIGNAL( sizeChanged( int ) ), this, SLOT( writeSize( int ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( writeSize( cv_Species::SpeciesFlag ) ) );
	connect( calcAdvantages, SIGNAL( initiativeChanged( int ) ), this, SLOT( writeInitiative( int ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( writeInitiative(cv_Species::SpeciesFlag)) );
	connect( calcAdvantages, SIGNAL( speedChanged( int ) ), this, SLOT( writeSpeed( int ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( writeSpeed(cv_Species::SpeciesFlag)) );
	connect( calcAdvantages, SIGNAL( defenseChanged( int ) ), labelDefenseValue, SLOT( setNum( int ) ) );
	connect( calcAdvantages, SIGNAL( healthChanged( int ) ), this, SLOT( printHealth( int ) ) );
	connect( calcAdvantages, SIGNAL( willpowerChanged( int ) ), dotsWill, SLOT( setValue( int ) ) );
	connect( spinBoxArmorGeneral, SIGNAL(valueChanged(int)), this, SLOT(setArmor()));
	connect( spinBoxArmorFirearms, SIGNAL(valueChanged(int)), this, SLOT(setArmor()));
	connect( character, SIGNAL( armorChanged(int,int)), this, SLOT( updateArmor( int, int ) ) );
// 	connect( character, SIGNAL( traitChanged( cv_Trait ) ), this, SLOT( changeSuper( cv_Trait ) ) );
// 	connect( dotsSuper, SIGNAL( valueChanged( int ) ), this, SLOT( emitSuperChanged( int ) ) );
// 	connect( this, SIGNAL( superChanged( cv_Trait ) ), character, SLOT( addTrait( cv_Trait ) ) );
	connect( dotsSuper, SIGNAL( valueChanged( int ) ), character, SLOT( setSuperTrait( int ) ) );
	connect( character, SIGNAL( superTraitChanged( int ) ), dotsSuper, SLOT( setValue( int ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hideSuper( cv_Species::SpeciesFlag ) ) );
	connect( character, SIGNAL( superTraitChanged( int ) ), this, SLOT( setFuelMaximum( int ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( setFuelMaximum( cv_Species::SpeciesFlag ) ) );

	dotsSuper->setValue( Config::superTraitDefaultValue );
}

AdvantagesWidget::~AdvantagesWidget() {
	delete fuelPerTurn;
	delete squaresFuel;
	delete dotsSuper;
	delete labelSuper;
	delete dotsHealth;
	delete labelSizeValue;
	delete labelInitiativeValue;
	delete labelSpeedValue;
	delete storage;
	delete calcAdvantages;
	delete layout;
}


void AdvantagesWidget::writeSize( int size ) {
	if ( character->species() == cv_Species::Werewolf ) {
		QString text = QString::number( calcAdvantages->size( cv_Shape::Hishu ) ) + "/" +
					   QString::number( calcAdvantages->size( cv_Shape::Dalu ) ) + "/" +
					   QString::number( calcAdvantages->size( cv_Shape::Gauru ) ) + "/" +
					   QString::number( calcAdvantages->size( cv_Shape::Urshul ) ) + "/" +
					   QString::number( calcAdvantages->size( cv_Shape::Urhan ) );
		labelSizeValue->setText( text );
	} else {
		labelSizeValue->setNum( size );
	}
}

void AdvantagesWidget::writeSize( cv_Species::SpeciesFlag species ) {
	if ( species == cv_Species::Werewolf ) {
		QString text = QString::number( calcAdvantages->size( cv_Shape::Hishu ) ) + "/" +
					   QString::number( calcAdvantages->size( cv_Shape::Dalu ) ) + "/" +
					   QString::number( calcAdvantages->size( cv_Shape::Gauru ) ) + "/" +
					   QString::number( calcAdvantages->size( cv_Shape::Urshul ) ) + "/" +
					   QString::number( calcAdvantages->size( cv_Shape::Urhan ) );
		labelSizeValue->setText( text );
	} else {
		labelSizeValue->setNum( calcAdvantages->size() );
	}
}

void AdvantagesWidget::writeInitiative( int initiative ) {
	if ( character->species() == cv_Species::Werewolf ) {
		QString text = QString::number( calcAdvantages->initiative( cv_Shape::Hishu ) ) + "/" +
					   QString::number( calcAdvantages->initiative( cv_Shape::Dalu ) ) + "/" +
					   QString::number( calcAdvantages->initiative( cv_Shape::Gauru ) ) + "/" +
					   QString::number( calcAdvantages->initiative( cv_Shape::Urshul ) ) + "/" +
					   QString::number( calcAdvantages->initiative( cv_Shape::Urhan ) );
		labelInitiativeValue->setText( text );
	} else {
		labelInitiativeValue->setNum( initiative );
	}
}

void AdvantagesWidget::writeInitiative( cv_Species::SpeciesFlag species ) {
	if ( species == cv_Species::Werewolf ) {
		QString text = QString::number( calcAdvantages->initiative( cv_Shape::Hishu ) ) + "/" +
					   QString::number( calcAdvantages->initiative( cv_Shape::Dalu ) ) + "/" +
					   QString::number( calcAdvantages->initiative( cv_Shape::Gauru ) ) + "/" +
					   QString::number( calcAdvantages->initiative( cv_Shape::Urshul ) ) + "/" +
					   QString::number( calcAdvantages->initiative( cv_Shape::Urhan ) );
		labelInitiativeValue->setText( text );
	} else {
		labelInitiativeValue->setNum( calcAdvantages->initiative() );
	}
}

void AdvantagesWidget::writeSpeed( int speed ) {
	if ( character->species() == cv_Species::Werewolf ) {
		QString text = QString::number( calcAdvantages->speed( cv_Shape::Hishu ) ) + "/" +
					   QString::number( calcAdvantages->speed( cv_Shape::Dalu ) ) + "/" +
					   QString::number( calcAdvantages->speed( cv_Shape::Gauru ) ) + "/" +
					   QString::number( calcAdvantages->speed( cv_Shape::Urshul ) ) + "/" +
					   QString::number( calcAdvantages->speed( cv_Shape::Urhan ) );
		labelSpeedValue->setText( text );
	} else {
		labelSpeedValue->setNum( speed );
	}
}

void AdvantagesWidget::writeSpeed( cv_Species::SpeciesFlag species ) {
	if ( species == cv_Species::Werewolf ) {
		QString text = QString::number( calcAdvantages->speed( cv_Shape::Hishu ) ) + "/" +
					   QString::number( calcAdvantages->speed( cv_Shape::Dalu ) ) + "/" +
					   QString::number( calcAdvantages->speed( cv_Shape::Gauru ) ) + "/" +
					   QString::number( calcAdvantages->speed( cv_Shape::Urshul ) ) + "/" +
					   QString::number( calcAdvantages->speed( cv_Shape::Urhan ) );
		labelSpeedValue->setText( text );
	} else {
		labelSpeedValue->setNum( calcAdvantages->speed() );
	}
}

void AdvantagesWidget::printHealth( int value ) {
	dotsHealth->setMaximum( value );
	dotsHealth->setValue( value );
}

void AdvantagesWidget::hideSuper( cv_Species::SpeciesFlag species ) {
	if ( species == cv_Species::Human ) {
		labelSuper->setHidden( true );
		dotsSuper->setHidden( true );

		labelFuel->setHidden( true );
		squaresFuel->setHidden( true );
		fuelPerTurn->setHidden( true );
	} else {
		labelSuper->setHidden( false );
		dotsSuper->setHidden( false );

		labelFuel->setHidden( false );
		squaresFuel->setHidden( false );
		fuelPerTurn->setHidden( false );

		for ( int i = 0; i < storage->species().count(); ++i ) {
			if ( cv_Species::toSpecies( storage->species().at( i ).name ) == species ) {
				labelSuper->setText( storage->species().at( i ).supertrait );
				labelFuel->setText( storage->species().at( i ).fuel );
			}
		}

	}
}

void AdvantagesWidget::setFuelMaximum( cv_Species::SpeciesFlag species ) {
	int maximum = storage->fuelMax( species, character->superTrait() );
	squaresFuel->setMaximum( maximum );

	int perTurn = storage->fuelPerTurn( species, character->superTrait() );
	fuelPerTurn->setText( tr( "%1/Turn" ).arg( perTurn ) );
}

void AdvantagesWidget::setFuelMaximum( int value ) {
	int maximum = storage->fuelMax( character->species(), value );
	squaresFuel->setMaximum( maximum );

	int perTurn = storage->fuelPerTurn( character->species(), value );
	fuelPerTurn->setText( tr( "%1/Turn" ).arg( perTurn ) );
}


void AdvantagesWidget::setArmor()
{
	character->setArmor(spinBoxArmorGeneral->value(), spinBoxArmorFirearms->value());
}
void AdvantagesWidget::updateArmor( int general, int firearms )
{
	spinBoxArmorGeneral->setValue(general);
	spinBoxArmorFirearms->setValue(firearms);
}





// void AdvantagesWidget::changeSuper( cv_Trait trait ) {
// 	if ( trait.type == cv_AbstractTrait::Super ) {
// 		dotsSuper->setValue( trait.value );
// 	}
// }


// void AdvantagesWidget::emitSuperChanged( int value ) {
// 	cv_Trait trait;
// 	trait.name = "Super";
// 	trait.value = value;trait.type = cv_AbstractTrait::Super;
// 	trait.category = cv_AbstractTrait::CategoryNo;
//
// 	emit superChanged(trait);
// }


