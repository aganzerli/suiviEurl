import qt


# ==================================================================================================================================
## Create a combo box
class ComboBox(qt.QtWidgets.QComboBox) :
    # ------------------------------------------------------------------------------------------------------------------------------
    ## Constructor
    ## @param onChange Function to execute when the value of the combo box is changed (by the user)
    def __init__(self, onChange= None) :
        super(ComboBox, self).__init__()

        self.setSizePolicy(qt.EXPANDING, qt.PREFERRED)
        self.setMaxVisibleItems(40)

        self.m_valueIndex_old= None

        self.installEventFilter(self)

        if onChange :
            self.set_onChange(onChange)

    # ------------------------------------------------------------------------------------------------------------------------------
    def eventFilter(self, source, event) :
        if event.type() == qt.QtCore.QEvent.KeyPress :
            if self.isEnabled() == True :
                if event.key() == qt.QtCore.Qt.Key_Escape :
                    if self.m_valueIndex_old is not None :
                        self.setValueIndex(self.m_valueIndex_old)
                    self.currentIndexChanged.emit(self.currentIndex())

        return qt.QtWidgets.QComboBox.eventFilter(self, source, event)

    # ------------------------------------------------------------------------------------------------------------------------------
    def wheelEvent(self, event) :
        event.ignore()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set whether the combo box is editable
    ## @param state Editable state of the combo box (@a bool)
    def setEditable(self, state) :
        self.setEnabled(state)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Clear the combo box
    def clear(self) :
        self.blockSignals(True)
        super(ComboBox, self).clear()
        self.blockSignals(False)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Add a text value to the combo box
    ## @param value Value to be added (@a string)
    def addValue(self, value, icon= None, enabled= True) :
        if isinstance(icon, str) :
            icon= qt.QtGui.QIcon(nut.expandEnv(icon))
        if not isinstance(icon, qt.QtGui.QIcon) :
            icon= None

        result= self.count()

        self.blockSignals(True)
        if icon is not None :
            self.addItem(icon, str(value))
        else :
            self.addItem(str(value))
        self.blockSignals(False)

        if not enabled :
            self.model().item(result).setEnabled(False)

        return result

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the value index of the combo box
    ## @param valueIndex New value index (@a int)
    def setValueIndex(self, valueIndex) :
        self.blockSignals(True)
        self.setCurrentIndex(valueIndex)
        self.blockSignals(False)

        self.m_valueIndex_old= valueIndex

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the text value of the combo box
    ## @param value New value (@a string)
    def setValue(self, value, emit= False) :
        value= str(value)
        for i in range(0, self.count()) :
            if self.itemText(i) == value :
                self.setValueIndex(i)
                break

        if emit :
            self.currentIndexChanged.emit(self.currentIndex())

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Get the number of values in the combo box
    ## @return Number of values (@a int)
    def valueCount(self) :
        return self.count()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Get the value index of the combo box
    ## @return Value index (@a string)
    def valueIndex(self) :
        return self.currentIndex()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Get the text value of the combo box
    ## @return Value (@a string)
    def value(self) :
        return self.currentText()

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onChange(self, function) :
        self.currentIndexChanged.connect(function)
