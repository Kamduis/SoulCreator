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




#from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QStyle, QStyleOption, QPainter

#from src.Config import Config
#from src.Debug import Debug




class BackgroundImageWidget(QWidget):
	"""
	\brief Ein einfaches Widget, in welchem ein Hintergrundbild angezeigt werden kann.
	"""

	def __init__(self, parent=None):
		super(BackgroundImageWidget, self).__init__(parent)


	def paintEvent(self, event):
		opt = QStyleOption()
		opt.initFrom(self)
		p = QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)


