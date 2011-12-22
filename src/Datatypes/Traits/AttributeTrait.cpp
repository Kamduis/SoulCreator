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

#include <QDebug>

#include "Exceptions/Exception.h"
#include "Parser/StringBoolParser.h"

#include "AttributeTrait.h"


AttributeTrait::AttributeTrait( QString txt, int val, cv_Species::Species spe, cv_AbstractTrait::Category ca, QObject* parent ) : Trait( txt, val, spe, cv_AbstractTrait::Attribute, ca ) {
}

AttributeTrait::AttributeTrait( cv_Trait trait, QObject* parent ) : Trait( trait, parent ) {
}

AttributeTrait::AttributeTrait( Trait* trait, QObject* parent ) : Trait( trait, parent ) {
}


int AttributeTrait::value() const {
// 	qDebug() << Q_FUNC_INFO << "Wird aufgerufen für" << name();
	if (isBonus()){
		qDebug() << Q_FUNC_INFO << "Wird aufgerufen für" << name() << "und gibt +1 zurück";
		return cv_Trait::value() + 1;
	} else {
		return cv_Trait::value();
	}
}


void AttributeTrait::setBonus( bool sw ) {
// 	qDebug() << Q_FUNC_INFO << "Wird aufgerufen!";
	if ( isBonus() != sw ) {
// 		qDebug() << Q_FUNC_INFO << "Wird verändert!";
		cv_Trait::setBonus( sw );

		emit bonusChanged( sw );
		emit valueChanged( value() );
	}
}
