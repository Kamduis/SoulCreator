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

#include "DerangementComboBox.h"


DerangementComboBox::DerangementComboBox( QWidget *parent ) : QComboBox( parent ) {
	connect( this, SIGNAL( currentIndexChanged( int ) ), this, SLOT( emitCurrentIndexChanged( int ) ) );
}


cv_Derangement DerangementComboBox::currentItem() {
	return v_list.at( currentIndex() );
}


void DerangementComboBox::addItem( cv_Derangement item ) {
	v_list.append( item );
	QComboBox::addItem( item.name() );
}

void DerangementComboBox::addItems( QList< cv_Derangement > items ) {
	v_list.append( items );

	for ( int i = 0; i < items.count(); i++ ) {
		QComboBox::addItem( items.at( i ).name() );
	}
}

void DerangementComboBox::emitCurrentIndexChanged( int idx ) {
	if ( idx >= 0 ) {
		cv_Derangement lcl_derangement = v_list.at( idx );
		emit currentIndexChanged( lcl_derangement );
	}
}
