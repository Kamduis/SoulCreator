#!/usr/bin/env python
# -*- coding: utf-8 -*-

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



from __future__ import division, print_function

import os
import sys
import subprocess
from cx_Freeze import setup, Executable

from src.Config import Config





if __name__ == "__main__":
	"""
	Erstellt eine ausführbare Datei in dem als obligatorisch anzugebenden Unterverzeichnis.

	Ausführung: `python setup.py build`
	"""

	# Process the includes, excludes and packages first
	includes = []
	excludes = []
	packages = []
	path = []

	## Resourcen bauen
	cmd_string = ("python", "createResources.py")
	retcode = subprocess.call(cmd_string, shell=False)
	if retcode != 0:
		sys.exit(retcode)

	if os.name == "nt":
		## Unter Windows müssen noch zwei Ordner kopiert und eine Datei erzeugt werden, damit auch SVG-Dateien korrekt dargestellt werden.
		# - plugins/iconengines
		# - plugins/imageformats
		# - qt.conf
		#
		# Da ich nicht weiß, wie ich den Namen des Zielordners bestimme, kann ich sie nicht automatisch kopieren/erstellen.
		pass

	if os.name == "nt":
		_base = "Win32GUI"
	else:
		_base = "Console"

	exe = Executable(
		script="SoulCreator.py",
		base = _base,
		#targetDir = r"build/test",	# Verursacht Schwierigkeiten, denn die Module werden in ein anderes Verzeichnis geschoben.
		compress = True,
		#copyDependentFiles = True,
		#appendScriptToExe = False,
		#appendScriptToLibrary = False,
		icon = None,
	)

	setup(
		name = Config.programName,
		version = Config.version(),
		description = Config.programDescription,
		author = Config.programAuthor,
		options = {"build_exe":
			{
				"includes": includes,
				"excludes": excludes,
				"packages": packages,
				"path": path,
			},
		},
		executables = [exe]
	)

	sys.exit(0)
