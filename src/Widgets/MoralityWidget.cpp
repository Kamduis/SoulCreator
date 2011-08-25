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

#include <QLineEdit>
#include <QDebug>

#include "TraitDots.h"
#include "../Storage/StorageTemplate.h"
#include "../Config/Config.h"

#include "MoralityWidget.h"


MoralityWidget::MoralityWidget( QWidget *parent ) : QWidget( parent )  {
	v_value = 0;
	
	storage = new StorageTemplate( this );
	character = StorageCharacter::getInstance();

	layout = new QGridLayout( this );
	setLayout( layout );

	labelHeader = new QLabel();
	labelHeader->setAlignment(Qt::AlignHCenter);

	layout->addWidget( labelHeader, 0, 0, 1, 3 );

	int layoutLine;

	for ( int i = Config::moralityTraitMax; i > 0; i-- ) {
		layoutLine =  Config::moralityTraitMax - i + 1;

		QLabel* label = new QLabel( QString::number( i ) );
		TraitDots* traitDots = new TraitDots();
		traitDots->setMaximum( 1 );

		layout->addWidget( label, layoutLine, 0 );
		layout->addWidget( traitDots, layoutLine, 2 );

		if ( i <= Config::derangementMoralityTraitMax ) {
			QLineEdit* lineEdit = new QLineEdit();

			layout->addWidget( lineEdit, layoutLine, 1 );
		}

		connect( traitDots, SIGNAL( valueClicked( int ) ), this, SLOT( resetValue( int ) ) );
	}

	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( renameHeader( cv_Species::SpeciesFlag ) ) );
	connect( character, SIGNAL( moralityChanged(int)), this, SLOT( setValue( int ) ) );
	connect( this, SIGNAL( valueChanged(int)), character, SLOT( setMorality( int ) ) );
	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( drawValue( int ) ) );

	setValue( Config::moralityTraitDefaultValue );
}

MoralityWidget::~MoralityWidget() {
	delete labelHeader;
	delete storage;
	delete layout;
}


int MoralityWidget::value() const {
	return v_value;
}

void MoralityWidget::setValue( int value ) {
	if ( v_value != value ) {
		v_value = value;
		emit valueChanged( value );
	}
}

void MoralityWidget::drawValue( int value ) {
	int i = 0;
	while ( i < value ) {
		TraitDots* traitDots = qobject_cast<TraitDots*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 2 )->widget() );
		traitDots->setValue(1);
		i++;
	}
	while ( i < layout->rowCount() - 1 ) {
		TraitDots* traitDots = qobject_cast<TraitDots*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 2 )->widget() );
		traitDots->setValue(0);
		i++;
	}
}


void MoralityWidget::resetValue( int value ) {
	// Verändere ich einen Punkt zu 1, wird der Gesamtwert erhöht, verändere ich einen Wert zu 0 wird der Gesamtwert reduziert.
	bool reduceValue = true;
	if ( value > 0 ) {
		reduceValue = false;
	}

	int newValue;

	bool changeFromHere = false;

	if ( reduceValue ) {
		for ( int i = layout->rowCount() - 1; i > 0; i-- ) {
			TraitDots* traitDots = qobject_cast<TraitDots*>( layout->itemAtPosition( i, 2 )->widget() );

			if ( traitDots->value() < 1 ) {
				newValue = layout->rowCount() - i;

				// Der Knopf auf den ich Drücke, soll schwarz bleiben. Esseidenn natürlich, es ist der unterste, und zuvor war der Wert schon 1, dann soll er abgewählt werden.
				if ( v_value == 1 && i == layout->rowCount() - 1 ) {
					newValue = 0;
				}

				break;
			}
		}
	} else {
		for ( int i = 1; i < layout->rowCount(); i++ ) {
			TraitDots* traitDots = qobject_cast<TraitDots*>( layout->itemAtPosition( i, 2 )->widget() );

			if ( traitDots->value() > 0 ) {
				newValue = layout->rowCount() - i;
				break;
			}
		}
	}
	if ( v_value != newValue ) {
		v_value = newValue;
// 		qDebug() << Q_FUNC_INFO << "Neuer Wert bei Herunterzählen:" << newValue;
		emit valueChanged( newValue );
	}
}


void MoralityWidget::renameHeader( cv_Species::SpeciesFlag species ) {
	for ( int i = 0; i < storage->species().count(); i++ ) {
		if ( cv_Species::toSpecies( storage->species().at( i ).name ) == species ) {
			labelHeader->setText( storage->species().at( i ).morale );
		}
	}
}






