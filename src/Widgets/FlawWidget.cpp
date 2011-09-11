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

#include <QVBoxLayout>
#include <QGroupBox>
#include <QDebug>

#include "CheckTrait.h"
#include "../Datatypes/cv_Trait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"
#include "../Storage/StorageTemplate.h"

#include "FlawWidget.h"


FlawWidget::FlawWidget( QWidget *parent ) : QWidget( parent )  {
	QVBoxLayout* layoutTop = new QVBoxLayout( this );
	setLayout( layoutTop );

	scrollArea = new QScrollArea( this );
	scrollArea->setSizePolicy( QSizePolicy::MinimumExpanding, QSizePolicy::Expanding );
	scrollArea->setWidgetResizable( true );
	scrollArea->setFrameStyle( 0 );

	layoutTop->addWidget( scrollArea );

	toolBox = new QToolBox();
	toolBox->setSizePolicy( QSizePolicy::Preferred, QSizePolicy::Expanding );

	scrollArea->setWidget( toolBox );
	toolBox->show();

	storage = new StorageTemplate( this );

	cv_Trait::Type type = cv_Trait::Flaw;

	v_categories = cv_Trait::getCategoryList( type );

	QList< cv_Trait* > list;

	// Merits werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.
	for ( int i = 0; i < v_categories.count(); i++ ) {
		// Für jede Kategorie wird ein eigener Abschnitt erzeugt.
		QWidget* widgetFlawCategory = new QWidget();
		QVBoxLayout* layoutFlawCategory = new QVBoxLayout();
		widgetFlawCategory->setLayout( layoutFlawCategory );
		toolBox->addItem( widgetFlawCategory, cv_Trait::toString( v_categories.at( i ), true ) );

		list = storage->traitsPtr( type, v_categories.at( i ) );

		for ( int j = 0; j < list.count(); j++ ) {
			for ( int k = 0; k < Config::traitMultipleMax; k++ ) {
				// Anlegen der Eigenschaft im Speicher
				cv_Trait* traitPtr = character->addTrait( *list[j] );

				// Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				CheckTrait *checkTrait = new CheckTrait( this, traitPtr, list[j] );
				checkTrait->setValue( 0 );
				layoutFlawCategory->addWidget( checkTrait );

				connect( checkTrait, SIGNAL( stateChanged( int ) ), this, SLOT( countItems() ) );

				// Eigenschaften mit Beschreibungstext werden mehrfach dargestellt, da man sie ja auch mehrfach erwerben kann. Alle anderen aber immer nur einmal.

				if ( !list.at( j )->custom ) {
					break;
				}
			}
		}

		// Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
		layoutFlawCategory->addStretch();
	}
}

FlawWidget::~FlawWidget() {
	delete storage;
	delete toolBox;
// 	delete dialog;
// 	delete button;
	delete scrollArea;
}


void FlawWidget::countItems() {
	for (int i = 0; i < v_categories.count(); i++){
		QList< cv_Trait > list = character->traits( cv_Trait::Flaw, v_categories.at(i) );

		int numberInCategory = 0;

		for ( int j = 0; j < list.count(); j++ ) {
			if ( list.at( j ).value > 0 ) {
				numberInCategory++;
			}
		}

		// Index der veränderten Kategorie in Liste suchen und dann die toolBox-Seite mit der identischen Indexzahl anpassen.
		int categoryIndex = v_categories.indexOf( v_categories.at(i) );

		if ( numberInCategory > 0 ) {
			toolBox->setItemText( categoryIndex, cv_Trait::toString( v_categories.at( categoryIndex ), true ) + " (" + QString::number( numberInCategory ) + ")" );
		} else {
			toolBox->setItemText( categoryIndex, cv_Trait::toString( v_categories.at( categoryIndex ), true ) );
		}
	}
}
