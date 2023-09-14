import qt


# ==================================================================================================================================
## Create an editable line of text
class TextEdit(qt.QtWidgets.QLineEdit) :
    s_change_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Constructor
    ## @param value Value of the text (@a string)
    ## @param onChange Function to execute when the value of the text is changed (by the user)
    def __init__(self, value= "", onChange= None) :
        super(TextEdit, self).__init__(value)

        self.setSizePolicy(qt.EXPANDING, qt.PREFERRED)

        self.m_value_old= value
        self.m_modified= False

        self.textChanged.connect(self._textChangedCB)
        self.editingFinished.connect(self._editingFinishedCB)
        self.installEventFilter(self)

        if onChange :
            self.set_onChange(onChange)

    # ------------------------------------------------------------------------------------------------------------------------------
    def eventFilter(self, source, event) :
        if event.type() == qt.QtCore.QEvent.KeyPress :
            if self.isReadOnly() == False :
                if event.key() == qt.QtCore.Qt.Key_Escape :
                    self.setValue(self.m_value_old)
                    self.clearFocus()

        return qt.QtWidgets.QLineEdit.eventFilter(self, source, event)

    # ------------------------------------------------------------------------------------------------------------------------------
    def _textChangedCB(self) :
        self.m_modified= True

    # ------------------------------------------------------------------------------------------------------------------------------
    def _editingFinishedCB(self) :
        if self.m_modified :
            self.m_modified= False
            self.s_change_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set whether the text is editable
    ## @param state Editable state of the text (@a bool)
    def setEditable(self, state) :
        self.setReadOnly(not state)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Get the value of the text
    ## @return Value (@a string)
    def value(self) :
        return self.text()

    # ------------------------------------------------------------------------------------------------------------------------------
    def setValue(self, value, emit= False) :
        if value is not None :
            value= str(value)
        else :
            value= ""

        self.blockSignals(True)
        self.setText(value)
        self.blockSignals(False)

        self.m_value_old= value
        self.m_modified= False

        if emit :
            self.s_change_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onChange(self, function) :
        self.s_change_sig.connect(function)


# ==================================================================================================================================
## Create an editable line of text
class IntEdit(TextEdit) :
    # ------------------------------------------------------------------------------------------------------------------------------
    ## Constructor
    ## @param value Value of the text (@a string)
    ## @param onChange Function to execute when the value of the text is changed (by the user)
    def __init__(self, value= 0.0, onChange= None) :
        super(IntEdit, self).__init__(str(value), onChange= onChange)

        self.setValidator(qt.QtGui.QIntValidator())

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Get the value of the text
    ## @return Value (@a string)
    def value(self) :
        return int(super(IntEdit, self).value())


# ==================================================================================================================================
## Create an editable line of text
class FloatEdit(TextEdit) :
    # ------------------------------------------------------------------------------------------------------------------------------
    ## Constructor
    ## @param value Value of the text (@a string)
    ## @param onChange Function to execute when the value of the text is changed (by the user)
    def __init__(self, value= 0.0, onChange= None) :
        super(FloatEdit, self).__init__(str(value), onChange= onChange)

        validator= qt.QtGui.QDoubleValidator()
        locale= qt.QtCore.QLocale(qt.QtCore.QLocale.English, qt.QtCore.QLocale.UnitedStates)
        validator.setLocale(locale)
        validator.setNotation(qt.QtGui.QDoubleValidator.StandardNotation)
        self.setValidator(validator)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Get the value of the text
    ## @return Value (@a string)
    def value(self) :
        v= super(FloatEdit, self).value()
        v= float(v) if v else 0.0

        return v
