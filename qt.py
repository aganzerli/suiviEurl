from PyQt5 import QtCore, QtGui, QtWidgets


# ----------------------------------------------------------------------------------------------------------------------------------
## @defgroup qtsp Size policies
## @{
## @name Size policies
## @{
FIXED= QtWidgets.QSizePolicy.Policy.Fixed
MINIMUM= QtWidgets.QSizePolicy.Policy.Minimum
MINIMUMEXPANDING= QtWidgets.QSizePolicy.Policy.MinimumExpanding
MAXIMUM= QtWidgets.QSizePolicy.Policy.Maximum
EXPANDING= QtWidgets.QSizePolicy.Policy.Expanding
PREFERRED= QtWidgets.QSizePolicy.Policy.Preferred
IGNORED= QtWidgets.QSizePolicy.Policy.Ignored
## @}
## @}

# ----------------------------------------------------------------------------------------------------------------------------------
## @defgroup qtav Alignment values
## @{
## @name Alignment values
## @{
ALIGNLEFT= QtCore.Qt.AlignLeft
ALIGNRIGHT= QtCore.Qt.AlignRight
ALIGNHCENTER= QtCore.Qt.AlignHCenter
ALIGNTOP= QtCore.Qt.AlignTop
ALIGNBOTTOM= QtCore.Qt.AlignBottom
ALIGNVCENTER= QtCore.Qt.AlignVCenter
ALIGNCENTER= QtCore.Qt.AlignCenter
ALIGNLUSTIFY= QtCore.Qt.AlignJustify
## @}
## @}


g_applicationWindow= None


# ----------------------------------------------------------------------------------------------------------------------------------
## Set the application window
## @param window Window (@QWidget)
def setApplicationWindow(window) :
    global g_applicationWindow

    g_applicationWindow= window


# ----------------------------------------------------------------------------------------------------------------------------------
## Get the application window
## @return Application window
## @remarks Default application window is unavailable in Maya and Houdini. In those cases, use @ref setApplicationWindow to override the default application window
def applicationWindow() :
    if g_applicationWindow : return g_applicationWindow

    return QtWidgets.QApplication.activeWindow()


# ----------------------------------------------------------------------------------------------------------------------------------
## Apply stylesheet to a widget
## @param widget Widget to apply stylesheet to
def applyStyleSheet(widget) :
    '''QtCore.QDir.setSearchPaths("nIcons", [nut.expandEnv("%NOID_PATH%/pipeline/noid_common/style/qss_icons/rc")])

    path= nut.expandEnv("%NOID_PATH%/pipeline/noid_common/style/style.qss").replace("\\", "/")
    try :
        file= open(path, "r")
    except :
        log.warning(path+" not found.")
        return

    text= file.read()'''

    widget.setStyle(QtWidgets.QStyleFactory.create("Plastique"))
    #widget.setStyleSheet(text)
