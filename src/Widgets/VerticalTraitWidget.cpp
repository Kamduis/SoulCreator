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

	QList< cv_Trait > list;
	QList< cv_Trait > listSkills;
	QList< cv_TraitDetail > listDetails;

	// Fertigkeiten werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.
	for ( int i = 0; i < categories.count(); i++ ) {
		list = storage.traits( v_type, categories.at( i ) );
		listSkills = storage.skills( categories.at( i ) );
		
		for ( int j = 0; j < list.count(); j++ ) {
// 			CharaTrait *trait = new CharaTrait( this, v_type, categories.at( i ), storage.traitNames( v_type, categories.at( i ) ).at( j ) );
			CharaTrait *trait = new CharaTrait( this, list.at( j ) );
// 			// Nur Fertigkeiten haben Spezialisierungen.
			if ( type = cv_Trait::Skill ) {
				listDetails = storage.skillSpecialties( listSkills.at( j ).name );
				
				// Es sollen die Spazialisierungen angezeigt werden können.
				for ( int k = 0; k < listDetails.count(); k++ ) {
					trait->addSpecialty( listDetails.at( k ) );
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


// VerticalTraitWidget::VerticalTraitWidget( QWidget *parent, cv_Trait::Type type ) : QWidget( parent )  {
// 	layout = new QVBoxLayout( this );
// 	setLayout( layout );
// 
// 	StorageTemplate storage;
// 
// 	v_type = type;
// 
// 	QList< cv_Trait::Category > categories;
// 	categories.append( cv_Trait::Mental );
// 	categories.append( cv_Trait::Physical );
// 	categories.append( cv_Trait::Social );
// 
// 	QStringList stringList;
// 	QList< cv_Trait > list;
// 	QList< cv_TraitDetail > detailList;
// 
// 	// Fertigkeiten werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.
// 	for ( int i = 0; i < categories.count(); i++ ) {
// 		stringList = storage.traitNames( v_type, categories.at( i ) );
// 
// 		for ( int j = 0; j < stringList.count(); j++ ) {
// 			list = storage.traits( v_type, categories.at( i ) );
// 
// // 			CharaTrait *trait = new CharaTrait( this, v_type, categories.at( i ), storage.traitNames( v_type, categories.at( i ) ).at( j ) );
// 			CharaTrait *trait = new CharaTrait( this, list.at( j ) );
// // 			// Nur Fertigkeiten haben Spezialisierungen.
// 			if ( type = cv_Trait::Skill ) {
// 				detailList = storage.skillSpecialties( storage.skillNames( categories.at( i ) ).at( j ) );
// 				// Es sollen die Spazialisierungen angezeigt werden können.
// 				for ( int k = 0; k < detailList.count(); k++ ) {
// 					trait->addSpecialty( detailList.at( k ) );
// 				}
// 			}
// 			layout->addWidget( trait );
// 		}
// 
// 		// Nur Abstand zwischen den Kategorien, nicht am Ende.
// // 		if (i < categories.count()-1){
// // 			layout->addSpacing(Config::traitCategorySpace);
// // 		}
// 	}
// 
// // 	layout->setRowMinimumHeight( storage.traitNames( v_type, cv_Trait::Mental ).count(), Config::traitCategorySpace );
// // 	layout->setRowMinimumHeight( storage.traitNames( v_type, cv_Trait::Mental ).count() + storage.traitNames( type, cv_Trait::Physical ).count() + 1, Config::traitCategorySpace );
// }

VerticalTraitWidget::~VerticalTraitWidget() {
	delete layout;
}


