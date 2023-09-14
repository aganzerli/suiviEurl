import qt


# ==================================================================================================================================
## Create a dialog
class Dialog(qt.QtWidgets.QDialog) :
    s_show_sig= qt.QtCore.pyqtSignal()
    s_hide_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Constructor
    ## @param parent Parent widget (@a QWidget)
    ## @param title Dialog title (@a string)
    ## @param isModal True to create a modal dialog (blocking the rest of the application), False to create a non modal dialog (@a bool)
    def __init__(self, parent, title, isModal= False) :
        #if not parent :
        #    parent= qt.applicationWindow()

        super(Dialog, self).__init__(parent)

        qt.applyStyleSheet(self)

        self.setWindowTitle(title)
        #self.setWindowIcon(qt.QtGui.QIcon(nut.expandEnv("%NOID_PATH%/image/logoColor.png")))
        self.setContentsMargins(8, 8, 8, 8)

        self.setModal(isModal)

        self.m_firstShow= True

    # ------------------------------------------------------------------------------------------------------------------------------
    def showEvent(self, event) :
        super(Dialog, self).showEvent(event)

        if not event.spontaneous() :
            desktop= qt.QtWidgets.QApplication.desktop()
            cursorPos= qt.QtGui.QCursor.pos()
            screen= desktop.screenNumber(cursorPos)
            centerPoint= desktop.screenGeometry(screen).center()
            frameGm= self.frameGeometry()
            frameGm.moveCenter(centerPoint)
            self.move(frameGm.topLeft())

            self.s_show_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def closeEvent(self, event) :
        super(Dialog, self).closeEvent(event)
        event.accept()

        self.s_hide_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the widget for this windpw
    ## @param widget Widget (@a QWidget)
    def setWidget(self, widget) :
        self.setLayout(widget.layout())

        return widget

    # ------------------------------------------------------------------------------------------------------------------------------
    def show(self) :
        super(Dialog, self).show()

        if self.m_firstShow :
            self.m_firstShow= False
            x= (qt.QtWidgets.QDesktopWidget().availableGeometry().width()-self.width())>>1
            y= (qt.QtWidgets.QDesktopWidget().availableGeometry().height()-self.height())>>1
            self.move(x, y)

        self.activateWindow()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Connect a function to execute when the window is shown
    ## @param function Function to connect
    def set_onShow(self, function) : self.s_show_sig.connect(function)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Connect a function to execute when the window is hidden
    ## @param function Function to connect
    def set_onHide(self, function) : self.s_hide_sig.connect(function)
