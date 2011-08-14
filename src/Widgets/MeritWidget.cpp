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

#include "CharaComboTrait.h"
#include "../Datatypes/cv_Trait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"

#include "MeritWidget.h"


MeritWidget::MeritWidget( QWidget *parent ) : QWidget( parent )  {
	layoutTop = new QVBoxLayout( this );
	setLayout( layoutTop );

	layout = new QVBoxLayout( this );

	layoutTop->addLayout( layout );
	layoutTop->addStretch();

	storage = new StorageTemplate( this );

	type = cv_Trait::Merit;

	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );

// 	for ( int i = 0; i < 10; i++ ) {
	CharaComboTrait *trait = new CharaComboTrait( this, type );

	for ( int j = 0; j < categories.count(); j++ ) {
		for ( int k = 0; k < storage->meritNames( categories.at( j ) ).count(); k++ ) {
			trait->addName( storage->meritNames( categories.at( j ) ).at( k ) );
		}
	}

	layout->addWidget( trait );

// 	}

	connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( addWidget() ) );
	connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( removeWidget() ) );
	connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( refillNameList() ) );
}

MeritWidget::~MeritWidget() {
	delete storage;
	delete layout;
}

void MeritWidget::addWidget() {
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
		CharaComboTrait *trait = new CharaComboTrait( this, type );

		for ( int j = 0; j < categories.count(); j++ ) {
			for ( int k = 0; k < storage->meritNames( categories.at( j ) ).count(); k++ ) {
				trait->addName( storage->meritNames( categories.at( j ) ).at( k ) );
			}
		}

		layout->addWidget( trait );

		// Natürlich muß auch das neue Widget so verbunden werden, daß es eine neue Eiegnschaftsauswahl erzeugen kann.
		connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( addWidget() ) );
		connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( removeWidget() ) );
		connect( trait, SIGNAL( nameChanged( QString ) ), this, SLOT( refillNameList() ) );
	}
}

void MeritWidget::removeWidget() {
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
}



void MeritWidget::refillNameList() {
	QStringList namesPossible;
	QStringList namesUsed;

	for ( int i = 0; i < categories.count(); i++ ) {
		for ( int j = 0; j < storage->meritNames( categories.at( i ) ).count(); j++ ) {
			namesPossible.append( storage->meritNames( categories.at( i ) ) );
		}
	}

	for ( int i = 0; i < layout->count(); i++ ) {
		CharaComboTrait *comboTrait = qobject_cast<CharaComboTrait *>( layout->itemAt( i )->widget() );
		namesUsed.append(comboTrait->name());
	}

	// Den leeren Eintrag am Anfang aus der Liste der zu entfernenden Einträge löschen. Soll ja immer auswählbar bleiben.
	namesUsed.removeAll( "" );

	// Dann Auswahlen bereinigen.
	for ( int i = 0; i < layout->count(); i++ ) {
		CharaComboTrait *comboTrait = qobject_cast<CharaComboTrait *>( layout->itemAt( i )->widget() );

		// Erst alle hinzufügen, die möglich sind.
		for ( int j = 0; j < namesPossible.count(); j++ ) {
			qDebug() << Q_FUNC_INFO << "Aktuell" << comboTrait->name() << "und ich füge hinzu" << namesPossible.at(j);
			comboTrait->addName(namesPossible.at(j));
		}
		
		// Dann alle entfernen, die schon vorhanden sind.
		for ( int j = 0; j < namesUsed.count(); j++ ) {
			// Die aktuelle Auswahl muß natürlich behalten werden.
			if ( namesUsed.at( j ) != comboTrait->name() ) {
				comboTrait->removeName( namesUsed.at( j ) );
			}
		}

// 		namesUsed.append( comboTrait->name() );
	}
}



