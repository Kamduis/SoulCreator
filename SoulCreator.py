#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) Victor von Rhein, 2011, 2012

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
\author Victor von Rhein

\mainpage Hauptseite

\section Zweck

Dieses Programm dient dazu, Charaktere für das Rollenspiel "World of Darkness" von Whilte Wolf zu erzeugen. Aktuell werden nur gewöhnliche Menschen, Wechselbälger, Magier, Vampire und Werwölfe von diesem Programm unterstüzt.
"""




import sys
import argparse

from PySide.QtGui import QApplication

from src.GlobalState import GlobalState
from src.Config import Config
from src.MainWindow import MainWindow



if __name__ == "__main__":
	"""
	Das Hauptprogramm

	@param argc Anzahl der Kommandozeilenparameter
	@param argv Inhalt der Kommandozeilenparameter (argv[0] = Name des Programms)
	@return int
	"""

	parser = argparse.ArgumentParser(description=Config.programDescription)

	parser.add_argument("--debug", action="store_true", help="Give debug information. Not recommended for printing or exporting character sheets.")
	#parser.add_argument("-v", "--verbose", action="store_true", help="Output useful information.")
	parser.add_argument("-V", "--version", action="version", version="{name}: {version}".format( name=sys.argv[0], version=Config.version()) )

	args = parser.parse_args()

	GlobalState.isDebug = args.debug

	app = QApplication(sys.argv)
	w = MainWindow()
	w.show()
	retcode = app.exec_()
	del w	# Ohne dies kann es beim Einfügen von QMenuBar in der ui-Datei zu einem Segfault kommen.
	sys.exit(retcode)
