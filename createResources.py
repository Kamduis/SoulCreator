#!/usr/bin/env python3
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



import os
import sys
import argparse
import subprocess

from src.Config import Config




if __name__ == "__main__":
	"""
	Creates the resource files for the program.
	"""

	parser = argparse.ArgumentParser(description="Creates resource and ui-files needed to run {}.".format(Config.PROGRAM_NAME))

	parser.add_argument("-v", "--verbose", action="store_true", help="Output useful information.")
	parser.add_argument("-V", "--version", action="version", version="{name}: {version}".format(
		name=sys.argv[0],
		version=Config.version(change=True)
	))

	args = parser.parse_args()

	cmd_path = Config.PATH_RESOURCE_BUILDER
	conversion_targets = {
		"qrc": {
			"dir": Config.PATH_RESOURCE,
			"ext": Config.FILEXT_RESOURCE,
		},
		"ui": {
			"dir": Config.PATH_UI,
			"ext": Config.FILEXT_UI,
		},
	}

	for target in conversion_targets.items():
		do_anything = False
		cmd = [ cmd_path, "--pyqt", ]
		file_list = os.listdir(target[1]["dir"])
		for fi in file_list:
			if fi.endswith(".{}".format(target[1]["ext"])):
				do_anything = True
				cmd.append(os.path.join(target[1]["dir"], fi))
		if args.verbose:
			cmd.insert(1, "-v")

		if do_anything:
			ret = subprocess.call(cmd, shell=False)
			if ret != 0:
				sys.exit(1)

	sys.exit(0)
