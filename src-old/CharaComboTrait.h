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

		/**
		 * Gibt zurück, ob es sich um eine Eigenschaft mit einem besonderen Text handelt.
		 **/
		bool custom() const;
		/**
		 * Gibt den besonderen Text der Eigenschaft zurück.
		 **/
		QString customText() const;

private:
		StorageCharacter *character;

		QComboBox* nameBox;
		QLineEdit* customBox;

		StorageTemplate* storage;

		bool v_custom;

	public slots:
		/**
		 * Ändert alle Parameter dieses Widgets, damit es der übergebenen Eigenschaft entspricht.
		 *
		 * \note Eigenschaften mit Zusatztext können beliebig oft aufgerufen werden. Und sie können auch alle den selben Zusatztext haben. Allerdings erhalten sie dann auch stets alle den selben Wert, wenn der Zusatztext identisch ist.
		 *
		 * \note Abgeändert von CharaTrait::setTrait(), um auch mit custom() umgehen zu können.
		 *
		 * \overload CharaTrait::setTrait()
		 **/
		virtual void setTrait(cv_Trait trait);
		/**
		 * Fügt einen Namen in die Combobox ein.
		 *
		 * \note Doppelte Einträge werden nicht hinzugefügt.
		 * 
		 * \todo Wenn in der Combobox der Name ausgewählt wird, muß CharaComboTrait automatisch Kategorie weitergeben.
		 **/
		void addName(QString names);
		/**
		 * Entfernt einen Namen aus der ComboBox
		 **/
		void removeName(QString names);
		/**
		 * Legt fest, ob es sich um eine Eigenschaft mit einem erklärenden Text handelt.
		 **/
		void setCustom(bool sw);

	private slots:
		/**
		 * Sorgt dafür, daß alle notwendigen Informationen dieser Eigenschaft in den Speicher übertragen werden.
		 *
		 * \note Eigenschaften, die einen besonderen text besitzen, werden nur dann in den Speicher übertragen, wenn dieser besondere text auch existiert.
		 **/
		void emitTraitChanged();
// 		/**
// 		 * Wann immer Index 0 (also kein Merit) in der Combobox angezeigt wird, werden die Punkte disabled.
// 		 *
// 		 * \todo Mit Wirkung versehen, damit bei Index 0 keine Punkte vergeben werden können.
// 		 *
// 		 * \bug Momentan keine Wirkung!
// 		 **/
// 		void enableWidgets(int index);
		/**
		 * Wann immer der Merit verändert wird, den dieses Widget darstellt, muß auch Typ und Vor allem Kategorie mitverändert werden. Außerdem wird herausgefunden, ob erklärender text erlaubt ist und dieser ermöglicht.
		 *
		 * \todo Außerdem müssen die Werte zurückgesetzt werden.
		 **/
		void changeParameters(QString name);

	signals:
		void nameChanged( QString name );
};

#endif
