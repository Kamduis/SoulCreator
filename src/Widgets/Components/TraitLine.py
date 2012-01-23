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

from PySide.QtCore import Signal
from PySide.QtGui import QWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel

from src.Config import Config
from src.Widgets.Components.TraitDots import TraitDots
from src.Debug import Debug




class TraitLine(QWidget):
	"""
	@brief Die grafische Darstellung einer einzigen Eigenschaft auf dem Charakterbogen.

	Die Simplen Eigenschaften (z.B. Attribute) bestehen nur aus Name und Wert. Bei kompliziertere Eigenschaften müssen noch Spezialisieren und andere Parameter beachtet werden.
	"""


	valueChanged = Signal(int)
	textChanged = Signal(str)
	buttonToggled = Signal(bool)


	def __init__(self, name, value, parent=None):
		QWidget.__init__(self, parent)

		self.__layout = QHBoxLayout()
		#self.__layout.setMargin( 0 )
		self.setLayout( self.__layout )

		self.__labelName = QLabel( self )

		self.__button = QPushButton( self )
		self.__button.setText( "..." )
		self.__button.setMaximumHeight( Config.inlineWidgetHeightMax )
		self.__button.setCheckable( True )

		self.__lineEdit = QLineEdit( self )
		self.__lineEdit.setMinimumWidth( Config.traitCustomTextWidthMin )
		self.__lineEdit.setMaximumHeight( Config.inlineWidgetHeightMax )

		self.__traitDots = TraitDots( self )

		self.__traitDots.valueChanged.connect(self.valueChanged)
		self.__traitDots.valueChanged.connect(self.enableButton)
		self.__button.toggled.connect(self.buttonToggled)
		self.__lineEdit.textChanged.connect(self.textChanged)

		self.name = name
		self.value = value
		#// Damit auch bei der Programminitialisierung die Spezialisierungen richtig enabled oder disabled sind.
		#enableSpecialties( value );

		self.__layout.addWidget( self.__labelName )
		self.__layout.addStretch()
		self.__layout.addWidget( self.__lineEdit )
		self.__layout.addWidget( self.__button )
		self.__layout.addWidget( self.__traitDots )



#QLabel* TraitLine::labelName() const {
	#return v_label_name;
#}


	@property
	def name(self):
		return self.__labelName.text()

	@name.setter
	def name( self, name ):
		self.__labelName.setText( name )


## Der beschreibende Text dieser Eigenschaft.
#QString TraitLine::text() const {
	#return lineEdit.text();
#}

	def setText( self, text ):
		self.__lineEdit.setText( text )


	@property
	def buttonText(self):
		"""
		Beschriftung des Knopfes.
		"""

		return self.__button.text()

	@buttonText.setter
	def buttonText( self, text ):
		self.__button.setText( unicode(text) )


	def __getValue(self):
		return self.__traitDots.value()

	def setValue( self, value ):
		"""
		\note Diese Funktion ist nicht privat, da ich diese Funktion als Slot benötige.
		"""

		#Debug.debug("Hurra! Setze Eigenschaft {} auf Wert {}".format(self.name(), value))
		self.__traitDots.setValue( value )

	## Der Wert, die hier dargestellten Eigenschaft.
	value = property(__getValue, setValue)


	def setPossibleValues( self, values ):
		"""
		Legt fest, welche Werte diese Zeile annehmen darf.
		"""

		self.__traitDots.setAllowedValues( values )


#int TraitLine::minimum() const {
	#return traitDots.minimum();
#}

#void TraitLine::setMinimum( int value ) {
	#traitDots.setMinimum( value );
#}


	def __getMaximum(self):
		"""
		Der Maximalwert für die Dargestellten Punkte.
		"""

		return self.__traitDots.maximum()

	def setMaximum(self, maximum):
		self.__traitDots.setMaximum(maximum)

	maximum = property(__getMaximum, setMaximum)


	def setEnabled( self, sw=True):
		self.__labelName.setEnabled(sw)
		self.__button.setEnabled(sw)
		self.__lineEdit.setEnabled(sw)
		self.__traitDots.setEnabled(sw)


	def setSpecialtyButtonChecked( self, sw=True ):
		"""
		Aktiviere oder Deaktiviere den Spezialisierungs-Knopf.
		"""

		self.__button.setChecked( sw )


	def setSpecialtiesHidden( self, sw=True ):
		"""
		Mit dieser Methode verstecke ich die Liste der Spezialisierungen. Schließlich haben nur Fertigkeiten eine Notwendigkeit dafür.
		"""

		if ( sw ):
			self.__button.hide()
		else:
			self.__button.show()


	def setSpecialtiesEnabled( self, sw=True ):
		self.__button.setEnabled( sw )


	def setDescriptionHidden( self, sw ):
		"""
		Mit dieser Methode verstecke ich die Textzeile, in welcher zusätzlicher Beschreibungstext eingegeben werden kann.
		"""

		if ( sw ):
			self.__lineEdit.hide()
		else:
			self.__lineEdit.show()


	def enableButton( self, value):
		if value > 0:
			self.__button.setEnabled(True)
		else:
			self.__button.setChecked(False)
			self.__button.setEnabled(False)


	#def emitSpecialtiesClicked(self):
		#self.specialtiesClicked.emit(self.name)




class CharaTrait(TraitLine):
	"""
	\brief Mit den gespeicherten Werten vernetzte Darstellung einer einzigen Eigenschaft auf dem Charakterbogen.

	Anders als \ref TraitLine, ist dieses Widget direkt mit der korrespondierenden Eigenschaft in der Klasse \ref StorageCharacter verknüpft. Ändert sich der Wert dort, wird automatisch dieses Widget entsprechend verändert. Gleichermaßen wird \ref StorageCharacter verändert, sollte der Benutzer dieses Widget ändern.

	\todo Solange kein Text in der Textbox einer Eigenschaft mit Zusatztext steht, sollte der Wert nicht verändert werden können.
	"""


	specialtiesClicked = Signal(bool, object)
	visibilityChanged = Signal(bool)


	def __init__(self, trait, parent=None):
		TraitLine.__init__(self, trait.name, trait.value, parent)

		self.__trait = trait

		# Falls ich mit der Maus den Wert ändere, muß er auch entsprechend verändert werden.
		self.valueChanged.connect(self.setTraitValue)
		self.textChanged.connect(self.setTraitCustomText)
		#connect( this, SIGNAL( typeChanged( cv_AbstractTrait::Type ) ), this, SLOT( hideSpecialtyWidget( cv_AbstractTrait::Type ) ) );
		#connect( this, SIGNAL( typeChanged( cv_AbstractTrait::Type ) ), this, SLOT( hideDescriptionWidget() ) );
		#connect( this, SIGNAL( specialtiesClicked( bool ) ), this, SLOT( emitSpecialtiesClicked( bool ) ) );
		self.buttonToggled.connect(self.emitSpecialtiesClicked)

		#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hideTraitIfNotAvailable( cv_Species::SpeciesFlag ) ) );
		self.__trait.valueChanged.connect(self.setValue)
		self.__trait.customTextChanged.connect(self.setText)
		self.__trait.specialtiesChanged.connect(self.setSpecialtiesButtonText)

		#// Die Signale hier zu verbinden funktioniert offensichtlich nicht. Vielleicht weil einige Fertigkeiten dann noch nicht existieren.
		#connect( traitPtr(), SIGNAL( availabilityChanged(bool)), this, SLOT( setEnabled(bool)) );
		self.__trait.availableChanged.connect(self.setEnabled)


	def setTraitValue( self, value ):
		"""
		Wenn der Wert dieses Widgets verändert wird, muß auch der dadurch repräsentierte Wert im Speicher verändert werden. Dies geschieht über diesen Slot.
		"""

		#Debug.debug("Eigenschaft {} erhält den Wert {}".format(self.__trait["name"], value))
		if self.__trait.value != value:
			self.__trait.value = value
		#Debug.debug("Eigenschaft {} hat den Wert {}".format(self.__trait["name"], self.__trait["value"]))


	#def __getCustomText() const {
		#return traitPtr()->customText();
	#}
	def setTraitCustomText( self, text ):
		"""
		Legt den Zusatztext fest.

		Dabei wird automatisch der Wert im Speicher aktualisiert und natürlich auch die Anzeige des Widget.
		"""

		if self.__trait.customText != text:
			self.__trait.customText = text

			#emit traitChanged( traitPtr() );


	def emitSpecialtiesClicked(self, sw):
		self.specialtiesClicked.emit(sw, self.__trait)


	def hideOrShowTrait_species(self, species):
		"""
		Versteckt oder zeigt diese Eigenschaft, je nach gewählter Spezies.
		"""

		visible = False
		if (not self.__trait.species or self.__trait.species == species):
			visible = True
			#Debug.debug("Verstecke {}, da Alter {} bzw. Ära {}".format(self.name, age, era))

		self.setVisible(visible)
		self.visibilityChanged.emit(visible)


	def hideOrShowTrait(self, age, era):
		"""
		Versteckt oder zeigt diese Eigenschaft.
		"""

		visible = True
		# Es können nur Eigenschaften versteckt werden, die einen age- bzw. era-Eintrag besitzen.
		if (self.__trait.age and self.__trait.age != age) or (self.__trait.era and self.__trait.era != era):
			visible = False
			#Debug.debug("Verstecke {}, da Alter {} bzw. Ära {}".format(self.name, age, era))

		self.setVisible(visible)
		self.visibilityChanged.emit(visible)


	def setSpecialtiesButtonText(self, specialties):
		#count = len(self.__trait.specialties)
		count = len(specialties)
		self.buttonText = count