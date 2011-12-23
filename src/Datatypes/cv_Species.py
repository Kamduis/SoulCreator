# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) 2011 by Victor von Rhein

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

#from PySide.QtCore import QObject, QFile

#from src.Config import Config
#from src.Error import ErrXmlParsing, ErrXmlOldVersion
#from ReadXml import ReadXml
#from src.Storage.StorageTemplate import StorageTemplate




class cv_Species(object):
	"""
	@brief Liest die Eigenschaften aus den beigefügten xml-Dateien.

	Diese Klasse dient dazu einen möglichst simplen Zugriff auf die Eigenschaften der WoD-Charaktere zu bieten. Dazu werden die Eigenschaften und all ihre Zusatzinformationen aus den xml-Dateien gelesen und in Listen gespeichert.
	"""

	Species = (
		"Animal",
		"Human",
		"Changeling",
		"Mage",
		"Vampire",
		"Werewolf",
		"All",
	)


	name = ""
	morale = ""
	supertrait = ""
	fuel = ""


	def __eq__(self, other):
		if id(self) == id(other):
			return True
		else:
			return ((self.name == other.name) and (self.morale == other.morale) and (self.supertrait == other.supertrait) and (self.fuel == other.fuel))


