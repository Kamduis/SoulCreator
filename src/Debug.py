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

import inspect

from src.GlobalState import GlobalState




class Debug():
	"""
	@brief Erlaubt einfachen Zugriff auf Debug-Informationen.
	"""


	@staticmethod
	def debug( *args ):
		"""
		Gibt einen Text aus, wobei der Ort des Aufrufs dieser Funktion vorangestellt ist.
		"""

		strPrnt = " ".join([unicode(item) for item in args])

		if GlobalState.isDebug:
			print("{:<78}\tl. {:<4}\t{:<18}\n\t{}".format(inspect.stack()[1][1], inspect.stack()[1][2], inspect.stack()[1][3], strPrnt))
