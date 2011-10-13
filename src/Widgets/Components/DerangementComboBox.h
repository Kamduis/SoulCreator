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

#ifndef DERANGEMENTCOMBOBOX_H
#define DERANGEMENTCOMBOBOX_H

#include <QList>

#include "Datatypes/Traits/cv_Derangement.h"

#include <QComboBox>


/**
 * @brief Eine Combobox für Geistesstörungen.
 *
 * Diese ComboBox zeigt milde und schwere Geistesstörungen in unterschiedlichen Farben an und bietet spezielle Signale.
 *
 * \todo Die Anzeige unterscheidet noch nicht zwischen milden und ernsten Störungen.
 **/

class DerangementComboBox : public QComboBox {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		DerangementComboBox( QWidget *parent = 0 );

		/**
		 * Gibt die derzeit ausgewählte Geistesstörung zurück.
		 **/
		cv_Derangement currentItem();

	private:
		QList< cv_Derangement > v_list;

	public slots:
		/**
		 * Fügt der Auswahlliste eine Geistesstörung hinzu.
		 **/
		void addItem(cv_Derangement item);
		/**
		 * Fügt der Auswahlliste eine Liste von Geistesstörungen hinzu.
		 **/
		void addItems(QList< cv_Derangement > items);

	private slots:
		void emitCurrentIndexChanged(int idx);

	signals:
		/**
		 * Signal wird ausgesandt, wann immer der aktuzelle Index verändert wird.
		 **/
		void currentIndexChanged( cv_Derangement derang );
};

#endif
