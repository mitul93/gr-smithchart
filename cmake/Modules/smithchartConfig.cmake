INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SMITHCHART smithchart)

FIND_PATH(
    SMITHCHART_INCLUDE_DIRS
    NAMES smithchart/api.h
    HINTS $ENV{SMITHCHART_DIR}/include
        ${PC_SMITHCHART_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SMITHCHART_LIBRARIES
    NAMES gnuradio-smithchart
    HINTS $ENV{SMITHCHART_DIR}/lib
        ${PC_SMITHCHART_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SMITHCHART DEFAULT_MSG SMITHCHART_LIBRARIES SMITHCHART_INCLUDE_DIRS)
MARK_AS_ADVANCED(SMITHCHART_LIBRARIES SMITHCHART_INCLUDE_DIRS)

