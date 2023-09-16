import qt


# ==================================================================================================================================
## Create a checkbox
class CheckBox(qt.QtWidgets.QCheckBox) :
    # ------------------------------------------------------------------------------------------------------------------------------
    ## Constructor
    ## @param text checkbox text (@a string)
    ## @param onClick Function to execute when the checkbox is clicked
    def __init__(self, text= "", onClick= None, isChecked= False, group= None) :
        super(CheckBox, self).__init__(text)

        self.setSizePolicy(qt.EXPANDING, qt.PREFERRED)

        if group : group.addButton(self)
        if isChecked : self.setChecked(True)
        if onClick : self.set_onClick(onClick)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Set the checked state of the checkbox
    ## @param state Checked state
    def setChecked(self, state) :
        self.blockSignals(True)
        super(CheckBox, self).setChecked(state)
        self.blockSignals(False)

    # ------------------------------------------------------------------------------------------------------------------------------
    ## Connect a function to execute when the checkbox is clicked
    ## @param onClick Function to connect
    def set_onClick(self, onClick) :
        self.stateChanged.connect(onClick)
