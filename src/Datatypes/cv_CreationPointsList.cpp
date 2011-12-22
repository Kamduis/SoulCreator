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


#include <QStringList>
#include <QDebug>

// #include "Config/Config.h"
// #include "Exceptions/Exception.h"

#include "cv_CreationPointsList.h"


cv_CreationPointsList::cv_CreationPointsList() : QList< cv_CreationPoints >() {
}


QString cv_CreationPointsList::outputPoint( int val ) {
	if ( val < 0 ) {
		return "<font color='red'>" + QString::number( val ) + "</font>";
	}
	return QString::number( val );
}


QString cv_CreationPointsList::pointString(cv_Species::SpeciesFlag spe, cv_AbstractTrait::Type tp ) {
	QStringList resultList;

	for ( int i = 0; i < this->count(); ++i ) {
		if ( this->at(i).species.testFlag(spe) && this->at( i ).type == tp ) {
			for ( int j = 0; j < this->at(i).points.count(); ++j ) {
				resultList.append(outputPoint(this->at(i).points.at(j)));
			}
		}
	}

	if (tp != cv_AbstractTrait::Skill){
		return QObject::tr("Points left: %1").arg(resultList.join( "/" ));
	} else {
		QString specialty = resultList.takeLast();
		QString result = resultList.join( "/" );

		return QObject::tr("Points left: %1 Specialties left: %2").arg(result).arg(specialty);
	}
}

QList< int >* cv_CreationPointsList::pointList( cv_Species::SpeciesFlag spe, cv_AbstractTrait::Type tp )
{
// 	qDebug() << Q_FUNC_INFO << spe << tp;
	for ( int i = 0; i < this->count(); ++i ) {
// 		qDebug() << Q_FUNC_INFO << this->at(i).species << this->at(i).type << this->at(i).points;
		if ( this->at(i).species.testFlag(spe) && this->at( i ).type == tp ) {
			return &this->operator[](i).points;
		}
	}

	qDebug() << Q_FUNC_INFO << "Da ging was schief!";
	return 0;
}


// QString cv_CreationPointsList::skillsOut() {
// 	QStringList resultList;
//
// 	for ( int i = 0; i < skills.count(); ++i ) {
// 		resultList.append( outputPoint( skills.at( i ) ) );
// 	}
//
// 	return resultList.join( "/" );
// }
//
// QString cv_CreationPointsList::skillSpecialtiesOut() {
// 	return outputPoint( skillSpecialties );
// }
//
// QString cv_CreationPointsList::meritsOut() {
// 	return outputPoint( merits );
// }
//
// QString cv_CreationPointsList::powersOut() {
// 	return outputPoint( powers );
// }


// bool cv_CreationPointsList::operator==( const cv_CreationPointsList& points ) const {
// 	if ( this == &points ) {
// 		return true;
// 	}
//
// 	bool result = species == points.species &&
// 				  attributes == points.attributes &&
// 				  skills == points.skills &&
// 				  skillSpecialties == points.skillSpecialties &&
// 				  merits == points.merits &&
// 				  powers == points.powers;
//
// 	return result;
// }
//
// bool cv_CreationPointsList::operator!=( const cv_CreationPointsList& points ) const {
// 	if ( this == &points ) {
// 		return false;
// 	}
//
// 	bool result = species != points.species ||
// 				  attributes != points.attributes ||
// 				  skills != points.skills ||
// 				  skillSpecialties != points.skillSpecialties ||
// 				  merits != points.merits ||
// 				  powers != points.powers;
//
// 	return result;
// }
