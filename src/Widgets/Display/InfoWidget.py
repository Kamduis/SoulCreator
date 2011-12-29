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

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QGridLayout, QLabel, QPushButton, QComboBox, QIcon, QSpinBox

from src.Config import Config
from src.Widgets.Components.CharaSpecies import CharaSpecies
from src.Widgets.Dialogs.NameDialog import NameDialog
from src.Debug import Debug




class InfoWidget(QWidget):
	"""
	@brief Das Widget, in welchem wichtige Informationen dargestellt werden.

	Spezies, Namen etc. des Charakters werden hier dargestellt.

	\todo Bei den Virtues und Vices wird bislang nur der erwachsene behrücksichtigt.
	"""

	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)
		
		self.__storage = template
		self.__character = character

		self.__layout = QGridLayout()
		self.setLayout( self.__layout )

		self.__labelName = QLabel( "" )
		self.__namePushButton = QPushButton( self.tr( "Name:" ) )
		#// 	QLabel* labelNameFull = new QLabel()
		#// 	QLabel* labelNameDisplay = new QLabel()
		#// 	QLabel* labelNameHonorific = new QLabel()
		#// 	QLabel* labelNameSuper = new QLabel()

		self.__labelGender = QLabel( self.tr( "Gender:" ) )
		self.__genderCombobox = QComboBox( self )
		for item in Config.genders:
			self.__genderCombobox.addItem( u"{} ({})".format(item[0], item[1]) )

		self.__labelAge = QLabel( self.tr( "Age:" ) )
		self.__spinBoxAge = QSpinBox( self )
		self.__spinBoxAge.setMinimum(6)
		self.__spinBoxAge.setMaximum(999)

		self.__labelSpecies = QLabel( self.tr( "Species:" ) )
		self.__speciesComboBox = CharaSpecies( self)

		self.__labelVirtue = QLabel( self.tr( "Virtue:" ) )
		self.__virtueCombobox = QComboBox( self )
		#self.__virtueCombobox.addItems( storage.virtueNames() )

		self.__labelVice = QLabel( self.tr( "Vice:" ) )
		self.__viceCombobox = QComboBox( self )
		#self.__viceCombobox.addItems( storage.viceNames() )

		self.__labelBreed = QLabel( self.tr( "Breed:" ) )
		self.__breedCombobox = QComboBox( self )
		#self.__breedCombobox.addItems( storage.breedNames() )

		self.__labelFaction = QLabel( self.tr( "Faction:" ) )
		self.__factionCombobox = QComboBox( self )
		#self.__factionCombobox.addItems( storage.factionNames() )

		self.__labelEra = QLabel( self.tr( "Era:" ) )
		self.__comboBoxEra = QComboBox( self )
		self.__comboBoxEra.addItems( Config.eras )

		self.__layout.addWidget( self.__namePushButton, 0, 0, Qt.AlignTop )
		self.__layout.addWidget( self.__labelName, 0, 1, 1, 2 )
		self.__layout.addWidget( self.__labelGender, 1, 0 )
		self.__layout.addWidget( self.__genderCombobox, 1, 1 )
		self.__layout.addWidget( self.__labelAge, 2, 0 )
		self.__layout.addWidget( self.__spinBoxAge, 2, 1 )
		self.__layout.addWidget( self.__labelSpecies, 3, 0 )
		self.__layout.addWidget( self.__speciesComboBox, 3, 1 )
		self.__layout.addWidget( self.__labelVirtue, 4, 0 )
		self.__layout.addWidget( self.__virtueCombobox, 4, 1 )
		self.__layout.addWidget( self.__labelVice, 5, 0 )
		self.__layout.addWidget( self.__viceCombobox, 5, 1 )
		self.__layout.addWidget( self.__labelBreed, 6, 0 )
		self.__layout.addWidget( self.__breedCombobox, 6, 1 )
		self.__layout.addWidget( self.__labelFaction, 7, 0 )
		self.__layout.addWidget( self.__factionCombobox, 7, 1 )
		self.__layout.addWidget( self.__labelEra, 0, 3 )
		self.__layout.addWidget( self.__comboBoxEra, 0, 4 )

		self.__namePushButton.clicked.connect(self.openNameDialog)
		self.__genderCombobox.currentIndexChanged[str].connect(self.changeGender)
		self.__spinBoxAge.valueChanged[int].connect(self.changeAge)
		self.__comboBoxEra.currentIndexChanged[str].connect(self.changeEra)
	#connect( virtueCombobox, SIGNAL( currentIndexChanged( int ) ), self, SLOT( changeVirtue( int ) ) );
	#connect( viceCombobox, SIGNAL( currentIndexChanged( int ) ), self, SLOT( changeVice( int ) ) );
	#connect( breedCombobox, SIGNAL( currentIndexChanged( int ) ), self, SLOT( changeBreed( int ) ) );
	#connect( factionCombobox, SIGNAL( currentIndexChanged( int ) ), self, SLOT( changeFaction( int ) ) );
		self.__character.ageChanged.connect(self.updateAge)
	#connect( character, SIGNAL( realIdentityChanged( cv_Identity ) ), self, SLOT( updateIdentity( cv_Identity ) ) );
	#connect( character, SIGNAL( virtueChanged( QString ) ), self, SLOT( updateVirtue( QString ) ) );
	#connect( character, SIGNAL( viceChanged( QString ) ), self, SLOT( updateVice( QString ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( updateBreedTitle( cv_Species::SpeciesFlag ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( updateFactionTitle( cv_Species::SpeciesFlag ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( updateBreedBox( cv_Species::SpeciesFlag ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( updateFactionBox( cv_Species::SpeciesFlag ) ) );
	#connect( character, SIGNAL( breedChanged( QString ) ), self, SLOT( updateBreed( QString ) ) );
	#connect( character, SIGNAL( factionChanged( QString ) ), self, SLOT( updateFaction( QString ) ) );
		self.__character.eraChanged.connect(self.updateEra)
#}


	def openNameDialog(self):
		"""
		Ruft einen Dialog auf, in welchem die zahlreichen Namen des Charakters eingetragen werden können.
		"""
		
		dialog = NameDialog( self.__character, self )
		dialog.exec_()


	def changeGender( self, gender ):
		"""
		Legt das Geschlecht des Charakters fest.
		"""

		self.__character.identities[0].gender = gender


	def changeAge( self, age ):
		"""
		Legt das Alter des Charakters fest.
		"""

		self.__character.age = age


#void InfoWidget::changeVirtue( int idx ) {
	#"""
	#Verändert die Tugend des Charakters.
	#"""
	
	#character->setVirtue( virtueCombobox->currentText() );
#}

#void InfoWidget::changeVice( int idx ) {
	#"""
	#Verändert das Laster des Charakters.
	#"""

	#character->setVice( viceCombobox->currentText() );
#}

#void InfoWidget::changeBreed( int idx ) {
	#"""
	#Verändert die Brut des Charakters.
	#"""

	#character->setBreed( breedCombobox->currentText() );
#}

#void InfoWidget::changeFaction( int idx ) {
	#"""
	#Verändert die Fraktion des Charakters.
	#"""

	#character->setFaction( factionCombobox->currentText() );
#}


	def changeEra( self, era ):
		"""
		Legt die zeitliche Ära fest, in welcher der Charakter zuhause ist.
		"""

		self.__character.era = era


#void InfoWidget::updateIdentity( cv_Identity id ) {
	#"""
	#Aktualisiert die Anzeige des Namens.
	
	#\bug Mit jedem Speichern und Laden wächst die Anzahl der unnötigen Leerzeichen am Ende an. Symptome sind zwar behoben, die ursache aber noch nicht.
	#"""

#// 	namePushButton->setText( cv_Name::displayNameDisplay( id.sureName, id.firstName(), id.nickName ) );

	#QString nameText = "";

	#if( !id.sureName.isEmpty() || !id.foreNames.isEmpty() ) {
		#nameText += cv_Name::displayNameFull( id.sureName, id.foreNames );
	#}

	#if( !id.nickName.isEmpty() ) {
		#if( !nameText.isEmpty() ) {
			#nameText += "\n";
		#}

		#nameText += cv_Name::displayNameDisplay( id.sureName, id.firstName(), id.nickName );
	#}

	#if( !id.honorificName.isEmpty() ) {
		#if( !nameText.isEmpty() ) {
			#nameText += "\n";
		#}

		#nameText += cv_Name::displayNameHonor( id.firstName(), id.honorificName );
	#}

	#if( !id.supernaturalName.isEmpty() ) {
		#if( !nameText.isEmpty() ) {
			#nameText += "\n";
		#}

		#nameText += id.supernaturalName;
	#}

	#labelName->setText( nameText );

	#if( id.gender == cv_Identity::Male ) {
		#genderCombobox->setCurrentIndex( 0 );
	#} else {
		#genderCombobox->setCurrentIndex( 1 );
	#}
#}


	def updateAge(self, age):
		"""
		Aktualisiert die Anzeige des Alters.
		"""

		#Debug.debug("Verändere Anzeige des Alters auf {}".format(age))
		self.__spinBoxAge.setValue(age)


#void InfoWidget::updateVirtue( QString txt ) {
	#"""
	#Aktualisiert die Anzeige der Tugend.
	#"""

	#virtueCombobox->setCurrentIndex( virtueCombobox->findText( txt ) );
#}

#void InfoWidget::updateVice( QString txt ) {
	#"""
	#Aktualisiert die Anzeige des Lasters.
	#"""

	#viceCombobox->setCurrentIndex( viceCombobox->findText( txt ) );
#}

#void InfoWidget::updateBreed( QString txt ) {
	#"""
	#Aktualisiert die Anzeige der Brut.
	#"""

	#breedCombobox->setCurrentIndex( breedCombobox->findText( txt ) );
#}

#void InfoWidget::updateFaction( QString txt ) {
	#"""
	#Aktualisiert die Anzeige der Fraktion.
	#"""

	#factionCombobox->setCurrentIndex( factionCombobox->findText( txt ) );
#}

#void InfoWidget::updateBreedTitle( cv_Species::SpeciesFlag spe ) {
	#"""
	#Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Bruten.
	#"""

	#labelBreed->setText( storage->breedTitle( spe )  + ":" );
#}

#void InfoWidget::updateFactionTitle( cv_Species::SpeciesFlag spe ) {
	#"""
	#Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Fraktionen
	#"""

	#labelFaction->setText( storage->factionTitle( spe )  + ":" );
#}

#void InfoWidget::updateBreedBox( cv_Species::SpeciesFlag spe ) {
	#"""
	#Wenn die Spezies sich ändert, muß die Auswahl der möglichen Bruten verändert werden.
	#"""

	#breedCombobox->clear();
	#breedCombobox->addItems( storage->breedNames( spe ) );
#}

#void InfoWidget::updateFactionBox( cv_Species::SpeciesFlag spe ) {
	#"""
	#Wenn die Spezies sich ändert, muß die Auswahl der möglichen Fraktionen verändert werden.
	#"""

	#factionCombobox->clear();
	#factionCombobox->addItems( storage->factionNames( spe ) );
#}


	def updateEra(self, era):
		"""
		Aktualisiert die Anzeige der Ära
		"""

		#Debug.debug("Verändere Anzeige der Ära auf {}".format(era))
		self.__comboBoxEra.setCurrentIndex(self.__comboBoxEra.findText(era))


