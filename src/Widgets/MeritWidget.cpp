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
#include <QIcon>
#include <QStyle>
#include <QDebug>

#include "CharaTrait.h"
#include "../Datatypes/cv_Trait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"
#include "../Storage/StorageTemplate.h"
#include "../CMakeConfig.h"

#include "MeritWidget.h"


MeritWidget::MeritWidget( QWidget *parent ) : QWidget( parent )  {
	QVBoxLayout* layoutTop = new QVBoxLayout( this );
	setLayout( layoutTop );

	scrollArea = new QScrollArea( this );
	scrollArea->setSizePolicy( QSizePolicy::MinimumExpanding, QSizePolicy::Expanding );
	scrollArea->setWidgetResizable( true );
	scrollArea->setFrameStyle(0);

	layoutTop->addWidget( scrollArea );

	QWidget* widget = new QWidget();
	layout = new QVBoxLayout( widget );

	widget->setLayout( layout );
	widget->setSizePolicy( QSizePolicy::Preferred, QSizePolicy::Expanding );
	scrollArea->setWidget( widget );
	widget->show();

	StorageTemplate storage;

	cv_Trait::Type type = cv_Trait::Merit;

	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );

	// Fertigkeiten werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.

	for ( int i = 0; i < categories.count(); i++ ) {
		for ( int j = 0; j < storage.meritNames( categories.at( i ) ).count(); j++ ) {
// 			qDebug() << Q_FUNC_INFO << storage.meritNames( categories.at( i ) ).at(j) << "ist besonders";
			for ( int k = 0; k < Config::traitMultipleMax; k++ ) {
				CharaTrait *trait = new CharaTrait( this, type, categories.at( i ), storage.meritNames( categories.at( i ) ).at( j ), storage.merits( categories.at( i ) ).at( j ).custom );
// 				trait->setCustom();
				layout->addWidget( trait );

				// Eigenschaften mit Beschreibungstext werden mehrfach dargestellt, da man sie ja auch mehrfach erwerben kann. Alle anderen aber immer nur einmal.
				if ( !storage.merits( categories.at( i ) ).at( j ).custom ) {
					break;
				}
			}
		}

		// Abstand zwischen den Kategorien, aber nicht am Ende.
		if ( i < categories.count() - 1 ) {
			layout->addSpacing( Config::traitCategorySpace );
		}
	}

	dialog = new SelectMeritsDialog(this);

	QHBoxLayout* layout_button = new QHBoxLayout();
	layoutTop->addLayout( layout_button );
	
	button = new QPushButton();
	button->setIcon( style()->standardIcon( QStyle::SP_FileDialogStart ) );
	
	layout_button->addStretch();
	layout_button->addWidget( button );

	connect(button, SIGNAL(clicked(bool)), dialog, SLOT(exec()));
}

MeritWidget::~MeritWidget() {
	delete layout;
}



