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

#include <QWidget>


/**
 * @brief Das Widget, in welchem sämtliche Merits angeordnet sind.
 *
 * Die Attribute werden in diesem Widget angeordnet.
 *
 * \todo Später sollen nur soviele Merits dargestellt werden, wie der Charakter tatsächlich hat +1. Will der Nutzer einen zusätzlichen Merit hinzufügen, füllt er diese leere Meritzeile aus und das Widget fügt automatisch eine weitere Leere Zeile am Ende ein. Alle leeren Merit-Widgets bis auf das letzte werden automatisch gelöscht.
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
		 * In diesem Layout werden die Attribute angeordnet.
		 **/
		QVBoxLayout *layout;

	public slots:

	private slots:

	signals:
};

#endif
