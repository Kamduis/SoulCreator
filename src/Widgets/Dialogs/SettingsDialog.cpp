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
#include <QStringList>
#include <QDebug>

#include "../../Config/Config.h"
#include "../../Exceptions/Exception.h"

#include "SettingsDialog.h"
#include "ui_SettingsDialog.h"


SettingsDialog::SettingsDialog( QWidget *parent ) : QDialog( parent ), ui( new Ui::SettingsDialog )  {
	ui->setupUi( this );

	connect( ui->buttonBox, SIGNAL( accepted() ), this, SLOT( saveChanges() ) );
	connect( ui->buttonBox, SIGNAL( rejected()), this, SLOT( reject()) );

	ui->fontComboBox_export->setCurrentFont(Config::exportFont);
}

SettingsDialog::~SettingsDialog() {
}


void SettingsDialog::saveChanges() {
	Config::exportFont = ui->fontComboBox_export->currentFont();

	accept();
}
