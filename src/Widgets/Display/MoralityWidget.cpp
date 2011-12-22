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

#include <QLineEdit>
#include <QDebug>

#include "Widgets/Components/DerangementComboBox.h"
#include "Widgets/Components/TraitDots.h"
// #include "Storage/StorageTemplate.h"
// #include "Datatypes/cv_Derangement.h"
#include "Config/Config.h"

#include "MoralityWidget.h"


MoralityWidget::MoralityWidget( QWidget *parent ) : QWidget( parent )  {
	v_value = 0;

	storage = new StorageTemplate( this );
	character = StorageCharacter::getInstance();

	layout = new QGridLayout( this );
	setLayout( layout );

	labelHeader = new QLabel();
	labelHeader->setAlignment( Qt::AlignHCenter );

	layout->addWidget( labelHeader, 0, 0, 1, 3 );

	int layoutLine;

	QList< cv_Trait > list;
	v_category = cv_AbstractTrait::getCategoryList( cv_AbstractTrait::Derangement );

	for ( int i = Config::moralityTraitMax; i > 0; i-- ) {
		layoutLine =  Config::moralityTraitMax - i + 1;

		QLabel* label = new QLabel( QString::number( i ) );
		TraitDots* traitDots = new TraitDots();
		traitDots->setMaximum( 1 );

		layout->addWidget( label, layoutLine, 0 );
		layout->addWidget( traitDots, layoutLine, 2 );

		if ( i <= Config::derangementMoralityTraitMax ) {
			DerangementComboBox* comboBox = new DerangementComboBox();
			comboBox->setMaximumHeight( Config::inlineWidgetHeightMax );

			layout->addWidget( comboBox, layoutLine, 1 );

			connect( comboBox, SIGNAL( currentIndexChanged( cv_Derangement ) ), this, SLOT( saveDerangements( cv_Derangement ) ) );
			connect( character, SIGNAL( derangementsChanged() ), this, SLOT( updateDerangements() ) );
		}

		connect( traitDots, SIGNAL( valueClicked( int ) ), this, SLOT( resetValue( int ) ) );
	}

	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( renameHeader( cv_Species::SpeciesFlag ) ) );

	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( updateDerangements( cv_Species::SpeciesFlag ) ) );
	connect( character, SIGNAL( moralityChanged( int ) ), this, SLOT( setValue( int ) ) );
	connect( this, SIGNAL( valueChanged( int ) ), character, SLOT( setMorality( int ) ) );
	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( drawValue( int ) ) );
	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( disableDerangements( int ) ) );

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
		traitDots->setValue( 1 );
		i++;
	}

	while ( i < layout->rowCount() - 1 ) {
		TraitDots* traitDots = qobject_cast<TraitDots*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 2 )->widget() );
		traitDots->setValue( 0 );
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

				// Der Knopf auf den ich drücke, soll schwarz bleiben. Esseidenn natürlich, es ist der unterste, und zuvor war der Wert schon 1, dann soll er abgewählt werden.

				if ( v_value == 1 && i == layout->rowCount() - 1 ) {
					newValue = 0;
				}

				break;
			}
		}
	} else {
		for ( int i = 1; i < layout->rowCount(); ++i ) {
			TraitDots* traitDots = qobject_cast<TraitDots*>( layout->itemAtPosition( i, 2 )->widget() );

			if ( traitDots->value() > 0 ) {
				newValue = layout->rowCount() - i;
				break;
			}
		}
	}

	// Hiermit wird ein zuvor weißgeklickter Punkt (Es ist ja jeweils ein 1-Punkte Trait angenommen) wieder schwarz gesetzt.
	drawValue( newValue );

	if ( v_value != newValue ) {
		v_value = newValue;
// 		qDebug() << Q_FUNC_INFO << "Neuer Wert bei Herunterzählen:" << newValue;
		emit valueChanged( newValue );
	}
}


void MoralityWidget::renameHeader( cv_Species::SpeciesFlag species ) {
	for ( int i = 0; i < storage->species().count(); ++i ) {
		if ( cv_Species::toSpecies( storage->species().at( i ).name ) == species ) {
			labelHeader->setText( "<b>" + storage->species().at( i ).morale + "</b>" );
		}
	}
}

void MoralityWidget::updateDerangements( cv_Species::SpeciesFlag species ) {
	QList< Trait* > list;
	QList< cv_Derangement > listToUse;

	for ( int j = 0; j < v_category.count(); ++j ) {
		list = storage->traits( cv_AbstractTrait::Derangement, v_category.at( j ) );

		for ( int k = 0; k < list.count(); ++k ) {
			if ( list.at( k )->species().testFlag( species ) ) {
				cv_Derangement lcl_derangement( list.at( k )->name(), 0, list.at( k )->species(), list.at( k )->category() );

// 				qDebug() << Q_FUNC_INFO << lcl_derangement.name << lcl_derangement.morality;

				listToUse.append( lcl_derangement );
			}
		}
	}

	for ( int i = 0; i < Config::derangementMoralityTraitMax; ++i ) {
		DerangementComboBox* comboBox = qobject_cast<DerangementComboBox*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 1 )->widget() );
		comboBox->clear();

		cv_Derangement emptyDerangement;

		comboBox->addItem( emptyDerangement );
		comboBox->addItems( listToUse );
	}
}

void MoralityWidget::updateDerangements() {
	QList< cv_Derangement* > list;
	QList< cv_AbstractTrait::Category > category = cv_AbstractTrait::getCategoryList( cv_AbstractTrait::Derangement );

	for ( int i = 0; i < category.count(); ++i ) {
		list.append( character->derangements( category.at( i ) ) );
	}

	for ( int i = 0; i < Config::derangementMoralityTraitMax; ++i ) {
		DerangementComboBox* comboBox = qobject_cast<DerangementComboBox*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 1 )->widget() );

		// Ist die Liste leer, werden alle Geistesstörungen auf Index 0 gesetzt.
		if ( list.count() == 0 ) {
			comboBox->setCurrentIndex( 0 );
		} else {
			for ( int k = 0; k < list.count(); ++k ) {
				if ( list.at( k )->morality() == i + 1 ) {
					comboBox->setCurrentIndex( comboBox->findText( list.at( k )->name() ) );
					break;
				} else if ( k == list.count() - 1 ) {	// Taucht keine Geistesstörung bei dieser Moralstufe in der Liste auzf, wird der Index auf 0 gesetzt.
					comboBox->setCurrentIndex( 0 );
				}
			}
		}
	}
}



void MoralityWidget::disableDerangements( int value ) {
	int lcl_value = value;

	if ( lcl_value > Config::derangementMoralityTraitMax ) {
		lcl_value = Config::derangementMoralityTraitMax;
	}

	int i = 0;

	while ( i < lcl_value ) {
		DerangementComboBox* comboBox = qobject_cast<DerangementComboBox*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 1 )->widget() );
		comboBox->setCurrentIndex( 0 );
		comboBox->setEnabled( false );
		i++;
	}

	while ( i < Config::derangementMoralityTraitMax ) {
		DerangementComboBox* comboBox = qobject_cast<DerangementComboBox*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 1 )->widget() );
		comboBox->setEnabled( true );
		i++;
	}
}

void MoralityWidget::saveDerangements( cv_Derangement dera ) {
	cv_Derangement derang;

	for ( int i = 0; i < Config::derangementMoralityTraitMax; ++i ) {
		DerangementComboBox* comboBox = qobject_cast<DerangementComboBox*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 1 )->widget() );

		if ( comboBox->currentItem() == dera ) {
			derang = dera;
			derang.setMorality(i + 1);
			break;
		}
	}

	character->addDerangement( derang );
}


