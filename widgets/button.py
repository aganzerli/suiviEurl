import qt


# ==================================================================================================================================
## Create a button
class Button(qt.QtWidgets.QPushButton) :
    # ------------------------------------------------------------------------------------------------------------------------------
    ## Constructor
    ## @param label Button label (@a string)
    ## @param checkable Specifies if the button should be checkable or not (@a bool)
    ## @param checked Specifies if the button should be checked or not (@a bool)
    ## @param group Button group owning this button (\ref ButtonGroup)
    ## @param onClick Function to execute when the button is clicked
    def __init__(self, label, width= None, checkable= False, checked= False, group= None, onClick= None) :
        super(Button, self).__init__(label, default= False, autoDefault= False)

        self.setSizePolicy(qt.MINIMUMEXPANDING, qt.PREFERRED)
        #self.setFixedHeight(26)

        if width :
            self.setFixedWidth(width)

        if checkable :
            self.setCheckable(True)
            self.setChecked(checked)

        if group :
            group.addButton(self)

        if onClick :
            self.set_onClick(onClick)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the checked state of the button
    ## @param state Checked state
    def setChecked(self, state) :
        self.blockSignals(True)
        super(Button, self).setChecked(state)
        self.blockSignals(False)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Connect a function to execute when the button is clicked
    ## @param function Function to connect
    def set_onClick(self, function) :
        self.clicked.connect(function)
