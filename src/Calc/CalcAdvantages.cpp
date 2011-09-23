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

#include "CalcAdvantages.h"

int CalcAdvantages::v_size = 0;
int CalcAdvantages::v_initiative = 0;
int CalcAdvantages::v_speed = 0;
int CalcAdvantages::v_defense = 0;
int CalcAdvantages::v_health = 0;
int CalcAdvantages::v_willpower = 0;


CalcAdvantages::CalcAdvantages( QObject* parent ): QObject( parent ) {
	character = StorageCharacter::getInstance();

	connect( character, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( calcSize( cv_Trait* ) ) );
	connect( character, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( calcInitiative( cv_Trait* ) ) );
	connect( character, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( calcSpeed( cv_Trait* ) ) );
	connect( character, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( calcDefense( cv_Trait* ) ) );
	connect( character, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( calcHealth( cv_Trait* ) ) );
	connect( character, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( calcWillpower( cv_Trait* ) ) );
	connect( this, SIGNAL( sizeChanged( int ) ), this, SLOT( calcHealth( int ) ) );
}


int CalcAdvantages::strength( int str, cv_Shape::WerewolfShape shape ) {
	switch ( shape ) {
		case cv_Shape::ShapeNo:
			return str;
		case cv_Shape::Hishu:
			return str;
		case cv_Shape::Dalu:
			return str + 1;
		case cv_Shape::Gauru:
			return str + 3;
		case cv_Shape::Urshul:
			return str + 2;
		case cv_Shape::Urhan:
			return str;
		default:
			throw eWerewolfShapeNotExisting( shape );
	}
}

int CalcAdvantages::dexterity( int dex, cv_Shape::WerewolfShape shape ) {
	switch ( shape ) {
		case cv_Shape::ShapeNo:
			return dex;
		case cv_Shape::Hishu:
			return dex;
		case cv_Shape::Dalu:
			return dex;
		case cv_Shape::Gauru:
			return dex + 1;
		case cv_Shape::Urshul:
			return dex + 2;
		case cv_Shape::Urhan:
			return dex + 2;
		default:
			throw eWerewolfShapeNotExisting( shape );
	}
}

int CalcAdvantages::stamina( int sta, cv_Shape::WerewolfShape shape ) {
	switch ( shape ) {
		case cv_Shape::ShapeNo:
			return sta;
		case cv_Shape::Hishu:
			return sta;
		case cv_Shape::Dalu:
			return sta + 1;
		case cv_Shape::Gauru:
			return sta + 2;
		case cv_Shape::Urshul:
			return sta + 2;
		case cv_Shape::Urhan:
			return sta + 1;
		default:
			throw eWerewolfShapeNotExisting( shape );
	}
}

int CalcAdvantages::manipulation( int man, cv_Shape::WerewolfShape shape ) {
	switch ( shape ) {
		case cv_Shape::ShapeNo:
			return man;
		case cv_Shape::Hishu:
			return man;
		case cv_Shape::Dalu:
			return man - 1;
		case cv_Shape::Gauru:
			return man;
		case cv_Shape::Urshul:
			return man - 3;
		case cv_Shape::Urhan:
			return man;
		default:
			throw eWerewolfShapeNotExisting( shape );
	}
}


int CalcAdvantages::size( cv_Shape::WerewolfShape shape ) const {
	switch ( shape ) {
		case cv_Shape::ShapeNo:
			return v_size;
		case cv_Shape::Hishu:
			return v_size;
		case cv_Shape::Dalu:
			return v_size + 1;
		case cv_Shape::Gauru:
			return v_size + 2;
		case cv_Shape::Urshul:
			return v_size + 1;
		case cv_Shape::Urhan:
			return v_size - 1;
		default:
			throw eWerewolfShapeNotExisting( shape );
	}
}

int CalcAdvantages::initiative( cv_Shape::WerewolfShape shape ) const {
	switch ( shape ) {
		case cv_Shape::ShapeNo:
			return v_initiative;
		case cv_Shape::Hishu:
			return v_initiative;
		case cv_Shape::Dalu:
			return v_initiative;
		case cv_Shape::Gauru:
			return v_initiative + 1;
		case cv_Shape::Urshul:
			return v_initiative + 2;
		case cv_Shape::Urhan:
			return v_initiative + 2;
		default:
			throw eWerewolfShapeNotExisting( shape );
	}
}

int CalcAdvantages::speed( cv_Shape::WerewolfShape shape ) const {
	switch ( shape ) {
		case cv_Shape::ShapeNo:
			return v_speed;
		case cv_Shape::Hishu:
			return v_speed;
		case cv_Shape::Dalu:
			return v_speed + 1;
		case cv_Shape::Gauru:
			return v_speed + 4;
		case cv_Shape::Urshul:
			return v_speed + 7;
		case cv_Shape::Urhan:
			return v_speed + 5;
		default:
			throw eWerewolfShapeNotExisting( shape );
	}
}

int CalcAdvantages::defense() const {
	return v_defense;
}

int CalcAdvantages::health() const {
	return v_health;
}

int CalcAdvantages::willpower() const {
	return v_willpower;
}

int CalcAdvantages::calcSize( cv_Trait* trait ) {
	if ( trait->type == cv_Trait::Merit && trait->name == "Giant" ) {
		int result = 5;

		if ( trait->value > 0 ) {
			result += 1;
		}

		if ( v_size != result ) {
			v_size = result;
			emit sizeChanged( result );
		}
	}

	return v_size;
}

int CalcAdvantages::calcInitiative( cv_Trait* trait ) {
	if (( trait->type == cv_Trait::Attribute && ( trait->name == "Dexterity" || trait->name == "Composure" ) )
			|| trait->type == cv_Trait::Merit && trait->name == "Fast Reflexes" ) {
		int val1 = 0;
		int val2 = 0;
		int val3 = 0;
		QList< cv_Trait > list;

		// Nur berechnen, wenn der veränderte Wert Einfluß auf die Initiative hat.

		if ( trait->type == cv_Trait::Attribute ) {
			val1 = trait->value;

			list = character->traits( cv_Trait::Merit, cv_Trait::Physical );

			for ( int i = 0; i < list.count(); i++ ) {
				if ( list.at( i ).name == "Fast Reflexes" ) {
					val3 = list.at( i ).value;
					break;
				}
			}

			if ( trait->name == "Composure" ) {
				list = character->traits( cv_Trait::Attribute, cv_Trait::Physical );

				for ( int i = 0; i < list.count(); i++ ) {
					if ( list.at( i ).name == "Dexterity" ) {
						val2 = list.at( i ).value;
						break;
					}
				}
			} else if ( trait->name == "Dexterity" ) {
				list = character->traits( cv_Trait::Attribute, cv_Trait::Mental );

				for ( int i = 0; i < list.count(); i++ ) {
					if ( list.at( i ).name == "Composure" ) {
						val2 = list.at( i ).value;
						break;
					}
				}
			}
		} else {	// Es bleibt nur noch Fast Reflexes übrig
			val3 = trait->value;
			list = character->traits( cv_Trait::Attribute, cv_Trait::Mental );

			for ( int i = 0; i < list.count(); i++ ) {
				if ( list.at( i ).name == "Composure" ) {
					val1 = list.at( i ).value;
					break;
				}
			}

			list = character->traits( cv_Trait::Attribute, cv_Trait::Physical );

			for ( int i = 0; i < list.count(); i++ ) {
				if ( list.at( i ).name == "Dexterity" ) {
					val2 = list.at( i ).value;
					break;
				}
			}
		}

		int result = val1 + val2 + val3;

		if ( v_initiative != result ) {
			v_initiative = result;
			emit initiativeChanged( result );
		}
	}

	return v_initiative;
}

int CalcAdvantages::calcSpeed( cv_Trait* trait ) {
	if (( trait->type == cv_Trait::Attribute && ( trait->name == "Strength" || trait->name == "Dexterity" ) )
			|| ( trait->type == cv_Trait::Merit && trait->name == "Fleet of Foot" ) ) {
		int val1 = 0;
		int val2 = 0;
		int val3 = 0;
		QList< cv_Trait > list;

		// Nur berechnen, wenn der veränderte Wert Einfluß auf die Initiative hat.

		if ( trait->type == cv_Trait::Attribute ) {
			val1 = trait->value;
			list = character->traits( cv_Trait::Merit, cv_Trait::Physical );

			for ( int i = 0; i < list.count(); i++ ) {
				if ( list.at( i ).name == "Fleet of Foot" ) {
					val3 = list.at( i ).value;
					break;
				}
			}

			if ( trait->name == "Strength" ) {
				list = character->traits( cv_Trait::Attribute, cv_Trait::Physical );

				for ( int i = 0; i < list.count(); i++ ) {
					if ( list.at( i ).name == "Dexterity" ) {
						val2 = list.at( i ).value;
						break;
					}
				}
			} else if ( trait->name == "Dexterity" ) {
				list = character->traits( cv_Trait::Attribute, cv_Trait::Physical );

				for ( int i = 0; i < list.count(); i++ ) {
					if ( list.at( i ).name == "Strength" ) {
						val2 = list.at( i ).value;
						break;
					}
				}
			}
		} else {	// Es bleibt nur noch Fleet of Foot übrig
			val3 = trait->value;
			list = character->traits( cv_Trait::Attribute, cv_Trait::Physical );

			for ( int i = 0; i < list.count(); i++ ) {
				if ( list.at( i ).name == "Strength" ) {
					val1 = list.at( i ).value;
					break;
				}
			}

			for ( int i = 0; i < list.count(); i++ ) {
				if ( list.at( i ).name == "Dexterity" ) {
					val2 = list.at( i ).value;
					break;
				}
			}
		}

		int result = val1 + val2 + 5 + val3;

		if ( v_speed != result ) {
			v_speed = result;
			emit speedChanged( result );
		}
	}

	return v_speed;
}

int CalcAdvantages::calcDefense( cv_Trait* trait ) {
	// Nur berechnen, wenn der veränderte Wert Einfluß auf die Defense hat.
	if ( trait->type == cv_Trait::Attribute && ( trait->name == "Wits" || trait->name == "Dexterity" ) ) {
		int val1 = trait->value;
		int val2 = 0;
		QList< cv_Trait > list;

		if ( trait->name == "Wits" ) {
			list = character->traits( cv_Trait::Attribute, cv_Trait::Physical );

			for ( int i = 0; i < list.count(); i++ ) {
				if ( list.at( i ).name == "Dexterity" ) {
					val2 = list.at( i ).value;
					break;
				}
			}
		} else if ( trait->name == "Dexterity" ) {
			list = character->traits( cv_Trait::Attribute, cv_Trait::Mental );

			for ( int i = 0; i < list.count(); i++ ) {
				if ( list.at( i ).name == "Wits" ) {
					val2 = list.at( i ).value;
					break;
				}
			}
		}

		int result = qMin( val1, val2 );

		if ( v_defense != result ) {
			v_defense = result;
			emit defenseChanged( result );
		}
	}

	return v_defense;
}

int CalcAdvantages::calcHealth( cv_Trait* trait ) {
	if ( trait->type == cv_Trait::Attribute && trait->name == "Stamina" ) {
		int result = trait->value + v_size;

		if ( v_health != result ) {
			v_health = result;
			emit healthChanged( result );
		}
	}

	return v_health;
}

int CalcAdvantages::calcHealth( int size ) {
	int val1 = 0;
	QList< cv_Trait > list = character->traits( cv_Trait::Attribute, cv_Trait::Physical );

	for ( int i = 0; i < list.count(); i++ ) {
		if ( list.at( i ).name == "Stamina" ) {
			val1 = list.at( i ).value;
			break;
		}
	}

	int result = size + val1;

	if ( v_health != result ) {
		v_health = result;
		emit healthChanged( result );
	}

	return v_health;
}

int CalcAdvantages::calcWillpower( cv_Trait* trait ) {
	// Nur berechnen, wenn der veränderte Wert Einfluß auf die Defense hat.
	if ( trait->type == cv_Trait::Attribute && ( trait->name == "Resolve" || trait->name == "Composure" ) ) {
		int val1 = trait->value;
		int val2 = 0;
		QList< cv_Trait > list;

		if ( trait->name == "Resolve" ) {
			list = character->traits( cv_Trait::Attribute, cv_Trait::Social );

			for ( int i = 0; i < list.count(); i++ ) {
				if ( list.at( i ).name == "Composure" ) {
					val2 = list.at( i ).value;
					break;
				}
			}
		} else if ( trait->name == "Composure" ) {
			list = character->traits( cv_Trait::Attribute, cv_Trait::Mental );

			for ( int i = 0; i < list.count(); i++ ) {
				if ( list.at( i ).name == "Resolve" ) {
					val2 = list.at( i ).value;
					break;
				}
			}
		}

		int result = val1 + val2;

		if ( v_willpower != result ) {
			v_willpower = result;
			emit willpowerChanged( result );
		}
	}

	return v_defense;
}

