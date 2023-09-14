# coding: latin-1


import weakref

import qt
import datetime
import math

import database as db
import widgets
import utils


VERSION= "0.7"


# ==================================================================================================================================
class NewYearWnd(widgets.Dialog) :
    s_confirm_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, database) :
        super(NewYearWnd, self).__init__(parent, "Nouvelle Année", True)

        self.m_database= weakref.ref(database)

        mainLayout= self.setWidget( widgets.VLayout() )

        hLayout= mainLayout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("Année") )
        label.setFixedWidth(80)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_annee= hLayout.addWidget( widgets.IntEdit() )

        mainLayout.addSpacing(8)

        self.m_ok= mainLayout.addWidget( widgets.Button("OK", onClick= self.confirm) )

        self.setMinimumWidth(250)
        self.adjustSize()
        self.setFixedHeight(self.height())

        self.set_onShow(self._showCB)

    # ------------------------------------------------------------------------------------------------------------------------------
    def _showCB(self) :
        self.m_annee.setValue(datetime.date.today().year)

    # ------------------------------------------------------------------------------------------------------------------------------
    def confirm(self) :
        self.close()

        self.m_database().addYear(self.m_annee.value())

        self.s_confirm_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onConfirm(self, function) :
        self.s_confirm_sig.connect(function)


# ==================================================================================================================================
class SuiviEurl(widgets.MainWindow) :
    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self) :
        super(SuiviEurl, self).__init__("SuiviEurl {0}".format(VERSION))

        self.m_database= db.Database()
        self.m_modified= False

        boldFont= qt.QtGui.QFont()
        boldFont.setPointSize(12)
        boldFont.setBold(True)

        self.m_newYearWnd= NewYearWnd(self, self.m_database)
        self.m_newYearWnd.set_onConfirm(self._yearChangeCB)

        self.m_configEntrepriseWnd= widgets.ConfigEntrepriseWnd(self, self.m_database)
        self.m_configEntrepriseWnd.set_onConfirm(self._dataChangeCB)

        self.m_configClientsWnd= widgets.ConfigClientsWnd(self, self.m_database)
        self.m_configClientsWnd.set_onConfirm(self._dataChangeCB)

        self.m_configWnd= widgets.ConfigWnd(self, self.m_database)
        self.m_configWnd.set_onConfirm(self._dataChangeCB)

        layout= self.setWidget( widgets.VLayout() )

        hLayout= layout.addWidget( widgets.HLayout() )
        label= hLayout.addWidget( widgets.Label("Année") )
        label.setFixedWidth(40)
        label.setAlignment(qt.ALIGNRIGHT|qt.ALIGNVCENTER)
        hLayout.addSpacing(8)
        self.m_yearSelect= hLayout.addWidget( widgets.ComboBox(onChange= self.load) )
        self.m_yearSelect.setFixedWidth(90)
        hLayout.addSpacing(4)
        self.m_yearAdd= hLayout.addWidget( widgets.Button("+", onClick= self.m_newYearWnd.show) )
        self.m_yearAdd.setFixedWidth(32)
        hLayout.addSpacing(4)
        self.m_yearDelete= hLayout.addWidget( widgets.Button("X", onClick= self._yearDeleteCB) )
        self.m_yearDelete.setFixedWidth(32)

        hLayout.addStretch()

        self.m_configEntreprise= hLayout.addWidget( widgets.Button("Config. Entreprise", onClick= self.m_configEntrepriseWnd.show) )
        self.m_configEntreprise.setFixedWidth(120)

        hLayout.addSpacing(8)

        self.m_configClients= hLayout.addWidget( widgets.Button("Config. Clients", onClick= self.m_configClientsWnd.show) )
        self.m_configClients.setFixedWidth(120)

        hLayout.addSpacing(8)

        self.m_config= hLayout.addWidget( widgets.Button("Config.", onClick= self.m_configWnd.show) )
        self.m_config.setFixedWidth(120)

        layout.addSpacing(8)

        layout= layout.addWidget( widgets.VLayout() )

        hLayout= layout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        self.m_resumeLabel= hLayout.addWidget( widgets.Label() )
        self.m_resumeLabel.setFont(boldFont)
        self.m_resumeLabel.setStyleSheet("background-color: #C0C0C0")

        self.m_resumeTable= layout.addWidget( widgets.ResumeTable(self.m_database) )

        layout.addSpacing(8)

        self.m_tabs= layout.addWidget( qt.QtWidgets.QTabWidget() )


        vLayout= widgets.VLayout()
        self.m_tabs.addTab(vLayout,"Créances")

        hLayout= vLayout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("Créances") )
        label.setFont(boldFont)
        label.setStyleSheet("background-color: #C0C0C0")

        button= hLayout.addWidget( widgets.Button("+", onClick= self._addCreancesCB) )
        button.setFixedWidth(32)

        self.m_creancesTable= vLayout.addWidget( widgets.CreancesTable(self.m_database, onChange= self._dataChangeCB) )


        vLayout= widgets.VLayout()
        self.m_tabs.addTab(vLayout,"Salaires")

        hLayout= vLayout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("Salaires") )
        label.setFont(boldFont)
        label.setStyleSheet("background-color: #C0C0C0")

        button= hLayout.addWidget( widgets.Button("+", onClick= self._addSalairesCB) )
        button.setFixedWidth(32)

        self.m_salairesTable= vLayout.addWidget( widgets.SalairesTable(self.m_database, onChange= self._dataChangeCB) )


        vLayout= widgets.VLayout()
        self.m_tabs.addTab(vLayout,"Dettes")

        hLayout= vLayout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("Dettes") )
        label.setFont(boldFont)
        label.setStyleSheet("background-color: #C0C0C0")

        button= hLayout.addWidget( widgets.Button("+", onClick= self._addDettesCB) )
        button.setFixedWidth(32)

        self.m_dettesTable= vLayout.addWidget( widgets.DettesTable(self.m_database, onChange= self._dataChangeCB) )


        vLayout= widgets.VLayout()
        self.m_tabs.addTab(vLayout,"Frais Fixes")

        hLayout= vLayout.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("Frais Fixes") )
        label.setFont(boldFont)
        label.setStyleSheet("background-color: #C0C0C0")

        button= hLayout.addWidget( widgets.Button("+", onClick= self._addFraisFixesCB) )
        button.setFixedWidth(32)

        self.m_fraisFixesTable= vLayout.addWidget( widgets.FraisFixesTable(self.m_database, onChange= self._dataChangeCB) )


        self.m_cotisationsFrame= widgets.CotisationsFrame(self.m_database, onChange= self._dataChangeCB)
        self.m_tabs.addTab(self.m_cotisationsFrame,"Cotisations")


        self.setMinimumWidth(1280)
        self.setMinimumHeight(840)

        self.m_save= qt.QtWidgets.QShortcut(qt.QtGui.QKeySequence(qt.QtCore.Qt.ControlModifier+qt.QtCore.Qt.Key_S), self)
        self.m_save.activated.connect(self.saveDatabase)

        '''self.m_updateTimer= qt.QtCore.QTimer(self)
        self.m_updateTimer.setInterval(60*1000) # 1m timer
        self.m_updateTimer.setSingleShot(False)
        self.m_updateTimer.timeout.connect(self.saveDatabase)
        self.m_updateTimer.start()'''

    # ------------------------------------------------------------------------------------------------------------------------------
    def showEvent(self, event) :
        super(SuiviEurl, self).showEvent(event)

        if not event.spontaneous() :
            self.m_database.load()

            self.m_yearSelect.clear()
            for y in self.m_database.years() :
                self.m_yearSelect.addValue(y)

            self.m_yearSelect.setValueIndex(self.m_yearSelect.valueCount()-1)

            self.load()

    # ------------------------------------------------------------------------------------------------------------------------------
    def closeEvent(self, event) :
        if self.m_modified :
            res= widgets.prompt("Enregistrer les modifications ?", options= ["Oui", "Non", "Annuler"])
            if res == "Oui" :
                self.saveDatabase()
                canExit= True
            elif res == "Non" :
                if widgets.prompt("Etes vous sur ?") == "Ok" :
                    canExit= True
                else :
                    canExit= False
            else :
                canExit= False
        else :
            canExit= True

        if canExit :
            event.accept()
        else:
            event.ignore()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _dataChangeCB(self) :
        self.setModified(True)

        self.load()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _yearChangeCB(self) :
        self.m_yearSelect.clear()
        for y in self.m_database.years() :
            self.m_yearSelect.addValue(y)

        self.m_yearSelect.setValueIndex(self.m_yearSelect.valueCount()-1)

        self._dataChangeCB()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _yearDeleteCB(self) :
        if widgets.prompt("Etes vous sur ?") == "Ok" :
            self.m_database.removeYear(self.m_yearSelect.value())

            self._yearChangeCB()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _addCreancesCB(self) :
        annee= self.m_database.year(self.m_yearSelect.value())
        if annee :
            annee.addItem("creances")

        self._dataChangeCB()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _addSalairesCB(self) :
        annee= self.m_database.year(self.m_yearSelect.value())
        if annee :
            annee.addItem("salaires")

        self._dataChangeCB()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _addDettesCB(self) :
        annee= self.m_database.year(self.m_yearSelect.value())
        if annee :
            annee.addItem("dettes")

        self._dataChangeCB()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _addFraisFixesCB(self) :
        annee= self.m_database.year(self.m_yearSelect.value())
        if annee :
            annee.addItem("fraisFixes")

        self._dataChangeCB()

    # ------------------------------------------------------------------------------------------------------------------------------
    def load(self) :
        self.m_database.compute()

        year= self.m_yearSelect.value()
        if not year :
            year= 0

        self.m_resumeLabel.setValue("Résumé {0}".format(year))

        self.m_resumeTable.load(year)
        self.m_creancesTable.load(year)
        self.m_salairesTable.load(year)
        self.m_dettesTable.load(year)
        self.m_fraisFixesTable.load(year)
        self.m_cotisationsFrame.load(year)

    # ------------------------------------------------------------------------------------------------------------------------------
    def setModified(self, state) :
        self.m_modified= state
        if self.m_modified :
            self.setWindowTitle("SuiviEurl {0} *".format(VERSION))
        else :
            self.setWindowTitle("SuiviEurl {0}".format(VERSION))

    # ------------------------------------------------------------------------------------------------------------------------------
    def saveDatabase(self) :
        if self.m_modified :
            self.m_database.save()

            self.setModified(False)


# ----------------------------------------------------------------------------------------------------------------------------------
def main() :
    app= qt.QtWidgets.QApplication([])
    #app.setStyle("Fusion")

    mainWnd= SuiviEurl()
    qt.setApplicationWindow(mainWnd)

    mainWnd.show()

    app.exec_()


# ----------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__" :
    main()
