import qt


# ==================================================================================================================================
## Create a horizontal layout
class HLayout(qt.QtWidgets.QWidget) :
    s_show_sig= qt.QtCore.pyqtSignal()
    s_hide_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self) :
        super(HLayout, self).__init__()

        self._m_layout= qt.QtWidgets.QHBoxLayout()
        self.setLayout(self._m_layout)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(3)
        self.setAlignment(qt.ALIGNLEFT)

    # ------------------------------------------------------------------------------------------------------------------------------
    def eventFilter(self, source, event) :
        if ( source is self ) :
            if event.type() == qt.QtCore.QEvent.DeferredDelete :
                print("HLayout : qt.QtCore.QEvent.DeferredDelete")
        return qt.QtWidgets.QWidget.eventFilter(self, source, event)

    # ------------------------------------------------------------------------------------------------------------------------------
    def showEvent(self, event) :
        super(HLayout, self).showEvent(event)

        if not event.spontaneous() :
            self.s_show_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def hideEvent(self, event) :
        super(HLayout, self).hideEvent(event)

        self.s_hide_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the margins for this layout
    ## @param left, top, right, bottom Margins (@a int)
    def setContentsMargins(self, left, top, right, bottom) :
        self._m_layout.setContentsMargins(left, top, right, bottom)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the spacing between items for this layout
    ## @param spacing Spacing (@a int)
    def setSpacing(self, spacing) :
        self._m_layout.setSpacing(spacing)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the alignment ot items for this layout
    ## @param alignment Alignment (@ref qtav)
    def setAlignment(self, alignment) :
        self._m_layout.setAlignment(alignment)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Clear this layout
    def clear(self) :
        qt.clearLayout(self._m_layout)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a widget to this layout
    ## @param widget Widget (@a QWidget)
    def addWidget(self, widget, alignment=None) :
        if alignment is not None:
            self._m_layout.addWidget(widget, alignment)
        else:
            self._m_layout.addWidget(widget)
        return widget

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Remove a widget from this layout
    ## @param widget Widget (@a QWidget)
    def removeWidget(self, widget) :
        self._m_layout.removeWidget(widget)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a spacing to this layout
    ## @param spacing Spacing (@a int)
    def addSpacing(self, spacing) :
        self._m_layout.addSpacing(spacing)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a stretchable region to this layout
    def addStretch(self) :
        self._m_layout.addStretch()

    # ------------------------------------------------------------------------------------------------------------------------------
    def setStretch(self, index, value) :
        self._m_layout.setStretch(index, value)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a separator to this layout
    def addSeparator(self) :
        line= qt.QtWidgets.QFrame()
        line.setFrameShape(qt.QtWidgets.QFrame.VLine)
        line.setStyleSheet("background-color: #404040")
        self.addWidget(line)

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


# ==================================================================================================================================
## Create a vertical layout
class VLayout(qt.QtWidgets.QWidget) :
    s_show_sig= qt.QtCore.pyqtSignal()
    s_hide_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self) :
        super(VLayout, self).__init__()

        self._m_layout= qt.QtWidgets.QVBoxLayout()
        self.setLayout(self._m_layout)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(3)
        self.setAlignment(qt.ALIGNTOP)

    # ------------------------------------------------------------------------------------------------------------------------------
    def showEvent(self, event) :
        super(VLayout, self).showEvent(event)

        if not event.spontaneous() : self.s_show_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def hideEvent(self, event) :
        super(VLayout, self).hideEvent(event)

        self.s_hide_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the margins for this layout
    ## @param left, top, right, bottom Margins (@a int)
    def setContentsMargins(self, left, top, right, bottom) :
        self._m_layout.setContentsMargins(left, top, right, bottom)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the spacing between items for this layout
    ## @param spacing Spacing (@a int)
    def setSpacing(self, spacing) :
        self._m_layout.setSpacing(spacing)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the alignment ot items for this layout
    ## @param alignment Alignment (@ref qtav)
    def setAlignment(self, alignment) :
        self._m_layout.setAlignment(alignment)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Clear this layout
    def clear(self) :
        qt.clearLayout(self._m_layout)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a widget to this layout
    ## @param widget Widget (@a QWidget)
    def addWidget(self, widget, alignment=None) :
        if alignment is not None:
            self._m_layout.addWidget(widget, alignment)
        else:
            self._m_layout.addWidget(widget)
        return widget

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Remove a widget from this layout
    ## @param widget Widget (@a QWidget)
    def removeWidget(self, widget) :
        self._m_layout.removeWidget(widget)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a spacing to this layout
    ## @param spacing Spacing (@a int)
    def addSpacing(self, spacing) :
        self._m_layout.addSpacing(spacing)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a stretchable region to this layout
    def addStretch(self) :
        self._m_layout.addStretch()

    # ------------------------------------------------------------------------------------------------------------------------------
    def setStretch(self, index, value) :
        self._m_layout.setStretch(index, value)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a separator to this layout
    def addSeparator(self) :
        line= qt.QtWidgets.QFrame()
        line.setFrameShape(qt.QtWidgets.QFrame.VLine)
        line.setStyleSheet("background-color: #404040")
        self.addWidget(line)

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
