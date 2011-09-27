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

#include "SelectWidget.h"


SelectWidget::SelectWidget( QWidget *parent ) : QListWidget( parent )  {
	new QListWidgetItem(QIcon(":types/images/svg/humans.svg"), tr("Information"), this);
	new QListWidgetItem(QIcon(":types/images/svg/maleprofile.svg"), tr("Attributes"), this);
	new QListWidgetItem(QIcon(":types/images/svg/high_jump.svg"), tr("Skills"), this);
	new QListWidgetItem(QIcon(":types/images/svg/karate.svg"), tr("Merits"), this);
	new QListWidgetItem(QIcon(":types/images/svg/knife.svg"), tr("Morality"), this);
	new QListWidgetItem(QIcon(":types/images/svg/bolt.svg"), tr("Powers"), this);
	new QListWidgetItem(QIcon(":types/images/svg/tail.svg"), tr("Flaws"), this);

	for (int i = 0; i < count(); i++){
		item(i)->setTextAlignment(Qt::AlignVCenter);
		item(i)->setFlags(Qt::ItemIsEnabled | Qt::ItemIsSelectable);
	}

	setIconSize(QSize(50,50));

// 	setViewMode(QListView::IconMode);
// 	setFlow(QListView::TopToBottom);
	
	setMaximumWidth(150);
}

SelectWidget::~SelectWidget() {
}

