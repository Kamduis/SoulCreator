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

#include <QDebug>

#include "CharaTrait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"
#include "../Storage/StorageTemplate.h"
#include "../CMakeConfig.h"

#include "VerticalTraitWidget.h"


VerticalTraitWidget::VerticalTraitWidget( QWidget *parent, cv_Trait::Type type ) : QWidget( parent )  {
	layout = new QVBoxLayout( this );
	setLayout( layout );

	StorageTemplate storage;

	v_type = type;

	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );

	// Fertigkeiten werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.
	for ( int i = 0; i < categories.count(); i++ ) {
		for ( int j = 0; j < storage.traitNames( v_type, categories.at( i ) ).count(); j++ ) {
			CharaTrait *trait = new CharaTrait( this, v_type, categories.at( i ), storage.traitNames( v_type, categories.at( i ) ).at( j ) );
			// Nur Fertigkeiten haben Spezialisierungen.
			if ( type = cv_Trait::Skill ) {
				// Es sollen die Spazialisierungen angezeigt werden können.
				for ( int k = 0; k < storage.skillSpecialties( storage.skillNames( categories.at( i ) ).at( j ) ).count(); k++ ) {
					trait->addSpecialty( storage.skillSpecialties( storage.skillNames( categories.at( i ) ).at( j ) ).at( k ) );
				}
			}
			layout->addWidget( trait );
		}

		// Nur Abstand zwischen den Kategorien, nicht am Ende.
// 		if (i < categories.count()-1){
// 			layout->addSpacing(Config::traitCategorySpace);
// 		}
	}

// 	layout->setRowMinimumHeight( storage.traitNames( v_type, cv_Trait::Mental ).count(), Config::traitCategorySpace );
// 	layout->setRowMinimumHeight( storage.traitNames( v_type, cv_Trait::Mental ).count() + storage.traitNames( type, cv_Trait::Physical ).count() + 1, Config::traitCategorySpace );
}

VerticalTraitWidget::~VerticalTraitWidget() {
	delete layout;
}


