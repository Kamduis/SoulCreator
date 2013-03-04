# -*- coding: utf-8 -*-

"""
# Copyright

Copyright (C) 2012 by Victor
victor@caern.de

# License

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from PyQt4.QtCore import QObject
from PyQt4.QtGui import QMessageBox

import src.Config as Config
import src.GlobalState as GlobalState
import src.IO.Shell as Shell
#from src.Error import ErrXmlTooOldVersion




class MessageBox(QMessageBox):
	"""
	@brief Diese Klasse stellt verschiedene Standardnachrichtenfenster für das Programm dar.

	Über das Standardnachrichtenfenster können die Nachrichten über Ausnahmen bequem an den Nutzer weitergegeben werden. Unter anderem existiert auch eine Nachrichtenbox für die Ausnahmebehandlung.
	"""


	@staticmethod
	def warning( parent, text ):
		"""
		Standardisierte Dialogbox für die Mitteilung einer Warnung an den Benutzer.

		Eine Warnung wird auch auf der kommandozeile ausgegeben, wenn "verbose" aktiviert ist.
		"""

		if GlobalState.is_verbose:
			Shell.print_warning( text )

		obj = QObject()
		QMessageBox.warning( parent, obj.tr("Warning"), str( text ) )


	@staticmethod
	def error( parent, text, critical=False ):
		"""
		Standardisierte Dialogbox für die Mitteilung eines Fehlers an den Benutzer.

		Ein Fehler wird auch auf der kommandozeile ausgegeben, wenn "verbose" aktiviert ist.

		\param critical=True macht daraus einen kritischen Fehler, bei welchem das Programm beendet werden muß.
		"""

		if GlobalState.is_verbose:
			Shell.print_error( text, critical=critical )

		obj = QObject()
		headline = obj.tr("Error")
		if critical:
			headline = obj.tr("Critical Error")
		QMessageBox.critical( parent, headline, str( text ) )
