# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) 2011 by Victor von Rhein

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

		#connect( traitDots, SIGNAL( valueChanged( int ) ), SIGNAL( valueChanged( int ) ) );
		self.__traitDots.valueChanged.connect(self.valueChanged)
		#connect( traitDots, SIGNAL( valueChanged( int ) ), self, SLOT( enableSpecialties( int ) ) );
		#connect( button, SIGNAL( clicked( bool ) ), self, SIGNAL( specialtiesClicked( bool ) ) );
		#connect( lineEdit, SIGNAL( textChanged( QString ) ), self, SIGNAL( textChanged( QString ) ) );

		self.setName( name )
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


	def name(self):
		return self.__labelName.text()

	def setName( self, name ):
		self.__labelName.setText( name )


#QString TraitLine::text() const {
	#return lineEdit.text();
#}

#void TraitLine::setText( QString text ) {
	#lineEdit.setText( text );
#}

	def __getButtonText(self):
		return self.__button.text()

	def __setButtonText( self, text ):
		self.__button.setText( unicode(text) )

	buttonText = property(__getButtonText, __setButtonText)


	def __getValue(self):
		return self.__traitDots.value()

	def setValue( self, value ):
		"""
		\note Diese Funktion ist nicht privat, da ich diese Funktion als Slot benötige.
		"""
		
		#Debug.debug("Hurra! Setze Eigenschaft {} auf Wert {}".format(self.name(), value))
		self.__traitDots.setValue( value )

	value = property(__getValue, setValue)


#void TraitLine::setPossibleValues( QList< int > valueList ) {
	#traitDots.setAllowedValues( &valueList );
#}

#int TraitLine::minimum() const {
	#return traitDots.minimum();
#}

#void TraitLine::setMinimum( int value ) {
	#traitDots.setMinimum( value );
#}

#void TraitLine::setSpecialtyButtonChecked( bool sw ) {
	#button.setChecked( sw );
#}



	def setSpecialtiesHidden( self, sw=True ):
		if ( sw ):
			self.__button.hide()
		else:
			self.__button.show()


	def setSpecialtiesEnabled( self, sw=True ):
		self.__button.setEnabled( sw )


	def setDescriptionHidden( self, sw ):
		if ( sw ):
			self.__lineEdit.hide()
		else:
			self.__lineEdit.show()

