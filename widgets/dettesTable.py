# coding: latin-1


import weakref

import qt
import database as db

import widgets
from .table import Table


# ==================================================================================================================================
class Delegate(qt.QtWidgets.QItemDelegate):
    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent) :
        super(Delegate, self).__init__(parent)

    # ------------------------------------------------------------------------------------------------------------------------------
    def createEditor(self, parent, option, index) :
        if self.parent().indexWidget(index) :
            return

        value= index.data(qt.QtCore.Qt.EditRole)
        slotLambda= lambda : self.parent()._changeCB(index)

        widget= None
        if index.column() == 1 : # Client
            widget= widgets.TextEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 2 : # Objet
            widget= widgets.TextEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 3 : # Montant HT
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 4 : # Montant TTC
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 5 : # TVA (%)
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 6 : # N° facture
            widget= widgets.TextEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 7 : # Date d'envoi
            if value is not None:
                widget= widgets.DateEdit(onChange= slotLambda)
                widget.setValue(value)
        elif index.column() == 8 : # Délai paiement
            widget= widgets.ComboBox(onChange= slotLambda)
            for i in db.DELAI_STR :
                widget.addValue(i)
            widget.setValueIndex(value)
        elif index.column() == 10 : # Statut
            widget= widgets.ComboBox(onChange= slotLambda)
            for i in db.STATUT_STR :
                widget.addValue(i)
            widget.setValueIndex(value)
        elif index.column() == 11 : # Date paiement
            if value is not None:
                widget= widgets.DateEdit(onChange= slotLambda)
                widget.setValue(value)
        elif index.column() == 12 : # Modalités paiement
            if value is not None:
                widget= widgets.TextEdit(onChange= slotLambda)
                widget.setValue(value)
        elif index.column() == 13 :
            widget= widgets.Button("X", onClick= slotLambda)

        if widget :
            self.parent().setIndexWidget(index, widget)

            widget.setStyleSheet("margin: 2px 2px;")
            widget.setFocus()


# ==================================================================================================================================
class DettesTable(Table) :
    s_change_sig= qt.QtCore.pyqtSignal()
    s_red= None
    s_green= None

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, database, onChange= None) :
        super(DettesTable, self).__init__([
            "Mois",
            "Fournisseur",
            "Objet",
            "Montant HT",
            "Montant TTC",
            "TVA (%)",
            "N° facture",
            "Date d'envoi",
            "Délai paiement",
            "Echéance",
            "Statut",
            "Date paiement",
            "Modalités",
            ""
            ],
            showToolTip= False)

        if not DettesTable.s_red :
            DettesTable.s_red= qt.QtGui.QColor(255, 128, 128)

        if not DettesTable.s_green :
            DettesTable.s_green= qt.QtGui.QColor(128, 255, 128)

        self.m_database= weakref.ref(database)
        self.m_year= 0
        self.m_rows= []

        self.setWidth(0, 90)
        self.setWidth(3, 90)
        self.setWidth(4, 90)
        self.setWidth(5, 60)
        self.setWidth(7, 90)
        self.setWidth(8, 90)
        self.setWidth(9, 90)
        self.setWidth(10, 90)
        self.setWidth(11, 90)
        self.setWidth(13, 32)

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
        self.setItemDelegateForColumn(10, Delegate(self))
        self.setItemDelegateForColumn(11, Delegate(self))
        self.setItemDelegateForColumn(12, Delegate(self))
        self.setItemDelegateForColumn(13, Delegate(self))

        #self.setSortingEnabled(True)
        #self.setSort(9, qr.QtCore.Qt.DescendingOrder)
        #self.set_onSort(self.reload)

        #self.m_popup= JobPopup(self)

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
        if columnIdx == 13 :
            return "X"
        elif columnIdx <= 12 :
            value= self.m_rows[rowIdx][columnIdx]
            if ( value is not None ) :
                if ( columnIdx == 7 ) or ( columnIdx == 9 ) or ( columnIdx == 11 ) :
                    return value.strftime("%d/%m/%y")
                elif columnIdx == 8 :
                    return db.DELAI_STR[value]
                elif columnIdx == 10 :
                    return db.STATUT_STR[value]
                else :
                    return value

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def editorData(self, columnIdx, rowIdx) :
        if columnIdx <= 12 :
            return self.m_rows[rowIdx][columnIdx]

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def bgColor(self, columnIdx, rowIdx) :
        value= self.m_rows[rowIdx][10]
        if value == db.STATUT_ENCOURS :
            return DettesTable.s_red
        elif value == db.STATUT_PAYE :
            return DettesTable.s_green

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
            dettes= annee.getParam("dettes")

            currentMonth= None
            rows= []
            for i in dettes :
                date= i.getParam("date")
                if currentMonth != date.month :
                    currentMonth= date.month
                    monthLabel= db.MONTHS[currentMonth-1]
                else :
                    monthLabel= "-"

                rows.append([
                    monthLabel,
                    i.getParam("nom"),
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

        '''for i in range(0, self.rowCount()) :
            self.openPersistentEditor(self.model().index(i, 1))
            self.openPersistentEditor(self.model().index(i, 2))
            self.openPersistentEditor(self.model().index(i, 3))
            self.openPersistentEditor(self.model().index(i, 4))
            self.openPersistentEditor(self.model().index(i, 5))
            self.openPersistentEditor(self.model().index(i, 6))
            self.openPersistentEditor(self.model().index(i, 7))
            self.openPersistentEditor(self.model().index(i, 8))
            self.openPersistentEditor(self.model().index(i, 10))
            self.openPersistentEditor(self.model().index(i, 11))
            self.openPersistentEditor(self.model().index(i, 12))
            self.openPersistentEditor(self.model().index(i, 13))'''

        #self.vertical_resize_table_to_content()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _changeCB(self, index) :
        annee= self.m_database().year(self.m_year)
        if annee :
            widget= self.indexWidget(index)
            if widget :
                dettes= annee.getParam("dettes")
                if index.row() < len(dettes) :
                    dette= dettes[index.row()]

                    if index.column() == 1 :
                        dette.setParam("nom", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 2 :
                        dette.setParam("objet", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 3 :
                        dette.setParam("montant", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 4 :
                        dette.setParam("montantTtc", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 5 :
                        dette.setParam("tva", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 6 :
                        dette.setParam("factureno", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 7 :
                        dette.setParam("date", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 8 :
                        dette.setParam("delai", widget.valueIndex())
                        self.s_change_sig.emit()
                    elif index.column() == 10 :
                        dette.setParam("statut", widget.valueIndex())
                        self.s_change_sig.emit()
                    elif index.column() == 11 :
                        dette.setParam("datePaiement", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 12 :
                        dette.setParam("modalites", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 13 :
                        if widgets.prompt("Etes vous sur ?") == "Ok" :
                            annee.removeItem("dettes", index.row())
                            self.s_change_sig.emit()

        self.closePersistentEditors()

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onChange(self, function) :
        self.s_change_sig.connect(function)
