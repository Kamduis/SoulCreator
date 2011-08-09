# Name
set (PROGRAM_NAME SoulCreator)

# A short Description
set (PROGRAM_DESCRIPTION "Charaktergenerator für die World of Darkness")

project(${PROGRAM_NAME})

cmake_minimum_required(VERSION 2.6)

# # Translation files
# SET(TRANS
# 	SoulCreator_de.ts
# )

find_package(Qt4 REQUIRED)

# # KDE-Bibliotheken werden verwendet.
# find_package(KDE4 REQUIRED)

# The version number.
set (PROGRAM_VERSION_MAJOR 0)
set (PROGRAM_VERSION_MINOR 0)
set (PROGRAM_VERSION_CHANGE 1)

# configure a header file to pass some of the CMake settings to the source code
configure_file (
	"${PROJECT_SOURCE_DIR}/CMakeConfig.h.in"
	"${PROJECT_BINARY_DIR}/CMakeConfig.h"
)

include_directories(
	${QT_INCLUDES}
# 	${KDE4_INCLUDES}# KDE-Bibliotheken
	${CMAKE_CURRENT_BINARY_DIR}
	# add the binary tree to the search path for include files so that we will find Config.h
	${PROJECT_BINARY_DIR}
)

# # Ermögliche Exceptions in Verbindung mit der KDE-Bibliothek
# add_definitions(${KDE4_ENABLE_EXCEPTIONS})

file (GLOB_RECURSE SoulCreator_SRCS "./src/*.cpp")

file (GLOB_RECURSE SoulCreator_MOC_HDRS "./src/*.h")

file (GLOB_RECURSE SoulCreator_UIS "./ui/*.ui")

file (GLOB SoulCreator_RCCS "./resources/*.qrc")

# # add translations ...
# QT4_ADD_TRANSLATION(QM
# 	${TRANS}
# )

qt4_automoc(${SoulCreator_SRCS})

QT4_WRAP_CPP(SoulCreator_MOC_SRCS ${SoulCreator_MOC_HDRS})

QT4_WRAP_UI(SoulCreator_UIS_H ${SoulCreator_UIS})

QT4_ADD_RESOURCES(SoulCreator_RCC_SRCS ${SoulCreator_RCCS})

# In order to build a Qt application, the Qt include directories needs to be added as well as a range of defines need to be set.
include(${QT_USE_FILE})

add_executable(SoulCreator
	${SoulCreator_SRCS}
	${SoulCreator_MOC_SRCS}
	${SoulCreator_UIS_H}
	${SoulCreator_RCC_SRCS}
# 	${QM}
)

target_link_libraries(SoulCreator
	${QT_QTCORE_LIBRARY}
	${QT_QTGUI_LIBRARY}
	${QT_QTSQL_LIBRARY}
# 	${KDE4_KDEUI_LIBS}# KDE-Bibliotheken
)



# # Doxygen
# # Unter Windows funktioniert das automatische Ausführen von Doxygen nicht richtig.
# IF (WIN32)
# ELSE (WIN32)
# 	FIND_PACKAGE(Doxygen)
# 
# 	IF (DOXYGEN_FOUND)
# 		SET(WORKTIME_VERSION
# 			${PROGRAM_VERSION_MAJOR}.${PROGRAM_VERSION_MINOR}.${PROGRAM_VERSION_CHANGE}
# 		)
# 
# 		configure_file(${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile.in
# 			${CMAKE_CURRENT_BINARY_DIR}/Doxyfile @ONLY
# 		)
# 
# 		ADD_CUSTOM_TARGET(doc ALL
# 			${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
# 			WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
# 			COMMENT "Generating API documentation with Doxygen" VERBATIM
# 		)
# 	ENDIF (DOXYGEN_FOUND)
# ENDIF (WIN32)
