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

#ifndef MERITWIDGET_H
#define MERITWIDGET_H

#include <QHBoxLayout>
#include <QScrollArea>
#include <QToolBox>
#include <QPushButton>

// #include "Storage/StorageTemplate.h"
#include "Storage/StorageCharacter.h"
// #include "Datatypes/cv_Trait.h"
// #include "Datatypes/cv_TraitDetail.h"
#include "Widgets/Dialogs/SelectMeritsDialog.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem sämtliche Merits angeordnet sind.
 *
 * \todo Einen Knopf erstellen, über den der Benutzer angeben kann, welche Merits er denn wirklich alle angezeigt haben will.
 *
 * \todo Bei Merits mit Zusatztext (Language) in diesem men+ ein Zahlenfle dangeben, bei welchem der benutzer einstellen kann, wieviele verschiedene dieser scheinbar identischen merits er angezeigt haben will.
 **/
class MeritWidget : public QWidget {
		Q_OBJECT

	public:
		/**
		 * Konstruktor.
		 **/
		MeritWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~MeritWidget();

	private:
		QHBoxLayout* layout;
		QScrollArea* scrollArea;
		QToolBox* toolBox;
// 		QPushButton* button;
// 		SelectMeritsDialog* dialog;
		StorageTemplate* storage;
		StorageCharacter* character;
		

		/**
		 * Damit ich nicht auch in anderen Funktionen stets alle Kategorien zusammensuchen muß, wird das hier global definiert und im Konstruktor gefüllt.
		 **/
		QList< cv_AbstractTrait::Category > v_category;

	public slots:

	private slots:
		/**
		 * Zält die Merits in einer Kategorie, deren Wert größer 0 ist. Dieser Wert wird dann in die Überschrift der einzelnen ToolBox-Seiten angezeigt, um dem Benutzer die Übersicht zu bewahren.
		 *
		 * Es wird nur dann etwas angezeigt, wenn der Weert größer 0 ist.
		 *
		 * \bug Merits mit Zusatztext werden nicht gezählt. Kann sein, daß das nur auftritt wenn nichts in der Textbox steht. Ist dann kein Problem, da es ohnehin nicht möglich sein dürfte, Werte einzugeben, wenn Zusatext nicht angegeben ist.
		 *
		 * \todo Momentan wird eine Liste mit allen Merits des Charakters erstellt und dann alle gezählt, deren Wert größer 0 ist. Das muß doch besser gehen.
		 **/
		void countMerits();

	signals:
// 		/**
// 		 * Die Anzahl der Angewählten Merits hat sich verändert, also wird dieses Signal gesandt.
// 		 **/
// 		numberOfMeritsChanged(cv_AbstractTrait::Category category /** Die Anzahl der Merits in dieser Kategorie hat sich verändert. */ );
};

#endif
