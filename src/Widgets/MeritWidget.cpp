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

#include <QGridLayout>
#include <QToolBox>
#include <QDebug>

#include "CharaTrait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"
#include "../CMakeConfig.h"

#include "MeritWidget.h"


MeritWidget::MeritWidget( QWidget *parent ) : QWidget( parent )  {
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

	cv_Trait::Type type = cv_Trait::Merit;

	v_categories.clear();
	v_categories.append( cv_Trait::Mental );
	v_categories.append( cv_Trait::Physical );
	v_categories.append( cv_Trait::Social );
	v_categories.append( cv_Trait::Item );
	v_categories.append( cv_Trait::FightingStyle );
	v_categories.append( cv_Trait::DebateStyle );
	v_categories.append( cv_Trait::Extraordinary );
	v_categories.append( cv_Trait::Species );

	QList< cv_Trait > list;

	// Merits werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.

	for ( int i = 0; i < v_categories.count(); i++ ) {
		// Für jede Kategorie wird ein eigener Abschnitt erzeugt.
		QWidget* widgetMeritCategory = new QWidget();
		QVBoxLayout* layoutMeritCategory = new QVBoxLayout();
		widgetMeritCategory->setLayout( layoutMeritCategory );
		toolBox->addItem( widgetMeritCategory, cv_Trait::toString( v_categories.at( i ), true ) );

		list = storage->merits( v_categories.at( i ) );

		for ( int j = 0; j < list.count(); j++ ) {
			for ( int k = 0; k < Config::traitMultipleMax; k++ ) {
				CharaTrait *charaTrait = new CharaTrait( this, list.at( j ) );
				// Wert definitiv ändern, damit alle Werte in den Charakter-Speicher übernommen werden.
				charaTrait->setValue( 5 );
				charaTrait->setValue( 0 );
				layoutMeritCategory->addWidget( charaTrait );

				connect( charaTrait, SIGNAL( traitChanged( cv_Trait ) ), this, SLOT( countMerits( cv_Trait ) ) );

				// Eigenschaften mit Beschreibungstext werden mehrfach dargestellt, da man sie ja auch mehrfach erwerben kann. Alle anderen aber immer nur einmal.

				if ( !list.at( j ).custom ) {
					break;
				}
			}
		}

// 		// Abstand zwischen den Kategorien, aber nicht am Ende.
// 		if ( i < categories.count() - 1 ) {
// 			layoutMeritCategory->addSpacing( Config::traitCategorySpace );
// 		}
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
	delete scrollArea;
}


void MeritWidget::countMerits( cv_Trait trait ) {
	QList< cv_Trait > list = character->merits( trait.category );

	int numberInCategory = 0;

	for ( int i = 0; i < list.count(); i++ ) {
		if ( list.at( i ).value > 0 ) {
			numberInCategory++;
		}
	}

	// Index der veränderten Kategorie in Liste suchen und dann die toolBox-Seite mit der identischen Indexzahl anpassen.
	int categoryIndex = v_categories.indexOf( trait.category );

	if ( numberInCategory > 0 ) {
		toolBox->setItemText( categoryIndex, cv_Trait::toString( v_categories.at( categoryIndex ), true ) + " (" + QString::number( numberInCategory ) + ")" );
	} else {
		toolBox->setItemText( categoryIndex, cv_Trait::toString( v_categories.at( categoryIndex ), true ) );
	}
}

