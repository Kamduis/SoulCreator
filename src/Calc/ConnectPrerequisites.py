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




import re

from src.Config import Config
from src.Datatypes.BasicTrait import BasicTrait
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

		\warning Wenn als Voraussetzung einer Eigenschaft zwei Augenschaften desselben Typs stehen, bei denen die eine Eigenschaft den identischen namen wie die zweite hat, nur das letztere noch weitere Buchstaben anhängen hat, kommt es zu Ersetzungsproblemen.
		"""

		typs = [ "Merit", "Flaw", "Subpower", ]
		#typs = [ "Merit" ]
		stopLoop = False
		for typ in typs:
			categoriesTraits = storage.categories(typ)
			for category in categoriesTraits:
				for trait in character.traits[typ][category].values():
					#Debug.debug("{trait} hat Voraussetzungen? {truth}".format(trait=trait.name, truth=trait.hasPrerequisites))
					if trait.hasPrerequisites:
						traitPrerequisites = trait.prerequisitesText
						#Debug.debug("Voraussetzungen von {trait}: {prerequisite}".format(trait=trait.name, prerequisite=trait.prerequisitesText))
						stopLoop = False
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
											# Überprüfen ob diese Eigenschaft tatsächlich in den Voraussetzungen enthalten ist. Bei dieser Überprüfung ist es wichtig, auf den ganuen Namen zu prüfen: "Status" != "Status: Camarilla"
											# Diese Überprüfung wird aber nur durchgeführt, wenn die Chance besteht, daß dieser String identisch ist.
											matchList = re.findall(r"(\w+\.[\w]+[:\s]*[\w]+)(?=[\s]*[><=.]+)", traitPrerequisites, re.UNICODE)
											if traitResource in matchList:
												## Vor <typ>.<trait> darf kein anderes Wort außer "and", "or" und "(" stehen.
												idxA = traitPrerequisites.index(traitResource)
												strBefore = traitPrerequisites[:idxA]
												strBefore = strBefore.rstrip()
												strBeforeList = strBefore.split(" ")
												if not strBeforeList[-1] or strBeforeList[-1] == "and" or strBeforeList[-1] == "or" or strBeforeList[-1] == "(":
													## \todo Den Namen der Eigenschaft mit einem Zeiger auf diese Eigenschaft im Speicher ersetzen.
													## Die Eigenschaft, von welcher diese hier abhängig ist, der entsprechenden Liste hinzufügen.
													trait.addPrerequisiteTrait(subsubitem)
													# Ändere den prerequisitesText dahingehend, daß der Verweis dort steht.
													# Ändert ohne viel Intelligenz. "Attribute.GiantKid > 1 and Attribute.Giant > 1" wird gnadenlos in "ptr00 > 1 and ptr00Kid > 1" verändert.
													#trait.prerequisitesText = trait.prerequisitesText.replace(traitResource, "ptr{}".format(id(subsubitem)))
													trait.prerequisitesText = re.sub(r"{}(?=[\s]*[><=.]+)".format(traitResource), "ptr{}".format(id(subsubitem)), trait.prerequisitesText)
													#Debug.debug(trait.prerequisiteTraits, trait.prerequisitesText)
													## Die Eigenschaften in den Voraussetzungen mit dem Merit verbinden.
													#Debug.debug("Verbinde {} mit {}".format(subsubitem.name, trait.name))
													subsubitem.traitChanged.connect(trait.checkPrerequisites)
													## Sind alle Voraussetzungen mit Verweisen ersetzt, kann man die Schleife hier abbrechen.
													traitString = re.search(r"(?<!ptr)\w+\.\w+", trait.prerequisitesText, re.UNICODE)
													if not traitString:
														#Debug.debug("Abbruch der Schleife")
														stopLoop = True
										if stopLoop:
											break
									if stopLoop:
										break
							if stopLoop:
								break
						## Es kann auch die Supereigenschaft als Voraussetzung vorkommen ...
						if Config.powerstatIdentifier in traitPrerequisites:
							character.powerstatChanged.connect(trait.checkPrerequisites)
						## ... oder die Moral
						if Config.moralityIdentifier in traitPrerequisites:
							character.moralityChanged.connect(trait.checkPrerequisites)


	@staticmethod
	def checkPrerequisites(trait, storage, character):
		if not isinstance(trait, BasicTrait):
			Debug.debug("Error!")
		else:
			if trait.hasPrerequisites and trait.prerequisiteTraits:
				## Angabe in den Ressourcen: <typ>.<trait>[.<specialty>] >|<|== ? and|or ...
				## Diese werden aufgeteilt in [[ <typ>, <trait>, <specialty> ] >|<|== ? and|or ... ]
				traitPrerequisites = trait.prerequisitesText
				#Debug.debug("{trait} hat Voraussetzungen? {truth}".format(trait=trait.name, truth=trait.hasPrerequisites))
				for item in trait.prerequisiteTraits:
					# Überprüfen, ob die Eigenschaft im Anforderungstext des Merits vorkommt.
					literalReference = "ptr{}".format(id(item))
					if literalReference in traitPrerequisites:
						## Spezialisierungen
						literalReferencePlusSpecial = "{}.".format(literalReference)
						if literalReferencePlusSpecial in traitPrerequisites:
							idx = traitPrerequisites.index(literalReferencePlusSpecial)
							#traitWithSpecial = re.search(r"\w+\.{1}(\w+)", traitPrerequisites[idx:])
							#special = traitWithSpecial.group(1)
							specialties = re.findall(r"\w+\.{1}(\w+)", traitPrerequisites[idx:])
							for special in specialties:
								if special in item.specialties:
									traitPrerequisites = traitPrerequisites.replace(".{}".format(special), "")
								else:
									traitPrerequisites = traitPrerequisites.replace("{}.{}".format(literalReference, special), "0")
						traitPrerequisites = traitPrerequisites.replace(literalReference, str(item.value))
				# Es kann auch die Supereigenschaft als Voraussetzung vorkommen ...
				if Config.powerstatIdentifier in traitPrerequisites:
					traitPrerequisites = traitPrerequisites.replace(Config.powerstatIdentifier, str(character.powerstat))
				# ... oder die Moral
				if Config.moralityIdentifier in traitPrerequisites:
					traitPrerequisites = traitPrerequisites.replace(Config.moralityIdentifier, str(character.morality))

				# Die Voraussetzungen sollten jetzt nurnoch aus Zahlen und logischen Operatoren bestehen.
				try:
					#Debug.debug(traitPrerequisites)
					result = eval(traitPrerequisites)
					#Debug.debug("Eigenschaft {} ({} = {})".format(trait.name, traitPrerequisites, result))
				except (NameError, SyntaxError):
					Debug.debug("Error bei {}: {}".format(trait.name, traitPrerequisites))
					result = False

				#Debug.debug("Eigenschaft {} wird verfügbar? {}".format(trait.name, result))
				trait.setAvailable(result)



