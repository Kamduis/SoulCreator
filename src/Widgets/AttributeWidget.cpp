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

#include <QVBoxLayout>
#include <QGroupBox>
#include <QDebug>

#include "CharaTrait.h"
#include "../Datatypes/cv_Trait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"
#include "../Storage/StorageTemplate.h"

#include "AttributeWidget.h"


AttributeWidget::AttributeWidget( QWidget *parent ) : QWidget( parent )  {
	layout = new QHBoxLayout( this );
	setLayout( layout );

	QFrame* frame = new QFrame( this );
	layout->addWidget( frame );

	QVBoxLayout* layoutHeader = new QVBoxLayout();
	frame->setLayout( layoutHeader );

	QLabel* labelPower = new QLabel( tr( "Power" ) );
	labelPower->setAlignment( Qt::AlignRight );

	QLabel* labelFinesse = new QLabel( tr( "Finesse" ) );
	labelFinesse->setAlignment( Qt::AlignRight );

	QLabel* labelResistance = new QLabel( tr( "Resistance" ) );
	labelResistance->setAlignment( Qt::AlignRight );

	layoutHeader->addWidget( labelPower, 0, 0 );
	layoutHeader->addWidget( labelFinesse, 1, 0 );
	layoutHeader->addWidget( labelResistance, 2, 0 );

	StorageTemplate storage;

	cv_Trait::Type type = cv_Trait::Attribute;

	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );

	QList< cv_Trait > list;

	for ( int i = 0; i < categories.count(); i++ ) {
		list = storage.attributes( categories.at( i ) );
		QGroupBox* categoriesBox = new QGroupBox();
		QVBoxLayout* layoutCategories = new QVBoxLayout();
		categoriesBox->setLayout( layoutCategories );

		layout->addWidget( categoriesBox );

		for ( int j = 0; j < list.count(); j++ ) {
			CharaTrait *trait = new CharaTrait( this, list.at( j ) );
			trait->setValue( 0 );
			trait->setValue( 1 );
			layoutCategories->addWidget( trait );
		}
	}
}

AttributeWidget::~AttributeWidget() {
	delete layout;
}
