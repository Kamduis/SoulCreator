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
#include <QDebug>

#include "../Exceptions/Exception.h"
#include "../Config/Config.h"
#include "../Storage/StorageTemplate.h"
#include "../Storage/StorageCharacter.h"

#include "InfoWidget.h"


InfoWidget::InfoWidget( QWidget *parent ) : QWidget( parent )  {
	layout = new QGridLayout( this );
	setLayout( layout );

	StorageTemplate storage;

	speciesComboBox = new QComboBox( this );

	connect( speciesComboBox, SIGNAL( currentIndexChanged( int ) ), this, SLOT( emitSpeciesChanged( int ) ) );
	connect( this, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( setStorageSpecies( cv_Species::SpeciesFlag ) ) );

	for ( int i = 0; i < storage.species().count(); i++ ) {
		if ( cv_Species::toSpecies( storage.species().at( i ).name ) != cv_Species::SpeciesAll ) {
			speciesComboBox->addItem( storage.species().at( i ).name );
		}
	}

	layout->addWidget( speciesComboBox );
}

InfoWidget::~InfoWidget() {
	delete layout;
}

void InfoWidget::emitSpeciesChanged( int index ) {
	qDebug() << Q_FUNC_INFO << "Spezies auf Indexposition" << index << "verändert";

	StorageTemplate storage;

	for ( int i = 0; i < storage.species().count(); i++ ) {
		if ( speciesComboBox->itemText( index ) == storage.species().at( i ).name ) {
			emit cv_Species::toSpecies( storage.species().at( i ).name );
			return;
		}
	}

	throw eSpeciesNotExisting();
}

void InfoWidget::setStorageSpecies( cv_Species::SpeciesFlag species ) {
	StorageCharacter character;

	character.setSpecies( species );
}
