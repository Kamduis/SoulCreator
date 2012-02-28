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


## \author Victor von Rhein
#
# \mainpage Hauptseite
#
# \section Zweck
#
# Dieses Programm dient dazu, Charaktere für das Rollenspiel "World of Darkness" von Whilte Wolf zu erzeugen. Aktuell werden nur gewöhnliche Menschen, Wechselbälger, Magier, Vampire und Werwölfe von diesem Programm unterstüzt.





import sys
import argparse
import signal

from PySide.QtGui import QApplication

from src.GlobalState import GlobalState
from src.Config import Config
from src.MainWindow import MainWindow
#from src.Debug import Debug




if __name__ == "__main__":
	"""
	Das Hauptprogramm

	@param argc Anzahl der Kommandozeilenparameter
	@param argv Inhalt der Kommandozeilenparameter (argv[0] = Name des Programms)
	@return int

	\todo Das Argument --onepage sollte auch genau das versprochene leisten.
	"""

	## Das Programm kann mit CTRL-C beendet werden.
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	parser = argparse.ArgumentParser(description=Config.programDescription)

	#parser.add_argument("-o", "--onepage", action="store_true", help="Charactersheets will consist of one page only. (Momentan noch ohne Funktion.)")
	parser.add_argument("-p", "--pdf", metavar="Name", nargs=1, help="Directly creates a pdf file of the specified name out of the loaded character and closes immediatly. If no character file is passed as an argument to this program, an empty character sheet will be created.")
	parser.add_argument("--debug", action="store_true", help="Give debug information. Not recommended for printing or exporting character sheets.")
	parser.add_argument("--develop", action="store_true", help=argparse.SUPPRESS)
	parser.add_argument("--fallback", action="store_true", help=argparse.SUPPRESS)
	parser.add_argument("-v", "--verbose", action="store_true", help="Output useful information.")
	parser.add_argument("-V", "--version", action="version", version="{name}: {version}".format( name=sys.argv[0], version=Config.version()) )
	parser.add_argument(dest="file", metavar="File/Species", nargs="?", help="Opens the character from this file at start. Instead of a file, the name of a supported species (human, changeling, mage, vampire, werewolf) may be entered, to create an empty character of the specified species, if no file of that specific name exists. This is most useful in combination with the -p option.")

	args = parser.parse_args()

	GlobalState.isDebug = args.debug
	GlobalState.isDevelop = args.develop
	GlobalState.isFallback = args.fallback
	GlobalState.isVerbose = args.verbose

	if GlobalState.isDebug:
		print("{} runs in debug mode".format(Config.programName))

	app = QApplication(sys.argv)
	w = MainWindow( args.file, exportPath=args.pdf )
	w.show()
	retcode = app.exec_()
