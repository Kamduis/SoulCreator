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
		 * In diesem Layout werden die Attribute angeordnet.
		 **/
		QGridLayout *layout;
		/**
		 * Eine Auswahlbox für die zur Verfügung stehenden Spezies.
		 **/
		CharaSpecies* speciesComboBox;


	public slots:

	private slots:

	signals:
};

#endif
