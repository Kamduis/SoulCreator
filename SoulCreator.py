#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Character generator for the White Wolf World of Darkness Pen and
Paper roleplaying game series.

# Examples

	python3 zenokraten.py

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




import sys
import argparse
import signal

from PyQt4.QtGui import QApplication

from src.GlobalState import GlobalState
import src.Config as Config
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

	parser = argparse.ArgumentParser(description=Config.PROGRAM_DESCRIPTION)

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
		print("{} runs in debug mode".format(Config.PROGRAM_NAME))

	app = QApplication(sys.argv)
	w = MainWindow( args.file, exportPath=args.pdf )
	w.show()
	retcode = app.exec_()
