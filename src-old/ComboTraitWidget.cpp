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

#include <QScrollArea>
#include <QDebug>

#include "CharaComboTrait.h"
#include "../Datatypes/cv_Trait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"

#include "ComboTraitWidget.h"


ComboTraitWidget::ComboTraitWidget( QWidget *parent, cv_Trait::Type type ) : QWidget( parent )  {
	layout = new QVBoxLayout( this );
	setLayout( layout );

	storage = new StorageTemplate( this );

	setType( type );

	v_categories.append( cv_Trait::Mental );
	v_categories.append( cv_Trait::Physical );
	v_categories.append( cv_Trait::Social );

// 	for ( int i = 0; i < 10; i++ ) {
	CharaComboTrait *trait = new CharaComboTrait( this, type );

	for ( int j = 0; j < v_categories.count(); j++ ) {
		for ( int k = 0; k < storage->traitNames( v_type, v_categories.at( j ) ).count(); k++ ) {
			trait->addName( storage->traitNames( v_type, v_categories.at( j ) ).at( k ) );
		}
	}

	layout->addWidget( trait );

// 	}

	connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( addWidget() ) );
	connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( removeWidget() ) );
	connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( refillNameList() ) );
}

ComboTraitWidget::~ComboTraitWidget() {
	delete storage;
	delete layout;
}

cv_Trait::Type ComboTraitWidget::type() const {
	return v_type;
}
void ComboTraitWidget::setType( cv_Trait::Type type ) {
	v_type = type;
}


void ComboTraitWidget::addWidget() {
	bool needToAdd = true;

	for ( int i = 0; i < layout->count(); i++ ) {
		CharaComboTrait *comboTrait = qobject_cast<CharaComboTrait *>( layout->itemAt( i )->widget() );

		if ( comboTrait->name().isEmpty() ) {
			needToAdd = false;
			break;
		}
	}

	// Wir fügen nur eine neue Eigenschaftsauswahl hinzu, wenn es keine Auswahl gibt, die einen leeren Namen anzeigt.
	if ( needToAdd ) {
		CharaComboTrait *trait = new CharaComboTrait( this, v_type );

		for ( int j = 0; j < v_categories.count(); j++ ) {
			for ( int k = 0; k < storage->traitNames( v_type, v_categories.at( j ) ).count(); k++ ) {
				trait->addName( storage->traitNames( v_type, v_categories.at( j ) ).at( k ) );
			}
		}

		layout->addWidget( trait );

		// Natürlich muß auch das neue Widget so verbunden werden, daß es eine neue Eiegnschaftsauswahl erzeugen kann.
		connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( addWidget() ) );
		connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( removeWidget() ) );
		connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( refillNameList() ) );
	}
}

void ComboTraitWidget::removeWidget() {
	// Suche die erste Box mit leerer Auswahl, damit wir die behalten können.
	// Da wir aber eigentlich die letzte behalten wollen, zählen wir rückwärts.
	bool isFirst = true;

	for ( int i = layout->count() - 1; i > -1; i-- ) {
		CharaComboTrait *comboTrait = qobject_cast<CharaComboTrait *>( layout->itemAt( i )->widget() );

		if ( comboTrait->name().isEmpty() ) {
			// Die erste behalten wir!
			if ( !isFirst ) {
				delete comboTrait;
			}

			isFirst = false;
		}
	}

	refillNameList();
}



void ComboTraitWidget::refillNameList() {
	QStringList namesPossible;
	QStringList namesUsed;

// 	qDebug() << Q_FUNC_INFO << "Es geht los! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!";

	for ( int i = 0; i < v_categories.count(); i++ ) {
		for ( int j = 0; j < storage->traitNames( v_type, v_categories.at( i ) ).count(); j++ ) {
			namesPossible.append( storage->traitNames( v_type, v_categories.at( i ) ) );
		}
	}

	namesPossible.removeDuplicates();

	for ( int i = 0; i < layout->count(); i++ ) {
		CharaComboTrait *comboTrait = qobject_cast<CharaComboTrait *>( layout->itemAt( i )->widget() );
		namesUsed.append( comboTrait->name() );
	}

	namesUsed.removeDuplicates();

	// Den leeren Eintrag am Anfang aus der Liste der zu entfernenden Einträge löschen. Soll ja immer auswählbar bleiben.
	namesUsed.removeAll( "" );

	// Dann Auswahlen bereinigen.
	for ( int i = 0; i < layout->count(); i++ ) {
		CharaComboTrait *comboTrait = qobject_cast<CharaComboTrait *>( layout->itemAt( i )->widget() );

		// Entferne alle Einträge, welche besonderen Text beinhalten.
		if (comboTrait->custom()){
			namesUsed.removeAll(comboTrait->name());
		}

// 		qDebug() << Q_FUNC_INFO << "Aktuell" << comboTrait->name();

		// Erst alle hinzufügen, die möglich sind.
		for ( int j = 0; j < namesPossible.count(); j++ ) {
// 			qDebug() << Q_FUNC_INFO << "Füge hinzu" << namesPossible.at( j ) << "in" << comboTrait->name();
			comboTrait->addName( namesPossible.at( j ) );
		}

		// Dann alle entfernen, die schon vorhanden sind.
		for ( int j = 0; j < namesUsed.count(); j++ ) {
			// Die aktuelle Auswahl muß natürlich behalten werden.
			// Alle Namen, welche erklärenden Text haben ebenfalls.
			if ( namesUsed.at( j ) != comboTrait->name() ) {
// 				qDebug() << Q_FUNC_INFO << "Entferne" << namesUsed.at( j ) << "in" << comboTrait->name() << "da" << comboTrait->custom();
				comboTrait->removeName( namesUsed.at( j ) );
			}
		}

// 		namesUsed.append( comboTrait->name() );
	}
}



