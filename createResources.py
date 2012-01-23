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

from src.Config import Config
from src.Tools import PathTools





if __name__ == "__main__":
	"""
	Erzeugt die notwendigen ui-Dateien und Resourcen, um SoulCreator verwenden zu können.
	"""

	## Resourcen bauen
	cmd_string_rcc = ["pyside-rcc", "-o", ]
	cmd_string_uic = ["pyside-uic", "-i", "0", "-o", ]

	buildResources = True
	if os.name == "nt":
		## Unter Windows sind pyside-rcc und pyside-uic nicht ohne absolute Pfadangabe aufrufbar. Dieser Pfad wird hier ermittelt.
		pathToRcc = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "PySide")
		if os.path.exists(pathToRcc):
			cmd_string_rcc[0] = os.path.join(pathToRcc, cmd_string_rcc[0])
		else:
			buildResources = False
		pathToUic = os.path.join(os.path.dirname(sys.executable), "Scripts")
		if os.path.exists(pathToUic):
			cmd_string_uic[0] = os.path.join(pathToUic, cmd_string_uic[0])
		else:
			buildResources = False

	if buildResources:
		print("Generate resource files for {}...".format(Config.programName))
		cmd_string_list = []
		for f in os.listdir(Config.resourceDir):
			if f.endswith(".qrc"):
				nameWOSuffix = f.split(".qrc")[0]
				cmd_string_lcl = cmd_string_rcc
				cmd_string_lcl.extend(["{}/{}/{}.py".format(PathTools.getPath(), Config.resourceDir, nameWOSuffix), "{}/{}/{}".format(PathTools.getPath(), Config.resourceDir, f)])
				cmd_string_list.append([ cmd_string_lcl, f, ])
		for f in os.listdir(Config.uiDir):
			if f.endswith(".ui"):
				nameWOSuffix = f.split(".ui")[0]
				cmd_string_lcl = cmd_string_uic[:]
				cmd_string_lcl.extend(["{}/{}/{}.py".format(PathTools.getPath(), Config.uiDir, nameWOSuffix), "{}/{}/{}".format(PathTools.getPath(), Config.uiDir, f)])
				cmd_string_list.append([ cmd_string_lcl, f, ])
		for cmd, f in cmd_string_list:
			print("Processing {}...".format(f))
			retcode = subprocess.call(cmd, shell=False)
			if retcode != 0:
				sys.exit(retcode)
		print("Done.")
	else:
		print("Warning: Resources not built. Old resource files used. Inconsistencies may occur.\nIf no old resource-files were present, you will not be able to run {}.".format(Config.programName))
		sys.exit(1)

	sys.exit(0)
