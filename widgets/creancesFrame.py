# coding: latin-1


import weakref

import qt

import widgets


# ==================================================================================================================================
class CreancesFrame(widgets.VLayout) :
    s_change_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, database, onChange= None) :
        super(CreancesFrame, self).__init__()

        self.m_database= weakref.ref(database)
        self.m_year= 0

        boldFont= qt.QtGui.QFont()
        boldFont.setPointSize(12)
        boldFont.setBold(True)

        hLayout= self.addWidget( widgets.HLayout() )
        hLayout.setFixedHeight(24)
        label= hLayout.addWidget( widgets.Label("Cotisations") )
        label.setFont(boldFont)
        label.setStyleSheet("background-color: #C0C0C0")

        button= hLayout.addWidget( widgets.Button("+", onClick= self._addCotisationsCB) )
        button.setFixedWidth(32)

        hLayout= self.addWidget( widgets.HLayout() )

        self.m_cotisationsResumeTable= hLayout.addWidget( widgets.CotisationsResumeTable(database, onChange= self.s_change_sig.emit) )
        self.m_cotisationsResumeTable.setFixedWidth(300)

        hLayout.addSpacing(8)

        self.m_cotisationsTable= hLayout.addWidget( widgets.CotisationsTable(database, onChange= self.s_change_sig.emit) )

        if onChange :
            self.set_onChange(onChange)

    # ------------------------------------------------------------------------------------------------------------------------------
    def _addCotisationsCB(self) :
        annee= self.m_database().year(self.m_year)
        if annee :
            annee.addItem("cotisations")

        self.s_change_sig.emit()

    # ------------------------------------------------------------------------------------------------------------------------------
    def load(self, year) :
        if not year :
            year= 0
        self.m_year= int(year)

        self.m_cotisationsResumeTable.load(self.m_year)
        self.m_cotisationsTable.load(self.m_year)

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onChange(self, function) :
        self.s_change_sig.connect(function)
