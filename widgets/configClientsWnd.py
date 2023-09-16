# coding: latin-1


import weakref

import widgets
import qt


# ==================================================================================================================================
class NewClientWnd(widgets.Dialog) :
    s_confirm_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, database) :
        super(NewClientWnd, self).__init__(parent, "Nouveau Client", True)

        self.m_database= weakref.ref(database)

        mainLayout= self.setWidget( widgets.VLayout() )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("Nom") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_nom= hLayout.addWidget( widgets.TextEdit() )

        mainLayout.addSpacing(8)

        self.m_ok= mainLayout.addWidget( widgets.Button("OK", onClick= self.confirm) )

        self.setMinimumWidth(250)
        self.adjustSize()
        self.setFixedHeight(self.height())

        self.set_onShow(self._showCB)

    # ------------------------------------------------------------------------------------------------------------------------------
    def _showCB(self) :
        self.m_nom.setValue("")

    # ------------------------------------------------------------------------------------------------------------------------------
    def confirm(self) :
        self.close()

        self.m_database().addClient(self.m_nom.value())

        self.s_confirm_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onConfirm(self, function) :
        self.s_confirm_sig.connect(function)


# ==================================================================================================================================
class ConfigClientsWnd(widgets.Dialog) :
    s_confirm_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, database) :
        super(ConfigClientsWnd, self).__init__(parent, "Config. Clients", True)

        self.m_database= weakref.ref(database)
        self.m_modified= False

        self.m_newClientWnd= NewClientWnd(self, database)
        self.m_newClientWnd.set_onConfirm(self._clientChangeCB)

        mainLayout= self.setWidget( widgets.VLayout() )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("Nom") )
        label.setFixedWidth(40)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_clientSelect= hLayout.addWidget( widgets.ComboBox(onChange= self.load) )
        self.m_clientSelect.setFixedWidth(90)
        hLayout.addSpacing(4)
        self.m_clientAdd= hLayout.addWidget( widgets.Button("+", onClick= self.m_newClientWnd.show) )
        self.m_clientAdd.setFixedWidth(32)
        hLayout.addSpacing(4)
        self.m_clientDelete= hLayout.addWidget( widgets.Button("X", onClick= self._clientDeleteCB) )
        self.m_clientDelete.setFixedWidth(32)

        mainLayout.addSpacing(8)

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("Addresse") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_adresse1= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChangeCB) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("CP, Ville") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_adresse2= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChangeCB) )

        self.setMinimumWidth(400)
        self.adjustSize()
        self.setFixedHeight(self.height())

        self.set_onShow(self._showCB)
        self.set_onHide(self._hideCB)

    # ------------------------------------------------------------------------------------------------------------------------------
    def _showCB(self) :
        self.m_modified= False

        self.m_clientSelect.clear()
        for y in self.m_database().clients() :
            self.m_clientSelect.addValue(y)

        self.load()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _hideCB(self) :
        if self.m_modified :
            self.s_confirm_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _clientChangeCB(self) :
        self.m_modified= True

        self.m_clientSelect.clear()
        for y in self.m_database().clients() :
            self.m_clientSelect.addValue(y)

        self.m_clientSelect.setValueIndex(self.m_clientSelect.valueCount()-1)

        self.load()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _clientDeleteCB(self) :
        if widgets.prompt("Etes vous sur ?") == "Ok" :
            if self.m_database().removeClient(self.m_clientSelect.value()) :
                self._clientChangeCB()
            else :
                widgets.prompt("Echec", text= "Impossible de supprimer le client, il est probablement référencé dans les créances...", options= ["Ok"])

    # ------------------------------------------------------------------------------------------------------------------------------
    def _valueChangeCB(self) :
        self.m_modified= True

        client= self.m_database().client(self.m_clientSelect.value())
        if client :
            client.setParam("adresse1", self.m_adresse1.value())
            client.setParam("adresse2", self.m_adresse2.value())

    # ------------------------------------------------------------------------------------------------------------------------------
    def load(self) :
        client= self.m_database().client(self.m_clientSelect.value())
        if client :
            self.m_adresse1.setValue(client.getParam("adresse1"))
            self.m_adresse2.setValue(client.getParam("adresse2"))
        else :
            self.m_adresse1.setValue("")
            self.m_adresse2.setValue("")

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onConfirm(self, function) :
        self.s_confirm_sig.connect(function)
