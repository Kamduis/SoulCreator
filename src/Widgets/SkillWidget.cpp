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

#include <QGroupBox>
#include <QDebug>

#include "CharaTrait.h"
#include "../Datatypes/cv_Trait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"

#include "SkillWidget.h"


SkillWidget::SkillWidget( QWidget *parent ) : QWidget( parent )  {
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

		QVBoxLayout* categoryLayout = new QVBoxLayout();

		QGroupBox* categoryBox = new QGroupBox( this );
		categoryBox->setTitle( cv_Trait::toString( categories.at( i ), true ) );

		categoryBox->setLayout( categoryLayout );

		layout->addWidget( categoryBox );

		for ( int j = 0; j < list.count(); j++ ) {
			CharaTrait *charaTrait = new CharaTrait( this, list.at( j ) );
			// Wert definitiv ändern, damit alle Werte in den Charakter-Speicher übernommen werden.
			charaTrait->setValue( 5 );
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

			categoryLayout->addWidget( charaTrait );
		}

// 		// Abstand zwischen den Kategorien, aber nicht am Ende.
// 		if ( i < categories.count() - 1 ) {
// 			layout->addSpacing( Config::traitCategorySpace );
// 		}
	}

// 	layout->setRowMinimumHeight( storage->skillNames( cv_Trait::Mental ).count(), Config::traitCategorySpace );
// 	layout->setRowMinimumHeight( storage->skillNames( cv_Trait::Mental ).count() + storage->skillNames( cv_Trait::Physical ).count() + 1, Config::traitCategorySpace );
}

SkillWidget::~SkillWidget() {
	delete layout;
}

void SkillWidget::toggleOffSpecialties( bool sw, QString skillName, QList< cv_TraitDetail > specialtyList ) {
	qDebug() << Q_FUNC_INFO << "Drücke" << skillName;
	QList< cv_Trait > list;

	for ( int i = 0; i < layout->count(); i++ ) {
		QGroupBox* box = qobject_cast<QGroupBox*>( layout->itemAt( i )->widget() );
		QVBoxLayout* lcl_layout = qobject_cast<QVBoxLayout*>( box->layout() );

		for ( int j = 0; j < lcl_layout->count(); j++ ) {
			list = storage->skills( categories.at( 0 ) );

			// Wir wollen nur die Eigenschaftswidgekts, nicht die Abstandshalter!

			if ( j == list.count() || j == list.count() + storage->skills( categories.at( 1 ) ).count() + 1 ) {
				j++;
			}

			CharaTrait *trait = qobject_cast<CharaTrait*>( lcl_layout->itemAt( j )->widget() );

			if ( trait->name() != skillName ) {
				trait->setSpecialtyButtonChecked( false );
			qDebug() << Q_FUNC_INFO << "Deaktivieren von" << trait->name();
			}
		}
	}
}


