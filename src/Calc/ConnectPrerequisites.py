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

import re

from src.Config import Config
from src.Datatypes.Trait import Trait
from src.Debug import Debug




class ConnectPrerequisites(object):
	"""
	@brief ???
	"""


	def __init__(self):
		pass


	@staticmethod
	def buildConnection(storage, character):
		"""
		Merits und Subpowers müssen mit allen Eigenschaften verknüpft werden, die in ihrer Prerequisits-Eigenschaft vorkommen.
		"""
		
		typs = ["Merit", "Subpower"]
		for typ in typs:
			categoriesTraits = storage.categories(typ)
			for category in categoriesTraits:
				for trait in character.traits[typ][category].values():
					#Debug.debug("{trait} hat Voraussetzungen? {truth}".format(trait=trait.name, truth=trait.hasPrerequisites))
					if trait.hasPrerequisites:
						traitPrerequisites = trait.prerequisitesText
						#Debug.debug("Voraussetzungen von {trait}: {prerequisite}".format(trait=trait.name, prerequisite=trait.prerequisitesText))
						for item in storage.traits.keys():
							## Angabe in den Ressourcen: <typ>.<trait>[.<specialty>]
							typResource = "{}.".format(item)
							if typResource in traitPrerequisites:
								#Debug.debug("{trait} hat {typ} als Voraussetzung!".format(trait=trait.name, typ=item))
								categories = storage.categories(item)
								for subitem in categories:
									for subsubitem in character.traits[item][subitem].values():
										## Überprüfen ob die Eigenschaft im Anforderungstext des Merits vorkommt.
										traitResource = "{}.{}".format(item, subsubitem.identifier)
										if traitResource in traitPrerequisites:
											## Vor <typ>.<trait> darf kein anderes Wort außer "and", "or" und "(" stehen.
											idxA = traitPrerequisites.index(traitResource)
											strBefore = traitPrerequisites[:idxA]
											strBefore = strBefore.rstrip()
											strBeforeList = strBefore.split(" ")
											if not strBeforeList[-1] or strBeforeList[-1] == u"and" or strBeforeList[-1] == u"or" or strBeforeList[-1] == u"(":
												## \todo Den Namen der Eigenschaft mit einem Zeiger auf diese Eigenschaft im Speicher ersetzen.
												## Die Eigenschaften in den Voraussetzungen mit dem Merit verbinden.
												#Debug.debug("Verbinde {} mit {}".format(subsubitem.name, trait.name))
												subsubitem.traitChanged.connect(trait.checkPrerequisites)
							## Es kann auch die Supereigenschaft als Voraussetzung vorkommen.
							if Config.powerstatIdentifier in traitPrerequisites:
								character.powerstatChanged.connect(trait.checkPrerequisites)


	@staticmethod
	def checkPrerequisites(trait, storage, character):
		if type(trait) != Trait:
			Debug.debug("Error!")
		else:
			if trait.hasPrerequisites:
				## Angabe in den Ressourcen: <typ>.<trait>[.<specialty>] >|<|== ? and|or ...
				## Diese werden aufgeteilt in [[ <typ>, <trait>, <specialty> ] >|<|== ? and|or ... ]
				traitPrerequisites = trait.prerequisitesText
				#Debug.debug("{trait} hat Voraussetzungen? {truth}".format(trait=trait.name, truth=trait.hasPrerequisites))
				for item in storage.traits.keys():
					categories = storage.categories(item)
					for subitem in categories:
						#Debug.debug(categories)
						for subsubitem in character.traits[item][subitem].values():
							# Überprüfen, ob die Eigenschaft im Anforderungstext des Merits vorkommt.
							traitResource = "{}.{}".format(item, subsubitem.identifier)
							if traitResource in traitPrerequisites:
								# Vor dem Fertigkeitsnamen darf kein anderes Wort außer "and", "or" und "(" stehen.
								idxA = traitPrerequisites.index(traitResource)
								strBefore = traitPrerequisites[:idxA]
								strBefore = strBefore.rstrip()
								strBeforeList = strBefore.split(" ")
								if not strBeforeList[-1] or strBeforeList[-1] == u"and" or strBeforeList[-1] == u"or" or strBeforeList[-1] == u"(":
									# Wenn Spezialisierungen vorausgesetzt werden.
									if "{}.".format(traitResource) in traitPrerequisites:
										idx = [0,0]
										idx[0] = traitPrerequisites.index("{}.".format(traitResource))
										## Dieser Vergleich setzt voraus, daß zwischen Spezialisierung und Vergleichsoperator mindestens ein Leerzeichen existiert.
										skillWithSpecialty = re.search(r"\w+\.{1}\w+\.{1}(\w+)", traitPrerequisites[idx[0]:])
										#Debug.debug(skillWithSpecialty.group())
										specialty = skillWithSpecialty.group(1)
										#Debug.debug(traitPrerequisites, specialty)
										if specialty in subsubitem.specialties:
											traitPrerequisites = traitPrerequisites.replace(".{}".format(specialty), "")
										else:
											traitPrerequisites = traitPrerequisites.replace("{}.{}".format(traitResource, specialty), "0")
										#Debug.debug(traitPrerequisites)
									#Debug.debug("{} hat einen Wert von {}".format(subsubitem.name, subsubitem.value))
									traitPrerequisites = traitPrerequisites.replace(traitResource, unicode(subsubitem.value))
				# Es kann auch die Supereigenschaft als Voraussetzung vorkommen.
				if Config.powerstatIdentifier in traitPrerequisites:
					traitPrerequisites = traitPrerequisites.replace(Config.powerstatIdentifier, unicode(character.powerstat))

				# Die Voraussetzungen sollten jetzt nurnoch aus Zahlen und logischen Operatoren bestehen.
				try:
					#Debug.debug(traitPrerequisites)
					result = eval(traitPrerequisites)
					#Debug.debug("Eigenschaft {} ({} = {})".format(trait.name, traitPrerequisites, result))
				except (NameError, SyntaxError) as e:
					Debug.debug("Error: {}".format(traitPrerequisites))
					result = False

				#Debug.debug("Eigenschaft {} wird verfügbar? {}".format(trait.name, result))
				trait.setAvailable(result)




	