import datetime

import qt


# ==================================================================================================================================
## Create an editable line of text
class DateEdit(qt.QtWidgets.QDateEdit) :
    # ------------------------------------------------------------------------------------------------------------------------------
    ## Constructor
    ## @param value Value of the text (@a string)
    ## @param onChange Function to execute when the value of the text is changed (by the user)
    def __init__(self, value= None, onChange= None) :
        super(DateEdit, self).__init__(value)

        self.setSizePolicy(qt.EXPANDING, qt.PREFERRED)
        self.setDisplayFormat("dd/MM/yy")
        #self.setDisplayFormat("yy/MM/dd")

        self.m_value_old= value

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

        return qt.QtWidgets.QDateEdit.eventFilter(self, source, event)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set whether the text is editable
    ## @param state Editable state of the text (@a bool)
    def setEditable(self, state) :
        self.setReadOnly(not state)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Get the value of the text
    ## @return Value (@a string)
    def value(self) :
        return datetime.date(self.date().year(), self.date().month(), self.date().day())

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the value of the text
    ## @param value New value (@a string)
    def setValue(self, value, emit= False) :
        if not value :
            value= None

        self.blockSignals(True)
        self.setDate(value)
        self.blockSignals(False)

        self.m_value_old= value

        if emit :
            self.editingFinished.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onChange(self, function) :
        self.editingFinished.connect(function)
