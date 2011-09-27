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

#ifndef CV_SPECIES_H
#define CV_SPECIES_H

#include <QString>


/**
 * @brief Datentyp für unterschiedliche Spezies der WoD.
 *
 * Jede Spezies der WoD hat einige variierende Eigeschaften, die über dieses Datentyp verwaltet werden können.
 */

class cv_Species {
	public:
		/**
		 * Auswahl der zur Verügung stehenden Spezies.
		 *
		 *  <table border=0px>
		 *  <tr>
		 *     <td><b>Flag</b></td>
		 *     <td><b>Value</b></td>
		 *     <td><b>Description</b></td>
		 *  </tr>
		 *  <tr>
		 *     <td>SpeciesFlag::SpeciesNo</td>
		 *     <td>000000</td>
		 *     <td>Keiner Spezies zuzuordnen</td>
		 *  </tr>
		 *  <tr>
		 *     <td>SpeciesFlag::Animal</td>
		 *     <td>000001</td>
		 *     <td>Mundane Tiere</td>
		 *  </tr>
		 *  <tr>
		 *     <td>SpeciesFlag::Human</td>
		 *     <td>000010</td>
		 *     <td>Mundane Menschen</td>
		 *  </tr>
		 *  <tr>
		 *     <td>SpeciesFlag::Changeling</td>
		 *     <td>000100</td>
		 *     <td>Wechselbälger</td>
		 *  </tr>
		 *  <tr>
		 *     <td>SpeciesFlag::Mage</td>
		 *     <td>001000</td>
		 *     <td>Magier</td>
		 *  </tr>
		 *  <tr>
		 *     <td>SpeciesFlag::Vampire</td>
		 *     <td>010000</td>
		 *     <td>Vampire</td>
		 *  </tr>
		 *  <tr>
		 *     <td>SpeciesFlag::Werewolf</td>
		 *     <td>100000</td>
		 *     <td>Werwölfe</td>
		 *  </tr>
		 *  <tr>
		 *     <td>SpeciesFlag::SpeciesAll</td>
		 *     <td>111111</td>
		 *     <td>Gehört zu allen Spezies. Ist die Binäre Summe aller anderen Spezies.</td>
		 *  </tr>
		 *  </table>
		*/
		enum SpeciesFlag {
			SpeciesNo	= 0x0,
			Animal		= 0x1,
			Human		= 0x2,
			Changeling	= 0x4,
			Mage		= 0x8,
			Vampire		= 0x10,
			Werewolf	= 0x20,
			SpeciesAll	= 0x3F
		};
		Q_DECLARE_FLAGS( Species, SpeciesFlag )	// Hiermit ermögliche ich die Verwendung von xx1|xx2|xx3

// 		/**
// 		 * Die Spezies.
// 		 **/
// 		SpeciesFlag species;
		/**
		 * Der Namen der Spezies.
		 **/
		QString name;
		/**
		 * Der Name der Moral-Eigenschaft.
		 **/
		QString morale;
		/**
		 * Der Name der übernatürlichen Eigenschaft.
		 **/
		QString supertrait;
		/**
		 * Der Namen der übernatürlichen Energieform, welche diese Spezies verwendet.
		 **/
		QString fuel;

		/**
		 * Gibt den Namen der Spezies aus. Anders als name() dient diese statische funktion dazu, den enum SpeciesFlag als String zurückzugeben, was ich für das Speichern in den XML_Dateien benötige.
		 **/
		static QString toString( SpeciesFlag flag );
		/**
		 * Wandelt den Namen einer Spezies in den dazu passenden enum SpeciesFlag um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien in Flags umzuwandeln.
		 **/
		static cv_Species::SpeciesFlag toSpecies( QString str );

		bool operator==( const cv_Species &points ) const;
};

Q_DECLARE_OPERATORS_FOR_FLAGS( cv_Species::Species )

#endif
