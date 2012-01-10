# Overview


## Requirements

SoulCreator requires Python Version 2.7 or greater and PySide Version 1.0 or greater.

### Linux


#### Debian/Ubuntu

To get PySide, just type the following line as root:

	apt-get install python-pyside


### Windows

To get Python for Windows, navigate to the [Python website](http://python.org/download/) and download and install the most recent Python2-Version for your architecture. After that, you should do the same with PySide. Get it from the [PySide homepage](http://developer.qt.nokia.com/wiki/PySide_Binaries_Windows).


## Installation

With the help of [cx_Freeze](http://cx-freeze.sourceforge.net/) it is possible to “freeze” SoulCreator into a executable file, with all dependancies bundlet with it. This executable will need no installed Python or PySide to work.

To create the executable, navigate to the SoulCreator root directory and then type the following in a shell:

	python setup.py build

The result is a build folder, in which you will find another folder and inside that the executable with its bundled files.


## Execution

To execute the Programm just start SoulCreator.py in an python environement.


### Linux

Most Linux distributions are already shipped with a sufficiently modern Python environmet. Just navigate to the folder in which you saved SoulCreator files and type the following in a shell:

	python SoulCreator.py

Alternativley you can set the executable flag for SoulCreator.py and start it directly:

	chmod +x SoulCreator.py
	./SoulCreator.py


### Windows

After you have installed Python and PySide, you should be able to start SoulCreator with a simple Doubleclick on SoulCreator.py.

