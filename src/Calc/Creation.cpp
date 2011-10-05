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

#include <QDebug>

// #include "Exceptions/Exception.h"
#include "Config/Config.h"

#include "Creation.h"


const QList< cv_AbstractTrait::Type > Creation::v_types = QList< cv_AbstractTrait::Type >()
		<< cv_AbstractTrait::Attribute
		<< cv_AbstractTrait::Skill
		<< cv_AbstractTrait::Merit
		<< cv_AbstractTrait::Power;


Creation::Creation( QObject* parent ): QObject( parent ) {
	v_points = cv_CreationPoints();

	character = StorageCharacter::getInstance();

	connect( character, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( calcPoints( cv_Trait* ) ) );
	connect( this, SIGNAL(pointsChanged(cv_CreationPoints)), this, SLOT( controlPoints(cv_CreationPoints) ));
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
	if ( v_types.contains( trait->type() ) ) {
		QList< Trait* > list;
		QList< int > pointList;
		// Nur bei Attributen und Fertigkeiten sind die zu verteilenden Punkte zwischen den Kategorien aufgeteilt.

		if ( trait->type() == cv_AbstractTrait::Attribute || trait->type() == cv_AbstractTrait::Skill ) {
			QList< cv_AbstractTrait::Category > categories = cv_AbstractTrait::getCategoryList( trait->type() );

			for ( int i = 0; i < categories.count(); i++ ) {
				int pts = 0;

				list = character->traits( trait->type(), categories.at( i ) );

				for ( int j = 0; j < list.count(); j++ ) {
					// Alle Punkte über 4 kosten 2 Erschaffungspunkte
					int ans = list.at( j )->value() - Config::creationTraitDouble;

					if ( ans < 0 ) {
						ans = 0;
					}

					pts += list.at( j )->value() - ans;

					pts += ans * 2;
				}

				pointList.append( pts );
			}

			// Liste wird nach größe sortiert, damit steht die größte Zahl ganz am Anfang un danach absteigend.
			qSort( pointList );

			// Bei Attributen ist der jeweils erste Punkt umsonst.
			if ( trait->type() == cv_AbstractTrait::Attribute ) {
				v_points.attributesA = Config::creationPointsAttA + 3 - pointList.at( 2 );
				v_points.attributesB = Config::creationPointsAttB + 3 - pointList.at( 1 );
				v_points.attributesC = Config::creationPointsAttC + 3 - pointList.at( 0 );
			} else if ( trait->type() == cv_AbstractTrait::Skill ) {
				v_points.skillsA = Config::creationPointsSkillA - pointList.at( 2 );
				v_points.skillsB = Config::creationPointsSkillB - pointList.at( 1 );
				v_points.skillsC = Config::creationPointsSkillC - pointList.at( 0 );
			}
		} else {
			int pts = 0;

			list = character->traits( trait->type() );

			for ( int j = 0; j < list.count(); j++ ) {
				// Alle Punkte über 4 kosten 2 Erschaffungspunkte
				int ans = list.at( j )->value() - Config::creationTraitDouble;

				if ( ans < 0 ) {
					ans = 0;
				}

				pts += list.at( j )->value() - ans;

				pts += ans * 2;
			}

			if ( trait->type() == cv_AbstractTrait::Merit ) {
				v_points.merits = Config::creationPointsMerits - pts;
			}
		}

// 		qDebug() << Q_FUNC_INFO << pointList;

		emit pointsChanged( points() );
	}
}

void Creation::controlPoints( cv_CreationPoints points )
{
	if (points.attributesA == 0 && points.attributesB == 0 && points.attributesC == 0){
		emit pointsDepleted(cv_AbstractTrait::Attribute);
	} else if (points.attributesA < 0 || points.attributesB < 0 || points.attributesC < 0){
		emit pointsNegative(cv_AbstractTrait::Attribute);
	} else {
		emit pointsPositive(cv_AbstractTrait::Attribute);
	}

	if (points.skillsA == 0 && points.skillsB == 0 && points.skillsC == 0){
		emit pointsDepleted(cv_AbstractTrait::Skill);
	} else if (points.skillsA < 0 || points.skillsB < 0 || points.skillsC < 0){
		emit pointsNegative(cv_AbstractTrait::Skill);
	} else {
		emit pointsPositive(cv_AbstractTrait::Skill);
	}

	if (points.merits == 0){
		emit pointsDepleted(cv_AbstractTrait::Merit);
	} else if (points.merits < 0){
		emit pointsNegative(cv_AbstractTrait::Merit);
	} else {
		emit pointsPositive(cv_AbstractTrait::Merit);
	}
}


