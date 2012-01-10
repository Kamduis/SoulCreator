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




import random




class Random():
	# Systemzeit als Seed nutzen
	random.seed(None)

	@staticmethod
	def random(valA, valB=0):
		"""
		Gibt einen zufälligen Wert zwischen valMin und valMax (jeweils einschließlich) zurück.
		"""

		if (valB < valA):
			valueMin = valB
			valueMax = valA
		else:
			valueMin = valA
			valueMax = valB

		return random.randint(valueMin, valueMax)