# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) 2011 by Victor von Rhein

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

#import traceback

#from PySide.QtCore import Qt
from PySide.QtGui import QListWidget, QListWidgetItem

#from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
from src.Debug import Debug




class CheckedList(QListWidget):
	"""
	@brief Erzeugt eine Liste, in welcher der Inhalt abgehakt werden kann.

	In dieser Liste kann der Nutzer sämtliche Einträge abhaken.
	"""

	def __init__(self, parent=None):
		QListWidget.__init__(self, parent)

		


#CheckedList::CheckedList( QWidget *parent ) : QListWidget( parent ) {
#// 	connect(this, SIGNAL(itemChanged ( QListWidgetItem * )), this, SLOT(emitCheckedItemsChanged()) );
#}


	def addCheckableItem( self, label, state ):
		"""
		Hängt einen Eintrag an das Ende der Liste an.
		"""
		
		self.insertCheckableItem( self.count(), label, state )


	def insertCheckableItem( self, index, label, state ):
		"""
		Fügt einen Eintrag an der angegebenen Indexposition ein.
		"""
		
		item = QListWidgetItem()
		item.setText( label )
		item.setCheckState( state )
		self.insertItem( index, item )


	def setCheckableItems( self, labels, state ):
		"""
		Setzt alle Einträge.
		
		Will man den Zustand eines einzelnen Eintrags verändern, sollte addCheckableItem() oder insertCheckableItem() verwendet werden. Nachträglich kann man den Zustand natürlich durch checkItem() manipulieren.
		"""
		
		for item in labels:
			self.addCheckableItem( item, state )


#void CheckedList::removeCheckableItem( int i ) {
	#delete item( i );
#}

#void CheckedList::setItemCheckState( int i, Qt::CheckState state ) {
	#item(i)->setCheckState(state);
#}



#// void CheckedList::emitCheckedItemsChanged(){
#// 	QStringList list;
#//
#// 	for (int i = 0; i < count(); ++i){
#// 		if (item(i)->checkState() == Qt::Checked)
#// 			list.append(item(i)->text());
#// 	}
#//
#// 	emit checkedItemsChanged(list);
#// }
