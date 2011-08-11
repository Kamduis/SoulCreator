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

#ifndef CHARACOMBOTRAIT_H
#define CHARACOMBOTRAIT_H

#include <QComboBox>
#include <QLineEdit>

#include "../Storage/StorageTemplate.h"

#include "CharaTrait.h"

/**
 * @brief Darstellung der vernetzten Eigenschaften mit Combobox.
 *
 * Merits, Kräfte etc. unterscheiden sich leicht von anderen Eigenschaften (Attribute, Fertigkeiten), da sie anstelle eines feststehenden Namens eine Auswahlbox haben, mit welcher die spezifische Eigenschaft ausgewählt werden kann.
 **/

class CharaComboTrait : public CharaTrait {
		Q_OBJECT

	public:
		/**
		 * Konstruktor.
		 *
		 * \todo Hat keinen Namen! Stattdessen wird die Combobox mit allen  möglichen Namen gefüllt, von denen man dann einen aussuchen kann.
		 **/
		CharaComboTrait( QWidget *parent, cv_Trait::Type type, int value = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~CharaComboTrait();

	private:
		QComboBox* nameBox;
		QLineEdit* customBox;

		StorageTemplate* storage;

	public slots:
		/**
		 * Fügt einen Namen in die Combobox ein.
		 *
		 * \todo Wenn in der Combobox der Name ausgewählt wird, muß CharaComboTrait automatisch Kategorie weitergeben.
		 **/
		void addName(QString names);

	private slots:
		void changeParameters(QString name);

	signals:
};

#endif
