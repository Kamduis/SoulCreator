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

#from PySide.QtCore import Qt, Signal
#from PySide.QtGui import QWidget, QVBoxLayout, QToolBox

#from src.Config import Config
#from src import Error
from src.Widgets.CategoryWidget import CategoryWidget
#from src.Widgets.Components.CheckTrait import CheckTrait
#from src.Debug import Debug




class SubPowerWidget(CategoryWidget):
	"""
	@brief Dieses Widget kann in Kategorien aufgeteilte Widgets aufnehmen. Es werden nur jene Kategorien angezeigt, welche auch ein anzuzeigendes Widget enthalten.
	"""


	def __init__(self, template, character, parent=None):
		CategoryWidget.__init__(self, template, character, typ="Subpower", isCheckable=True, parent=parent)



