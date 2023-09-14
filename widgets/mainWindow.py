import qt


# ==================================================================================================================================
## Create a main window
class MainWindow(qt.QtWidgets.QMainWindow) :
    s_show_sig= qt.QtCore.pyqtSignal()
    s_hide_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Constructor
    ## @param title Window title (@a string)
    def __init__(self, title) :
        super(MainWindow, self).__init__()

        #qt.applyStyleSheet(self)

        self.setWindowTitle(title)
        self.setContentsMargins(8, 8, 8, 8)

    # ------------------------------------------------------------------------------------------------------------------------------
    def showEvent(self, event) :
        super(MainWindow, self).showEvent(event)

        if not event.spontaneous() :
            self.s_show_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def closeEvent(self, event) :
        super(MainWindow, self).closeEvent(event)

        self.s_hide_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the widget for this windpw
    ## @param widget Widget
    def setWidget(self, widget) :
        self.setCentralWidget(widget)

        return widget

    # ------------------------------------------------------------------------------------------------------------------------------
    def show(self) :
        super(MainWindow, self).show()

        self.activateWindow()
        #flags= self.windowFlags()
        #self.setWindowFlags(flags | qt.QtCore.Qt.WindowStaysOnTopHint)  # set always on top flag, makes window disappear
        #self.setWindowFlags(flags) # clear always on top flag, makes window disappear
        #super(MainWindow, self).show()

    # ------------------------------------------------------------------------------------------------------------------------------
    def showMaximized(self) :
        super(MainWindow, self).showMaximized()

        self.activateWindow()
        #flags= self.windowFlags()
        #self.setWindowFlags(flags | qt.QtCore.Qt.WindowStaysOnTopHint)  # set always on top flag, makes window disappear
        #self.setWindowFlags(flags) # clear always on top flag, makes window disappear
        #super(MainWindow, self).showMaximized()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Connect a function to execute when the window is shown
    ## @param function Function to connect
    def set_onShow(self, function) :
        self.s_show_sig.connect(function)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Connect a function to execute when the window is hidden
    ## @param function Function to connect
    def set_onHide(self, function) :
        self.s_hide_sig.connect(function)
