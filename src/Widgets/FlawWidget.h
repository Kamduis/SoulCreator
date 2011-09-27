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

#ifndef FLAWWIDGET_H
#define FLAWWIDGET_H

#include <QHBoxLayout>
#include <QScrollArea>
#include <QToolBox>

#include "Storage/StorageTemplate.h"
#include "Storage/StorageCharacter.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem sämtliche Attribute angeordnet sind.
 *
 * Die Nachteile werden in diesem Widget angeordnet.
 **/
class FlawWidget : public QWidget {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		FlawWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~FlawWidget();

	private:
		StorageTemplate* storage;
		StorageCharacter* character;

		QScrollArea* scrollArea;
		QToolBox* toolBox;
		
		/**
		 * Damit ich nicht auch in anderen Funktionen stets alle Kategorien zusammensuchen muß, wird das hier global definiert und im Konstruktor gefüllt.
		 **/
		QList< cv_Trait::Category > v_categories;

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
		void countItems();

	signals:
};

#endif
