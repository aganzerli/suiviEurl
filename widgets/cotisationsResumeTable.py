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

        if index.column() == 1 : # plafond_ss
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)
        elif index.column() == 4 : # formation_professionnelle
            widget= widgets.FloatEdit(onChange= slotLambda)
            widget.setValue(value)

        if widget :
            self.parent().setIndexWidget(index, widget)

            widget.setStyleSheet("margin: 2px 2px;")
            widget.setFocus()


# ==================================================================================================================================
class CotisationsResumeTable(Table) :
    s_change_sig= qt.QtCore.pyqtSignal()
    s_boldFont= None
    s_red= None
    s_green= None
    s_alignment= [
        qt.ALIGNRIGHT|qt.ALIGNVCENTER,
        qt.ALIGNHCENTER|qt.ALIGNVCENTER
        ]

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, database, onChange= None) :
        super(CotisationsResumeTable, self).__init__([
            "Cotisation",
            "Montant"
            ],
            showToolTip= False)

        if not CotisationsResumeTable.s_boldFont :
            CotisationsResumeTable.s_boldFont= qt.QtGui.QFont()
            CotisationsResumeTable.s_boldFont.setPointSize(12)
            CotisationsResumeTable.s_boldFont.setBold(True)

        if not CotisationsResumeTable.s_red :
            CotisationsResumeTable.s_red= qt.QtGui.QColor(255, 128, 128)

        if not CotisationsResumeTable.s_green :
            CotisationsResumeTable.s_green= qt.QtGui.QColor(128, 255, 128)

        self.m_database= weakref.ref(database)
        self.m_year= 0
        self.m_rows= []

        self.setWidth(1, 90)

        self.setRowHeight(24)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(qt.QtWidgets.QAbstractItemView.NoSelection)

        self.setItemDelegateForColumn(1, Delegate(self))

        if onChange :
            self.set_onChange(onChange)

    # ------------------------------------------------------------------------------------------------------------------------------
    def mousePressEvent(self, e) :
        self.closePersistentEditors()

        index= self.indexAt(qt.QtCore.QPoint(e.x(), e.y()))
        if self.itemDelegateForColumn(index.column()) and ( ( index.row() == 0 ) or ( index.row() == 4 ) ) :
            self.openPersistentEditor(index)

    # ------------------------------------------------------------------------------------------------------------------------------
    def data(self, columnIdx, rowIdx) :
        if columnIdx <= 1 :
            return self.m_rows[rowIdx][columnIdx]

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def editorData(self, columnIdx, rowIdx) :
        if columnIdx <= 1 :
            return self.m_rows[rowIdx][columnIdx]

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def font(self, columnIdx, rowIdx) :
        if rowIdx == 9 :
            return CotisationsResumeTable.s_boldFont

    # ------------------------------------------------------------------------------------------------------------------------------
    def bgColor(self, columnIdx, rowIdx) :
        if rowIdx == 12 :
            return CotisationsResumeTable.s_red if self.m_rows[rowIdx][1] < 0.0 else CotisationsResumeTable.s_green

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def alignment(self, columnIdx, rowIdx) :
        return CotisationsResumeTable.s_alignment[columnIdx]

    # ------------------------------------------------------------------------------------------------------------------------------
    def load(self, year) :
        if not year :
            year= 0
        self.m_year= int(year)

        annee= self.m_database().year(self.m_year)

        plafond_ss= annee.getParam("plafond_ss") if annee else 0.0
        maladie_maternite= annee.getParam("maladie_maternite") if annee else 0.0
        maladie_indemnite= annee.getParam("maladie_indemnite") if annee else 0.0
        allocations_familiales= annee.getParam("allocations_familiales") if annee else 0.0
        formation_professionnelle= annee.getParam("formation_professionnelle") if annee else 0.0
        retraite_de_base= annee.getParam("retraite_de_base") if annee else 0.0
        retraite_complementaire= annee.getParam("retraite_complementaire") if annee else 0.0
        invalidite_deces= annee.getParam("invalidite_deces") if annee else 0.0
        csg_crds= annee.getParam("csg_crds") if annee else 0.0
        total_urssaf= annee.getParam("total_urssaf") if annee else 0.0
        cotisations_total= annee.getParam("cotisations_total") if annee else 0.0
        reste= total_urssaf-cotisations_total

        taux_sur_salaire_net= annee.getParam("taux_sur_salaire_net") if annee else 0.0
        taux_sur_total= annee.getParam("taux_sur_total") if annee else 0.0

        rows= [
            ("Plafond annuel sécurité sociale", plafond_ss),
            ("Maladie-maternité", maladie_maternite),
            ("Maladie-indemnité journalières", maladie_indemnite),
            ("Allocations familiales", allocations_familiales),
            ("Contribution à la formation professionnelle", formation_professionnelle),
            ("Retraite de base", retraite_de_base),
            ("Retraire complementaire", retraite_complementaire),
            ("Invalidité décès", invalidite_deces),
            ("CSG et CRDS", csg_crds),
            ("Total", total_urssaf),
            (None, None),
            ("Cotisations payées", cotisations_total),
            ("Reste", reste),
            (None, None),
            ("Taux cotisations sur salaire net (%)", taux_sur_salaire_net),
            ("Taux cotisations sur total (%)", taux_sur_total)
            ]

        self.model().beginResetModel()
        self.m_rows= rows
        self.model().endResetModel()

    # ------------------------------------------------------------------------------------------------------------------------------
    def _changeCB(self, index) :
        annee= self.m_database().year(self.m_year)
        if annee :
            widget= self.indexWidget(index)
            if widget :
                if index.row() == 0 :
                    annee.setParam("plafond_ss", widget.value())
                    self.s_change_sig.emit()
                elif index.row() == 4 :
                    annee.setParam("formation_professionnelle", widget.value())
                    self.s_change_sig.emit()

        self.closePersistentEditors()

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onChange(self, function) :
        self.s_change_sig.connect(function)
