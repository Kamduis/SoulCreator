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

#ifndef MERITWIDGET_H
#define MERITWIDGET_H

#include <QVBoxLayout>

#include "../Storage/StorageTemplate.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem sämtliche Merits angeordnet sind.
 *
 * Die Attribute werden in diesem Widget angeordnet.
 *
 * \todo Später sollen nur soviele Merits dargestellt werden, wie der Charakter tatsächlich hat +1. Will der Nutzer einen zusätzlichen Merit hinzufügen, füllt er diese leere Meritzeile aus und das Widget fügt automatisch eine weitere Leere Zeile am Ende ein. Alle leeren Merit-Widgets bis auf das letzte werden automatisch gelöscht.
 *
 * \todo In den Comboboxen sollen alle Merits angeboten werden, außer denen, die schon gewählt wurden.
 **/
class MeritWidget : public QWidget {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		MeritWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~MeritWidget();

	private:
		/**
		 * In diesem Layout werden die Eigenschaften angeordnet.
		 **/
		QVBoxLayout *layout;
		/**
		 * Ein übergeordnetes Layout, um den Stretch am Ende einzufügen, ohne zu verhindern, daß das automastische Casten der Eigenschaften dadurch gestört wird.
		 **/
		QVBoxLayout *layoutTop;

		/**
		 * Zugriff auf alle zur Verfügung stehenden Eigenscahften.
		 **/
		StorageTemplate* storage;

		/**
		 * Der Typ, dem alle Eigenschaften in diesem Widget angehören sollen.
		 **/
		cv_Trait::Type type;
		/**
		 * Eine Liste der kategorien, die in diesem Widget gewünscht sind.
		 **/
		QList< cv_Trait::Category > categories;

	public slots:

	private slots:
		/**
		 * Fügt eine neue Eigenschaftsauswahl hinzu, sollte keine Eigenscahft ohne mit leerer Auswahl vorhanden sein.
		 **/
		void addWidget();
		/**
		 * Entfernt alle Eigenschaftsauswahlen, welche nicht notwendig sind. Also alle, die einen leeren Namen anzeigen bis auf eine.
		 **/
		void removeWidget();
		/**
		 * Sorgt dafür, daß alle angezeigten Eigenscahften nur jene Marits auswählen können, die nicht schon in einer anderen Eigenschaftsdarstellung ausgewählt sind.
		 *
		 * \todo Natürlich muß Sichergestellt werden, daß Eigenschaften mit erklärendem Text (Language), mehrfach ausgewählt werden können.
		 *
		 * \todo Die Liste wird zwar wieder aufgefüllt, wenn ein Merit-Widget gelöscht wird, aber erst wenn vorher ein anderer Merit ausgewählt wurde.
		 **/
		void refillNameList();

	signals:
};

#endif
