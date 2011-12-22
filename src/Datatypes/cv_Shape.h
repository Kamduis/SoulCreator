/**
 * \file
 * \author Victor von Rhein <victor@caern.de>
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

#ifndef CV_SHAPE_H
#define CV_SHAPE_H

#include <QString>

/**
 * @brief Diese Klasse hält die Funktionen bezüglich der verschiedenen Gestalten eines Werwolfs vor.
 */
class cv_Shape {
	public:
		enum WerewolfShape {
			ShapeNo,
			Hishu,
			Dalu,
			Gauru,
			Urshul,
			Urhan
		};
		/**
		 * Wandelt einen Text in die passende Gestalt um.
		 **/
		static QString toString(cv_Shape::WerewolfShape shape);
		/**
		 * Gibt den Namen der Gestalt aus.
		 **/
		static cv_Shape::WerewolfShape toShape( QString str );
		/**
		 * Gibt eine Liste aller möglichen Gestalten aus.
		 **/
		static QList< cv_Shape::WerewolfShape > getShapeList();

	private:
		/**
		 * Eine Liste aller Werwolfgestalten
		 **/
		static const QList< cv_Shape::WerewolfShape > v_shapeListWerewolf;

};

#endif

