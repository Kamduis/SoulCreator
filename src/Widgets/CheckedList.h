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

#ifndef CHECKEDLIST_H
#define CHECKEDLIST_H

#include <QListWidget>


/**
 * @brief Erzeugt eine Liste, in welcher der Inhalt abgehakt werden kann.
 *
 * In dieser Liste kann der Nutzer sämtliche Einträge abhaken.
 **/

class CheckedList : public QListWidget {
		Q_OBJECT

	public:
		/**
		 *Konstruktor
		 **/
		CheckedList( QWidget *parent = 0 );

//	private:

	public slots:
		/**
		 * Hängt einen Eintrag an das Ende der Liste an.
		 **/
		void addCheckableItem( QString label /** Name des Eintrags. */, Qt::CheckState state = Qt::Unchecked /** Zustand des Eintrags. */ );
		/**
		 * Fügt einen Eintrag nach der angegebenen Position ein.
		 **/
		void insertCheckableItem( int i /** Position nach welcher der neue Eintrag eingefügt wird. */, QString label /** Name des Eintrags. */, Qt::CheckState state = Qt::Unchecked /** Zustand des Eintrags. */ );
		/**
		 * Setzt die gesamte Liste an Einträgen.
		 *
		 * Will man den Zustand eines einzelnen Eintrags verändern, sollte addCheckableItem() oder insertCheckableItem() verwendet werden. Nachträglich kann man den zustand natürlich durch checkItem() manipulieren.
		 **/
		void setCheckableItems( QStringList labels /** Name der Einträge. */, Qt::CheckState state = Qt::Unchecked /** Zustand aller Einträge. */ );
		/**
		 * Entfertn den Eintrag an der angegebenen Position.
		 **/
		void removeCheckableItem( int i /** Position des zu entfernenden Eintrags. */ );
		/**
		 * Abhaken des Eintrags (oder den Haken wieder entfernen).
		 **/
		void setItemCheckState( int i /** Position des zu entfernenden Eintrags. */, Qt::CheckState state = Qt::Checked /** Zustand des Eintrags. */ );

	private slots:

	signals:
// 		/**
// 		 * Signal wird ausgesandt, wann immer sich der Inhalt des Widgets verändert hat.
// 		 **/
// 		void checkedItemsChanged( QStringList );
};

#endif
