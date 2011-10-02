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
#include <QToolBox>
#include <QDebug>

#include "CharaTrait.h"
// #include "Datatypes/cv_Trait.h"
// #include "Exceptions/Exception.h"
// #include "Config/Config.h"
#include "Widgets/Dialogs/MessageBox.h"

#include "SkillWidget.h"


SkillWidget::SkillWidget( QWidget *parent ) : QWidget( parent )  {
	layout = new QHBoxLayout( this );
	setLayout( layout );

	toolBox = new QToolBox();

	layout->addWidget(toolBox);

	character = StorageCharacter::getInstance();
	storage = new StorageTemplate( this );

	cv_AbstractTrait::Type type = cv_AbstractTrait::Skill;

	v_categoryList = cv_AbstractTrait::getCategoryList(type);

	QList< Trait* > list;

	// Fertigkeiten werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.
	for ( int i = 0; i < v_categoryList.count(); i++ ) {
		// Für jede Kategorie wird ein eigener Abschnitt erzeugt.
		QWidget* widgetSkillCategory = new QWidget();
		QVBoxLayout* layoutSkillCategory = new QVBoxLayout();

		widgetSkillCategory->setLayout( layoutSkillCategory );

		toolBox->addItem( widgetSkillCategory, cv_AbstractTrait::toString( v_categoryList.at( i ), true ) );

		try {
			list = storage->traits2( type, v_categoryList.at( i ) );
		} catch (eTraitNotExisting &e) {
			MessageBox::exception(this, e.message(), e.description());
		}

		for ( int j = 0; j < list.count(); j++ ) {
			// Anlegen der Eigenschaft im Speicher
			Trait* traitPtr = character->addTrait( list[j] );
			// Die Spezialisierungen werden nicht übernommen, da im Charakter nur jene gespeichert werden, die der Charakter auch tatsächlich hat.
			traitPtr->clearDetails();

			// Anlegen des Widgets, das diese Eigenschaft repräsentiert.
			CharaTrait* charaTrait = new CharaTrait( this, traitPtr, list[j] );
			charaTrait->setValue( 0 );

			// Fertigkeiten haben Spezialisierungen.
			connect( charaTrait, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), this, SLOT( toggleOffSpecialties( bool, QString, QList< cv_TraitDetail > ) ) );
			connect( charaTrait, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), this, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ) );
			
			layoutSkillCategory->addWidget( charaTrait );
		}

		// Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
		layoutSkillCategory->addStretch();
	}
}

SkillWidget::~SkillWidget() {
	delete layout;
}

void SkillWidget::toggleOffSpecialties( bool sw, QString skillName, QList< cv_TraitDetail > specialtyList ) {
// 	qDebug() << Q_FUNC_INFO << "Drücke" << skillName;
	QList< Trait* > list;

	for ( int j = 1; j < layout->count(); j++ ) {
		CharaTrait* trait = qobject_cast<CharaTrait*>( layout->itemAt( j )->widget() );

		if ( trait->name() != skillName ) {
			trait->setSpecialtyButtonChecked( false );
// 				qDebug() << Q_FUNC_INFO << "Deaktivieren von" << trait->name();
		}
	}
}


