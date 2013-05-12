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
import ast
import tempfile
import zlib

from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import QObject

import src.Config as Config
import src.Tools.PathTools as PathTools
import src.GlobalState as GlobalState
from src.Error import ErrXmlOldVersion, ErrFileNotOpened
from src.IO.ReadXml import ReadXml
import src.Debug as Debug

## Fallback to normal ElementTree, sollte lxml nicht installiert sein.
lxmlLoadad = False
try:
	from lxml import etree
	lxmlLoadad = True
except ImportError:
	try:
		import xml.etree.cElementTree as etree
	except ImportError:
		try:
			import xml.etree.ElementTree as etree
		except ImportError:
			print("Failed to import ElementTree from any known place")




class ReadXmlTemplate(QObject, ReadXml):
	"""
	@brief Liest die Eigenschaften aus den beigefügten xml-Dateien.

	Diese Klasse dient dazu einen möglichst simplen Zugriff auf die Eigenschaften der WoD-Charaktere zu bieten. Dazu werden die Eigenschaften und all ihre Zusatzinformationen aus den xml-Dateien gelesen und in Listen gespeichert.
	"""


	exception_raised = Signal( str, str )


	def __init__(self, template, parent=None):
		"""
		\warning Aufgrund der multiplen Vererbung wird nicht die super()-Methode beim Aufruf der __init__()-Methoden der Elternkalssen verwendet.
		"""

		QObject.__init__(self, parent)
		ReadXml.__init__(self)

		self.__storage = template

		## Die Template-Dateien alle für das Laden vorbereiten.
		self.__templateFiles = []
		path_to_templates = os.path.join( PathTools.program_path(), Config.PATH_RESOURCE, Config.RESOURCE_DIR_TEMPLATES )
		for template_file in os.listdir(path_to_templates):
			if template_file.endswith(".{}".format(Config.FILE_SUFFIX_COMPRESSED)):
				self.__templateFiles.append( os.path.join( path_to_templates, template_file ) )


	def read(self):
		"""
		Diese Methode startet den Lesevorgang.

		Es wird kontrolliert, ob es sich um eine Zuässige Template-Datei für dieses Programm handelt

		\exception ErrXmlTooOldVersion Die XML-Datei hat die falsche Version.

		\exception ErrXmlOldVersion Die XML-Datei hat die falsche Version.

		\exception ErrXmlParsing Beim Parsen der XML-Datei ist ein Fehler aufgetreten.
		"""

		#dbgStart = Debug.timehook()
		for item in self.__templateFiles:
			Debug.debug( "Reading from file \"{}\".".format(item), level=2 )
			file_content = None
			with open(item, mode="rb") as fi:
				file_content = fi.read()

			## Erzeuge eine temporäre Datei, mit der etree umgehen kann und schreibe den Inhalt aus der Qt-Resource in selbige hinein.
			file_like = tempfile.SpooledTemporaryFile()
			## Dank dieser Einstellung kann ich zlib verwenden um Dateien zu dekomprimieren, welche mittels des gzip-Moduls komprimiert wurden.
			decompressed_object = zlib.decompressobj(16 + zlib.MAX_WBITS)
			file_like.write(decompressed_object.decompress(file_content))
			file_like.seek(0)

			xml_content = etree.parse(file_like)
			file_like.close()

			xml_root_element = xml_content.getroot()

			version_source = xml_root_element.attrib["version"]
			required_source = False
			if "required" in xml_root_element.attrib:
				required_source = xml_root_element.attrib["required"].lower() == "true"
			#Debug.debug(versionSource)

			try:
				self.checkXmlVersion( xml_root_element.tag, version_source, item, required=required_source )
			except ErrXmlOldVersion as e:
				text_description = self.tr( "{} Loading of template will be continued but errors may occur.".format( str( e ) ) )
				self.exception_raised.emit( text_description, "warning" )

			result = self.readSpecies(xml_content)
			self.readTemplate(xml_content, result[0], result[1])
		#Debug.timesince(dbgStart)


	def readSpecies(self, tree):
		"""
		Einlesen der Spezies, für welche die Eigenschaften in der gerade eingelsenen Datei gelten.

		Nicht alle existierenden Spezies sind spielbar, sollen also nicht ausgewählt werden können.
		"""

		traitsRoot = tree.find("Template")
		species = ""
		if "species" in traitsRoot.attrib:
			species = traitsRoot.attrib["species"]
		playable = True
		if "playable" in traitsRoot.attrib:
			playable = ast.literal_eval(traitsRoot.attrib["playable"])

		return [ species, playable ]


	def readTemplate(self, tree, species, isplayable=True):
		"""
		Einlesen aller verfügbarer Eigenschaften.
		"""

		self.readSpeciesData(tree.find("Template/Traits"), species, isplayable)
		self.readCharacteristics(tree.find("Template/Traits/Virtue"))
		self.readCharacteristics(tree.find("Template/Traits/Vice"))
		self.readTraits(tree.find("Template/Traits/Attribute"), species)
		self.readTraits(tree.find("Template/Traits/Skill"), species)
		self.readTraits(tree.find("Template/Traits/Merit"), species)
		self.readTraits(tree.find("Template/Traits/Flaw"), species)
		self.readTraits(tree.find("Template/Traits/Power"), species)
		self.readSubPowers(tree.find("Template/Traits/Subpower"), species)
		self.readCreationPoints(tree.find("Template/Creation"), species)
		self.readGroups(tree.find("Template/Group/Breed"), species)
		self.readGroups(tree.find("Template/Group/Faction"), species)
		self.readGroups(tree.find("Template/Group/Organisation"), species)
		self.readGroups(tree.find("Template/Group/Party"), species)
		self.readPowerstat(tree.find("Template/Traits/Powerstat"), species)
		self.readDerangements(tree.find("Template/Traits/Derangement"), species)
		self.readWeapons(tree.findall("Template/Items/Weapons"))
		self.readArmor(tree.findall("Template/Items/Armor"))
		self.readEquipment(tree.findall("Template/Items/Equipment"))
		self.readAutomobiles(tree.findall("Template/Items/Automobiles"))
		self.readExtraordinaryItems(tree.findall("Template/Items/Extraordinary"))


	def readSpeciesData(self, root, species, isplayable=True):
		"""
		Einlesen aller Spezies-abhängigen Parameter.
		"""

		speciesData = {
			"morale": self.getElementAttribute(root, "morale"),
			"powerstat": self.getElementAttribute(root, "powerstat"),
			"fuel": self.getElementAttribute(root, "fuel"),
			"playable": isplayable,
		}

		self.__storage.appendSpecies( species, speciesData )


	def readCharacteristics(self, root):
		"""
		Einlesen aller Tugenden.
		"""

		characteristics = self.__readTraitData(root)

		for item in characteristics:
			self.__storage.appendCharacteristic(root.tag, item)


	def readTraits( self, root, species ):
		"""
		Lese die Eigenschaften aus den Template-Dateien.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()
		"""

		if root is not None:
			if root.tag == "Power":
				self.__storage.setPowerName(species, self.getElementAttribute(root, "name"))
			for category in root.getiterator("Category"):
				categoryName = category.attrib["name"]
				traits = self.__readTraitData(category, species)
				for trait in traits:
					traitId = trait["id"]
					del trait["id"]
					self.__storage.addTrait( root.tag, categoryName, traitId, trait )


	def readSubPowers( self, root, species ):
		"""
		Lese die Unterkräfte aus den Template-Dateien.

		Diese werden zwar auch im trait-Dictionary gespeichert, haben aber andere Attribute als die normalen Eigenschaften.
		"""

		if root is not None:
			self.__storage.setSubPowerName(species, self.getElementAttribute(root, "name"))
			#Debug.debug(list(root))
			for categoryElement in list(root):
				if categoryElement.tag == "Category":
					categoryName = categoryElement.attrib["name"]
					## In diese Liste werden alle Unterkräfte geschrieben und erst wenn die gesamte Kategorie ausgelesen ist, werden selbige in den Speicher geschrieben.
					subPowerList = []
					cheap = []
					only = []
					for element in list(categoryElement):
						if element.tag == "trait":
							listOfPowers = {}
							listOfPrerequisites = []
							listOfOnlys = []
							for subelement in list(element):
								if subelement.tag == "power":
									listOfPowers.setdefault(subelement.text, int(subelement.attrib["value"]))
								elif subelement.tag == "prerequisites":
									listOfPrerequisites.append("({})".format(subelement.text))
								elif subelement.tag == "only":
									listOfOnlys.append("{}".format(subelement.text))
							powerPrerequisites = " and ".join(["Power.{} > {}".format(powerName, powerValue - 1) for powerName, powerValue in listOfPowers.items()])
							if powerPrerequisites:
								powerPrerequisites = "({})".format(powerPrerequisites)
								listOfPrerequisites.append(powerPrerequisites)
							subPowerData = {
								"name": element.attrib["name"],
								"level": self.getElementAttribute(element, "level"),
								"species": species,
								"costFuel": self.getElementAttribute(element, "costFuel"),
								"costWill": self.getElementAttribute(element, "costWill"),
								"roll": self.getElementAttribute(element, "roll"),
								"powers": listOfPowers,
								"prerequisites": " and ".join(listOfPrerequisites),
								"cheap": [],
								"only": listOfOnlys,
							}
							itemsToInt = (
								"level",
							)
							for item in itemsToInt:
								if subPowerData[item]:
									subPowerData[item] = int(subPowerData[item])
								else:
									subPowerData[item] = 0
							#Debug.debug(subPowerData["name"], subPowerData["prerequisites"])
							identifier = self.getElementAttribute(element, "id")
							if not identifier:
								identifier = subPowerData["name"]
							subPowerList.append([
								categoryName,
								identifier,
								subPowerData,
							])
						elif element.tag == "cheap":
							cheap.append(element.text)
						elif element.tag == "only":
							only.append(element.text)
					#Debug.debug(subPowerList)
					for item in subPowerList:
						if cheap:
							item[2]["cheap"] = cheap
						if only:
							item[2]["only"] = only
						self.__storage.addTrait( root.tag, item[0], item[1], item[2] )


	def readCreationPoints( self, root, species ):
		"""
		Lese die Erschaffungspunkte aus, die den jeweiligen Spezies zur Verfügung stehen.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()
		"""

		if root is not None:
			for typElement in root.getiterator("Type"):
				typ = typElement.attrib["name"]
				resultList = []
				for pointsElement in typElement.getiterator("points"):
					points = int(pointsElement.attrib["value"])
					resultList.append(points)
				self.__storage.appendCreationPoints( species, typ, resultList )


	def readGroups( self, root, species ):
		"""
		Liest die verschiedenen Gruppierungsnamen der einzelnen Spezies ein.
		"""

		if root is not None:
			groupCategory = root.tag
			groupCategoryName = root.attrib["name"]
			self.__storage.appendTitle( species, groupCategory, groupCategoryName )
			for element in list(root):
				if element.tag == "item":
					#Debug.debug(element.tag, element.attrib["name"])
					groupName = element.attrib["name"]
					infos = {}
					for subElement in list(element):
						if subElement.tag == "kith":
							abilityList = []
							for subsubElement in list(subElement):
								if subsubElement.tag == "ability":
									abilityList.append(subsubElement.text)
							self.__storage.addKith(groupName, subElement.attrib["name"], " ".join(abilityList))
						elif subElement.tag == "weakness":
							infos["weakness"] = subElement.text
						elif subElement.tag == "blessing":
							infos["blessing"] = subElement.text
						elif subElement.tag == "bonus":
							for subsubElement in list(subElement):
								for subsubsubElement in list(subsubElement):
									if subsubsubElement.tag == "item":
										bonusTraits = {
											"type": subsubElement.tag,
											"name": subsubsubElement.attrib["name"]
										}
										if bonusTraits:
											self.__storage.appendBonusTrait( species, groupName, bonusTraits )
					self.__storage.appendTitle( species, groupCategory, groupCategoryName, element.attrib["name"], infos )


	def readPowerstat( self, root, species ):
		"""
		Lese die Informationen über die Auswirkungen der Supereigenschaft.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()
		"""

		if root is not None:
			#Debug.debug(root.tag)
			for element in root.getiterator("powerstat"):
				powerstatData = {
					"fuelMax": int(element.attrib["fuelMax"]),
					"fuelPerTurn": int(element.attrib["fuelPerTurn"]),
					"traitMax": int(element.attrib["traitMax"]),
				}
				powerstatValue = int(element.text)
				self.__storage.appendPowerstat( species, powerstatValue, powerstatData )


	def readDerangements( self, root, species ):
		"""
		Liest die Geistesstörungen aus den Template-Dateien.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()
		"""

		if root is not None:
			#Debug.debug(root.tag, level=4)
			for mildElement in root.getiterator("mild"):
				mild = mildElement.attrib["name"]
				descriptionMild = ""
				for descriptionElement in mildElement.getiterator("description"):
					descriptionMild = descriptionElement.text
				severeVersions = []
				for severeElement in mildElement.getiterator("severe"):
					severe = severeElement.attrib["name"]
					descriptionSevere = ""
					for descriptionElement in severeElement.getiterator("description"):
						descriptionSevere = descriptionElement.text
					self.__storage.appendDerangement(species=species, name=severe, dependancy=[], description=descriptionSevere, isSevere=True)
					severeVersions.append(severe)
				self.__storage.appendDerangement(species=species, name=mild, dependancy=severeVersions, description=descriptionMild, isSevere=False)


	def readWeapons(self, root):
		"""
		Einlesen der Waffen.

		\todo Die Einteilung der Kategorie wird noch nicht wahrgenommen.
		"""

		for weapons in root:
			if GlobalState.is_fallback or not self.getElementAttribute(weapons, "fallback") == "True":
				for typElement in list(weapons):
					if typElement.tag == "Type":
						typeName = self.getElementAttribute(typElement, "name")
						for categoryElement in list(typElement):
							if categoryElement.tag == "Category":
								for weaponElement in list(categoryElement):
									if weaponElement.tag == "weapon":
										#Debug.debug(weaponElement.attrib["name"])
										weaponName = weaponElement.attrib["name"]
										weaponData = {
											"damage": self.getElementAttribute(weaponElement, "damage"),
											"ranges": self.getElementAttribute(weaponElement, "ranges"),
											"capacity": self.getElementAttribute(weaponElement, "capacity"),
											"strength": self.getElementAttribute(weaponElement, "strength"),
											"size": self.getElementAttribute(weaponElement, "size"),
											"durability": self.getElementAttribute(weaponElement, "durability"),
										}
										self.__storage.addWeapon( typeName, weaponName, weaponData )


	def readArmor(self, root):
		"""
		Einlesen der Rüstungen.
		"""

		for armors in root:
			if GlobalState.is_fallback or not self.getElementAttribute(armors, "fallback") == "True":
				for armorElement in list(armors):
					if armorElement.tag == "armor":
						armorName = armorElement.attrib["name"]
						armorData = {
							"general": int(self.getElementAttribute(armorElement, "general")),
							"firearms": int(self.getElementAttribute(armorElement, "firearms")),
							"defense": int(self.getElementAttribute(armorElement, "defense")),
							"speed": int(self.getElementAttribute(armorElement, "speed")),
						}
						self.__storage.addArmor( armorName, armorData )


	def readEquipment(self, root):
		"""
		Einlesen der Ausrüstung.
		"""

		for equipment in root:
			if GlobalState.is_fallback or not self.getElementAttribute(equipment, "fallback") == "True":
				for equipmentElement in list(equipment):
					if equipmentElement.tag == "equipment":
						equipmentName = equipmentElement.attrib["name"]
						equipmentData = {
							"durability": int(self.getElementAttribute(equipmentElement, "durability")),
							"size": int(self.getElementAttribute(equipmentElement, "size")),
							"cost": int(self.getElementAttribute(equipmentElement, "cost")),
						}
						self.__storage.addEquipment( equipmentName, equipmentData )


	def readAutomobiles(self, root):
		"""
		Einlesen der Fahrzeuge.

		\todo Die Einteilung der Kategorie wird noch nicht wahrgenommen.
		"""

		for automobiles in root:
			if GlobalState.is_fallback or not self.getElementAttribute(automobiles, "fallback") == "True":
				for element in list(automobiles):
					if element.tag == "Type":
						itemTyp = element.attrib["name"]
						for subElement in list(element):
							if subElement.tag == "Category":
								for subsubElement in list(subElement):
									if subsubElement.tag == "item":
										itemName = subsubElement.attrib["name"]
										itemData = {
											"durability": int(self.getElementAttribute(subsubElement, "durability")),
											"size": int(self.getElementAttribute(subsubElement, "size")),
											"acceleration": int(self.getElementAttribute(subsubElement, "acceleration")),
											"safeSpeed": int(self.getElementAttribute(subsubElement, "safeSpeed")),
											"maxSpeed": int(self.getElementAttribute(subsubElement, "maxSpeed")),
											"maxHandling": int(self.getElementAttribute(subsubElement, "maxHandling")),
											"occupants": self.getElementAttribute(subsubElement, "occupants"),
											"cost": float(self.getElementAttribute(subsubElement, "cost")),
										}
										self.__storage.addAutomobile( itemTyp, itemName, itemData )


	def readExtraordinaryItems(self, root):
		"""
		Einlesen der magischen Gegenstände.
		"""

		for extraordinary in root:
			if GlobalState.is_fallback or not self.getElementAttribute(extraordinary, "fallback") == "True":
				for element in list(extraordinary):
					if element.tag == "Type":
						itemTyp = element.attrib["name"]
						for subElement in list(element):
							if subElement.tag == "item":
								itemName = subElement.attrib["name"]
								itemData = {
									#"durability": int(self.getElementAttribute(equipmentElement, "durability")),
									#"size": int(self.getElementAttribute(equipmentElement, "size")),
									"cost": float(self.getElementAttribute(subElement, "cost")),
								}
								self.__storage.addExtraordinaryItem( itemTyp, itemName, itemData )


	def __readTraitData(self, root, species=None, typ=None, category=None):
		"""
		Einlesen aller Eigenschaftswerte.

		Gibt ein Dictionary folgender Form zurück:

		{
			"typ": <Typ der ausgelesenen Eigenschaften>,
			"traits" [<Liste der Eigenschaftsdaten der gefundenen Eigenschaften>]
		}

		\todo Eine Eigenschaft kann mehrfach vorkommen, da andere Spezies andere Spezialisierungen mitbringen mögen.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()

		\todo Dictionary-keys "cheap" und "only" werden nicht ausgelesen sondern nur als [] gesetzt.
		"""

		listOfTraits = []
		if root is not None:
			for traitElement in root.getiterator("trait"):
				listOfSpecialties = []
				for traitSubElement in traitElement.getiterator("specialty"):
					listOfSpecialties.append(traitSubElement.text)
				listOfSpecialties.sort()
				listOfPrerequisites = []
				for traitSubElement in traitElement.getiterator("prerequisites"):
					listOfPrerequisites.append(traitSubElement.text)
				listOfValues = []
				for traitSubElement in traitElement.getiterator("value"):
					listOfValues.append(int(traitSubElement.text))
				traitData = {
					"id": self.getElementAttribute(traitElement, "id"),			# Einzigartiger Identifier der Eigenschaft. Ist meist identisch mit dem Namen.
					"name": traitElement.attrib["name"],							# Name der Eigenschaft (alle)
					"level": self.getElementAttribute(traitElement, "level"),		# Stufe der Eigenschaft (Subpowers)
					"values": [0],													# Erlaubte Werte, welche diese Eigenschaft annehmen kann. (Merits)
					"species": species,												# Die Spezies, für welche diese Eigenschaft zur Verfügung steht.
					"age": self.getElementAttribute(traitElement, "age"),			# Die Alterskategorie, für welche diese Eigenschaft zur Verfügung steht.
					"era": [],														# Die Zeitalterkategorie, für welche diese Eigenschaft zur Verfügung steht.
					"custom": self.getElementAttribute(traitElement, "custom"),	# Handelt es sich um eine Kraft mit Zusatztext?
					"specialties": listOfSpecialties,									# Dieser Eigenschaft zugeteilten Spezialisierungen (Skills)
					"prerequisites": " and ".join(listOfPrerequisites),				# Voraussetzungen für diese Eigenschaft (Merits, Subpowers)
					"cheap": [],
					"only": [],
				}
				eraText = self.getElementAttribute(traitElement, "era")
				if eraText:
					traitData["era"] = eraText.split(Config.XML_SEPARATION_SYMBOL)
				if not traitData["id"]:
					traitData["id"] = traitData["name"]
				traitData["values"].extend(listOfValues)
				listOfTraits.append(traitData)

		return listOfTraits
