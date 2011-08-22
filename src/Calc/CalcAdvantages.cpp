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

#include "CalcAdvantages.h"

CalcAdvantages::CalcAdvantages( QObject* parent ): QObject( parent ) {
	character = StorageCharacter::getInstance();

	connect( character, SIGNAL( traitChanged( cv_Trait ) ), this, SLOT( calcSize( cv_Trait ) ) );
	connect( character, SIGNAL( traitChanged( cv_Trait ) ), this, SLOT( calcSpeed( cv_Trait ) ) );
	connect( character, SIGNAL( traitChanged( cv_Trait ) ), this, SLOT( calcDefense( cv_Trait ) ) );
}

int CalcAdvantages::calcSize( cv_Trait trait ) {
	if ( trait.type == cv_Trait::Merit && trait.name == "Giant" ) {
		int result = 5;

		if ( trait.value > 0 ) {
			result += 1;
		}

		emit sizeChanged( result );

		return result;
	}
}

int CalcAdvantages::calcSpeed( cv_Trait trait ) {
	if ( trait.type == cv_Trait::Attribute ) {
		bool exists = false;

		int val1 = trait.value;
		int val2;

		if (trait.name == "Strength") {
			for ( int i = 0; i < character->traits( cv_Trait::Attribute, cv_Trait::Physical ).count(); i++ ) {
				if ( character->traits( cv_Trait::Attribute, cv_Trait::Physical ).at( i ).name == "Dexterity" ) {
					val2 = character->traits( cv_Trait::Attribute, cv_Trait::Physical ).at( i ).value;
					exists = true;
					break;
				}
			}
			if ( !exists ) {
				val2 = 0;
				exists = false;
			}
		} else if (trait.name == "Dexterity") {
			for ( int i = 0; i < character->traits( cv_Trait::Attribute, cv_Trait::Physical ).count(); i++ ) {
				if ( character->traits( cv_Trait::Attribute, cv_Trait::Physical ).at( i ).name == "Strength" ) {
					val2 = character->traits( cv_Trait::Attribute, cv_Trait::Physical ).at( i ).value;
					exists = true;
					break;
				}
			}
			if ( !exists ) {
				val2 = 0;
				exists = false;
			}
		}

		int result = val1 + val2 + 5;

		emit speedChanged( result );

		return result;
	}
}

int CalcAdvantages::calcDefense( cv_Trait trait ) {
	if (( trait.type == cv_Trait::Attribute && ( trait.name == "Wits" || trait.name == "Dexterity" ) )
			|| trait.type == cv_Trait::Merit && trait.name == "Fast Reflexes" ) {
		int val1;
		int val2;
		int val3;

		bool exists = false;

		// Nur berechnen, wenn der veränderte Wert Einfluß auf die Defense hat.
		if ( trait.type == cv_Trait::Attribute ) {
			val1 = trait.value;
			for ( int i = 0; i < character->traits( cv_Trait::Merit, cv_Trait::Physical ).count(); i++ ) {
				if ( character->traits( cv_Trait::Merit, cv_Trait::Physical ).at( i ).name == "Fast Reflexes" ) {
					val3 = character->traits( cv_Trait::Merit, cv_Trait::Physical ).at( i ).value;
					exists = true;
					break;
				}
			}

			if ( !exists ) {
				val3 = 0;
				exists = false;
			}
			if ( trait.name == "Wits" ) {
				for ( int i = 0; i < character->traits( cv_Trait::Attribute, cv_Trait::Physical ).count(); i++ ) {
					if ( character->traits( cv_Trait::Attribute, cv_Trait::Physical ).at( i ).name == "Dexterity" ) {
						val2 = character->traits( cv_Trait::Attribute, cv_Trait::Physical ).at( i ).value;
						exists = true;
						break;
					}
				}
				if ( !exists ) {
					val2 = 0;
					exists = false;
				}
			} else if ( trait.name == "Dexterity" ) {
				for ( int i = 0; i < character->traits( cv_Trait::Attribute, cv_Trait::Mental ).count(); i++ ) {
					if ( character->traits( cv_Trait::Attribute, cv_Trait::Mental ).at( i ).name == "Wits" ) {
						val2 = character->traits( cv_Trait::Attribute, cv_Trait::Mental ).at( i ).value;
						exists = true;
						break;
					}
				}
				if ( !exists ) {
					val2 = 0;
					exists = false;
				}
			}
		} else if ( trait.type == cv_Trait::Merit && trait.name == "Fast Reflexes" ) {
			val3 = trait.value;
			for ( int i = 0; i < character->traits( cv_Trait::Attribute, cv_Trait::Mental ).count(); i++ ) {
				if ( character->traits( cv_Trait::Attribute, cv_Trait::Mental ).at( i ).name == "Wits" ) {
					val1 = character->traits( cv_Trait::Attribute, cv_Trait::Mental ).at( i ).value;
					exists = true;
					break;
				}
			}
			if ( !exists ) {
				val1 = 0;
				exists = false;
			}
			for ( int i = 0; i < character->traits( cv_Trait::Attribute, cv_Trait::Physical ).count(); i++ ) {
				if ( character->traits( cv_Trait::Attribute, cv_Trait::Physical ).at( i ).name == "Dexterity" ) {
					val2 = character->traits( cv_Trait::Attribute, cv_Trait::Physical ).at( i ).value;
					exists = true;
					break;
				}
			}
			if ( !exists ) {
				val2 = 0;
				exists = false;
			}
		}

// 		qDebug() << Q_FUNC_INFO << "Attribute: " << val1 << val2 << "und Merit:" << val3;

		int result = qMin( val1, val2 ) + val3;

		emit defenseChanged( result );

		return result;
	}
}

