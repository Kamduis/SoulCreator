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

#ifndef CV_NAME_H
#define CV_NAME_H

#include <QStringList>
#include <QString>

/**
 * @brief Diese Klasse speichert den vollständigen Namen eines Charakters.
 *
 * Jede Person besitzt eine Vielzahl von Namen, die über diese Klasse leicht zu verwalten sind.
 *
 * Bei Personen mit mehreren Identitäten, sollte eine Liste dieser Klasse angelegt werden, in welcher für jede Identität ein Eintrag vorgenommen wird. Auch ein Künstlername fällt unter diese Kategorie, solta also mit einem weiteren Listeneintrag realisiert werden.
 */
class cv_Name {
	public:
		/**
		 * Vorname.
		 *
		 * Dieser Name wurde dem Charakter von seinen Eltern gegeben. Es besteht die Möglichkeit, mehr als einen Vornamen zu besitzen, wesewegen diese Variable vom Typ StringList ist. Der erste Vorname in dieser Liste ist immer auch der Rufname.
		 *
		 * \sa firstName
		 **/
		QStringList foreName;
		/**
		 * Rufname
		 *
		 * Bei Personen mit nur einem Vornamen entspricht \ref firstName dem \ref foreName. Bei Personen mit mehreren Vornamen ist \ref firstName immer der allererste \ref foreName.
		 *
		 * \sa foreName
		 **/
		QString firstName() const;
		/**
		 * Nachname
		 *
		 * Der Familienname der Eltern.
		 **/
		QString sureName;
		/**
		 * Namenszusatz
		 *
		 * Hierunter fallen beispielsweise Adelsprädikate (von, von und zu, etc.)
		 **/
		QString affixName;
		/**
		 * Geburtsname.
		 *
		 * Dieser Name wurde dem Charakter von seinen Eltern gegeben und besteht aus Rufname (\ref firstName) und Nachname (\ref sureName) plus Namenszusatz (\ref affixName).
		 *
		 * \note Die Kenntnis dieses Namens erleichtert Magiern sympathische Magie.
		 **/
		QString birthName() const;
		/**
		 * Beiname.
		 *
		 * Ein Beinahme, den der Charakter entweder durch ehrenvolle Taten, durch körperliche Besonderheiten oder durch Mißgeschick erworben hat.
		 *
		 * - der Starke
		 * - die Schöne
		 * - die Kleine
		 * - der Treue
		 **/
		QString additionalName;
		/**
		 * Spitzname.
		 *
		 * Mit diesem Namen wird der Charakter meist von Freunden (Menschen) gerufen.
		 **/
		QString nickName;
		/**
		 * Name unter den Übernatürlichen
		 *
		 * Dies ist der Name, der von den übrigen Kreaturen seiner Spezies verwendet wird.
		 **/
		QString supernaturalName;
};

#endif

