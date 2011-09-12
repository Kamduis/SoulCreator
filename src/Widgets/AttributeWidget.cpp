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

#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QGroupBox>
#include <QStringList>
#include <QDebug>

#include "CharaTrait.h"
#include "../Calc/CalcAdvantages.h"
#include "../Datatypes/cv_Trait.h"
#include "../Datatypes/cv_Shape.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"
#include "../Storage/StorageTemplate.h"

#include "AttributeWidget.h"


AttributeWidget::AttributeWidget( QWidget *parent ) : QWidget( parent )  {
	character = StorageCharacter::getInstance();

	layout = new QHBoxLayout( this );
	setLayout( layout );

// 	QFrame* frame = new QFrame( this );
// 	layout->addWidget( frame );
//
// 	QVBoxLayout* layoutHeader = new QVBoxLayout();
// 	frame->setLayout( layoutHeader );
//
// 	QLabel* labelPower = new QLabel( tr( "Power" ) );
// 	labelPower->setAlignment( Qt::AlignRight );
//
// 	QLabel* labelFinesse = new QLabel( tr( "Finesse" ) );
// 	labelFinesse->setAlignment( Qt::AlignRight );
//
// 	QLabel* labelResistance = new QLabel( tr( "Resistance" ) );
// 	labelResistance->setAlignment( Qt::AlignRight );
//
// 	layoutHeader->addWidget( labelPower, 0, 0 );
// 	layoutHeader->addWidget( labelFinesse, 1, 0 );
// 	layoutHeader->addWidget( labelResistance, 2, 0 );

	StorageTemplate storage;

	cv_Trait::Type type = cv_Trait::Attribute;

	QList< cv_Trait::Category > categories = cv_Trait::getCategoryList( type );

	QList< cv_Trait* > list;

	labelStr = new QLabel( this );
	labelDex = new QLabel( this );
	labelSta = new QLabel( this );

	connect( this, SIGNAL( speciesChanged( bool ) ), labelStr, SLOT( setHidden( bool ) ) );
	connect( this, SIGNAL( speciesChanged( bool ) ), labelDex, SLOT( setHidden( bool ) ) );
	connect( this, SIGNAL( speciesChanged( bool ) ), labelSta, SLOT( setHidden( bool ) ) );

	for ( int i = 0; i < categories.count(); i++ ) {
		list = storage.traitsPtr( type, categories.at( i ) );
		QGroupBox* categoriesBox = new QGroupBox();
		QVBoxLayout* layoutCategories = new QVBoxLayout();
		categoriesBox->setLayout( layoutCategories );

		layout->addWidget( categoriesBox );

		for ( int j = 0; j < list.count(); j++ ) {
			// Jedes einzelne Attribut wird nochmal in ein hor. Layout gesteckt, damit ich bei den Werwölfen die Attributswerte aller Formen angeben kann.
			QHBoxLayout* layoutAttribute = new QHBoxLayout();
			layoutCategories->addLayout( layoutAttribute );

			// Anlegen der Eigenschaft im Speicher
			cv_Trait* traitPtr = character->addTrait( *list[j] );

			// Anlegen des Widgets, das diese Eigenschaft repräsentiert.
			CharaTrait *trait = new CharaTrait( this, traitPtr, list[j] );
			trait->setValue( 1 );

			layoutAttribute->addWidget( trait );

			if ( trait->category() == cv_Trait::Physical ) {
				if ( trait->name() == "Strength" ) {
					layoutAttribute->addWidget( labelStr );
					connect( trait, SIGNAL( valueChanged( int ) ), this, SLOT( updateshapeValuesStr( int ) ) );
				} else if ( trait->name() == "Dexterity" ) {
					layoutAttribute->addWidget( labelDex );
					connect( trait, SIGNAL( valueChanged( int ) ), this, SLOT( updateshapeValuesDex( int ) ) );
				} else if ( trait->name() == "Stamina" ) {
					layoutAttribute->addWidget( labelSta );
					connect( trait, SIGNAL( valueChanged( int ) ), this, SLOT( updateshapeValuesSta( int ) ) );
				}
			}

		}
	}

	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( emitSpeciesChanged( cv_Species::SpeciesFlag ) ) );
}

AttributeWidget::~AttributeWidget() {
	delete labelStr;
	delete labelDex;
	delete labelSta;
	delete layout;
}


void AttributeWidget::updateshapeValuesStr( int val ) {
	QStringList txt;

	// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	for ( int i = 1; i < cv_Shape::getShapeList().count(); i++ ) {
		txt.append( QString::number( CalcAdvantages::strength( val, cv_Shape::getShapeList().at( i ) ) ) );
	}

	labelStr->setText( txt.join( "/" ) );
}

void AttributeWidget::updateshapeValuesDex( int val ) {
	QStringList txt;

	// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	for ( int i = 1; i < cv_Shape::getShapeList().count(); i++ ) {
		txt.append( QString::number( CalcAdvantages::dexterity( val, cv_Shape::getShapeList().at( i ) ) ) );
	}

	labelDex->setText( txt.join( "/" ) );
}

void AttributeWidget::updateshapeValuesSta( int val ) {
	QStringList txt;

	// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	for ( int i = 1; i < cv_Shape::getShapeList().count(); i++ ) {
		txt.append( QString::number( CalcAdvantages::stamina( val, cv_Shape::getShapeList().at( i ) ) ) );
	}

	labelSta->setText( txt.join( "/" ) );
}

void AttributeWidget::emitSpeciesChanged( cv_Species::SpeciesFlag spe ) {
	if ( spe == cv_Species::Werewolf ) {
		emit speciesChanged( false );
	} else {
		emit speciesChanged( true );
	}
}
