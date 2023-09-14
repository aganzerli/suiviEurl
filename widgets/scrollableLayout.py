import qt

from .layout import HLayout, VLayout


# ==================================================================================================================================
## Create a vertical scrollable layout
class VScrollableLayout(qt.QtWidgets.QScrollArea) :
    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self) :
        super(VScrollableLayout, self).__init__()
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(qt.QtCore.Qt.ScrollBarAlwaysOff)

        self._m_layout= VLayout()
        self.setWidget(self._m_layout)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Clear this layout
    def clear(self) : self._m_layout.clear()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a widget to this layout
    ## @param widget Widget (@a QWidget)
    def addWidget(self, widget) :
        self._m_layout.addWidget(widget)

        return widget

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a spacing to this layout
    ## @param spacing Spacing (@a int)
    def addSpacing(self, spacing) : self._m_layout.addSpacing(spacing)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a stretchable region to this layout
    def addStretch(self) : self._m_layout.addStretch()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a separator to this layout
    def addSeparator(self) : self._m_layout.addSeparator()
