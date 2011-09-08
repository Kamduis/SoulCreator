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

#ifndef INFOWIDGET_H
#define INFOWIDGET_H

#include <QGridLayout>
#include <QLineEdit>
#include <QComboBox>

#include "../Storage/StorageCharacter.h"
#include "CharaSpecies.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem wichtige Informationen dargestellt werden.
 *
 * Spezies, Namen etc. des Charakters werden hier dargestellt.
 *
 * \todo Bislanbg wird nur die Spezies dargestellt. Name, Organisation etc. fehlen alle noch.
 **/
class InfoWidget : public QWidget {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		InfoWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~InfoWidget();

	private:
		/**
		 * Datenspeicher der Charkaterwerte.
		 **/
		StorageCharacter *character;
		/**
		 * In diesem Layout werden die Attribute angeordnet.
		 **/
		QGridLayout *layout;
		/**
		 * Feld für den Namen.
		 **/
		QLineEdit* nameLineEdit;
		/**
		 * Auswahl des Geschlechts.
		 **/
		QComboBox* genderCombobox;
		/**
		 * Eine Auswahlbox für die zur Verfügung stehenden Spezies.
		 **/
		CharaSpecies* speciesComboBox;
		/**
		 * Auswahl der Virtues
		 **/
		QComboBox* virtueCombobox;
		/**
		 * Auswahl der Brut (Seeming, Path, Clan, Auspice)
		 **/
		QComboBox* breedCombobox;
		/**
		 * Auswahl der Fraktion (Court, Order, Covenant, Tribe)
		 **/
		QComboBox* factionCombobox;
		/**
		 * Auswahl der Vices
		 **/
		QComboBox* viceCombobox;

	public slots:

	private slots:
		/**
		 * Verändert die im Charakter gespeicherte echte Identität.
		 *
		 * \todo Momentan ist die echte Identität auch die einzige, welche verwendet wird. Und ich nutze nur den allerersten Vornamen als Speicher.
		 **/
		void modifyRealIdentity();
		/**
		 * Aktualisiert die Anzeige des Namens.
		 *
		 * \bug Mit jedem Speichern und Laden wächst die Anzahl der unnötigen Leerzeichen am Ende an. Symptome sind zwar behoben, die ursache aber noch nicht.
		 **/
		void updateIdentity(cv_Identity);

	signals:
};

#endif
