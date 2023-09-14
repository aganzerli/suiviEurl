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
        value= index.data(qt.QtCore.Qt.EditRole)
        slotLambda= lambda : self.parent()._changeCB(index)

        widget= None

        if index.column() == 1 : # Objet
            widget= widgets.TextEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 2 : # Montant HT
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 3 : # Date d'envoi
            if value is not None:
                widget= widgets.DateEdit(onChange= slotLambda)
                widget.setValue(value)
        elif index.column() == 4 : # Statut
            widget= widgets.ComboBox(onChange= slotLambda)
            for i in db.STATUT_STR :
                widget.addValue(i)
            widget.setValueIndex(value)
        elif index.column() == 5 :
            widget= widgets.Button("X", onClick= slotLambda)

        if widget :
            self.parent().setIndexWidget(index, widget)

            widget.setStyleSheet("margin: 2px 2px;")
            widget.setFocus()


# ==================================================================================================================================
class SalairesTable(Table) :
    s_change_sig= qt.QtCore.pyqtSignal()
    s_red= None
    s_green= None

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, database, onChange= None) :
        super(SalairesTable, self).__init__([
            "Mois",
            "Objet",
            "Montant",
            "Date",
            "Statut",
            ""
            ],
            showToolTip= False)

        if not SalairesTable.s_red :
            SalairesTable.s_red= qt.QtGui.QColor(255, 128, 128)

        if not SalairesTable.s_green :
            SalairesTable.s_green= qt.QtGui.QColor(128, 255, 128)

        self.m_database= weakref.ref(database)
        self.m_year= 0
        self.m_rows= []

        self.setWidth(0, 90)
        self.setWidth(2, 90)
        self.setWidth(3, 90)
        self.setWidth(4, 90)
        self.setWidth(5, 32)

        self.setRowHeight(24)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(qt.QtWidgets.QAbstractItemView.NoSelection)

        self.setItemDelegateForColumn(1, Delegate(self))
        self.setItemDelegateForColumn(2, Delegate(self))
        self.setItemDelegateForColumn(3, Delegate(self))
        self.setItemDelegateForColumn(4, Delegate(self))
        self.setItemDelegateForColumn(5, Delegate(self))

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
        if columnIdx == 5 :
            return "X"
        elif columnIdx <= 4 :
            value= self.m_rows[rowIdx][columnIdx]
            if ( value is not None ) :
                if columnIdx == 3 :
                    return value.strftime("%d/%m/%y")
                elif columnIdx == 4 :
                    return db.STATUT_STR[value]
                else :
                    return value

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def editorData(self, columnIdx, rowIdx) :
        if columnIdx <= 4 :
            return self.m_rows[rowIdx][columnIdx]

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def bgColor(self, columnIdx, rowIdx) :
        value= self.m_rows[rowIdx][4]
        if value == db.STATUT_ENCOURS :
            return SalairesTable.s_red
        elif value == db.STATUT_PAYE :
            return SalairesTable.s_green

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
            salaires= annee.getParam("salaires")

            currentMonth= None
            rows= []
            for i in salaires :
                date= i.getParam("date")
                if currentMonth != date.month :
                    currentMonth= date.month
                    monthLabel= db.MONTHS[currentMonth-1]
                else :
                    monthLabel= "-"

                rows.append([
                    monthLabel,
                    i.getParam("objet"),
                    i.getParam("montant"),
                    i.getParam("date"),
                    i.getParam("statut")
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
                salaires= annee.getParam("salaires")
                if index.row() < len(salaires) :
                    salaire= salaires[index.row()]

                    if index.column() == 1 :
                        salaire.setParam("objet", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 2 :
                        salaire.setParam("montant", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 3 :
                        salaire.setParam("date", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 4 :
                        salaire.setParam("statut", widget.valueIndex())
                        self.s_change_sig.emit()
                    elif index.column() == 5 :
                        if widgets.prompt("Etes vous sur ?") == "Ok" :
                            annee.removeItem("salaires", index.row())
                            self.s_change_sig.emit()

        self.closePersistentEditors()

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onChange(self, function) :
        self.s_change_sig.connect(function)
