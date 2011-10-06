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

#include <QGridLayout>
#include <QDebug>

#include "CharaTrait.h"
// #include "Datatypes/cv_Trait.h"
// #include "Exceptions/Exception.h"
// #include "Config/Config.h"
// #include "Storage/StorageTemplate.h"
#include "Widgets/Dialogs/MessageBox.h"

#include "PowerWidget.h"


PowerWidget::PowerWidget( QWidget *parent ) : QWidget( parent )  {
	character = StorageCharacter::getInstance();

	layout = new QHBoxLayout( this );
	setLayout( layout );

	toolBox = new QToolBox();

	layout->addWidget( toolBox );

	storage = new StorageTemplate(this);

	cv_AbstractTrait::Type type = cv_AbstractTrait::Power;

	QList< cv_AbstractTrait::Category > categoryList = cv_AbstractTrait::getCategoryList( type );

	QList< Trait* > list;

	// Powers werden in einer Spalte heruntergeschrieben.
	for ( int i = 0; i < categoryList.count(); i++ ) {
		try {
			list = storage->traits( type, categoryList.at( i ) );
		} catch ( eTraitNotExisting &e ) {
			MessageBox::exception( this, e.message(), e.description() );
		}

		// Für jede Kategorie wird ein eigener Abschnitt erzeugt.
		QWidget* widgetPowerCategory = new QWidget();
		QVBoxLayout* layoutPowerCategory = new QVBoxLayout();

		widgetPowerCategory->setLayout( layoutPowerCategory );

		toolBox->addItem( widgetPowerCategory, cv_AbstractTrait::toString( categoryList.at( i ), true ) );

		connect(character, SIGNAL(speciesChanged(cv_Species::SpeciesFlag)), this, SLOT(updateHeaders(cv_Species::SpeciesFlag)));

		for ( int j = 0; j < list.count(); j++ ) {
			for ( int k = 0; k < Config::traitMultipleMax; k++ ) {
				// Anlegen der Eigenschaft im Speicher
				Trait* traitPtr = character->addTrait( list[j] );

				// Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				CharaTrait* charaTrait = new CharaTrait( this, traitPtr, list[j] );
				charaTrait->setValue( 0 );

				layoutPowerCategory->addWidget( charaTrait );

				// Eigenschaften mit Beschreibungstext werden mehrfach dargestellt, da man sie ja auch mehrfach erwerben kann. Alle anderen aber immer nur einmal.
				if ( !list.at( j )->custom() ) {
					break;
				}
			}

			// Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
			layoutPowerCategory->addStretch();
		}
	}
}

PowerWidget::~PowerWidget() {
	delete toolBox;
	delete layout;
	delete storage;
}


void PowerWidget::updateHeaders( cv_Species::SpeciesFlag spe )
{
	QStringList list = storage->powerHeaders( spe );

	for (int i = 0; i < list.count(); i++){
		toolBox->setItemEnabled(i, true);
		toolBox->setItemText(i, list.at(i));
	}
	if (list.count() < toolBox->count()){
		for (int i = list.count(); i < toolBox->count(); i++){
			toolBox->setItemText(i, "");
			toolBox->setItemEnabled(i, false);
		}
	}
}

