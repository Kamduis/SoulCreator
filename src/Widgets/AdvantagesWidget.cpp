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
#include <QSpinBox>
#include <QDebug>

#include "CharaTrait.h"
#include "../Datatypes/cv_Trait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"

#include "AdvantagesWidget.h"


AdvantagesWidget::AdvantagesWidget( QWidget *parent ) : QWidget( parent )  {
	layout = new QGridLayout( this );
	layout->setMargin(0);
	setLayout( layout );

	calcAdvantages = new CalcAdvantages(this);

	QLabel* labelSize = new QLabel(tr("Size"));
	QSpinBox* spinBoxSize = new QSpinBox(this);
	spinBoxSize->setValue(0);

	QLabel* labelSpeed = new QLabel(tr("Speed"));
	QSpinBox* spinBoxSpeed = new QSpinBox(this);
	spinBoxSpeed->setValue(0);

	QLabel* labelInitiative = new QLabel(tr("Initiative"));
	
	QLabel* labelDefense = new QLabel(tr("Defense"));
	QSpinBox* spinBoxDefense = new QSpinBox(this);
	spinBoxDefense->setValue(0);
	
	QLabel* labelArmor = new QLabel(tr("Armor"));

	layout->addWidget(labelSize, 0, 0);
	layout->addWidget(spinBoxSize, 0, 1);
	layout->addWidget(labelSpeed, 1, 0);
	layout->addWidget(spinBoxSpeed, 1, 1);
	layout->addWidget(labelInitiative, 2, 0);
	layout->addWidget(labelDefense, 3, 0);
	layout->addWidget(spinBoxDefense, 3, 1);
	layout->addWidget(labelArmor, 4, 0);

	connect(calcAdvantages, SIGNAL(speedChanged(int)), spinBoxSpeed, SLOT(setValue(int)));
	connect(calcAdvantages, SIGNAL(sizeChanged(int)), spinBoxSize, SLOT(setValue(int)));
	connect(calcAdvantages, SIGNAL(defenseChanged(int)), spinBoxDefense, SLOT(setValue(int)));
}

AdvantagesWidget::~AdvantagesWidget() {
	delete calcAdvantages;
	delete layout;
}
