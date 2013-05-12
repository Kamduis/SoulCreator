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

import src.Config as Config
from src.Datatypes.BasicTrait import BasicTrait
import src.Debug as Debug
#from src.Error import ErrTraitPrerequisite




def build_connection(storage, character):
	"""
	Merits und Subpowers müssen mit allen Eigenschaften verknüpft werden, die in ihrer Prerequisits-Eigenschaft vorkommen.

	\warning Wenn als Voraussetzung einer Eigenschaft zwei Eigenschaften desselben Typs stehen, bei denen die eine Eigenschaft den identischen Namen wie die zweite hat, nur das letztere noch weitere Buchstaben anhängen hat, kommt es zu Ersetzungsproblemen.
	"""

	typs = [ "Merit", "Flaw", "Subpower", ]
	for typ in typs:
		trait_categories = storage.categories(typ)
		for category in trait_categories:
			for trait in character.traits[typ][category].values():
				#Debug.debug("{trait} hat Voraussetzungen? {truth}".format(trait=trait.name, truth=trait.hasPrerequisites))
				if trait.hasPrerequisites:
					_do_connect(trait, storage, character)


def _do_connect(trait, storage, character):
	"""
	Durchsucht alle existierenden Eigenschaften und kontrolliert, ob sie als Voraussetzung für <trait> in Frage kommen.
	"""

	trait_prerequisites = trait.prerequisitesText
	Debug.debug(
		"Voraussetzungen von {trait}: {prerequisite}".format(trait=trait.name, prerequisite=trait_prerequisites),
		level=4,
	)
	stop_loop = False
	for prerequisite_typ in storage.traits.keys():
		## Angabe in den Ressourcen: <typ>.<trait>[.<specialty>]
		typ_resource = "{}.".format(prerequisite_typ)
		## Ist eine Eigenschaft diesen Typs eine Voraussetzung der Eigenschaft?
		if typ_resource in trait_prerequisites:
			#Debug.debug("{trait} hat {typ} als Voraussetzung!".format(trait=trait.name, typ=item))
			for prerequisite_category in storage.categories(prerequisite_typ):
				for prerequisite_trait in character.traits[prerequisite_typ][prerequisite_category].values():
					## Überprüfen ob die Eigenschaft im Anforderungstext des Merits vorkommt.
					trait_resource = "{}.{}".format(prerequisite_typ, prerequisite_trait.identifier)
					if trait_resource in trait_prerequisites:
						# Überprüfen ob diese Eigenschaft tatsächlich in den Voraussetzungen enthalten ist. Bei dieser Überprüfung ist es wichtig, auf den ganuen Namen zu prüfen: "Status" != "Status: Camarilla"
						# Diese Überprüfung wird aber nur durchgeführt, wenn die Chance besteht, daß dieser String identisch ist.
						match_list = re.findall(r"(\w+\.[\w]+[:\s]*[\w]+)(?=[\s]*[><=.]+)", trait_prerequisites, re.UNICODE)
						if trait_resource in match_list:
							stop_loop = _create_connection( trait, prerequisite_trait, trait_prerequisites, trait_resource )
							if stop_loop:
								return
	if not stop_loop:
		## Es kann auch die Supereigenschaft als Voraussetzung vorkommen ...
		if Config.POWERSTAT_IDENTIFIER in trait_prerequisites:
			character.powerstatChanged.connect(trait.checkPrerequisites)
		## ... oder die Moral
		if Config.MORALITY_IDENTIFIER in trait_prerequisites:
			character.moralityChanged.connect(trait.checkPrerequisites)


def _create_connection( trait, prerequisite_trait, trait_prerequisites, trait_resource ):
	"""
	Erzeugt die connection zwischen <trait> und den in Frage kommenden Voraussetzungen.
	"""

	## Vor <typ>.<trait> darf kein anderes Wort außer "and", "or" und "(" stehen.
	idxA = trait_prerequisites.index(trait_resource)
	strBefore = trait_prerequisites[:idxA]
	strBefore = strBefore.rstrip()
	strBeforeList = strBefore.split(" ")
	if not strBeforeList[-1] or strBeforeList[-1] == "and" or strBeforeList[-1] == "or" or strBeforeList[-1] == "(":
		## \todo Den Namen der Eigenschaft mit einem Zeiger auf diese Eigenschaft im Speicher ersetzen.
		## Die Eigenschaft, von welcher diese hier abhängig ist, der entsprechenden Liste hinzufügen.
		trait.addPrerequisiteTrait(prerequisite_trait)
		# Ändere den prerequisitesText dahingehend, daß der Verweis dort steht.
		# Ändert ohne viel Intelligenz. "Attribute.GiantKid > 1 and Attribute.Giant > 1" wird gnadenlos in "ptr00 > 1 and ptr00Kid > 1" verändert.
		#trait.prerequisitesText = trait.prerequisitesText.replace(traitResource, "ptr{}".format(id(subsubitem)))
		trait.prerequisitesText = re.sub(r"{}(?=[\s]*[><=.]+)".format(trait_resource), "ptr{}".format(id(prerequisite_trait)), trait.prerequisitesText)
		#Debug.debug(trait.prerequisiteTraits, trait.prerequisitesText)
		## Die Eigenschaften in den Voraussetzungen mit dem Merit verbinden.
		#Debug.debug("Verbinde {} mit {}".format(subsubitem.name, trait.name))
		prerequisite_trait.traitChanged.connect(trait.checkPrerequisites)
		## Sind alle Voraussetzungen mit Verweisen ersetzt, ist diese Funktion erfolgreich beendet.
		traitString = re.search(r"(?<!ptr)\w+\.\w+", trait.prerequisitesText, re.UNICODE)
		if not traitString:
			return True
	## Sind nicht alle Voraussetzungen mit Verweisen ersetzt, ist diese Funktion zwar beendet, aber es wird kein Erfolg ausgegeben.
	return False


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
			if Config.POWERSTAT_IDENTIFIER in traitPrerequisites:
				traitPrerequisites = traitPrerequisites.replace(Config.POWERSTAT_IDENTIFIER, str(character.powerstat))
			# ... oder die Moral
			if Config.MORALITY_IDENTIFIER in traitPrerequisites:
				traitPrerequisites = traitPrerequisites.replace(Config.MORALITY_IDENTIFIER, str(character.morality))

			# Die Voraussetzungen sollten jetzt nurnoch aus Zahlen und logischen Operatoren bestehen.
			## eval() is dangerous
			## Aber ast.literal_eval() erlaubt nicht das Auswerten von "a < b" etc.
			## Es werden ausschließlich Zahlen, Klammern "(" und ")" und die Zeichen "<" "<=" ">" ">=" "==" und "!=" sowie den logischen Verknüpfungen "and" und "or" erlaubt.
			#traitPrerequisites = "1 < 2 and 2 < 3"
			if re.match( r"^(\(*\d+\s*[<>=!]+\s*\d+\)*\s*(and|or)?\s*)+$", traitPrerequisites ):
				try:
					result = eval(traitPrerequisites)
					#Debug.debug("Eigenschaft {} ({} = {})".format(trait.name, traitPrerequisites, result))
				except (NameError, SyntaxError):
					Debug.debug("Error bei {}: {}".format(trait.name, traitPrerequisites))
					result = False
			else:
				raise ValueError("Only digits, spaces and the symbols \"<\", \">\", \"=\", \"!\", \"(\" and \")\" are allowed at this point.")

			Debug.debug( "Eigenschaft \"{}\" wird verfügbar? {}!".format(trait.name, result), level=4 )
			trait.setAvailable(result)
