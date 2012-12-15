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

from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QVBoxLayout, QScrollArea, QGroupBox

import src.Config as Config
#from src import Error
from src.Widgets.Components.CharaTrait import CharaTrait
from src.Widgets.TraitWidget import TraitWidget
#from src.Debug import Debug




class SkillWidget(TraitWidget):
	"""
	@brief Das Widget, in welchem sämtliche Fertigkeiten angeordnet sind.

	Wird bei irgendeiner Fertigkeit der Spazialisierungen-Knopf gedrückt, werden alle anderen Spezialisierungs-Knöpfe ausgeschalten.
	"""


	specialtiesActivated = Signal(bool, object)


	def __init__(self, template, character, parent=None):
		super(SkillWidget, self).__init__(template, character, parent)

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__scrollArea = QScrollArea()
		## Die Auflistung der Fertigkeiten soll auch unter Windows einen transparenten Hintergrund haben.
		self.__scrollArea.setObjectName("transparentWidget")
		## \todo Sollte nicht vom Betriebssystem, sondern vom verwendeten Style abhängen.
		if os.name == "nt":
			self.__scrollArea.setStyleSheet( "QWidget#transparentWidget { background: transparent; }" )
		self.__layout.addWidget( self.__scrollArea)

		self.__scrollLayout = QVBoxLayout()

		self.__scrollWidget = QWidget()
		## Die Auflistung der Fertigkeiten soll auch unter Windows einen transparenten Hintergrund haben. Indem ich den selben Namen wie zuvor vergebe, wirkt auch das Stylsheet auf dieses Widget.
		self.__scrollWidget.setObjectName("transparentWidget")
		#self.__scrollWidget.setStyleSheet( "QWidget#transparentWidget { background-color:transparent; }" )
		#scrollWidget.setMinimumSize(this.width(), 400);
		self.__scrollWidget.setLayout(self.__scrollLayout)

		typ = "Skill"

		## Eine Liste, in der alle Eigenschafts-Widgets aufgelistet werden.
		self.__traitWidgets = []

		for item in Config.CATEGORIES_MAIN:
			#Debug.debug(self._character.traits)

			# Für jede Kategorie wird ein eigener Abschnitt erzeugt.
			widgetSkillCategory = QGroupBox()
			widgetSkillCategory.setTitle(item)
			widgetSkillCategory.setFlat(True)

			layoutSkillCategory = QVBoxLayout()
			widgetSkillCategory.setLayout( layoutSkillCategory );

			self.__scrollLayout.addWidget( widgetSkillCategory )

			__list = list( self._character.traits[typ][item].items() )
			__list.sort()
			for skill in __list:
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = CharaTrait( skill[1], self )
				traitWidget.buttonText = 0
				traitWidget.setDescriptionHidden( True )
				traitWidget.enableButton(0)	# Zu Beginn sollen die Spezailisierungen nicht enabled sein.

				# Dieses Widget auch an Liste anhängen, damit ich einfacher darauf zugreifen kann.
				traitListItem = traitWidget
				self.__traitWidgets.append(traitListItem)

				# Es werden nur Fertigkeiten der richtigen Alters- und Zeit-Kategorie angezeigt.
				self.hideReasonChanged.connect(traitWidget.hideOrShowTrait)
				# Fertigkeiten haben Spezialisierungen.
				traitWidget.specialtiesClicked.connect(self.uncheckOtherButtons)
				traitWidget.specialtiesClicked.connect(self.specialtiesActivated.emit)
				## Wenn sich die Spezialisierungen ändern, sollen die veränderten Spezialisierungen auch angezeigt werden. Das wird so gelöst, als wäre der Knopf für die Spezialisierungen erneut gedrückt worden.
				#skill.specialtiesChanged.connect(self.emitSpecialtiesActivated)

				layoutSkillCategory.addWidget( traitWidget )

				self.maxTraitChanged.connect(traitWidget.setMaximum)

			# Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
			self.__scrollLayout.addStretch()

		self.__scrollArea.setWidget(self.__scrollWidget)
		self.__scrollArea.setWidgetResizable(True)
		self.__scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.__scrollArea.setMinimumWidth(self.__scrollArea.viewport().minimumWidth())


	def uncheckOtherButtons( self, sw, trait ):
		"""
		Über diese Funktion werden alle anderen Spezialisierungs-Knöpfe deaktiviert, sobald einer aktiviert wird.
		"""

		#Debug.debug("Drücke {}".format(skillName))
		if sw:
			for item in self.__traitWidgets:
				if item.name != trait.name:
					item.setSpecialtyButtonChecked(False)


	#def emitSpecialtiesActivated(self, specialties):
		#self.specialtiesActivated.emit(True, specialties)

