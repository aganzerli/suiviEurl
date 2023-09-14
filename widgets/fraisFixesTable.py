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

        if index.column() == 0 :
            widget= widgets.TextEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 1 :
            widget= widgets.ComboBox(onChange= slotLambda)
            for i in db.OCCURENCE_STR[0:2] :
                widget.addValue(i)
            widget.setValueIndex(value)
        elif index.column() == 2 :
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 3 :
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 4 :
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 5 :
            widget= widgets.Button("X", onClick= slotLambda)
        else :
            widget= None

        if widget :
            self.parent().setIndexWidget(index, widget)

            widget.setStyleSheet("margin: 2px 2px;")
            widget.setFocus()


# ==================================================================================================================================
class FraisFixesTable(Table) :
    s_change_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, database, onChange= None) :
        super(FraisFixesTable, self).__init__([
            "Objet",
            "Occurence",
            "Montant HT",
            "Montant TTC",
            "TVA (%)",
            ""
            ],
            showToolTip= False)

        self.m_database= weakref.ref(database)
        self.m_year= 0
        self.m_rows= []

        self.setWidth(1, 128)
        self.setWidth(2, 128)
        self.setWidth(3, 128)
        self.setWidth(4, 128)
        self.setWidth(5, 32)

        self.setRowHeight(24)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(qt.QtWidgets.QAbstractItemView.NoSelection)

        self.setItemDelegateForColumn(0, Delegate(self))
        self.setItemDelegateForColumn(1, Delegate(self))
        self.setItemDelegateForColumn(2, Delegate(self))
        self.setItemDelegateForColumn(3, Delegate(self))
        self.setItemDelegateForColumn(4, Delegate(self))
        self.setItemDelegateForColumn(5, Delegate(self))

        #self.clicked.connect(self._clickCB)
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
        if columnIdx == 5 :
            return "X"
        elif columnIdx <= 4 :
            value= self.m_rows[rowIdx][columnIdx]
            if ( value is not None ) :
                if columnIdx == 1 :
                    return db.OCCURENCE_STR[value]
                else :
                    return value

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def editorData(self, columnIdx, rowIdx) :
        if columnIdx <= 4 :
            return self.m_rows[rowIdx][columnIdx]

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
            fraisFixes= annee.getParam("fraisFixes")

            rows= [
                [
                    i.getParam("objet"),
                    i.getParam("occurence"),
                    i.getParam("montant"),
                    i.getParam("montantTtc"),
                    i.getParam("tva")
                    ] for i in fraisFixes
                ]
        else :
            rows= []

        self.model().beginResetModel()
        self.m_rows= rows
        self.model().endResetModel()

        '''for i in range(0, self.rowCount()) :
            self.openPersistentEditor(self.model().index(i, 0))
            self.openPersistentEditor(self.model().index(i, 1))
            self.openPersistentEditor(self.model().index(i, 2))
            self.openPersistentEditor(self.model().index(i, 3))
            self.openPersistentEditor(self.model().index(i, 4))
            self.openPersistentEditor(self.model().index(i, 5))'''

        #self.vertical_resize_table_to_content()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _changeCB(self, index) :
        annee= self.m_database().year(self.m_year)
        if annee :
            widget= self.indexWidget(index)
            if widget :
                fraisFixes= annee.getParam("fraisFixes")
                if index.row() < len(fraisFixes) :
                    fraisFixe= fraisFixes[index.row()]

                    if index.column() == 0 :
                        fraisFixe.setParam("objet", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 1 :
                        fraisFixe.setParam("occurence", widget.valueIndex())
                        self.s_change_sig.emit()
                    elif index.column() == 2 :
                        fraisFixe.setParam("montant", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 3 :
                        fraisFixe.setParam("montantTtc", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 4 :
                        fraisFixe.setParam("tva", widget.value())
                        self.s_change_sig.emit()
                    elif index.column() == 5 :
                        if widgets.prompt("Etes vous sur ?") == "Ok" :
                            annee.removeItem("fraisFixes", index.row())
                            self.s_change_sig.emit()

        self.closePersistentEditors()

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onChange(self, function) :
        self.s_change_sig.connect(function)
