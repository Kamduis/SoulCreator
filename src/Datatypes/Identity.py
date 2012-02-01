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

from PySide.QtCore import QObject, Signal
#from PySide.QtGui import QDialog

from src.Config import Config
#from src.Widgets.Components.CharaSpecies import CharaSpecies
#from src.Widgets.Dialogs.NameDialog import NameDialog
from src.Debug import Debug




class Identity(QObject):
	"""
	@brief Diese Klasse speichert die vollständige Identität eines Charakters.

	Jede Person besitzt eine Vielzahl von Namen, die über diese Klasse leicht zu verwalten sind.

	Bei Personen mit mehreren Identitäten, sollte eine Liste dieser Klasse angelegt werden, in welcher für jede Identität ein Eintrag vorgenommen wird. Auch ein Künstlername fällt unter diese Kategorie, solta also mit einem weiteren Listeneintrag realisiert werden.

	\bug Wendet man copy.deepcopy auf diese Klasse an, stürzt das programm ab.
	"""


	# Dieses Signal wird ausgesandt, wann immer sich ein Teil des Namens verändert hat.
	nameChanged = Signal()
	# Dieses Signal wird ausgesandt, wann immer sich das Geschlecht geändert hat.
	genderChanged = Signal((), (str,))
	# Dieses Signal wird ausgesandt, wann immer sich ein Teil der Identität verändert hat.
	identityChanged = Signal()


	def __init__( self, surname="", firstname="", parent=None ):
		"""
		\note Als Umgehung des deepcopy-Bugs mit dieser Klasse sind die eigentlich provaten Attribute dieser Klasse nur als protected gekennzeichnet. Um eine saubere Kopie durchführen zu können, muß ich schließlich auf sie zugreifen können.
		"""
		
		QObject.__init__(self, parent)
		
		# Liste zur Speicherung von Namen.
		#
		# {
		# 	"forenames": [Name1, Name2, Name3, ...],
		# 	"surname": Name,
		# 	"honorname": Name,
		# 	"nickame": Name,
		# 	"supername": Name,
		# }
		#
		# \sa firstName
		self._name = {
			## Vorname.
			#
			# Dieser Name wurde dem Charakter von seinen Eltern gegeben. Es besteht die Möglichkeit, mehr als einen Vornamen zu besitzen, wesewegen diese Variable vom Typ StringList ist. Der erste Vorname in dieser Liste ist immer auch der Rufname.
			#
			# \sa self.firstName
			"forenames": [firstname],
			## Nachname
			#
			# Der Familienname der Eltern.
			"surname": surname,
			# Ein Beinahme, den der Charakter entweder durch ehrenvolle Taten, durch körperliche Besonderheiten oder durch Mißgeschick erworben hat.
			#
			# - der Starke
			# - die Schöne
			# - die Kleine
			# - der Treue
			"honorname": "",
			## Spitzname.
			#
			# Mit diesem Namen wird der Charakter meist von Freunden (Menschen) gerufen.
			"nickname": "",
			## Name unter den Übernatürlichen
			#
			# Dies ist der Name, der von den übrigen Kreaturen seiner Spezies verwendet wird.
			"supername": "",
		}
		
		## Geschlecht
		self._gender = "Male"

		self.nameChanged.connect(self.identityChanged.emit)
		self.genderChanged.connect(self.identityChanged.emit)


	def __eq__(self, other):
		return (
			self.forenames == other.forenames and
			self.surname == other.surname and
			self.honorname == other.honorname and
			self.nickname == other.nickname and
			self.supername == other.supername and
			self.gender == other.gender
		)


	def __ne__(self, other):
	    return not self.__eq__(other)


	def __getForenames(self):
		return self._name["forenames"]

	def __setForenames(self, names):
		"""
		\brief Legt die Formnamen fest.

		Das Argument wird nur dann übernommen, wenn wenigstens ein Vorname in der Liste nicht aus Whitespace besteht. Leer darf die Liste allerdings sein.
		"""
		
		if self._name["forenames"] != names:
			self._name["forenames"] = names
			self.nameChanged.emit()

	forenames = property(__getForenames, __setForenames)


	def __getFirstName(self):
		"""
		Rufname.
		
		Bei Personen mit nur einem Vornamen entspricht \ref firstName dem \ref foreName. Bei Personen mit mehreren Vornamen ist \ref firstName immer der allererste \ref foreName.
		"""
		
		return self._name["forenames"][0]

	firstname = property(__getFirstName)


	def __getSurname(self):
		"""
		Nachname
		"""
		
		return self._name["surname"]

	def __setSurname(self, name):
		if self._name["surname"] != name:
			self._name["surname"] = name
			self.nameChanged.emit()

	surname = property(__getSurname, __setSurname)


	def __getRealname(self):
		"""
		Geburtsname.
		
		Dieser Name wurde dem Charakter von seinen Eltern gegeben und besteht aus Rufname (\ref firstName) und Nachname (\ref sureName) plus Namenszusatz (\ref affixName).
		
		\note Die Kenntnis dieses Namens erleichtert Magiern sympathische Magie.
		"""
		
		if (not self.firstname or not self.surname):
			# In diesem Fall benötige ich keinen Abstand zwischen den Namen, da je einer leer ist.
			return "{}{}".format(firstname, surname)
		else:
			return "{} {}".format(firstname, surname)

	realname = property(__getRealname)

	
	def __getHonorname(self):
		return self._name["honorname"]

	def __setHonorname(self, name):
		if self._name["honorname"] != name:
			self._name["honorname"] = name
			self.nameChanged.emit()

	honorname = property(__getHonorname, __setHonorname)


	def __getNickname(self):
		return self._name["nickname"]

	def __setNickname(self, name):
		if self._name["nickname"] != name:
			self._name["nickname"] = name
			self.nameChanged.emit()

	nickname = property(__getNickname, __setNickname)


	def __getSupername(self):
		return self._name["supername"]

	def __setSupername(self, name):
		if self._name["supername"] != name:
			self._name["supername"] = name
			self.nameChanged.emit()

	supername = property(__getSupername, __setSupername)


	def __getGender(self):
		return self._gender

	def setGender(self, gender):
		if self._gender != gender:
			self._gender = gender
			self.genderChanged[str].emit(gender)
			self.genderChanged.emit()

	gender = property(__getGender, setGender)

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, val):
		if self._value != val:
			self._value = val
			self.identityChanged.emit()


	def reset(self):
		self.forenames = [""]
		self.surname = ""
		self.nickname = ""
		self.honorname = ""
		self.supername = ""
		self.gender = Config.genders[0][0]


	@staticmethod
	def displayNameFull( last, fores ):
		"""
		Voller Name.
		
		Die Summe aller Namen wird formatiert und als ein einziger String ausgegeben.
		"""

		displayFull = ""

		if ( fores ):
			if type(fores) == list:
				displayFull = fores[0]
				for item in fores[1:]:
					displayFull += u" {}".format(item)
			else:
				displayFull = fores

		# Vor dem Nachnamen nur dann ein Leerzeichen, wenn schon etwas davor steht.
		if ( displayFull ):
			displayFull += " "
		displayFull += last

		return displayFull


	@staticmethod
	def displayNameDisplay( last, first, nick ):
		"""
		Angezeigter Name.
		
		Dieser Name kann auf dem Charakterbogen angezeigt werden.
		"""
		
		displayDisplay = first
		if ( nick ):
			displayDisplay += u" \"{}\"".format(nick)

		# Vor dem Nachnamen nur dann ein Leerzeichen, wenn schon etwas davor steht.
		if ( displayDisplay ):
			displayDisplay += " "
		displayDisplay += last

		return displayDisplay


	@staticmethod
	def displayNameHonor( first, honor ):
		"""
		Ehrenname
		"""
		
		displayHonor = first
		if ( honor ):
			displayHonor += u" {}".format(honor)

		return displayHonor

