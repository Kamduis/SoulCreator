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
#include "Parser/StringBoolParser.h"

#include "SkillTrait.h"


SkillTrait::SkillTrait( QString txt, int val, cv_Species::Species spe, cv_AbstractTrait::Category ca, QObject* parent ) : Trait( txt, val, spe, cv_AbstractTrait::Attribute, ca ) {
}

SkillTrait::SkillTrait( cv_Trait trait, QObject* parent ) : Trait( trait, parent ) {
}

SkillTrait::SkillTrait( Trait* trait, QObject* parent ) : Trait( trait, parent ) {
}

