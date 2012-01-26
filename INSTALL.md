# Overview


## Requirements

SoulCreator requires Python Version 2.7 or greater and PySide Version 1.0 or greater. (If PySide will be available for Python3, it is planned, to switch SoulCreator from Python2 to Python3.)


### Linux


#### Debian/Ubuntu

To get PySide, just type the following line as root:

	apt-get install python-pyside


### Windows

To get Python for Windows, navigate to the [Python website](http://python.org/download/) and download and install the most recent Python2-Version for your architecture. After that, you should do the same with PySide. Get it from the [PySide homepage](http://developer.qt.nokia.com/wiki/PySide_Binaries_Windows).


## Generation resource files

Prior to the first start of SoulCreator, the ui- and resource-files have to be generated.

To do that, just execute the `reateResources.py`-Skript.

	python createResources.py

This is not necessary, if you have a frozen executable (see the section *Freezing*). In the process of Freezing, the necessary resource files will automatically be created.


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

If you have a frozen executable, just execute the file `SoulCreator` (or `SoulCreator.exe` on Windows), to start the program.

The next section will describe, how to generate such a *frozen* Executable.


## Freezing

With the help of [cx_Freeze](http://cx-freeze.sourceforge.net/) it is possible to *freeze* SoulCreator into a executable file, with all dependencies bundled with it. This executable will need no installed Python or PySide to work.

To create the executable, navigate to the SoulCreator root directory and then type the following in a shell:

	python setup.py build

The result is a build folder, in which you will find another folder and inside that the executable with its bundled files.


### Windows

On Windows, some of the images of SoulCreator may not be displayed correctly, if run as frozen executable. To get the correct behaviour, it is necessary, to copy following folders from your python installation to the directory containing the *frozen* executable:

* Python-root-folder`\Lib\site-packages\PySide\plugins\iconengines` to Programm-root-folder`\plugins\iconengines`
* Python-root-folder`\Lib\site-packages\PySide\plugins\imageformats` to Programm-root-folder`\plugins\imageformats`

Next, you have to create a file named `qt.conf` inside your frozen applications root folder with the following content:

	[Paths]
	Binaries = .
	Plugins = plugins

Now the svg-images should be displayed correctly.

