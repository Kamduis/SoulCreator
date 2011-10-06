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

// #include <QToolBox>
#include <QDebug>

#include "CharaTrait.h"
// #include "Exceptions/Exception.h".h"
// #include "Config/Config.h"
#include "Widgets/Dialogs/MessageBox.h"

#include "MeritWidget.h"


MeritWidget::MeritWidget( QWidget *parent ) : QWidget( parent )  {
	layout = new QHBoxLayout( this );
	setLayout( layout );

	toolBox = new QToolBox();

	layout->addWidget(toolBox);

	storage = new StorageTemplate( this );

	cv_AbstractTrait::Type type = cv_AbstractTrait::Merit;

	v_category = cv_AbstractTrait::getCategoryList(type);

	QList< Trait* > list;

	// Merits werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.
	for ( int i = 0; i < v_category.count(); i++ ) {
		// Für jede Kategorie wird ein eigener Abschnitt erzeugt.
		QWidget* widgetMeritCategory = new QWidget();
		QVBoxLayout* layoutMeritCategory = new QVBoxLayout();
		
		widgetMeritCategory->setLayout( layoutMeritCategory );
		
		toolBox->addItem( widgetMeritCategory, cv_AbstractTrait::toString( v_category.at( i ), true ) );

		try {
			list = storage->traits( type, v_category.at( i ) );
		} catch (eTraitNotExisting &e) {
			MessageBox::exception(this, e.message(), e.description());
		}

		for ( int j = 0; j < list.count(); j++ ) {
			for ( int k = 0; k < Config::traitMultipleMax; k++ ) {
				// Anlegen der Eigenschaft im Speicher
				Trait* traitPtr = character->addTrait( list[j] );

				// Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				CharaTrait* charaTrait = new CharaTrait( this, traitPtr, list[j] );
				charaTrait->setValue( 0 );
				layoutMeritCategory->addWidget( charaTrait );

				connect( charaTrait, SIGNAL( valueChanged( int ) ), this, SLOT( countMerits() ) );

				// Eigenschaften mit Beschreibungstext werden mehrfach dargestellt, da man sie ja auch mehrfach erwerben kann. Alle anderen aber immer nur einmal.

				if ( !list.at( j )->custom() ) {
					break;
				}
			}
		}

		// Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
		layoutMeritCategory->addStretch();
	}

// 	dialog = new SelectMeritsDialog( this );
//
// 	QHBoxLayout* layout_button = new QHBoxLayout();
// 	layoutTop->addLayout( layout_button );
//
// 	button = new QPushButton();
// 	button->setIcon( style()->standardIcon( QStyle::SP_FileDialogStart ) );
//
// 	layout_button->addStretch();
// 	layout_button->addWidget( button );
//
// 	connect( button, SIGNAL( clicked( bool ) ), dialog, SLOT( exec() ) );
}

MeritWidget::~MeritWidget() {
	delete storage;
	delete toolBox;
// 	delete dialog;
// 	delete button;
	delete layout;
}


void MeritWidget::countMerits() {
	for (int i = 0; i < v_category.count(); i++){
		QList< Trait* > list = character->traits( cv_AbstractTrait::Merit, v_category.at(i) );

		int numberInCategory = 0;

		for ( int j = 0; j < list.count(); j++ ) {
			if ( list.at( j )->value() > 0 ) {
				numberInCategory++;
			}
		}

		// Index der veränderten Kategorie in Liste suchen und dann die toolBox-Seite mit der identischen Indexzahl anpassen.
		int categoryIndex = v_category.indexOf( v_category.at(i) );

		if ( numberInCategory > 0 ) {
			toolBox->setItemText( categoryIndex, cv_AbstractTrait::toString( v_category.at( categoryIndex ), true ) + " (" + QString::number( numberInCategory ) + ")" );
		} else {
			toolBox->setItemText( categoryIndex, cv_AbstractTrait::toString( v_category.at( categoryIndex ), true ) );
		}
	}
}

