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

#include <QGroupBox>
#include <QDebug>

#include "CharaTrait.h"
#include "Datatypes/cv_Trait.h"
#include "Exceptions/Exception.h"
#include "Config/Config.h"
#include "Widgets/Dialogs/MessageBox.h"

#include "SkillWidget.h"


SkillWidget::SkillWidget( QWidget *parent ) : QWidget( parent )  {
	character = StorageCharacter::getInstance();

	layout = new QGridLayout( this );
	setLayout( layout );

	int actualColumn = 0;

	cv_Trait::Type type = cv_Trait::Skill;

	v_categories = cv_Trait::getCategoryList( type );

	QList< Trait* > list;

	for ( int i = 0; i < v_categories.count(); i++ ) {
		try {
			list = storage->traits2( type, v_categories.at( i ) );
		} catch ( eTraitNotExisting &e ) {
			MessageBox::exception( this, e.message(), e.description() );
		}

		// Zeichnen des Separators zwischen den einzelnen Kategorien
		// Aber nicht an allererster Stelle
		if ( i > 0 ) {
			actualColumn++;

			QFrame* vLine = new QFrame( this );
			vLine->setFrameStyle( QFrame::VLine );
			layout->addWidget( vLine, 1, actualColumn, list.count(), 1, Qt::AlignHCenter );

// 			layout->setColumnMinimumWidth( actualColumn, Config::traitCategorySpace );
			layout->setColumnStretch( actualColumn, 1 );

			// Jetzt sind wir in der Spalte für die tatsächlchen Eigenschaften
			actualColumn++;
		}

		// Aber zuerst kommt die Überschrift für die einzelnen Kategorien.
		QLabel* header = new QLabel();

		header->setAlignment( Qt::AlignHCenter );

		header->setText( "<b>" + cv_Trait::toString( v_categories.at( i ) ) + "</b>" );

		layout->addWidget( header, 0, actualColumn );

		// Einfügen der tatsächlichen Fertigkeiten
		for ( int j = 0; j < list.count(); j++ ) {
			// Anlegen der Eigenschaft im Speicher
			Trait* lcl_trait = list[j];
			Trait* traitPtr = character->addTrait( lcl_trait );
			// Die Spezialisierungen werden nicht übernommen, da im Charakter nur jene gespeichert werden, die der Charakter auch tatsächlich hat.
			traitPtr->clearDetails();

			// Anlegen des Widgets, das diese Eigenschaft repräsentiert.
			CharaTrait* charaTrait = new CharaTrait( this, traitPtr, list[j] );
			charaTrait->setValue( 0 );

			// Nur Fertigkeiten haben Spezialisierungen.
			if ( type = cv_Trait::Skill ) {
				connect( charaTrait, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), this, SLOT( toggleOffSpecialties( bool, QString, QList< cv_TraitDetail > ) ) );

				connect( charaTrait, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), this, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ) );
			}

			layout->addWidget( charaTrait, j + 1, actualColumn );
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
// 	qDebug() << Q_FUNC_INFO << "Drücke" << skillName;
	QList< Trait* > list;

	// Nur Spalten 0, 2 und 4 werden verwendet. 1 und 3 sind für optische Trennung.
	for ( int i = 0; i < layout->columnCount(); i = i + 2 ) {
		// durch das +2 kann die Schleife für einen Ausgang über ihre Grenze hinausspringen. Also diese zusätzliche Abbruchbedingung.
// 		if (i >= layout->columnCount()){
// 			break;
// 		}

		for ( int j = 1; j < layout->rowCount(); j++ ) {
// 			qDebug() << Q_FUNC_INFO << "Reihe" << j << "Spalte" << i;

			CharaTrait* trait = qobject_cast<CharaTrait*>( layout->itemAtPosition( j, i )->widget() );

			if ( trait->name() != skillName ) {
				trait->setSpecialtyButtonChecked( false );
// 				qDebug() << Q_FUNC_INFO << "Deaktivieren von" << trait->name();
			}
		}
	}
}


