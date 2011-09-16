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

#ifndef MORALITYWIDGET_H
#define MORALITYWIDGET_H

#include <QGridLayout>
#include <QLabel>

#include "../Datatypes/cv_Species.h"
#include "../Storage/StorageTemplate.h"
#include "../Storage/StorageCharacter.h"

#include <QWidget>


/**
 * @brief Dieses Widget stellt die Moral-Tabelle dar.
 *
 * Diese Tabelle zeigt die aktuelle Moralstufe an und bietet Platz für das Eintragen von Geistesstörungen.
 *
 * \todo Die eingetragenen Geistesstörungen werden noch nicht gespeichert oder geladen.
 **/
class MoralityWidget : public QWidget {
		Q_OBJECT
		/**
		 * Speichert den aktuellen Wert des Widgets.
		 *
		 * Dieser Wert stellt die Zahl der ausgefüllten Punkte dar.
		 *
		 * Wird ein Punkt angeklickt, wird das Widget auf den Wert aller Punkte unter diesem, einschließlich diesem, gesetzt. Die Ausnahme ist der unterste Punkt. Wird dort geklickt, wird der Wert des Widgets auf 0 gesetzt. Ist der unterste Punkt aber leer, wird er in diesem Fall auf 1 gesetzt.
		 *
		 * \access value(), setValue()
		 *
		 * \notifier valueChanged()
		 **/
		Q_PROPERTY( int value READ value WRITE setValue NOTIFY valueChanged )

	public:
		MoralityWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~MoralityWidget();

		QLabel* labelHeader;

		int value() const;

	private:
		QGridLayout* layout;
		StorageTemplate* storage;
		StorageCharacter* character;
		QList< cv_Trait::Category > v_categories;

		int v_value;

	public slots:
		void setValue(int value);

	private slots:
		/**
		 * Setzt die Überschrift dieses Widgets auf einen neuen Namen. Der name hängt von der Spezies ab.
		 **/
		void renameHeader(cv_Species::SpeciesFlag species /** Jede Spezies hat einen eigenen Namen für ihre Moral. Legt man die Spezies fest, wird automatisch die Überschrift angepaßt. */);
		/**
		 * Belegt die Auswahlfelder für die Geistesstörungen neu, so daß immer nur jene angeboten werden, welche ein Charakter dieser Spezies haben kann
		 **/
		void updateDerangements(cv_Species::SpeciesFlag species);
		/**
		 * Speichert die gewählte Geistesstörung im Charakter.
		 *
		 * \todo Es muß ein neuer DAtentyp für die GEiostesstörungen entwickelt werden, damit ich weiß, bei welcher Moral sie platziert werden müssen.
		 *
		 * \todo Wenn ich weiß bei welcher Moral die Geistesstörungen platziert werden, kann ich auch beim ändern des INdex einer Geistesstörungsbox diese direkt im Charakter ändern, ohne alle löschen und neu abarbeiten zu müssen.
		 **/
		void saveDerangements(QString txt);
		/**
		 * Ändert sich der Wert des Widgets, wird hierüber die passende Anzahl an Punkten schwarz ausgemalt.
		 **/
		void drawValue(int value);
		/**
		 * Wird mit der Maus auf den Punkten herumgeklickt, sorgt diese Funktion dafür, daß der richtige Wert des Widgets ermittelt wird.
		 **/
		void resetValue(int value);
		/**
		 * Die ComboBox für die Geistesstörungen wird bis zu dem Wert disabled, der im Argument angegeben wird. Mit dem Disablen werden sie auch gleichzeitig auf den (leeren) Index 0 gesetzt.
		 *
		 * disableDerangements(7) resultiert darin, daß alle FElder für GEistesstörungen disabled werden.
		 **/
		void disableDerangements(int value);

	signals:
		void valueChanged(int value);
};

#endif
