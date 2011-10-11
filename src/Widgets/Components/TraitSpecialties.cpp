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

#include <QDebug>

#include "TraitSpecialties.h"


TraitSpecialties::TraitSpecialties( QWidget* parent ) : CheckedList( parent ) {
	connect( this, SIGNAL( itemChanged( QListWidgetItem* ) ), this, SLOT( emitCheckedSpecialtiesChanged( ) ) );
}

TraitSpecialties::~TraitSpecialties() {
}


QString TraitSpecialties::skill() const {
	return v_skill;
}
void TraitSpecialties::setSkill( QString skillName ) {
	if ( v_skill != skillName ) {
		v_skill = skillName;

		emit skillChanged( skillName );
	}
}


void TraitSpecialties::addSpecialty( QString spec ) {
// 	insertSpecialty(checkedList->count(), spec);
	addCheckableItem( spec );
}

void TraitSpecialties::insertSpecialty( int i, QString spec ) {
	insertCheckableItem( i, spec );

// 	emit numberChanged(checkedList->count());
}

void TraitSpecialties::setSpecialties( QList< cv_TraitDetail > specList ) {
	QList< cv_TraitDetail > list = specList;

	Qt::CheckState state;
	for ( int i = 0; i < list.count(); ++i ) {
		if ( list.at( i ).value ) {
			state = Qt::Checked;
		} else {
			state = Qt::Unchecked;
		}

		addCheckableItem( list.at( i ).name, state );
	}

}



void TraitSpecialties::removeSpecialty( QString spec ) {
	for ( int i = 0; i < count(); ++i ) {
		if ( item( i )->text() == spec ) {
			removeSpecialty( i );
			break;
		}
	}
}

void TraitSpecialties::removeSpecialty( int i ) {
	removeCheckableItem( i );

// 	emit numberChanged(checkedList->count());
}

void TraitSpecialties::emitCheckedSpecialtiesChanged( ) {
	QStringList listChecked;

	for ( int i = 0; i < count(); ++i ) {
		if ( item( i )->checkState() != Qt::Unchecked ) {
			listChecked.append( item( i )->text() );
		}
	}

	emit checkedSpecialtiesChanged( listChecked );
}



