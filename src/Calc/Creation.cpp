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

#include <QDebug>

#include "Exceptions/Exception.h"
#include "Config/Config.h"

#include "Creation.h"


const QList< cv_Trait::Type > Creation::v_types = QList< cv_Trait::Type >()
		<< cv_Trait::Attribute
		<< cv_Trait::Skill
		<< cv_Trait::Merit
		<< cv_Trait::Power;


Creation::Creation( QObject* parent ): QObject( parent ) {
	v_points = cv_CreationPoints();

	character = StorageCharacter::getInstance();

	connect( character, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( calcPoints( cv_Trait* ) ) );
}


cv_CreationPoints Creation::points() const {
	return v_points;
}

void Creation::setPoints( cv_CreationPoints points ) {
	if ( v_points != points ) {
		v_points = points;

		emit pointsChanged( points );
	}
}

void Creation::calcPoints( cv_Trait* trait ) {
// 	qDebug() << Q_FUNC_INFO << trait->type << "<->" << v_types;
	if ( v_types.contains( trait->type ) ) {
		QList< cv_Trait > list;
		QList< int > pointList;
		// Nur bei Attributen und Fertigkeiten sind die zu verteilenden Punkte zwischen den Kategorien aufgeteilt.

		if ( trait->type == cv_Trait::Attribute || trait->type == cv_Trait::Skill ) {
			QList< cv_Trait::Category > categories = cv_Trait::getCategoryList( trait->type );

			for ( int i = 0; i < categories.count(); i++ ) {
				int pts = 0;

				list = character->traits( trait->type, categories.at( i ) );

				for ( int j = 0; j < list.count(); j++ ) {
					// Alle Punkte über 4 kosten 2 Erschaffungspunkte
					int ans = list.at( j ).value - Config::creationTraitDouble;

					if ( ans < 0 ) {
						ans = 0;
					}

					pts += list.at( j ).value - ans;

					pts += ans * 2;
				}

				pointList.append( pts );
			}

			// Liste wird nach größe sortiert, damit steht die größte Zahl ganz am Anfang un danach absteigend.
			qSort( pointList );

			// Bei Attributen ist der jeweils erste Punkt umsonst.
			if ( trait->type == cv_Trait::Attribute ) {
				v_points.attributesA = cv_CreationPoints::creationPointsAttA + 3 - pointList.at( 2 );
				v_points.attributesB = cv_CreationPoints::creationPointsAttB + 3 - pointList.at( 1 );
				v_points.attributesC = cv_CreationPoints::creationPointsAttC + 3 - pointList.at( 0 );
			} else if ( trait->type == cv_Trait::Skill ) {
				v_points.skillsA = cv_CreationPoints::creationPointsSkillA - pointList.at( 2 );
				v_points.skillsB = cv_CreationPoints::creationPointsSkillB - pointList.at( 1 );
				v_points.skillsC = cv_CreationPoints::creationPointsSkillC - pointList.at( 0 );
			}
		} else {
			int pts = 0;

			list = character->traits( trait->type );

			for ( int j = 0; j < list.count(); j++ ) {
				// Alle Punkte über 4 kosten 2 Erschaffungspunkte
				int ans = list.at( j ).value - Config::creationTraitDouble;

				if ( ans < 0 ) {
					ans = 0;
				}

				pts += list.at( j ).value - ans;

				pts += ans * 2;
			}

			if ( trait->type == cv_Trait::Merit ) {
				v_points.merits = cv_CreationPoints::creationPointsMerits - pts;
			}
		}

// 		qDebug() << Q_FUNC_INFO << pointList;

		emit pointsChanged( points() );
	}
}
