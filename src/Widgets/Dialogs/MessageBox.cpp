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

#include <QObject>
#include <QDebug>

#include "../../Config/Config.h"

#include "MessageBox.h"

QMessageBox::StandardButton MessageBox::exception ( QWidget* parent, QString message, QString description ) {
	QString text = formatText(message, description);

	critical ( parent, tr ( "Exception" ), text );
}

QMessageBox::StandardButton MessageBox::exception ( QWidget* parent, Exception error ) {
	QString text = formatText(error.message(),  error.description());

	critical ( parent, tr ( "Exception" ), text );
}

QMessageBox::StandardButton MessageBox::exception ( QWidget* parent ) {
	QString text = formatText(tr ( "A problem occured." ),  tr ( "Cause or consequences of this problem are not known. Proceed on your own risk." ));

	critical ( parent, tr ( "Exception" ), text );
}

QString MessageBox::formatText ( QString message, QString description ) {
	return formatMessage(message) + formatDescription(description);
}


QString MessageBox::formatMessage ( QString message ) {
	QString importantText = "<p>"
							"<span style='color:" + Config::importantTextColorName() + "; font-size:large'>"
							+ message +
							"</span>"
							"</p>";

	return importantText;
}

QString MessageBox::formatDescription ( QString description ) {
	QString descriptionText = "<p>" + description + "</p>";

	return descriptionText;
}


