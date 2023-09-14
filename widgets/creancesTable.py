# coding: latin-1


import weakref

import qt
import database as db

import widgets
from .table import Table
import invoice
import utils


# ==================================================================================================================================
class Delegate(qt.QtWidgets.QItemDelegate):
    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent) :
        super(Delegate, self).__init__(parent)

    # ------------------------------------------------------------------------------------------------------------------------------
    def createEditor(self, parent, option, index) :
        value= index.data(qt.QtCore.Qt.EditRole)
        slotLambda= lambda : self.parent()._changeCB(index)

        widget= None

        if index.column() == 1 : # Client
            widget= widgets.ComboBox(onChange= slotLambda)
            widget.addValue("")
            for i in self.parent().m_database().clients() :
                widget.addValue(i)
            widget.setValue(value)
        elif index.column() == 2 : # Intitule
            widget= widgets.TextEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 3 : # Objet
            widget= widgets.TextEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 4 : # Montant HT
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 5 : # Montant TTC
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 6 : # TVA (%)
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 7 : # N° facture
            widget= widgets.TextEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 8 : # Date d'envoi
            if value is not None:
                widget= widgets.DateEdit(onChange= slotLambda)
                widget.setValue(value)
        elif index.column() == 9 : # Délai paiement
            widget= widgets.ComboBox(onChange= slotLambda)
            for i in db.DELAI_STR :
                widget.addValue(i)
            widget.setValueIndex(value)
        elif index.column() == 11 : # Statut
            widget= widgets.ComboBox(onChange= slotLambda)
            for i in db.STATUT_STR :
                widget.addValue(i)
            widget.setValueIndex(value)
        elif index.column() == 12 : # Date paiement
            if value is not None:
                widget= widgets.DateEdit(onChange= slotLambda)
                widget.setValue(value)
        elif index.column() == 13 : # Modalités paiement
            if value is not None:
                widget= widgets.TextEdit(onChange= slotLambda)
                widget.setValue(value)
        elif index.column() == 14 :
            widget= widgets.Button("F", onClick= slotLambda)
        elif index.column() == 15 :
            widget= widgets.Button("X", onClick= slotLambda)

        if widget :
            self.parent().setIndexWidget(index, widget)

            widget.setStyleSheet("margin: 2px 2px;")
            widget.setFocus()


# ==================================================================================================================================
class CreancesTable(Table) :
    s_change_sig= qt.QtCore.pyqtSignal()
    s_red= None
    s_green= None

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, database, onChange= None) :
        super(CreancesTable, self).__init__([
            "Mois", # 0
            "Client", # 1
            "Intitulé", # 2
            "Objet", # 3
            "Montant HT", # 4
            "Montant TTC", # 5
            "TVA (%)", # 6
            "N° facture", # 7
            "Date d'envoi", # 8
            "Délai paiement", # 9
            "Echéance", # 10
            "Statut", # 11
            "Date paiement", # 12
            "Modalités", # 13
            "",
            ""
            ],
            showToolTip= False)

        if not CreancesTable.s_red :
            CreancesTable.s_red= qt.QtGui.QColor(255, 128, 128)

        if not CreancesTable.s_green :
            CreancesTable.s_green= qt.QtGui.QColor(128, 255, 128)

        self.m_database= weakref.ref(database)
        self.m_year= 0
        self.m_rows= []

        self.setWidth(0, 90)
        self.setWidth(1, 90)
        self.setWidth(4, 90)
        self.setWidth(5, 90)
        self.setWidth(6, 60)
        self.setWidth(7, 90)
        self.setWidth(8, 90)
        self.setWidth(9, 90)
        self.setWidth(10, 90)
        self.setWidth(11, 90)
        self.setWidth(12, 90)
        self.setWidth(14, 32)
        self.setWidth(15, 32)

        self.setRowHeight(24)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(qt.QtWidgets.QAbstractItemView.NoSelection)

        self.setItemDelegateForColumn(1, Delegate(self))
        self.setItemDelegateForColumn(2, Delegate(self))
        self.setItemDelegateForColumn(3, Delegate(self))
        self.setItemDelegateForColumn(4, Delegate(self))
        self.setItemDelegateForColumn(5, Delegate(self))
        self.setItemDelegateForColumn(6, Delegate(self))
        self.setItemDelegateForColumn(7, Delegate(self))
        self.setItemDelegateForColumn(8, Delegate(self))
        self.setItemDelegateForColumn(9, Delegate(self))
        self.setItemDelegateForColumn(11, Delegate(self))
        self.setItemDelegateForColumn(12, Delegate(self))
        self.setItemDelegateForColumn(13, Delegate(self))
        self.setItemDelegateForColumn(14, Delegate(self))
        self.setItemDelegateForColumn(15, Delegate(self))

        if onChange :
            self.set_onChange(onChange)

    # ------------------------------------------------------------------------------------------------------------------------------
    def mousePressEvent(self, e) :
        self.closePersistentEditors()

        index= self.indexAt(qt.QtCore.QPoint(e.x(), e.y()))
        if self.itemDelegateForColumn(index.column()) :
            self.openPersistentEditor(index)

    # ------------------------------------------------------------------------------------------------------------------------------
    def data(self, columnIdx, rowIdx) :
        if columnIdx == 14 :
            return "F"
        elif columnIdx == 15 :
            return "X"
        elif columnIdx <= 13 :
            value= self.m_rows[rowIdx][columnIdx]
            if ( value is not None ) :
                if ( columnIdx == 8 ) or ( columnIdx == 10 ) or ( columnIdx == 12 ) :
                    return value.strftime("%d/%m/%y")
                elif columnIdx == 9 :
                    return db.DELAI_STR[value]
                elif columnIdx == 11 :
                    return db.STATUT_STR[value]
                else :
                    return value

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def editorData(self, columnIdx, rowIdx) :
        if columnIdx <= 13 :
            return self.m_rows[rowIdx][columnIdx]

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def bgColor(self, columnIdx, rowIdx) :
        value= self.m_rows[rowIdx][11]
        if value == db.STATUT_ENCOURS :
            return CreancesTable.s_red
        elif value == db.STATUT_PAYE :
            return CreancesTable.s_green

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def alignment(self, columnIdx, rowIdx) :
        return qt.ALIGNHCENTER|qt.ALIGNVCENTER

    # ------------------------------------------------------------------------------------------------------------------------------
    def load(self, year) :
        if not year :
            year= 0
        self.m_year= int(year)

        annee= self.m_database().year(self.m_year)
        if annee :
            creances= annee.getParam("creances")

            currentMonth= None
            rows= []
            for i in creances :
                date= i.getParam("date")
                if currentMonth != date.month :
                    currentMonth= date.month
                    monthLabel= db.MONTHS[currentMonth-1]
                else :
                    monthLabel= "-"

                rows.append([
                    monthLabel,
                    i.getParam("nom"),
                    i.getParam("intitule"),
                    i.getParam("objet"),
                    i.getParam("montant"),
                    i.getParam("montantTtc"),
                    i.getParam("tva"),
                    i.getParam("factureno"),
                    i.getParam("date"),
                    i.getParam("delai"),
                    i.getParam("echeance"),
                    i.getParam("statut"),
                    i.getParam("datePaiement"),
                    i.getParam("modalites")
                    ])
        else :
            rows= []

        self.model().beginResetModel()
        self.m_rows= rows
        self.model().endResetModel()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _changeCB(self, index) :
        annee= self.m_database().year(self.m_year)
        if annee :
            widget= self.indexWidget(index)
            if widget :
                creances= annee.getParam("creances")
                if index.row() < len(creances) :
                    creance= creances[index.row()]

                    if index.column() == 1 :
                        creance.setParam("nom", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 2 :
                        creance.setParam("intitule", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 3 :
                        creance.setParam("objet", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 4 :
                        creance.setParam("montant", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 5 :
                        creance.setParam("montantTtc", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 6 :
                        creance.setParam("tva", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 7 :
                        creance.setParam("factureno", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 8 :
                        creance.setParam("date", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 9 :
                        creance.setParam("delai", widget.valueIndex())
                        self.s_change_sig.emit()
                    elif index.column() == 11 :
                        creance.setParam("statut", widget.valueIndex())
                        self.s_change_sig.emit()
                    elif index.column() == 12 :
                        creance.setParam("datePaiement", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 13 :
                        creance.setParam("modalites", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 14 :
                        path= invoice.generate(creance, self.m_database().entreprise(), self.m_database().client(creance.getParam("nom")))
                        if path :
                            utils.browse(path)
                        '''if widgets.prompt("Etes vous sur ?") == "Ok" :
                            annee.removeItem("creances", index.row())
                            self.s_change_sig.emit()'''
                    elif index.column() == 15 :
                        if widgets.prompt("Etes vous sur ?") == "Ok" :
                            annee.removeItem("creances", index.row())
                            self.s_change_sig.emit()

        self.closePersistentEditors()

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onChange(self, function) :
        self.s_change_sig.connect(function)
