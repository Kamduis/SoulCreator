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

#ifndef POWERWIDGET_H
#define POWERWIDGET_H

#include <QHBoxLayout>
#include <QToolBox>
#include <QPushButton>

// #include "Datatypes/cv_TraitDetail.h"
#include "Storage/StorageCharacter.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem sämtliche Übernatürlichen Kräfte angeordnet sind.
 *
 * \bug Da ich die Eigenschaften, welche für die jeweilige Spezies nicht gelten nur verstecke, nehmen sie doch ein klein wenig Platz weg. Und das fällt tatsächlich auf!
 *
 * \todo Ein gesondertes Widget für die Sonderkräfte machen. Hier tauchen die Übergeordneten Powers auf, in dem anderen Widget dann die speziellen Kräfte (Vampire-Rituale, Werwolf-Gaben + Rituale, Mage-Rotes, Changeling-???)
 **/
class PowerWidget : public QWidget {
		Q_OBJECT

	public:
		/**
		 * Konstruktor.
		 **/
		PowerWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~PowerWidget();

	private:
		QHBoxLayout* layout;
		QToolBox* toolBox;
		StorageCharacter* character;
		StorageTemplate* storage;

	public slots:

	private slots:
		/**
		 * Verändert bei jedem wechsel der Spezies die Überschriften der einzelnen Kategorien der Kräfte.
		 **/
		void updateHeaders( cv_Species::SpeciesFlag spe );

	signals:
};

#endif
