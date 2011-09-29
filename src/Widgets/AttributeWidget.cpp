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
 * along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QGroupBox>
#include <QStringList>
#include <QDebug>

#include "CharaTrait2.h"
#include "Calc/CalcAdvantages.h"
#include "Datatypes/cv_Trait.h"
#include "Datatypes/cv_Shape.h"
#include "Exceptions/Exception.h"
#include "Config/Config.h"
#include "Storage/StorageTemplate.h"
#include "Widgets/Dialogs/MessageBox.h"

#include "AttributeWidget.h"


AttributeWidget::AttributeWidget( QWidget *parent ) : QWidget( parent )  {
	character = StorageCharacter::getInstance();

	layout = new QGridLayout( this );
	setLayout( layout );

// 	QFrame* frame = new QFrame( this );
// 	layout->addWidget( frame );
//
// 	QVBoxLayout* layoutHeader = new QVBoxLayout();
// 	frame->setLayout( layoutHeader );
//
	QLabel* labelPower = new QLabel( "<b>" + tr( "Power" ) + "</b>" );
	labelPower->setAlignment( Qt::AlignRight );

	QLabel* labelFinesse = new QLabel( "<b>" + tr( "Finesse" ) + "</b>" );
	labelFinesse->setAlignment( Qt::AlignRight );

	QLabel* labelResistance = new QLabel( "<b>" + tr( "Resistance" ) + "</b>" );
	labelResistance->setAlignment( Qt::AlignRight );

	int actualRow = 1;
	int actualColumn = 0;

	layout->addWidget( labelPower, actualRow, actualColumn );
	actualRow++;
	layout->addWidget( labelFinesse, actualRow, actualColumn );
	actualRow++;
	layout->addWidget( labelResistance, actualRow, actualColumn );

	StorageTemplate storage;

	cv_Trait::Type type = cv_Trait::Attribute;

	QList< cv_Trait::Category > categories = cv_Trait::getCategoryList( type );

	QList< Trait* > list;

	labelStr = new QLabel( this );
	labelDex = new QLabel( this );
	labelSta = new QLabel( this );
	labelMan = new QLabel( this );

	connect( this, SIGNAL( speciesChanged( bool ) ), labelStr, SLOT( setHidden( bool ) ) );
	connect( this, SIGNAL( speciesChanged( bool ) ), labelDex, SLOT( setHidden( bool ) ) );
	connect( this, SIGNAL( speciesChanged( bool ) ), labelSta, SLOT( setHidden( bool ) ) );
	connect( this, SIGNAL( speciesChanged( bool ) ), labelMan, SLOT( setHidden( bool ) ) );

	for ( int i = 0; i < categories.count(); i++ ) {
		try {
			list = storage.traits2( type, categories.at( i ) );
		} catch (eTraitNotExisting &e) {
			MessageBox::exception(this, e.message(), e.description());
		}

		// Zeichnen des Separators zwischen den einzelnen Kategorien
		actualColumn++;

		QFrame* vLine = new QFrame( this );
		vLine->setFrameStyle( QFrame::VLine );
		layout->addWidget( vLine, 1, actualColumn, list.count(), 1, Qt::AlignHCenter );

// 		layout->setColumnMinimumWidth(actualColumn, Config::traitCategorySpace);
		layout->setColumnStretch( actualColumn, 1 );

		// Jetzt sind wir in der Spalte für die tatsächlchen Attribute
		actualColumn++;

		// Aber zuerst kommt die Überschrift für die einzelnen Kategorien.
		QLabel* header = new QLabel();
		header->setAlignment( Qt::AlignHCenter );
		header->setText( "<b>" + cv_Trait::toString( categories.at( i ) ) + "</b>" );
		layout->addWidget( header, 0, actualColumn );

		// Einfügen der tatsächlichen Attribute

		for ( int j = 0; j < list.count(); j++ ) {
			// Anlegen der Eigenschaft im Speicher
			Trait* traitPtr = character->addTrait( list[j] );

			// Anlegen des Widgets, das diese Eigenschaft repräsentiert.
			CharaTrait2* trait = new CharaTrait2( this, traitPtr, list[j] );
			trait->setValue( 1 );

			layout->addWidget( trait, j + 1, actualColumn );

			if ( trait->category() == cv_Trait::Physical ) {
				if ( trait->name() == "Strength" ) {
					layout->addWidget( labelStr, j + 1, actualColumn + 1 );
					connect( trait, SIGNAL( valueChanged( int ) ), this, SLOT( updateshapeValuesStr( int ) ) );
				} else if ( trait->name() == "Dexterity" ) {
					layout->addWidget( labelDex, j + 1, actualColumn + 1 );
					connect( trait, SIGNAL( valueChanged( int ) ), this, SLOT( updateshapeValuesDex( int ) ) );
				} else if ( trait->name() == "Stamina" ) {
					layout->addWidget( labelSta, j + 1, actualColumn + 1 );
					connect( trait, SIGNAL( valueChanged( int ) ), this, SLOT( updateshapeValuesSta( int ) ) );
				}
			} else if ( trait->category() == cv_Trait::Social ) {
				if ( trait->name() == "Manipulation" ) {
					layout->addWidget( labelMan, j + 1, actualColumn + 1 );
					connect( trait, SIGNAL( valueChanged( int ) ), this, SLOT( updateshapeValuesMan( int ) ) );
				}
			}
		}

		// Bei Werwölfen erscheint hier zusatztext. Und damit der Sparator richtig gesetzt wird, muß die aktuelle Spalte ein weitergezählt werden.
		actualColumn++;
	}

	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( emitSpeciesChanged( cv_Species::SpeciesFlag ) ) );
}

AttributeWidget::~AttributeWidget() {
	delete labelMan;
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

void AttributeWidget::updateshapeValuesMan( int val ) {
	QStringList txt;

	// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	for ( int i = 1; i < cv_Shape::getShapeList().count(); i++ ) {
		txt.append( QString::number( CalcAdvantages::manipulation( val, cv_Shape::getShapeList().at( i ) ) ) );
	}

	labelMan->setText( txt.join( "/" ) );
}

void AttributeWidget::emitSpeciesChanged( cv_Species::SpeciesFlag spe ) {
	if ( spe == cv_Species::Werewolf ) {
		emit speciesChanged( false );
	} else {
		emit speciesChanged( true );
	}
}
