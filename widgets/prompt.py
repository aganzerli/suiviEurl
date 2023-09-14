import qt

from .button    import Button
from .dialog    import Dialog
from .layout    import HLayout, VLayout
from .label     import Label


# ==================================================================================================================================
## Create a prompt message box with 'Ok' and 'Cancel' buttons
class Prompt(Dialog) :
    # ------------------------------------------------------------------------------------------------------------------------------
    ## Constructor
    ## @param title Message box title (@a string)
    ## @param text Message box text (@a string)
    def __init__(self, title, text= None, options= ["Ok", "Cancel"]) :
        super(Prompt, self).__init__(qt.applicationWindow(), title, True)

        if not text :
            text= title

        self.setContentsMargins(16, 16, 16, 16)

        mainLayout= self.setWidget( VLayout() )

        mainLayout.addWidget( Label(text) )

        mainLayout.addSpacing(16)

        buttonLayout= mainLayout.addWidget( HLayout() )
        for o in options :
            buttonLayout.addWidget( Button(o, onClick= self._buttonCB) )

        self.setMinimumWidth(300)

        self.adjustSize()
        self.setFixedSize(self.size())

        self.set_onShow(self._showCB)

    # ------------------------------------------------------------------------------------------------------------------------------
    def _showCB(self) :
        self.m_result= None

    # ------------------------------------------------------------------------------------------------------------------------------
    def _buttonCB(self) :
        self.m_result= self.sender().text()
        self.accept()

    # ------------------------------------------------------------------------------------------------------------------------------
    def result(self) : return self.m_result


# ----------------------------------------------------------------------------------------------------------------------------------
## Pop a prompt message box
## @param title Message box title (@a string)
## @param text Message box text (@a string)
## @return True if 'Ok' was clicked, false otherwise (@a bool)
def prompt(title, text= None, options= ["Ok", "Cancel"]) :
    wnd= Prompt(title, text, options)
    wnd.exec_()

    return wnd.result()
