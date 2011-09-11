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
#include <QPushButton>
#include <QComboBox>

#include "../Storage/StorageCharacter.h"
#include "../Storage/StorageTemplate.h"
#include "CharaSpecies.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem wichtige Informationen dargestellt werden.
 *
 * Spezies, Namen etc. des Charakters werden hier dargestellt.
 *
 * \todo Bislanbg wird nur die Spezies dargestellt. Name, Organisation etc. fehlen alle noch.
 *
 * \todo Bei den Virtues und Vices wird bislang nur der erwachsene behrücksichtigt.
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
		 * Gesamte mögliche Chraktereigenschaften.
		 **/
		StorageTemplate *storage;
		/**
		 * Datenspeicher der Charkaterwerte.
		 **/
		StorageCharacter *character;
		/**
		 * In diesem Layout werden die Attribute angeordnet.
		 **/
		QGridLayout *layout;
		/**
		 * Knopf für den Namen. Über diese Schlatfläche wird ein Fenster aufgerufen, welches das Eintragen des Namens ermöglicht.
		 **/
		QPushButton* namePushButton;
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
		 * Ruft einen Dialog auf, in welchem die zahlreichen Namen des Charakters eingetragen werden können.
		 **/
		void openNameDialog();
		/**
		 * Verändert das Geschlecht des Charakters.
		 **/
		void changeGender(int gen);
		/**
		 * Verändert die Tugend des Charakters.
		 **/
		void changeVirtue(int idx);
		/**
		 * Verändert das Laster des Charakters.
		 **/
		void changeVice(int idx);
		/**
		 * Verändert die Brut des Charakters.
		 **/
		void changeBreed(int idx);
		/**
		 * Verändert die Fraktion des Charakters.
		 **/
		void changeFaction(int idx);
		/**
		 * Aktualisiert die Anzeige des Namens.
		 *
		 * \bug Mit jedem Speichern und Laden wächst die Anzahl der unnötigen Leerzeichen am Ende an. Symptome sind zwar behoben, die ursache aber noch nicht.
		 **/
		void updateIdentity(cv_Identity id );
		/**
		 * Aktualisiert die Anzeige der Tugend.
		 **/
		void updateVirtue(QString txt);
		/**
		 * Aktualisiert die Anzeige des Lasters.
		 **/
		void updateVice(QString txt);
		/**
		 * Aktualisiert die Anzeige der Brut.
		 **/
		void updateBreed(QString txt);
		/**
		 * Aktualisiert die Anzeige der Fraktion.
		 **/
		void updateFaction(QString txt);
		/**
		 * Wenn die Spezies sich ändert, muß die Auswahl der möglichen Bruten verändert werden.
		 **/
		void updateBreedBox(cv_Species::SpeciesFlag spe);
		/**
		 * Wenn die Spezies sich ändert, muß die Auswahl der möglichen Fraktionen verändert werden.
		 **/
		void updateFactionBox(cv_Species::SpeciesFlag spe);

	signals:
};

#endif
