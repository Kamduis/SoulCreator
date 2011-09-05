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

#include "CharaTrait2.h"
#include "../Datatypes/cv_Trait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"

#include "SkillWidget.h"


SkillWidget::SkillWidget( QWidget *parent ) : QWidget( parent )  {
	character = StorageCharacter::getInstance();
	
	layout = new QVBoxLayout( this );
	setLayout( layout );

	cv_Trait::Type type = cv_Trait::Skill;

	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );

	QList< cv_Trait > list;
	QList< cv_TraitDetail > listDetails;

	// Fertigkeiten werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.
	for ( int i = 0; i < categories.count(); i++ ) {
		list = storage->skills( categories.at( i ) );

		for ( int j = 0; j < list.count(); j++ ) {
			// Anlegen der Eigenschaft im Speicher
			cv_Trait* traitPtr = character->addTrait( list[j] );

			qDebug() << Q_FUNC_INFO << traitPtr;

			// Anlegen des Widgets, das diese Eigenschaft repräsentiert.
			CharaTrait2 *charaTrait = new CharaTrait2( this, traitPtr );
			charaTrait->setValue( 0 );
			// Nur Fertigkeiten haben Spezialisierungen.
			if ( type = cv_Trait::Skill ) {
				// Es sollen die Spazialisierungen angezeigt werden können.
				listDetails = storage->skillSpecialties( list.at( j ).name );

				for ( int k = 0; k < listDetails.count(); k++ ) {
					charaTrait->addSpecialty( listDetails.at( k ) );
				}
				connect( charaTrait, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), this, SLOT( toggleOffSpecialties( bool, QString, QList< cv_TraitDetail > ) ) );
				connect( charaTrait, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), this, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ) );
			}
			layout->addWidget( charaTrait );
		}
		// Abstand zwischen den Kategorien, aber nicht am Ende.
		if ( i < categories.count() - 1 ) {
			layout->addSpacing( Config::traitCategorySpace );
		}
	}

// 	layout->setRowMinimumHeight( storage->skillNames( cv_Trait::Mental ).count(), Config::traitCategorySpace );
// 	layout->setRowMinimumHeight( storage->skillNames( cv_Trait::Mental ).count() + storage->skillNames( cv_Trait::Physical ).count() + 1, Config::traitCategorySpace );
}

SkillWidget::~SkillWidget() {
	delete layout;
}

void SkillWidget::toggleOffSpecialties( bool sw, QString skillName, QList< cv_TraitDetail > specialtyList ) {
// 	qDebug() << Q_FUNC_INFO << "Drücke" << skillName;
	QList< cv_Trait > list;

	for ( int i = 0; i < layout->count(); i++ ) {
		list = storage->skills( categories.at( 0 ) );

		// Wir wollen nur die Eigenschaftswidgekts, nicht die Abstandshalter!
		if ( i == list.count() || i == list.count() + storage->skills( categories.at( 1 ) ).count() + 1 ) {
			i++;
		}
		CharaTrait2 *trait = qobject_cast<CharaTrait2*>( layout->itemAt( i )->widget() );

		if ( trait->name() != skillName ) {
			trait->setSpecialtyButtonChecked( false );
// 			qDebug() << Q_FUNC_INFO << "Deaktivieren von" << trait->name();
		}
	}
}


