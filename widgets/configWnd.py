# coding: latin-1


import weakref

import widgets
import qt


# ==================================================================================================================================
class ConfigWnd(widgets.Dialog) :
    s_confirm_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, database) :
        super(ConfigWnd, self).__init__(parent, "Config.", True)

        self.m_database= weakref.ref(database)
        self.m_modified= False

        mainLayout= self.setWidget( widgets.VLayout() )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("Intitulé par défaut") )
        label.setFixedWidth(100)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_intitule_default= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("Objet par défaut") )
        label.setFixedWidth(100)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_objet_default= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("N° facture auto") )
        label.setFixedWidth(100)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_factureno_auto= hLayout.addWidget( widgets.CheckBox(onClick= self._valueChange) )

        self.setMinimumWidth(400)
        self.adjustSize()
        self.setFixedHeight(self.height())

        self.set_onShow(self._showCB)
        self.set_onHide(self._hideCB)

    # ------------------------------------------------------------------------------------------------------------------------------
    def _showCB(self) :
        self.m_modified= False

        self.m_intitule_default.setValue(self.m_database().getParam("intitule_default"))
        self.m_objet_default.setValue(self.m_database().getParam("objet_default"))
        self.m_factureno_auto.setChecked(self.m_database().getParam("factureno_auto"))

    # ------------------------------------------------------------------------------------------------------------------------------
    def _hideCB(self) :
        if self.m_modified :
            self.m_database().setParam("intitule_default", self.m_intitule_default.value())
            self.m_database().setParam("objet_default", self.m_objet_default.value())
            self.m_database().setParam("factureno_auto", self.m_factureno_auto.isChecked())

            self.s_confirm_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _valueChange(self) :
        self.m_modified= True

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onConfirm(self, function) :
        self.s_confirm_sig.connect(function)
