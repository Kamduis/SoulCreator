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

import copy

from PySide.QtCore import QObject, Signal

#from src.Error import ErrFileNotOpened
from src.Config import Config
#from src import Error
from src.Debug import Debug




class Creation(QObject):
	"""
	\brief Berechnet die verbleibenden Punkte bei der Charaktererschaffung.
	"""


	pointsChanged = Signal(object)
	pointsChangedNegative = Signal(str)
	pointsChangedPositive = Signal(str)
	pointsChangedZero = Signal(str)


	def __init__(self, template, character, parent=None):
		QObject.__init__(self, parent)

		self.__storage = template
		self.__character = character

		self.__creationPoints = self.__storage.creationPoints
		self.__availablePoints = copy.deepcopy(self.__creationPoints)

		self.pointsChanged.connect(self.controlPoints)
		#connect( character, SIGNAL( speciesChanged(cv_Species::SpeciesFlag)), this, SLOT( controlPoints() ) );


	@property
	def creationPoints(self):
		return self.__creationPoints


	@property
	def creationPointsAvailable(self):
		return self.__availablePoints


	def calcPoints( self, trait ):
		"""
		Berechnet die noch verfügbaren Punkte.

		\note Beim Abzählen, der bereits verbrauchten Punkte werden nur Eigenschaften beachtet, die auch der aktuellen Spezies des Charakters angehören. Damit können bspw. Punkte für die Kräfte eines Mages vergeben werden, dann kann man die Spezies ändern, frische Punkte für die Kräfte als Changeling vergeben und wieder auf den Mage wechseln und die ursprünglich dort vergebenen Punkte sind noch verfügbar. Beim Speichern allerdings sollten nur die Punkte der aktuellen Spezies beachtet werden, so daß dieser Effekt beim Laden natürlich nicht eintritt.
		"""

		## Herausfinden, welchem Typ diese Eigenschaft angehört.
		typ = None
		stopLoop = False
		for item in self.__storage.traits:
			for subitem in self.__storage.traits[item]:
				if trait.name in self.__storage.traits[item][subitem]:
					typ = item
					stopLoop = True
					break
			if stopLoop:
				break

		pointList = []

		categories = self.__storage.categories(typ)

		specialtyPoints = 0
		for item in categories:
			points = 0
			for trait in self.__character.traits[typ][item].values():
				## Es werden nur Eigenschaften beachtet, die auch der aktuellen Spezies des Charakters angehören.
				if not trait.species or trait.species == self.__character.species:
					ans = trait.value - Config.creationTraitDouble

					if ans < 0:
						ans = 0

					points += trait.value - ans
					points += ans * 2

					if trait.specialties:
						specialtyPoints += len(trait.specialties)

			pointList.append(points)

		# Liste wird nach Größe sortiert, damit steht die kleinste Zahl ganz am Anfang und danach aufsteigend.
		pointList.sort()

		# Natürlich gilt das nicht für den Eintrag der Spezialisierungen, die immer am Anfang stehen.
		if typ == "Skill":
			pointList.insert( 0, specialtyPoints )

		# Bei Attributen ist der jeweils erste Punkt umsonst.
		if typ == "Attribute":
			pointList = [item - 3 for item in pointList]
		if typ == "Merit" or typ == "Power":
			ans = sum(pointList)
			pointList = [ans]

		self.__availablePoints[self.__character.species][typ] = [x - y for x, y in zip(self.__creationPoints[self.__character.species][typ], pointList)]
		#Debug.debug("{} {}: {} ({})".format(self.__character.species, typ, self.__availablePoints[self.__character.species], self.__creationPoints[self.__character.species]))

		self.pointsChanged.emit(self.__availablePoints)


	def controlPoints(self):
		"""
		Kontrolliert, ob die Punkte erschöpft sind oder gar übermäßig ausgeschöpft wurden und sendet entsprechende Signale aus.
		"""

		for subitem in self.__availablePoints[self.__character.species]:
			if any(x < 0 for x in self.__availablePoints[self.__character.species][subitem]):
				#Debug.debug("Negativ {}".format(subitem))
				self.pointsChangedNegative.emit(subitem)
			elif any(x > 0 for x in self.__availablePoints[self.__character.species][subitem]):
				#Debug.debug("Positiv {}".format(subitem))
				self.pointsChangedPositive.emit(subitem)
			else:
				#Debug.debug("Zero {}".format(subitem))
				self.pointsChangedZero.emit(subitem)


