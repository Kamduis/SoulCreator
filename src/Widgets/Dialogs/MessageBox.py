# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) 2011 by Victor von Rhein

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

from PySide.QtCore import QObject
from PySide.QtGui import QMessageBox

from src.Config import Config
from src.Error import ErrXmlTooOldVersion




class MessageBox(QMessageBox):
	"""
	@brief Diese Klasse stellt verschiedene Standardnachrichtenfenster für das Programm dar.

	Über das Standardnachrichtenfenster können die Nachrichten über Ausnahmen bequem an den Nutzer weitergegeben werden. Unter anderem existiert auch eine Nachrichtenbox für die Ausnahmebehandlung.
	"""

	@staticmethod
	def exception(parent, message, description):
		obj = QObject()

		text = MessageBox.formatText(message, description)
		QMessageBox.critical(parent, obj.tr("Exception"), text)


#QMessageBox::StandardButton MessageBox::exception ( QWidget* parent, Exception error ) {
	#QString text = formatText(error.message(),  error.description());

	#critical ( parent, tr ( "Exception" ), text );
#}

#QMessageBox::StandardButton MessageBox::exception ( QWidget* parent ) {
	#QString text = formatText(tr ( "A problem occured." ),  tr ( "Cause or consequences of this problem are not known. Proceed on your own risk." ));

	#critical ( parent, tr ( "Exception" ), text );
#}

	@staticmethod
	def formatText ( message, description ):
		return MessageBox.formatMessage(message) + MessageBox.formatDescription(description)



	@staticmethod
	def formatMessage ( message ):
		importantText = "<p><span style='color:" + Config.importantTextColorName + "; font-size:large'>{}</span></p>".format(message)

		return importantText


	@staticmethod
	def formatDescription ( description ):
		descriptionText = "<p>{}</p>".format(description)

		return descriptionText


