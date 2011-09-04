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

#include "../Exceptions/Exception.h"

#include "cv_Shape.h"

QString cv_Shape::toString( cv_Shape::WerewolfShape shape ) {
	switch ( shape ) {
		case cv_Shape::ShapeNo:
			return QObject::tr( "Without Shape" );
		case cv_Shape::Hishu:
			return QObject::tr( "Hishu" );
		case cv_Shape::Dalu:
			return QObject::tr( "Dalu" );
		case cv_Shape::Gauru:
			return QObject::tr( "Gauru" );
		case cv_Shape::Urshul:
			return QObject::tr( "Urshul" );
		case cv_Shape::Urhan:
			return QObject::tr( "Urhan" );
		default:
			throw eWerewolfShapeNotExisting( shape );
	}
}

cv_Shape::WerewolfShape cv_Shape::toShape( QString str ) {
	if ( str == "ShapeNo" )
		return cv_Shape::ShapeNo;
	else if ( str == "Hishu" )
		return cv_Shape::Hishu;
	else if ( str == "Dalu" )
		return cv_Shape::Dalu;
	else if ( str == "Gauru" )
		return cv_Shape::Gauru;
	else if ( str == "Urshul" )
		return cv_Shape::Urshul;
	else if ( str == "Urhan" )
		return cv_Shape::Urhan;
	else
		throw eWerewolfShapeNotExisting( str );
}