# coding: latin-1


import weakref

import widgets
import qt


# ==================================================================================================================================
class ConfigEntrepriseWnd(widgets.Dialog) :
    s_confirm_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, database) :
        super(ConfigEntrepriseWnd, self).__init__(parent, "Config. Entreprise", True)

        self.m_database= weakref.ref(database)
        self.m_modified= False

        mainLayout= self.setWidget( widgets.VLayout() )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("Nom") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_nom= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("Addresse") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_adresse1= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("CP, Ville") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_adresse2= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        mainLayout.addSpacing(8)

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("Capital") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_capital= hLayout.addWidget( widgets.FloatEdit(onChange= self._valueChange) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("Siren") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_siren= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("Siret") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_siret= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("RCS numero") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_numero_rcs= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("RCS ville") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_ville_rcs= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("TVA intra") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_numero_tva= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        mainLayout.addSpacing(8)

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("Banque") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_banque= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("IBAN") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_iban= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("BIC/SWIFT") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_bicswift= hLayout.addWidget( widgets.TextEdit(onChange= self._valueChange) )

        self.setMinimumWidth(400)
        self.adjustSize()
        self.setFixedHeight(self.height())

        self.set_onShow(self._showCB)
        self.set_onHide(self._hideCB)

    # ------------------------------------------------------------------------------------------------------------------------------
    def _showCB(self) :
        self.m_modified= False

        entreprise= self.m_database().entreprise()
        self.m_nom.setValue(entreprise.getParam("nom"))
        self.m_adresse1.setValue(entreprise.getParam("adresse1"))
        self.m_adresse2.setValue(entreprise.getParam("adresse2"))
        self.m_capital.setValue(entreprise.getParam("capital"))
        self.m_siren.setValue(entreprise.getParam("siren"))
        self.m_siret.setValue(entreprise.getParam("siret"))
        self.m_numero_rcs.setValue(entreprise.getParam("numero_rcs"))
        self.m_ville_rcs.setValue(entreprise.getParam("ville_rcs"))
        self.m_numero_tva.setValue(entreprise.getParam("numero_tva"))
        self.m_banque.setValue(entreprise.getParam("banque"))
        self.m_iban.setValue(entreprise.getParam("iban"))
        self.m_bicswift.setValue(entreprise.getParam("bicswift"))

    # ------------------------------------------------------------------------------------------------------------------------------
    def _hideCB(self) :
        if self.m_modified :
            entreprise= self.m_database().entreprise()
            entreprise.setParam("nom", self.m_nom.value())
            entreprise.setParam("adresse1", self.m_adresse1.value())
            entreprise.setParam("adresse2", self.m_adresse2.value())
            entreprise.setParam("capital", self.m_capital.value())
            entreprise.setParam("siren", self.m_siren.value())
            entreprise.setParam("siret", self.m_siret.value())
            entreprise.setParam("numero_rcs", self.m_numero_rcs.value())
            entreprise.setParam("ville_rcs", self.m_ville_rcs.value())
            entreprise.setParam("numero_tva", self.m_numero_tva.value())
            entreprise.setParam("banque", self.m_banque.value())
            entreprise.setParam("iban", self.m_iban.value())
            entreprise.setParam("bicswift", self.m_bicswift.value())

            self.s_confirm_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _valueChange(self) :
        self.m_modified= True

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onConfirm(self, function) :
        self.s_confirm_sig.connect(function)
