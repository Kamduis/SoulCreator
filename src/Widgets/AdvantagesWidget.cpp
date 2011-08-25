/**
 * \file
 * \author Victor von Rhein <goliath@caern.de>
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
 * along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <QSpinBox>
#include <QDebug>

#include "CharaTrait.h"
#include "../Datatypes/cv_Trait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"

#include "AdvantagesWidget.h"


AdvantagesWidget::AdvantagesWidget( QWidget *parent ) : QWidget( parent )  {
	calcAdvantages = new CalcAdvantages( this );
	moralityWidget = new MoralityWidget( this );
	storage = new StorageTemplate( this );
	character = StorageCharacter::getInstance();

	layout = new QVBoxLayout( this );
	layout->setMargin( 0 );

	advantagesLayout = new QGridLayout();
	advantagesLayout->setColumnMinimumWidth( 1, 0 );

	setLayout( layout );

	layout->addLayout( advantagesLayout );

	QLabel* labelSize = new QLabel( tr( "Size:" ) );
	QLabel* labelSizeValue = new QLabel( this );
	labelSizeValue->setNum( 0 );

	QLabel* labelInitiative = new QLabel( tr( "Initiative:" ) );
	QLabel* labelInitiativeValue = new QLabel( this );
	labelInitiativeValue->setNum( 0 );

	QLabel* labelSpeed = new QLabel( tr( "Speed:" ) );
	QLabel* labelSpeedValue = new QLabel( this );
	labelSpeedValue->setNum( 0 );

	QLabel* labelDefense = new QLabel( tr( "Defense:" ) );
	QLabel* labelDefenseValue = new QLabel( this );
	labelDefenseValue->setNum( 0 );

	QLabel* labelArmor = new QLabel( tr( "Armor:" ) );
	QSpinBox* spinBoxArmor = new QSpinBox( this );
	spinBoxArmor->setMinimum( 0 );

	advantagesLayout->addWidget( labelSize, 0, 0 );
	advantagesLayout->addWidget( labelSizeValue, 0, 1 );
	advantagesLayout->addWidget( labelInitiative, 1, 0 );
	advantagesLayout->addWidget( labelInitiativeValue, 1, 1 );
	advantagesLayout->addWidget( labelSpeed, 2, 0 );
	advantagesLayout->addWidget( labelSpeedValue, 2, 1 );
	advantagesLayout->addWidget( labelDefense, 3, 0 );
	advantagesLayout->addWidget( labelDefenseValue, 3, 1 );
	advantagesLayout->addWidget( labelArmor, 4, 0 );
	advantagesLayout->addWidget( spinBoxArmor, 4, 1 );

	QLabel* labelHealth = new QLabel( tr( "Health" ) );
	labelHealth->setAlignment( Qt::AlignHCenter );

	QHBoxLayout* layoutHealthDots = new QHBoxLayout();

	dotsHealth = new TraitDots( );
	dotsHealth->setReadOnly(true);

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
	dotsWill->setReadOnly(true);

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
	dotsSuper->setReadOnly(true);

	layoutSuperDots->addStretch();
	layoutSuperDots->addWidget( dotsSuper );
	layoutSuperDots->addStretch();

	layout->addSpacing( Config::traitCategorySpace );

	layout->addWidget( labelSuper );
	layout->addLayout( layoutSuperDots );

	layout->addSpacing( Config::traitCategorySpace );

	layout->addWidget( moralityWidget );

	layout->addStretch();

	connect( calcAdvantages, SIGNAL( sizeChanged( int ) ), labelSizeValue, SLOT( setNum( int ) ) );
	connect( calcAdvantages, SIGNAL( initiativeChanged( int ) ), labelInitiativeValue, SLOT( setNum( int ) ) );
	connect( calcAdvantages, SIGNAL( speedChanged( int ) ), labelSpeedValue, SLOT( setNum( int ) ) );
	connect( calcAdvantages, SIGNAL( defenseChanged( int ) ), labelDefenseValue, SLOT( setNum( int ) ) );
	connect( calcAdvantages, SIGNAL( healthChanged( int ) ), this, SLOT( printHealth( int ) ) );
	connect( calcAdvantages, SIGNAL( willpowerChanged( int ) ), dotsWill, SLOT( setValue(int)) );
// 	connect( character, SIGNAL( traitChanged( cv_Trait ) ), this, SLOT( changeSuper( cv_Trait ) ) );
// 	connect( dotsSuper, SIGNAL( valueChanged( int ) ), this, SLOT( emitSuperChanged( int ) ) );
// 	connect( this, SIGNAL( superChanged( cv_Trait ) ), character, SLOT( addTrait( cv_Trait ) ) );
	connect( dotsSuper, SIGNAL( valueChanged( int ) ), character, SLOT( setSuperTrait( int ) ) );
	connect( character, SIGNAL( superTraitChanged( int ) ), dotsSuper, SLOT( setValue( int ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hideSuper( cv_Species::SpeciesFlag ) ) );

	dotsSuper->setValue( Config::superTraitDefaultValue );
}

AdvantagesWidget::~AdvantagesWidget() {
	delete dotsSuper;
	delete labelSuper;
	delete dotsHealth;
	delete storage;
	delete moralityWidget;
	delete calcAdvantages;
	delete layout;
}


void AdvantagesWidget::printHealth( int value ) {
	dotsHealth->setMaximum( value );
	dotsHealth->setValue( value );
}

void AdvantagesWidget::hideSuper( cv_Species::SpeciesFlag species ) {
	if ( species == cv_Species::Human ) {
		labelSuper->setHidden( true );
		dotsSuper->setHidden( true );
	} else {
		labelSuper->setHidden( false );
		dotsSuper->setHidden( false );

		for ( int i = 0; i < storage->species().count(); i++ ) {
			if ( cv_Species::toSpecies( storage->species().at( i ).name ) == species ) {
				labelSuper->setText( storage->species().at( i ).supertrait );
			}
		}

	}
}

// void AdvantagesWidget::changeSuper( cv_Trait trait ) {
// 	if ( trait.type == cv_Trait::Super ) {
// 		dotsSuper->setValue( trait.value );
// 	}
// }


// void AdvantagesWidget::emitSuperChanged( int value ) {
// 	cv_Trait trait;
// 	trait.name = "Super";
// 	trait.value = value;trait.type = cv_Trait::Super;
// 	trait.category = cv_Trait::CategoryNo;
//
// 	emit superChanged(trait);
// }


