# Overview


## Requirements

SoulCreator requires Python Version 2.7 or greater and PySide Version 1.0 or greater. (If PySide will be available for Python3, it is planned, to switch SoulCreator from Python2 to Python3.)


### Linux


#### Debian/Ubuntu

To get PySide, just type the following line as root:

	apt-get install python-pyside


### Windows

To get Python for Windows, navigate to the [Python website](http://python.org/download/) and download and install the most recent Python2-Version for your architecture. After that, you should do the same with PySide. Get it from the [PySide homepage](http://developer.qt.nokia.com/wiki/PySide_Binaries_Windows).


## Installation

With the help of [cx_Freeze](http://cx-freeze.sourceforge.net/) it is possible to “freeze” SoulCreator into a executable file, with all dependencies bundled with it. This executable will need no installed Python or PySide to work.

To create the executable, navigate to the SoulCreator root directory and then type the following in a shell:

	python setup.py build

The result is a build folder, in which you will find another folder and inside that the executable with its bundled files.


## Execution

To execute the Program just start SoulCreator.py in an python environment.


### Linux

Most Linux distributions are already shipped with a sufficiently modern Python environment. Just navigate to the folder in which you saved SoulCreator files and type the following in a shell:

	python SoulCreator.py

Alternatively you can set the executable flag for SoulCreator.py and start it directly:

	chmod +x SoulCreator.py
	./SoulCreator.py


### Windows

After you have installed Python and PySide, you should be able to start SoulCreator with a simple double-click on `SoulCreator.py`.


### Frozen Executable

If you have the before mentioned frozen executable, just execute the file `SoulCreator` (or `SoulCreator.exe` on Windows), to start the program.

