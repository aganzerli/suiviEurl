import qt


# ==================================================================================================================================
## Create a label
class Label(qt.QtWidgets.QLabel) :
    # ------------------------------------------------------------------------------------------------------------------------------
    ## Constructor
    ## @param value Value (text) of the label (@a string)
    def __init__(self, value= "") :
        super(Label, self).__init__(value)
        self.setSizePolicy(qt.MINIMUMEXPANDING, qt.PREFERRED)
        #self.setStyleSheet("background-color: transparent;")

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Get the value of the label
    ## @return Value (@a string)
    def value(self) :
        return self.text()

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the value of the label
    ## @param value New value (@a string)
    def setValue(self, value) :
        self.blockSignals(True)
        if not value : value= ""
        self.setText(str(value))
        self.blockSignals(False)
