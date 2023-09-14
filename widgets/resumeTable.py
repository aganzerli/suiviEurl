# coding: latin-1


import weakref

import database as db

import qt
from .table import Table


'''# ==================================================================================================================================
class Delegate(qr.QtWidgets.QItemDelegate):
    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent) :
        super(Delegate, self).__init__(parent)

    # ------------------------------------------------------------------------------------------------------------------------------
    def createEditor(self, parent, option, index) :
        if self.parent().indexWidget(index) : return

        value= index.data(qr.QtCore.Qt.EditRole)

        if index.column() == 6 :
            widget= statusCounts.StatusCounts(value[0], value[1])

        self.parent().setIndexWidget(index, widget)

        widget.setStyleSheet("margin: 2px 0px;")'''


# ==================================================================================================================================
class ResumeTable(Table) :
    s_boldFont= None
    s_red= None
    s_green= None

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, database) :
        super(ResumeTable, self).__init__([
            "Emissions",
            "Salaires",
            "Dettes",
            "Frais Fixes",
            "Cotisations Payées",
            "Bilan Est.",
            "Bilan"
            ],
            verticalHeaders= db.MONTHS+["Total"],
            showToolTip= False)

        if not ResumeTable.s_boldFont :
            ResumeTable.s_boldFont= qt.QtGui.QFont()
            ResumeTable.s_boldFont.setPointSize(12)
            ResumeTable.s_boldFont.setBold(True)

        if not ResumeTable.s_red :
            ResumeTable.s_red= qt.QtGui.QColor(255, 128, 128)

        if not ResumeTable.s_green :
            ResumeTable.s_green= qt.QtGui.QColor(128, 255, 128)

        self.m_database= weakref.ref(database)
        self.m_year= 0
        self.m_rows= []

        '''self.setWidth(0, 128)
        self.setWidth(1, 96)'''

        self.setRowHeight(20)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(qt.QtWidgets.QAbstractItemView.NoSelection)

        #self.setItemDelegateForColumn(6, Delegate(self))

        #self.setSortingEnabled(True)
        #self.setSort(9, qr.QtCore.Qt.DescendingOrder)
        #self.set_onSort(self.reload)

        #self.m_popup= JobPopup(self)

    # ------------------------------------------------------------------------------------------------------------------------------
    def data(self, columnIdx, rowIdx) :
        if columnIdx == 0 :
            return self.m_rows[rowIdx][0]
        elif columnIdx == 1 :
            return self.m_rows[rowIdx][1]
        elif columnIdx == 2 :
            return self.m_rows[rowIdx][2]
        elif columnIdx == 3 :
            return self.m_rows[rowIdx][3]
        elif columnIdx == 4 :
            if rowIdx == 12 :
                t= self.m_rows[rowIdx][columnIdx]
                return "{} / {}".format(t[0], t[1])
            else :
                return self.m_rows[rowIdx][4]
        elif columnIdx == 5 :
            return self.m_rows[rowIdx][5]
        elif columnIdx == 6 :
            return self.m_rows[rowIdx][6]

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def bgColor(self, columnIdx, rowIdx) :
        if rowIdx == 12 :
            if columnIdx == 4 :
                t= self.m_rows[rowIdx][columnIdx]
                return ResumeTable.s_red if t[0] < t[1] else ResumeTable.s_green
            elif columnIdx == 6 :
                return ResumeTable.s_red if self.m_rows[rowIdx][columnIdx] < 0.0 else ResumeTable.s_green

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def font(self, columnIdx, rowIdx) :
        if rowIdx == 12 :
            return ResumeTable.s_boldFont

        return None

    '''# ------------------------------------------------------------------------------------------------------------------------------
    def fgColor(self, columnIdx, rowIdx) :
        flags= self.m_rows[rowIdx][FLAGS_IDX]

        if flags&ISPAUSED :
            return g_pausedColor
        elif flags&HASERRORS :
            return g_colors[3]
        elif flags&ISCANCELLED :
            return g_colors[4]
        elif flags&ISCOMPLETE :
            return g_colors[2]
        elif flags&ISRUNNING :
            return g_colors[1]

        return g_colors[0]'''

    # ------------------------------------------------------------------------------------------------------------------------------
    def alignment(self, columnIdx, rowIdx) :
        return qt.ALIGNHCENTER|qt.ALIGNVCENTER

    # ------------------------------------------------------------------------------------------------------------------------------
    def load(self, year) :
        if not year :
            year= 0
        self.m_year= int(year)

        annee= self.m_database().year(self.m_year)

        creances_parMois= annee.getParam("creances_parMois") if annee else [0]*len(db.MONTHS)
        salaires_parMois= annee.getParam("salaires_parMois") if annee else [0]*len(db.MONTHS)
        dettes_parMois= annee.getParam("dettes_parMois") if annee else [0]*len(db.MONTHS)
        fraisFixes_parMois= annee.getParam("fraisFixes_parMois") if annee else [0]*len(db.MONTHS)
        cotisations_parMois= annee.getParam("cotisations_parMois") if annee else [0]*len(db.MONTHS)
        bilanEst_parMois= annee.getParam("bilanEst_parMois") if annee else [0]*len(db.MONTHS)
        bilan_parMois= annee.getParam("bilan_parMois") if annee else [0]*len(db.MONTHS)

        creances_total= annee.getParam("creances_total") if annee else 0.0
        salaires_total= annee.getParam("salaires_total") if annee else 0.0
        dettes_total= annee.getParam("dettes_total") if annee else 0.0
        fraisFixes_total= annee.getParam("fraisFixes_total") if annee else 0.0
        cotisations_total= annee.getParam("cotisations_total") if annee else 0.0

        total_urssaf= annee.getParam("total_urssaf") if annee else 0.0

        balance= annee.getParam("balance") if annee else 0.0

        rows= [ [creances_parMois[i], -salaires_parMois[i], -dettes_parMois[i], -fraisFixes_parMois[i], cotisations_parMois[i], bilanEst_parMois[i], bilan_parMois[i] ] for i in range(len(salaires_parMois)) ]
        rows.append( [creances_total, -salaires_total, -dettes_total, -fraisFixes_total, (-cotisations_total, -total_urssaf,), None, balance ] )

        self.model().beginResetModel()
        self.m_rows= rows
        self.model().endResetModel()

        self.vertical_resize_table_to_content()
