/**
 * \file
 * \author Victor von Rhein <victor@caern.de>
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

#include "CheckedList.h"


CheckedList::CheckedList( QWidget *parent ) : QListWidget( parent ) {
// 	connect(this, SIGNAL(itemChanged ( QListWidgetItem * )), this, SLOT(emitCheckedItemsChanged()) );
}


void CheckedList::addCheckableItem( QString label, Qt::CheckState state ) {
	insertCheckableItem( this->count(), label, state );
}

void CheckedList::insertCheckableItem( int i, QString label, Qt::CheckState state ) {
	QListWidgetItem *item = new QListWidgetItem;
	item->setText( label );
	item->setCheckState( state );
	insertItem( i, item );

// 	emitCheckedItemsChanged();
}

void CheckedList::setCheckableItems( QStringList labels, Qt::CheckState state ) {
	for ( int i = 0; i < labels.count(); ++i ) {
		addCheckableItem( labels.at( i ), state );
	}
}


void CheckedList::removeCheckableItem( int i ) {
	delete item( i );
}

void CheckedList::setItemCheckState( int i, Qt::CheckState state ) {
	item(i)->setCheckState(state);
}



// void CheckedList::emitCheckedItemsChanged(){
// 	QStringList list;
//
// 	for (int i = 0; i < count(); ++i){
// 		if (item(i)->checkState() == Qt::Checked)
// 			list.append(item(i)->text());
// 	}
//
// 	emit checkedItemsChanged(list);
// }
