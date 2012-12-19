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

import src.GlobalState as GlobalState
import src.Config as Config
from src.MainWindow import MainWindow
#import src.Debug as Debug




# Pylint-Einstellungen
# pylint: disable-msg=C0103




def main( argv, file=None, pdf=None, verbose=None, debug=0, develop=None, fallback=None ):
	"""
	Entry Point.
	"""

	GlobalState.is_verbose = verbose
	GlobalState.is_develop = develop
	GlobalState.is_fallback = fallback
	# Debug-Level soll immer als Zahl gespeichert werden. Der Zugehörige Name kann über das Tupel Config.DEBUG_LEVELS herausgefunden werden.
	if debug in Config.DEBUG_LEVELS:
		GlobalState.debug_level = Config.DEBUG_LEVELS.index( debug )
	else:
		GlobalState.debug_level = int( debug )

	if GlobalState.debug_level and GlobalState.debug_level > Config.DEBUG_LEVEL_NONE:
		print("{name} runs in debug mode (debug-level: {level_index} \"{level_name}\").".format(
			name=Config.PROGRAM_NAME,
			level_index=GlobalState.debug_level,
			level_name=Config.DEBUG_LEVELS[GlobalState.debug_level],
		))
		if GlobalState.debug_level >= Config.DEBUG_LEVEL_MODIFIES_EXPORTS:
			print("WARNING! Exporting and printing character sheets is not recommended.")

	if GlobalState.is_develop:
		print( "{name} runs in development mode.".format(
			name=Config.PROGRAM_NAME,
		))
		print( "WARNING! You may encounter unexpected behaviour. Data loss is possible. Proceed only, if you know, what you are doing." )

	app = QApplication( argv )
	w = MainWindow( file, exportPath=pdf )
	w.show()
	retcode = app.exec_()




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
	# Als Argument kann der Name oder die Nummer des Debug-levels eingegeben werden. Bei der Liste der erlaubten Möglichkeiten wird der Name immer nach der zugehörigen Nummer eingefügt.
	__choices_debug_level = []
	for item in range( len( Config.DEBUG_LEVELS ) ):
		__choices_debug_level.append( str(item) )
		__choices_debug_level.append( Config.DEBUG_LEVELS[item] )
	parser.add_argument("--debug", nargs="?", choices=__choices_debug_level, const=Config.DEBUG_LEVELS[Config.DEBUG_LEVEL_STD], default="0", help="Give debug information. {level_index_none} ({level_name_none}) means, that no debug information will be printed (standard behaviour). {level_index_normal} ({level_name_normal}) is the normal behaviour, if the option string is present, but no argument given. Debug from {level_index_mod} ({level_name_mod}) and above are not recommended for printing and/or exporting character sheets.".format(
		level_index_none=Config.DEBUG_LEVEL_NONE,
		level_name_none=Config.DEBUG_LEVELS[Config.DEBUG_LEVEL_NONE],
		level_index_normal=Config.DEBUG_LEVEL_STD,
		level_name_normal=Config.DEBUG_LEVELS[Config.DEBUG_LEVEL_STD],
		level_index_mod=Config.DEBUG_LEVEL_MODIFIES_EXPORTS,
		level_name_mod=Config.DEBUG_LEVELS[Config.DEBUG_LEVEL_MODIFIES_EXPORTS],
	) )
	## Development. Some tasks are automatic, that normally the user would have to undertake, like choosing a file name for saving characters and other stuff. Very dangerous for normal work.
	parser.add_argument("--develop", action="store_true", help=argparse.SUPPRESS)
	parser.add_argument("--fallback", action="store_true", help=argparse.SUPPRESS)
	parser.add_argument("-v", "--verbose", action="store_true", help="Output useful information.")
	parser.add_argument("-V", "--version", action="version", version="{name}: {version}".format( name=sys.argv[0], version=Config.version()) )
	parser.add_argument(dest="file", metavar="File/Species", nargs="?", help="Opens the character from this file at start. Instead of a file, the name of a supported species (human, changeling, mage, vampire, werewolf) may be entered, to create an empty character of the specified species, if no file of that specific name exists. This is most useful in combination with the -p option.")

	args = parser.parse_args()

	## Hauptprogramm starten
	main( sys.argv, file=args.file, pdf=args.pdf, verbose=args.verbose, debug=args.debug, develop=args.develop, fallback=args.fallback )
