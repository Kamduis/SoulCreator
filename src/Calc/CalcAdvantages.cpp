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

#include "Exceptions/Exception.h"

#include "CalcAdvantages.h"

int CalcAdvantages::v_size = 0;
int CalcAdvantages::v_initiative = 0;
int CalcAdvantages::v_speed = 0;
int CalcAdvantages::v_defense = 0;
int CalcAdvantages::v_health = 0;
int CalcAdvantages::v_willpower = 0;


CalcAdvantages::CalcAdvantages( QObject* parent ) : QObject( parent ) {
	construct();

	QList< cv_AbstractTrait::Type > types;
	types.append( cv_AbstractTrait::Attribute );
	types.append( cv_AbstractTrait::Merit );

	QList< Trait* > list;

	bool stopLoop = false;

	for ( int i = 0; i < types.count(); ++i ) {
		list = character->traits( types.at( i ) );

		for ( int j = 0; j < list.count(); ++j ) {
			if ( types.at( i ) == cv_AbstractTrait::Attribute ) {
				if ( list.at( j )->name() == "Wits" ) {
					attrWit = list.at( j );
				} else if ( list.at( j )->name() == "Resolve" ) {
					attrRes = list.at( j );
				} else if ( list.at( j )->name() == "Strength" ) {
					attrStr = list.at( j );
				} else if ( list.at( j )->name() == "Dexterity" ) {
					attrDex = list.at( j );
				} else if ( list.at( j )->name() == "Stamina" ) {
					attrSta = list.at( j );
				} else if ( list.at( j )->name() == "Composure" ) {
					attrCom = list.at( j );
				}

				if ( attrWit != 0 && attrRes != 0 && attrStr != 0 && attrDex != 0 && attrSta != 0 && attrCom != 0 ) {
					break;
				}
			} else if ( types.at( i ) == cv_AbstractTrait::Merit ) {
				if ( list.at( j )->name() == "Giant" ) {
					meritGiant = list.at( j );
				} else if ( list.at( j )->name() == "Fast Reflexes" ) {
					meritFastReflexes = list.at( j );
				} else if ( list.at( j )->name() == "Fleet of Foot" ) {
					meritFleetOfFoot = list.at( j );
				}

				if ( meritGiant != 0 && meritFleetOfFoot != 0 && meritFastReflexes != 0 ) {
					break;
				}
			}
		}
	}

	connect( attrWit, SIGNAL( valueChanged( int ) ), this, SLOT( calcInitiative() ) );
	connect( attrWit, SIGNAL( valueChanged( int ) ), this, SLOT( calcDefense() ) );
	connect( attrRes, SIGNAL( valueChanged( int ) ), this, SLOT( calcWillpower() ) );
	connect( attrStr, SIGNAL( valueChanged( int ) ), this, SLOT( calcSpeed() ) );
	connect( attrDex, SIGNAL( valueChanged( int ) ), this, SLOT( calcSpeed() ) );
	connect( attrDex, SIGNAL( valueChanged( int ) ), this, SLOT( calcInitiative() ) );
	connect( attrDex, SIGNAL( valueChanged( int ) ), this, SLOT( calcDefense() ) );
	connect( attrSta, SIGNAL( valueChanged( int ) ), this, SLOT( calcHealth() ) );
	connect( attrCom, SIGNAL( valueChanged( int ) ), this, SLOT( calcWillpower() ) );
	connect( meritGiant, SIGNAL( valueChanged( int ) ), this, SLOT( calcSize() ) );
	connect( meritFastReflexes, SIGNAL( valueChanged( int ) ), this, SLOT( calcInitiative() ) );
	connect( meritFleetOfFoot, SIGNAL( valueChanged( int ) ), this, SLOT( calcSpeed() ) );
	connect( this, SIGNAL( sizeChanged( int ) ), this, SLOT( calcHealth() ) );
}

CalcAdvantages::~CalcAdvantages() {
	// Verursachen beim Beenden des Programms seltsamer weise einen SEGFAULT.
// 	delete attrWit;
// 	delete attrRes;
// 	delete attrStr;
// 	delete attrDex;
// 	delete attrSta;
// 	delete attrCom;
// 	delete meritGiant;
// 	delete meritFastReflexes;
// 	delete meritFleetOfFoot;
}


void CalcAdvantages::construct() {
	character = StorageCharacter::getInstance();

	attrRes = 0;
	attrStr = 0;
	attrDex = 0;
	attrSta = 0;
	attrCom = 0;
	meritGiant = 0;
	meritFleetOfFoot = 0;
	meritFastReflexes = 0;
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


int CalcAdvantages::calcSize() {
	int result = 5;

	if ( meritGiant->value() > 0 ) {
		result += 1;
	}

	if ( v_size != result ) {
		v_size = result;
		emit sizeChanged( result );
	}

	return v_size;
}

int CalcAdvantages::calcInitiative() {
	int result = attrDex->value() + attrCom->value() + meritFastReflexes->value();

	if ( v_initiative != result ) {
		v_initiative = result;
		emit initiativeChanged( result );
	}

	return v_initiative;
}

int CalcAdvantages::calcSpeed() {
	int result = attrStr->value() + attrDex->value() + 5 + meritFleetOfFoot->value();

	if ( v_speed != result ) {
		v_speed = result;
		emit speedChanged( result );
	}

	return v_speed;
}

int CalcAdvantages::calcDefense() {
	int result = qMin( attrWit->value(), attrDex->value() );

	qDebug() << Q_FUNC_INFO << v_defense;

	if ( v_defense != result ) {
		v_defense = result;
		emit defenseChanged( result );
	}

	return v_defense;
}

int CalcAdvantages::calcHealth() {
	int result = attrSta->value() + v_size;

	if ( v_health != result ) {
		v_health = result;
		emit healthChanged( result );
	}

	return v_health;
}

int CalcAdvantages::calcWillpower() {
	int result = attrRes->value() + attrCom->value();

	if ( v_willpower != result ) {
		v_willpower = result;
		emit willpowerChanged( result );
	}

	return v_willpower;
}


