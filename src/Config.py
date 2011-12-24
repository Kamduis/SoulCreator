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

from PySide.QtCore import QSize
from PySide.QtGui import QColor

##include "CMakeConfig.h"

#// #include "Exceptions/Exception.h"

##include "Config.h"




class Config():
	"""
	@brief Konfigurationsklasse des Programms.

	Hier werden die Konfigurationseinstellungen gespeichert.
	"""

	# Programmdaten
	programName = "SoulCreator"
	programVersionMajor = 0
	programVersionMinor = 6
	programVersionChange = 0
	programDescription = "Charaktergenerator für die World of Darkness."
	organization = "Caern"

	# Konfigurationsdatei
	configFile = "config.ini"

	# Vordefinierte Farben
	importantTextColorName = "darkBlue"

	# Einstellungen für das Auswahl-Widget
	selectIconSize = QSize(50,50)
	selectWidgetWidth = 150
	
	pointsNegative = QColor(255,0,0)
	pointsPositive = QColor(0,0,255)
	vSpace = 5
	#const int Config::traitCategorySpace = 10;
	#const int Config::traitMultipleMax = 3;
	#const int Config::displayTimeout = 10000;
	traitCustomTextWidthMin = 100;
	inlineWidgetHeightMax = 18;
	#const int Config::spinBoxNoTextWidth = 30;
	#const int Config::traitListVertivalWidth = 300;
	#const int Config::traitMax = 5;
	#const int Config::moralityTraitMax = 10;
	#const int Config::derangementMoralityTraitMax = 7;
	#const int Config::moralityTraitDefaultValue = 7;
	#const int Config::willpowerMax = 10;
	#const int Config::superTraitMin = 1;
	#const int Config::superTraitMax = 10;
	#const int Config::superTraitDefaultValue = 1;
	#const int Config::creationTraitDouble = 4;

	#const qreal Config::textSizeFactorPrintNormal = 0.45;
	#const qreal Config::textSizeFactorPrintSmall = 0.33;

	#QFont Config::exportFont = QFont();
	#QFont Config::windowFont = QFont();


	#QString Config::name() {
		#return PROGRAM_NAME;
	#}


	@staticmethod
	def version():
		"""
		Die aktuelle Version des Programms ausschließlich der Change-Nummer.
		
		Programme mit unterschieldicher Versionsnummer sind zueinander nicht notwendigerweise kompatibel.
		"""
		
		return "{}.{}".format(Config.programVersionMajor, Config.programVersionMinor)


	@staticmethod
	def versionDetail():
		"""
		Die aktuelle Version des Programms einschließlich der Change-Nummer.
		
		Unterscheiden sich Programme in ihrer Change-Nummer, aber der Rest ihrer Versionsnummer ist gleich, sollten eigentlich keine Kompatibilitätsprobleme mit den Template-Dateien und den gespeicherten Charakteren auftreten.
		"""
		
		return "{}.{}.{}".format(Config.programVersionMajor, Config.programVersionMinor, Config.programVersionChange)


	@staticmethod
	def color(colorName):
		"""
		Gibt die Farbe, deren Namen bekannt ist, als QColor zurück.
		"""
		
		return QColor( colorName )

#QString Config::saveDir() {
	#return "save";
#}
