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

#ifndef COMBOTRAITWIDGET_H
#define COMBOTRAITWIDGET_H

#include <QVBoxLayout>

#include "../Storage/StorageTemplate.h"

#include <QWidget>


/**
 * @brief Dieses Widget ordnet Widgets der Klasse \ref CharaComboTrait an und sorgt dafür, daß die Anzahl der Widgets minimal bleibt.
 *
 * Es wird zu beginn nur ein einziges \ref CharaComboTrait angezeigt. Sobald dieses dazu genutzt wird, eine Eigenschaft darzustellen, erscheint ein zweites Widget mit leerer Anzeige. Wird auch dieses genutzt, erscheint ein drittes und so weiter. Wird ein Widget wieder geleert, verschwindet es automatisch.
 *
 * Der Inhalt der Comboboxen wird automatisch so befüllt, daß nur die Eigenschaften ausgewählt werden können, die nicht schon von einem anderen \ref CharaComboTrait in diesem Widget angezeigt werden.
 *
 * \todo Die Breite der angezeigten combobox (von CharaComboTrait) variiert, je nachdem welche Länge noch möglich ist. Die Länge sollte stets gleich breit definiert werden.
 **/
class ComboTraitWidget : public QWidget {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		ComboTraitWidget( QWidget *parent = 0, cv_Trait::Type type = cv_Trait::Merit );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~ComboTraitWidget();

		/**
		 * Gibt den Typ zurück, dem alle Eigenschaften in diesem Widget angehören sollen.
		 **/
		cv_Trait::Type type() const;

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
		 * Zugriff auf alle zur Verfügung stehenden Eigenschaften.
		 **/
		StorageTemplate* storage;

		/**
		 * Der Typ, dem alle Eigenschaften in diesem Widget angehören sollen.
		 **/
		cv_Trait::Type v_type;
		/**
		 * Eine Liste der kategorien, die in diesem Widget gewünscht sind.
		 **/
		QList< cv_Trait::Category > v_categories;

	public slots:
		/**
		 * Legt den Typ fest, dem alle Eigenschaften in diesem Widget angehören.
		 **/
		void setType( cv_Trait::Type type);

	private slots:
		/**
		 * Fügt eine neue Eigenschaftsauswahl hinzu, sollte keine Eigenschaft ohne mit leerer Auswahl vorhanden sein.
		 **/
		void addWidget();
		/**
		 * Entfernt alle Eigenschaftsauswahlen, welche nicht notwendig sind. Also alle, die einen leeren Namen anzeigen bis auf eine.
		 **/
		void removeWidget();
		/**
		 * Sorgt dafür, daß alle angezeigten Eigenschaften nur jene Marits auswählen können, die nicht schon in einer anderen Eigenschaftsdarstellung ausgewählt sind.
		 *
		 * \todo Natürlich muß Sichergestellt werden, daß Eigenschaften mit erklärendem Text (Language), mehrfach ausgewählt werden können.
		 *
		 * \bug Wird ein Widget gelöscht, wird zwar der Inhalt der vorhandenen Comboboxes angepaßt, aber irgendwie bricht die alphatische Reihenfolge zusammen, bis ich wieder eine andere Combobox ändere.
		 **/
		void refillNameList();

	signals:
};

#endif
