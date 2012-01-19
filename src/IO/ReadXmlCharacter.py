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

import ast
from xml.dom.minidom import parse, parseString

from PySide.QtCore import QObject, QDate, QByteArray, Signal

from src.Config import Config
from src.Error import ErrXmlOldVersion
from src.Debug import Debug




class ReadXmlCharacter(QObject):
	"""
	@brief Liest die gespeicherten Charakterwerte in das Programm.

	Diese Klasse dient dazu, einen auf Datenträger gespeicherten Charakter wieder in das Programm zu laden.
	"""


	exceptionRaised = Signal(str, bool)


	def __init__(self, character, parent=None):
		QObject.__init__(self, parent)

		self.__character = character


	def read( self, fileName ):
		"""
		Startet den Lesevorgang.
		"""

		xmlContent = parse(fileName)
		xmlRootElement = xmlContent.documentElement

		#debugList = []
		#for attrib in xmlRootElement.attributes.items():
			#debugList.append("{key}=\"{value}\"".format(key=attrib[0], value=attrib[1]))
		#Debug.debug("\n".join(debugList))

		versionSource = xmlRootElement.getAttribute("version")

		try:
			self.checkXmlVersion( xmlRootElement.tagName, versionSource )
		except ErrXmlOldVersion as e:
			messageText = self.tr("While opening the character file the following problem arised:\n{} {}\nIt appears, that the character will be importable, so the process will be continued. But some character values may be wrong after importing.".format(e.message, e.description))
			self.exceptionRaised.emit(messageText, e.critical)
			self.readSoulCreator()

		self.readCharacterInfo(xmlRootElement)
		self.readCharacterIdentity(xmlRootElement)
		self.readDates(xmlRootElement)
		self.readDerangements(xmlRootElement)
		self.readTraits(xmlRootElement)
		self.readItems(xmlRootElement)
		self.readPicture(xmlRootElement)


	def readCharacterInfo(self, root):
		"""
		Lese die grundlegenden Charakterinformationen aus.
		"""

		self.__character.species = self.getElementText(root.getElementsByTagName("species")[0])
		self.__character.era = self.getElementText(root.getElementsByTagName("era")[0])
		self.__character.virtue = self.getElementText(root.getElementsByTagName("virtue")[0])
		self.__character.vice = self.getElementText(root.getElementsByTagName("vice")[0])
		self.__character.breed = self.getElementText(root.getElementsByTagName("breed")[0])
		self.__character.faction = self.getElementText(root.getElementsByTagName("faction")[0])
		self.__character.organisation = self.getElementText(root.getElementsByTagName("organisation")[0])
		self.__character.party = self.getElementText(root.getElementsByTagName("party")[0])
		self.__character.height = float(self.getElementText(root.getElementsByTagName("height")[0]))
		self.__character.weight = int(self.getElementText(root.getElementsByTagName("weight")[0]))
		self.__character.eyes = self.getElementText(root.getElementsByTagName("eyes")[0])
		self.__character.hair = self.getElementText(root.getElementsByTagName("hair")[0])
		self.__character.nationality = self.getElementText(root.getElementsByTagName("nationality")[0])
		self.__character.description = self.getElementText(root.getElementsByTagName("description")[0])
		self.__character.powerstat = int(self.getElementText(root.getElementsByTagName("powerstat")[0]))
		self.__character.morality = int(self.getElementText(root.getElementsByTagName("morality")[0]))


	def readCharacterIdentity(self, root):
		"""
		Lese die Identitäten des Charkaters aus.

		\note Derzeit gibt es nur eine. forenames="" surename="" honorname="" nickname="" supername="" gender="Male"
		"""

		identitiesList = root.getElementsByTagName("identities")[0].getElementsByTagName("identity")
		realIdentity = identitiesList[0]
		#debugList = []
		#for attrib in realIdentity.attributes.items():
			#debugList.append("{key}=\"{value}\"".format(key=attrib[0], value=attrib[1]))
		#Debug.debug("\n".join(debugList))
		self.__character.identities[0].forenames = realIdentity.getAttribute("forenames").split(" ")
		self.__character.identities[0].surename = realIdentity.getAttribute("surename")
		self.__character.identities[0].honorname = realIdentity.getAttribute("honorname")
		self.__character.identities[0].nickname = realIdentity.getAttribute("nickname")
		self.__character.identities[0].supername = realIdentity.getAttribute("supername")
		self.__character.identities[0].gender = realIdentity.getAttribute("gender")


	def readDates(self, root):
		"""
		Lese die Daten aus (Geburtsdatum, Verwandlungsdatum, aktuelles Datum im Spiel).
		"""

		dates = root.getElementsByTagName("dates")[0]
		self.__character.dateBirth = QDate.fromString(dates.getAttribute("birth"), Config.dateFormat)
		self.__character.dateBecoming = QDate.fromString(dates.getAttribute("becoming"), Config.dateFormat)
		self.__character.dateGame = QDate.fromString(dates.getAttribute("game"), Config.dateFormat)


	def readDerangements(self, root):
		"""
		Liest die Geistesstörungen des Charakters.

		\note Es ist wichtig, daß die Geistesstörungen in der richtigen Moral-Reihenfolge eingelesen werden (hoch nach tief). Dies ist der Grund, weil schwere Geistesstörungen nicht erlaubt sind, wenn ihre milde form nicht vorhanden ist.
		"""

		derangements = {}

		derangementList = root.getElementsByTagName("derangements")[0].getElementsByTagName("derangement")
		for derangement in derangementList:
			moralityValue = int(derangement.getAttribute("morality"))
			derangementName = self.getElementText(derangement)
			derangements[moralityValue] = derangementName
		
		self.__character.derangements = derangements


	def readTraits(self, root):
		"""
		Liest die Eigenschaften des Charakters aus.

		\todo ich marschiere hier durch alle Eigenschaften, um die Eigenschaft des richtigen Namens zu finden, damit ich customText abarbeiten kann. Das geht doch bestimmt auch mit Direktzugriff.
		"""

		traitTypeList = root.getElementsByTagName("Traits")[0].getElementsByTagName("Type")
		for typ in traitTypeList:
			typName = typ.getAttribute("name")
			traitCategoryList = typ.getElementsByTagName("Category")
			for category in traitCategoryList:
				categoryName = category.getAttribute("name")
				traitList = category.getElementsByTagName("trait")
				for trait in traitList:
					traitName = trait.getAttribute("name")
					traitCustomText = trait.getAttribute("customText")
					traitValue = int(trait.getAttribute("value"))
					#Debug.debug(typName, categoryName, traitName, traitCustomText, traitValue)
					# Wenn die Eigenschaft nicht im Charakter-Speicher existiert (also in den Template-Dateien nicht vorkam), wird sie ignoriert.
					for item in self.__character.traits[typName][categoryName].values():
						if item.name == traitName:
							# Wenn eine Eigenschaft mit Zusatztext bereits im Speicher existiert, muß weitergesucht werden, bis eine Eigenschaft gleichen Namens mit identischem oder ohne Zusatztext gefunden wurde.
							if item.customText and item.customText != traitCustomText:
								continue

							item.value = traitValue
							#Debug.debug("Ändere Eigenschaft {} zu {}".format(item.name, item.value))
							# Zusatztext
							item.customText = traitCustomText

							specialtiesList = trait.getElementsByTagName("specialties")
							if specialtiesList:
								specialtiesText = self.getElementText(specialtiesList[0])
								item.specialties = [n for n in specialtiesText.split(Config.sepChar)]
								#Debug.debug(specialtiesText)
							break


	def readItems(self, root):
		"""
		Liest die Gegenstände des Charakters aus.
		"""

		items = root.getElementsByTagName("Items")[0]
		self.readWeapons(items)
		self.readArmor(items)
		self.readEquipment(items)


	def readWeapons(self, root):
		"""
		Liest die Waffen des Charakters aus.
		"""

		weaponCategoryList = root.getElementsByTagName("Weapons")[0].getElementsByTagName("Category")
		for category in weaponCategoryList:
			categoryName = category.getAttribute("name")
			weaponList = category.getElementsByTagName("weapon")
			for weapon in weaponList:
				weaponName = self.getElementText(weapon)
				self.__character.addWeapon(categoryName, weaponName)


	def readArmor(self, root):
		"""
		Liest die Rüstung des Charakters aus.
		"""

		armor = root.getElementsByTagName("armor")[0]
		armorDedicated = ast.literal_eval(armor.getAttribute("dedicated"))
		armorName = self.getElementText(armor)
		self.__character.setArmor(armorName, armorDedicated)


	def readEquipment(self, root):
		"""
		Liest die Besitztümer des Charakters.
		"""

		equipmentList = root.getElementsByTagName("Equipment")[0].getElementsByTagName("equipment")
		for equipment in equipmentList:
			equipmentName = self.getElementText(equipment)
			self.__character.addEquipment(equipmentName)


	def readPicture(self, root):
		"""
		Ließt das Charakterbild aus.
		"""

		if root.getElementsByTagName("picture"):
			picture = root.getElementsByTagName("picture")[0]
			imageData = QByteArray.fromBase64(str(self.getElementText(picture)))
			image = QPixmap()
			image.loadFromData(imageData, Config.pictureFormat)
			self.__character.picture = image


	def checkXmlVersion(self, name, version ):
		"""
		Überprüft die Version der XML-Datei. Damit ist die SoulCreator-Version gemeint.
		"""

		if name == Config.programName:
			if version == Config.version():
				return
			else:
				# Unterschiede in der Minor-Version sind ignorierbar, Unterschiede in der Major-Version allerdings nicht.
				splitVersion = version.split(".")
				splitVersion = [int(item) for item in splitVersion]

				## Es ist darauf zu achten, daß Charaktere bis Version 0.6 nicht mit SoulCreator 0.7 und neuer geladen werden können.
				if( splitVersion[0] != Config.programVersionMajor or splitVersion[1] < 7):
					raise Error.ErrXmlTooOldVersion( version )
				else:
					raise Error.ErrXmlOldVersion( version )
		else:
			raise Error.ErrXmlVersion( "{} {}".format(Config.programName, Config.version()), "{} {}".format(name, version) )


	def getElementText(self, element):
		"""
		Übergibt den Text im Text-Element eines Knotens. Existiert ein solches nicht, wird ein leerer String zurückgegeben.

		<bla>Text</bla>
		"""

		#Debug.debug(u"\"{}\"".format("".join(child.data for child in element.childNodes if child.nodeType==child.TEXT_NODE)))
		return u"".join(child.data for child in element.childNodes if child.nodeType==child.TEXT_NODE)


