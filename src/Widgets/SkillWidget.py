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

from PySide.QtCore import Qt, Signal
from PySide.QtGui import QWidget, QVBoxLayout, QScrollArea, QGroupBox

from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
from src.Widgets.Components.CharaTrait import CharaTrait
from src.Debug import Debug




class SkillWidget(QWidget):
	"""
	@brief Das Widget, in welchem sämtliche Fertigkeiten angeordnet sind.

	Wird bei irgendeiner Fertigkeit der Spazialisierungen-Knopf gedrückt, werden alle anderen Spezialisierungs-Knöpfe ausgeschalten.
	"""


	specialtiesActivated = Signal(bool, object)
	hideReasonChanged = Signal(str, str)


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)
		
		self.__character = character
		self.__storage = template

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__scrollArea = QScrollArea()
		self.__layout.addWidget( self.__scrollArea)

		self.__scrollLayout = QVBoxLayout()

		self.__scrollWidget = QWidget()
		#scrollWidget.setMinimumSize(this.width(), 400);
		self.__scrollWidget.setLayout(self.__scrollLayout)

		typ = "Skill"

		categoryList = (
			"Mental",
			"Physical",
			"Social",
		)

		## Eine Liste, in der alle Eigenschafts-Widgets aufgelistet werden.
		self.__traitWidgets = []

		for item in categoryList:
			#Debug.debug(self.__character.traits)
			__list = self.__character.traits[typ][item]

			# Für jede Kategorie wird ein eigener Abschnitt erzeugt.
			widgetSkillCategory = QGroupBox()
			widgetSkillCategory.setTitle(item)
			widgetSkillCategory.setFlat(True)
			
			layoutSkillCategory = QVBoxLayout()
			widgetSkillCategory.setLayout( layoutSkillCategory );

			self.__scrollLayout.addWidget( widgetSkillCategory )

			for skill in __list.values():
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = CharaTrait( skill, self )
				traitWidget.buttonText = 0
				traitWidget.setDescriptionHidden( True )

				# Dieses Widget auch an Liste anhängen, damit ich einfacher darauf zugreifen kann.
				traitListItem = traitWidget
				self.__traitWidgets.append(traitListItem)

				# Fertigkeiten haben Spezialisierungen.
				#connect( traitPtr, SIGNAL( detailsChanged( int )), charaTrait, SLOT( setButtonText(int)) );
				#connect( character, SIGNAL( characterResetted()), this, SLOT( uncheckAllButtons()) );
				self.__character.eraChanged.connect(self.emitHideReasonChanged)
				self.__character.ageChanged.connect(self.emitHideReasonChanged)
				self.hideReasonChanged.connect(traitWidget.hideOrShowTrait)
				traitWidget.specialtiesClicked.connect(self.uncheckOtherButtons)
				#connect( charaTrait, SIGNAL( specialtiesActivated( bool, QString, QList< cv_TraitDetail > ) ), this, SIGNAL( specialtiesActivated( bool, QString, QList< cv_TraitDetail > ) ) );
				traitWidget.specialtiesClicked.connect(self.specialtiesActivated.emit)
				## Wenn sich die Spezialisierungen ändern, sollen die veränderten Spezialisierungen auch angezeigt werden. Das wird so gelöst, als wäre der Knopf für die Spezialisierungen erneut gedrückt worden.
				#skill.specialtiesChanged.connect(self.emitSpecialtiesActivated)

				layoutSkillCategory.addWidget( traitWidget )

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


	#def uncheckAllButtons(self):
		"""
		Alle Spezialisierungsknöpfe werden wieder auf Standard gesetzt.
		"""
		
		#// Da hinter jeder Box ein Stretch eingefügt ist, muß dieser übersprungen werden.
		#for ( int j = 0; j < scrollLayout->count(); j=j+2 ) {
			#QGroupBox* box = qobject_cast<QGroupBox*>( scrollLayout->itemAt( j )->widget() );
	#// 		qDebug() << Q_FUNC_INFO << box->layout()->count();

			#for (int k = 0; k < box->layout()->count(); ++k){
				#CharaTrait* trait = qobject_cast<CharaTrait*>( box->layout()->itemAt( k )->widget() );

				#trait->setSpecialtyButtonChecked( false );
			#}
		#}
	#}


	def emitHideReasonChanged(self, reason):
		ageStr = Config.ages[0]
		if self.__character.age < Config.adultAge:
			ageStr = Config.ages[1]
		eraStr = self.__character.era
		self.hideReasonChanged.emit(ageStr, eraStr)


	#def emitSpecialtiesActivated(self, specialties):
		#self.specialtiesActivated.emit(True, specialties)
