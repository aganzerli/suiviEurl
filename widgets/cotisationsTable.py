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

        if index.column() == 1 : # Montant HT
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 2 : # Date d'envoi
            if value is not None:
                widget= widgets.DateEdit(onChange= slotLambda)
                widget.setValue(value)
        elif index.column() == 3 : # Modalités paiement
            widget= widgets.TextEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 4 :
            widget= widgets.Button("X", onClick= slotLambda)

        if widget :
            self.parent().setIndexWidget(index, widget)

            widget.setStyleSheet("margin: 2px 2px;")
            widget.setFocus()


# ==================================================================================================================================
class CotisationsTable(Table) :
    s_change_sig= qt.QtCore.pyqtSignal()
    s_red= None
    s_green= None

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, database, onChange= None) :
        super(CotisationsTable, self).__init__([
            "Mois",
            "Montant",
            "Date",
            "Modalités",
            ""
            ],
            showToolTip= False)

        if not CotisationsTable.s_red :
            CotisationsTable.s_red= qt.QtGui.QColor(255, 128, 128)

        if not CotisationsTable.s_green :
            CotisationsTable.s_green= qt.QtGui.QColor(128, 255, 128)

        self.m_database= weakref.ref(database)
        self.m_year= 0
        self.m_rows= []

        self.setWidth(0, 90)
        self.setWidth(1, 90)
        self.setWidth(2, 90)
        self.setWidth(4, 32)

        self.setRowHeight(24)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(qt.QtWidgets.QAbstractItemView.NoSelection)

        self.setItemDelegateForColumn(1, Delegate(self))
        self.setItemDelegateForColumn(2, Delegate(self))
        self.setItemDelegateForColumn(3, Delegate(self))
        self.setItemDelegateForColumn(4, Delegate(self))

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
        if columnIdx == 4 :
            return "X"
        elif columnIdx <= 3 :
            value= self.m_rows[rowIdx][columnIdx]
            if ( value is not None ) :
                if columnIdx == 2 :
                    return value.strftime("%d/%m/%y")
                else :
                    return value

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def editorData(self, columnIdx, rowIdx) :
        if columnIdx <= 3 :
            value= self.m_rows[rowIdx][columnIdx]
            return value

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
            cotisations= annee.getParam("cotisations")

            currentMonth= None
            rows= []
            for i in cotisations :
                date= i.getParam("date")
                if currentMonth != date.month :
                    currentMonth= date.month
                    monthLabel= db.MONTHS[currentMonth-1]
                else :
                    monthLabel= "-"

                rows.append([
                    monthLabel,
                    i.getParam("montant"),
                    i.getParam("date"),
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
                cotisations= annee.getParam("cotisations")
                if index.row() < len(cotisations) :
                    cotisation= cotisations[index.row()]

                    if index.column() == 1 :
                        cotisation.setParam("montant", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 2 :
                        cotisation.setParam("date", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 3 :
                        cotisation.setParam("modalites", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 4 :
                        if widgets.prompt("Etes vous sur ?") == "Ok" :
                            annee.removeItem("cotisations", index.row())
                            self.s_change_sig.emit()

        self.closePersistentEditors()

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onChange(self, function) :
        self.s_change_sig.connect(function)
