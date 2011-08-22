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

#include <QGridLayout>
#include <QDebug>

#include "CharaTrait.h"
#include "../Datatypes/cv_Trait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"
#include "../Storage/StorageTemplate.h"

#include "AttributeWidget.h"


AttributeWidget::AttributeWidget( QWidget *parent ) : QWidget( parent )  {
	layout = new QGridLayout( this );
	setLayout( layout );

	StorageTemplate storage;

	cv_Trait::Type type = cv_Trait::Attribute;

	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );

	for ( int i = 0; i < categories.count(); i++ ) {
		for ( int j = 0; j < storage.attributeNames( categories.at(i) ).count(); j++ ) {
			CharaTrait *trait = new CharaTrait( this, storage.attributes( categories.at(i) ).at( j ) );
			trait->setValue(1);
			// Zwischen den Attributsgruppen eine Spalte als Zwischenraum freilassen.
			layout->addWidget( trait, j, 2*i );
		}
		if (i > 0) {
			layout->setColumnMinimumWidth( (2*i)-1, Config::traitCategorySpace);
		}
	}

}

AttributeWidget::~AttributeWidget() {
	delete layout;
}
