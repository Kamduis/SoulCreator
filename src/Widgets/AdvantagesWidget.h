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

#ifndef ADVANTAGESEWIDGET_H
#define ADVANTAGESEWIDGET_H

#include <QGridLayout>

#include "../Storage/StorageCharacter.h"
#include "../Calc/CalcAdvantages.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem sämtliche berechneten Werte angeordnet sind.
 *
 * Die Werte, welche aus den Eigenschaften des Charakters berechnet werden, kommen allesamt in dieses Widget.
 *
 * \todo Diese Klasse sollte nicht auf den Charakter im Speicher verweisen, sondern auf eine Berechnungsklasse, deren Signale dann direkt die Ergebnisse hier anzeigen lassen.
 **/
class AdvantagesWidget : public QWidget {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		AdvantagesWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~AdvantagesWidget();

	private:
		/**
		 * In diesem Layout werden die berechneten Charakterwerte angeordnet.
		 **/
		QGridLayout *layout;
		CalcAdvantages* calcAdvantages;

	public slots:

	private slots:

	signals:
};

#endif
