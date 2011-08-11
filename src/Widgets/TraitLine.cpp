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

// #include "Storage.h"

#include "TraitLine.h"


// TraitLine::TraitLine( QWidget *parent, cv_Trait::Type type, cv_Trait::Category category, QString name, int value) : QWidget(parent){
// 	QHBoxLayout *layout = new QHBoxLayout();
// 	layout->setMargin(0);
// 	setLayout(layout);
//
// 	label_name = new QLabel();
// 	traitDots = new TraitDots();
// // 	specialties = new Specialties();
//
// 	setType(type);
// 	setCategory(category);
// 	setName(name);
// 	setValue(value);
//
// 	layout->addWidget(label_name);
// // 	layout->addWidget(specialties);
// 	layout->addWidget(traitDots);
//
// 	connect (traitDots, SIGNAL(valueChanged ( int )), SIGNAL(valueChanged ( int )));
// //	connect (traitDots, SIGNAL(valueChanged ( int )), this, SLOT(storeTrait ()));
// // 	connect (specialties, SIGNAL(numberChanged ( int )), this, SLOT(hideSpecialties (int)));
// // 	connect (specialties , SIGNAL(clicked ( CheckedList* )), SIGNAL(specialtiesClicked (CheckedList*)));
//
// // 	hideSpecialties(0);
// //	storeTrait();
// }
TraitLine::TraitLine( QWidget *parent, QString name, int value ) : QWidget( parent ) {
	v_layout = new QHBoxLayout();
	v_layout->setMargin( 0 );
	setLayout( v_layout );

	v_label_name = new QLabel( this );
	button = new QPushButton( this );
	button->setText( tr( "Specialties" ) );
	button->setCheckable( true );
	traitDots = new TraitDots( this );

	connect( traitDots, SIGNAL( valueChanged( int ) ), SIGNAL( valueChanged( int ) ) );
	connect( traitDots, SIGNAL( valueChanged( int ) ), this, SLOT( enableSpecialties( int ) ) );
	connect( button, SIGNAL( clicked( bool ) ), this, SIGNAL( specialtiesClicked( bool ) ) );

	setName( name );
	setValue( value );
	// Damit auch bei der Programminitialisierung die Spezialisierungen richtig enabled oder disabled sind.
	enableSpecialties( value );

	v_layout->addWidget( v_label_name );
	v_layout->addStretch();
	v_layout->addWidget( button );
	v_layout->addWidget( traitDots );

}

TraitLine::~TraitLine() {
	delete traitDots;
	delete v_label_name;
}


QHBoxLayout* TraitLine::layout() const {
	return v_layout;
}

QLabel* TraitLine::labelName() const {
	return v_label_name;
}


QString TraitLine::name() const {
	return v_label_name->text();
}

void TraitLine::setName( QString name ) {
	v_label_name->setText( name );
}

int TraitLine::value() const {
	return traitDots->value();
}

void TraitLine::setValue( int value ) {
	traitDots->setValue( value );
}

int TraitLine::minimum() const {
	return traitDots->minimum();
}

void TraitLine::setMinimum( int value ) {
	traitDots->setMinimum( value );
}

void TraitLine::setSpecialtyButtonChecked( bool sw ) {
	button->setChecked( sw );
}



void TraitLine::hideSpecialties( bool sw ) {
	if ( sw )
		button->hide();
	else
		button->show();
}

void TraitLine::enableSpecialties( int number ) {
	if ( number > 0 ) {
		button->setEnabled( true );
	} else {
		button->setEnabled( false );
	}
}

