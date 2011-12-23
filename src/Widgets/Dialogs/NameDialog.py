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

##include <QDebug>

##include "Exceptions/Exception.h"
#// #include "Config/Config.h"

##include "ReadXml.h"



from __future__ import division, print_function

#from PySide.QtCore import Qt
from PySide.QtGui import QDialog

##from src.Config import Config
#from src.Storage.StorageTemplate import StorageTemplate
from src.Storage.StorageCharacter import StorageCharacter
#from src.Widgets.Components.CharaSpecies import CharaSpecies
from src.Datatypes.Identity.cv_Name import cv_Name

from ui.ui_NameDialog import Ui_NameDialog




class NameDialog(QDialog):
	"""
	@brief Dialog zur Auswahl der darzustellenden Merits.

	Alle Merits darzustellen ist wohl etwas viel. Über diesen Dialog kann der Benutzer auswählen, welche und im Falle von Merits mit Zusatztext, wieviele er angezeigt haben möchte.
	"""

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)

		self.ui = Ui_NameDialog()
		self.ui.setupUi(self)

		self.__character = StorageCharacter()

		self.ui.lineEdit_firstName.textChanged.connect(self.showNames)
		self.ui.lineEdit_additionalForenames.textChanged.connect(self.showNames)
		self.ui.lineEdit_surename.textChanged.connect(self.showNames)
		self.ui.lineEdit_honorificName.textChanged.connect(self.showNames)
		self.ui.lineEdit_nickname.textChanged.connect(self.showNames)
		self.ui.lineEdit_specialName.textChanged.connect(self.showNames)
	#connect( ui.buttonBox, SIGNAL( accepted() ), this, SLOT( saveNames() ) );
	#connect( ui.buttonBox, SIGNAL( rejected() ), this, SLOT( reject() ) );

	#// Der Erste Name in der Liste ist der firstName() und damit schon abgehandelt.
	#QString foreNames;
	#for( int i = 1; i < character.identities().at( 0 ).foreNames.count(); i++ ) {
		#foreNames.append( character.identities().at( 0 ).foreNames.at( i ) );
		#if( i < character.identities().at( 0 ).foreNames.count() - 1 ) {
			#foreNames.append( " " );
		#}
	#}

	#ui.lineEdit_firstName.setText( character.identities().at( 0 ).firstName() );
	#ui.lineEdit_additionalForenames.setText( foreNames );
	#ui.lineEdit_surename.setText( character.identities().at( 0 ).sureName );
	#ui.lineEdit_honorificName.setText( character.identities().at( 0 ).honorificName );
	#ui.lineEdit_nickname.setText( character.identities().at( 0 ).nickName );
	#ui.lineEdit_specialName.setText( character.identities().at( 0 ).supernaturalName );

	#showNames();
#}


	def showNames(self):
		"""
		Zeigt den resultierenden Namen an. Einmal der Name, wie er später auf der Schaltfläche zu sehen sein wird, die diesen Dialog aufruft, einmal den vollständigen Namen mit allen Bestandteilen.
		"""
		
		forenames = self.ui.lineEdit_additionalForenames.text().split( " " )
		forenames.insert( 0, self.ui.lineEdit_firstName.text() )

		self.ui.label_displayFull.setText( cv_Name.displayNameFull( self.ui.lineEdit_surename.text(), forenames ) )
		self.ui.label_displayDisplay.setText( cv_Name.displayNameDisplay( self.ui.lineEdit_surename.text(), self.ui.lineEdit_firstName.text(), self.ui.lineEdit_nickname.text() ) )
		self.ui.label_displayHonorific.setText( cv_Name.displayNameHonor( self.ui.lineEdit_firstName.text(), self.ui.lineEdit_honorificName.text() ) )
		self.ui.label_displaySuper.setText( self.ui.lineEdit_specialName.text() )


#void NameDialog::saveNames() {
	#character.realIdentity.foreNames.clear();

	#QString foreNames = ui.lineEdit_additionalForenames.text();
	#QStringList foreNameList;
	#if( !foreNames.isEmpty() ) {
		#foreNameList = foreNames.split( " " );
	#}

	#foreNameList.insert( 0, ui.lineEdit_firstName.text() );

	#cv_Identity id;
	#id.foreNames = foreNameList;
	#id.sureName = ui.lineEdit_surename.text();
	#id.honorificName = ui.lineEdit_honorificName.text();
	#id.nickName = ui.lineEdit_nickname.text();
	#id.supernaturalName = ui.lineEdit_specialName.text();

	#character.setRealIdentity( id );

	#accept();
#}

