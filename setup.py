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



import os
import sys
from cx_Freeze import setup, Executable
import sip
import subprocess

from src.Config import Config




if __name__ == "__main__":
	"""
	Umrechnung aus dem karthesischen Koordinatensystem in das Polarkoordinatensystem und andersherum.
	"""

	## Resourcen bauen
	cmd_rcc = ["pyside-rcc", "-o", "resources/rc_resource.py", "resources/rc_resource.qrc"]
	retcode = subprocess.call(cmd_rcc, shell=False)

	if retcode != 0:
		sys.exit(retcode)

	cmd_uic_1 = ["pyside-uic", "-i", "0", "-o", "ui/ui_AdvantagesWidget.py", "ui/ui_AdvantagesWidget.ui"]
	retcode = subprocess.call(cmd_uic_1, shell=False)

	if retcode != 0:
		sys.exit(retcode)

	cmd_uic_2 = ["pyside-uic", "-i", "0", "-o", "ui/ui_MainWindow.py", "ui/ui_MainWindow.ui"]
	retcode = subprocess.call(cmd_uic_2, shell=False)

	if retcode != 0:
		sys.exit(retcode)

	cmd_uic_3 = ["pyside-uic", "-i", "0", "-o", "ui/ui_NameDialog.py", "ui/ui_NameDialog.ui"]
	retcode = subprocess.call(cmd_uic_3, shell=False)


	if retcode != 0:
		sys.exit(retcode)

	if os.name == "nt":
		_base = "Win32GUI"
	else:
		_base = "Console"


	exe = Executable(
		script="SoulCreator.py",
		base = _base
	)


	setup(
		name = Config.programName,
		version = Config.version(),
		description = Config.programDescription,
		executables = [exe]
	)

	sys.exit(0)
