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

QList< cv_AbstractTrait::Type > Creation::types() {
	return v_types;
}


Creation::Creation( QObject* parent ): QObject( parent ) {
	character = StorageCharacter::getInstance();
	storage = new StorageTemplate( this );

	v_pointsList = *storage->creationPoints();

	connect( this, SIGNAL( pointsChanged() ), this, SLOT( controlPoints() ) );
	connect( character, SIGNAL( speciesChanged(cv_Species::SpeciesFlag)), this, SLOT( controlPoints() ) );
}

Creation::~Creation() {
	delete storage;
}



cv_CreationPointsList Creation::pointsList() const {
	return v_pointsList;
}

void Creation::setPoints( cv_CreationPointsList pts ) {
	if ( v_pointsList != pts ) {
		v_pointsList = pts;

		emit pointsChanged();
	}
}

void Creation::calcPoints( Trait* trait ) {
	QList< Trait* > list;
	QList< int > pointList;
	QList< cv_AbstractTrait::Category > categories = cv_AbstractTrait::getCategoryList( trait->type() );

	// Für die Fertigkeitsspezialisierungen.
	int dets = 0;
	
	for ( int i = 0; i < categories.count(); ++i ) {
		int pts = 0;

		list = character->traits( trait->type(), categories.at( i ) );

		for ( int j = 0; j < list.count(); ++j ) {
			// Alle Punkte über 4 kosten 2 Erschaffungspunkte
			int ans = list.at( j )->value() - Config::creationTraitDouble;

			if ( ans < 0 ) {
				ans = 0;
			}

			pts += list.at( j )->value() - ans;

			pts += ans * 2;

			if (!list.at(j)->details().isEmpty()) {
				dets += list.at(j)->details().count();
// 				qDebug() << Q_FUNC_INFO << dets;
			}
		}

		pointList.append( pts );
	}

	// Liste wird nach Größe sortiert, damit steht die größte Zahl ganz am Anfang un danach absteigend.
	qSort( pointList );

	// Natürlich gilt das nicht für den Eintrag des Spezialisierungen, die immer am Anfang stehen.
	// Am Anfang deswegen, weil qSort von Klein nach groß sortiert, und ich deswegen von hinten die Liste auslese.
	if (trait->type() == cv_AbstractTrait::Skill){
		pointList.prepend( dets );
	}

	// Bei Attributen ist der jeweils erste Punkt umsonst.
	if ( trait->type() == cv_AbstractTrait::Attribute ) {
		for ( int i = 0; i < pointList.count(); ++i ) {
			v_pointsList.pointList( character->species(), trait->type() )->operator[]( i ) = storage->creationPoints()->pointList( character->species(), trait->type() )->at( i ) + 3 - pointList.at( pointList.count() - 1 - i );

// 			qDebug() << Q_FUNC_INFO << *v_pointsList.pointList(character->species(), trait->type());
		}
	} else
		if ( trait->type() == cv_AbstractTrait::Merit || trait->type() == cv_AbstractTrait::Power ) {
			int sum = 0;

			for ( int i = 0; i < pointList.count(); ++i ) {
				sum += pointList.at( i );
			}

			v_pointsList.pointList( character->species(), trait->type() )->operator[]( 0 ) = storage->creationPoints()->pointList( character->species(), trait->type() )->at( 0 ) - sum;

// 			qDebug() << Q_FUNC_INFO << *v_pointsList.pointList(character->species(), trait->type()) << character->species() << trait->type();
		} else {
			for ( int i = 0; i < pointList.count(); ++i ) {
// 			qDebug() << Q_FUNC_INFO << pointList.count();

				v_pointsList.pointList( character->species(), trait->type() )->operator[]( i ) = storage->creationPoints()->pointList( character->species(), trait->type() )->at( i ) - pointList.at( pointList.count() - 1 - i );

// 			qDebug() << Q_FUNC_INFO << *v_pointsList.pointList(character->species(), trait->type());
			}
		}

	emit pointsChanged();
}


void Creation::controlPoints() {
	for ( int i = 0; i < v_types.count(); ++i ) {
		bool isZero = true;
		bool isNegative = false;

		for ( int j = 0; j < v_pointsList.pointList( character->species(), v_types.at( i ) )->count(); ++j ) {
			if ( v_pointsList.pointList( character->species(), v_types.at( i ) )->at( j ) < 0 ) {
				// Wenn schon eine Kategorie negativ ist, muß ich nicht weiterkontrollieren.
				isNegative = true;
				break;
			} else if ( v_pointsList.pointList( character->species(), v_types.at( i ) )->at( j ) != 0 ) {
				isZero = false;
			}
		}

		if (isNegative){
			emit pointsNegative( v_types.at( i ) );
			continue;
		} else if ( isZero ) {
			emit pointsDepleted( v_types.at( i ) );
		} else {
			emit pointsPositive( v_types.at( i ) );
		}
	}
}


