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

#ifndef CREATION_H
#define CREATION_H

// #include "Datatypes/cv_Trait.h"
#include "Datatypes/cv_CreationPointsList.h"
#include "Storage/StorageCharacter.h"

#include <QObject>

/**
 * \brief Berechnet die verbleibenden Punkte bei der Charaktererschaffung.
 */

class Creation : public QObject {
		Q_OBJECT

	public:
		Creation( QObject* parent = 0 );
		~Creation();

		/**
		 * Gibt die Anzahl der noch verfügbaren Punkte bei der Charaktererschaffung zurück.
		 *
		 * \note Bevor die Anzahl der freien Punkte ausgegeben wird, wird sie jedesmal berechnet.
		 **/
		cv_CreationPointsList pointsList() const;
		/**
		 * Gibt alle Eigenschaftstypen aus, bei denen die Berechnung der freien Erschaffungspunkte überhaupt nötig ist.
		 **/
		static QList< cv_AbstractTrait::Type > types();

		
	private:
		/**
		 * Zeiger auf die Klasse, welche sämtliche Charaterwerte enthält. Eine Änderung der Werte in dieser Klasse sorgen dafür, daß sich auch die Anzeige anpaßt. Und ändert man einen Wert in der Anzeige, wird automatisch die dadurch repräsentierte Eigenschaft in dieser Klasse verändert.
		 */
		StorageCharacter* character;
		StorageTemplate* storage;

		static const QList< cv_AbstractTrait::Type > v_types;
		cv_CreationPointsList v_pointsList;

	public slots:
		/**
		 * Legt die noch verfügbaren Punkte für die Charaktererschaffung fest.
		 *
		 * \note Sendet das Signal creationPointsChanged() aus.
		 **/
		void setPoints( cv_CreationPointsList pts );
		/**
		 * Berechnet die noch verfügbaren Punkte.
		 **/
		void calcPoints( Trait* trait );

	private slots:
		/**
		 * Kontrolliert, ob die Punkte erschöpft sind oder gar übermäßig ausgeschöpft wurden und sendet entsprechende Signale aus.
		 *
		 * \sa pointsDepleted
		 *
		 * \sa pointsNegative
		 *
		 * \sa pointsPositive
		 **/
		void controlPoints();

	signals:
		/**
		* Dieses Signal wird ausgesandt, wann immer sich die Anzahl der noch freien Erschaffungspunkte ändert.
		**/
		void pointsChanged();
		/**
		* Dieses Signal wird ausgesandt, wann immer sich die Anzahl der noch freien Erschaffungspunkte für einen Typ erschöpft.
		**/
		void pointsDepleted( cv_AbstractTrait::Type type /** Dies ist der Typ, dessen Punkte erschöpft sind. */ );
		/**
		* Dieses Signal wird ausgesandt, wann immer sich die Anzahl der noch freien Erschaffungspunkte für einen Typ ändert und das Resultat negativ ist.
		**/
		void pointsNegative( cv_AbstractTrait::Type type /** Dies ist der Typ, dessen Punkte negativ sind. */ );
		/**
		* Dieses Signal wird ausgesandt, wann immer sich die Anzahl der noch freien Erschaffungspunkte für einen Typ ändert und das Resultat positiv ist.
		**/
		void pointsPositive( cv_AbstractTrait::Type type /** Dies ist der Typ, dessen Punkte positiv sind. */ );
};

#endif

