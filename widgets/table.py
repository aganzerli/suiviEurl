import qt


# ==================================================================================================================================
class Table_model(qt.QtCore.QAbstractTableModel) :
    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, table, horizontalHeaders, verticalHeaders) :
        super(Table_model, self).__init__()

        self.m_table= table
        self.m_hheaders= horizontalHeaders
        self.m_vheaders= verticalHeaders

    # ------------------------------------------------------------------------------------------------------------------------------
    def columnCount(self, parent= qt.QtCore.QModelIndex()) :
        return len(self.m_hheaders)

    # ------------------------------------------------------------------------------------------------------------------------------
    def columnNames(self) : return self.m_hheaders

    # ------------------------------------------------------------------------------------------------------------------------------
    def columnName(self, idx) : return self.m_hheaders[idx]

    # ------------------------------------------------------------------------------------------------------------------------------
    def columnIndex(self, columnName) :
        try :
            idx= self.m_hheaders.index(columnName)
        except :
            idx= -1

        return idx

    # ------------------------------------------------------------------------------------------------------------------------------
    def rowCount(self, parent= qt.QtCore.QModelIndex()) :
        return len(self.m_vheaders) if self.m_vheaders is not None else self.m_table.rowCount()

    # ------------------------------------------------------------------------------------------------------------------------------
    def data(self, index, role) :
        if index.isValid() :
            if role == qt.QtCore.Qt.DisplayRole : return self.m_table.data(index.column(), index.row())
            elif role == qt.QtCore.Qt.DecorationRole: return self.m_table.icon(index.column(), index.row())
            elif role == qt.QtCore.Qt.ForegroundRole : return self.m_table.fgColor(index.column(), index.row())
            elif role == qt.QtCore.Qt.BackgroundRole : return self.m_table.bgColor(index.column(), index.row())
            elif role == qt.QtCore.Qt.EditRole : return self.m_table.editorData(index.column(), index.row())
            elif role == qt.QtCore.Qt.TextAlignmentRole : return self.m_table.alignment(index.column(), index.row())
            elif role == qt.QtCore.Qt.FontRole : return self.m_table.font(index.column(), index.row())
        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def headerData(self, section, orientation, role= qt.QtCore.Qt.DisplayRole) :
        if role == qt.QtCore.Qt.DisplayRole :
            if orientation == qt.QtCore.Qt.Horizontal :
                return self.m_hheaders[section]
            elif orientation == qt.QtCore.Qt.Vertical :
                return self.m_vheaders[section]
        elif role == qt.QtCore.Qt.TextAlignmentRole :
            if orientation == qt.QtCore.Qt.Horizontal :
                return qt.ALIGNHCENTER|qt.ALIGNVCENTER
            elif orientation == qt.QtCore.Qt.Vertical :
                return qt.ALIGNRIGHT|qt.ALIGNVCENTER
        elif role == qt.QtCore.Qt.InitialSortOrderRole :
            return qt.QtCore.Qt.DescendingOrder
        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def table(self) :
        return self.m_table

    # ------------------------------------------------------------------------------------------------------------------------------
    def sort(self, column, order) :
        self.m_table.m_sortColumn= column
        self.m_table.m_sortReverse= (order==qt.QtCore.Qt.AscendingOrder)
        self.m_table.s_sort_sig.emit()


# ==================================================================================================================================
class Table(qt.QtWidgets.QTableView) :
    s_sort_sig= qt.QtCore.pyqtSignal()

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, horizontalHeaders, verticalHeaders= None, showToolTip= True) :
        super(Table, self).__init__()

        self.m_rows= []
        self.m_model= Table_model(self, horizontalHeaders, verticalHeaders)
        self.m_pressed= False
        self.m_emitSignals= True
        self.m_showToolTip= showToolTip
        self.m_height= 26
        self.setSort(0, False)

        ''' create table '''
        self.setModel(self.m_model)
        #self.setFrameStyle(qt.QtWidgets.QFrame.NoFrame)
        #self.setShowGrid(False)
        self.setFocusPolicy(qt.QtCore.Qt.NoFocus)
        self.setEditTriggers(qt.QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(qt.QtWidgets.QAbstractItemView.SelectRows)
        #self.setContentsMargins(0, 0, 0, 0)

        header= self.verticalHeader()
        if verticalHeaders is None:
            header.setVisible(False)
            header.setSectionResizeMode(qt.QtWidgets.QHeaderView.Fixed)
        else :
            #header.setVisible(True)
            #header.setSizePolicy(qt.EXPANDING, qt.PREFERRED)
            header.setMinimumSectionSize(1)
            header.setHighlightSections(False)
            #for i in range(0, self.m_model.rowCount()) :
            #    header.setSectionResizeMode(i, qt.QtWidgets.QHeaderView.Stretch)

        header= self.horizontalHeader()
        #header.setSizePolicy(qt.EXPANDING, qt.PREFERRED)
        header.setMinimumSectionSize(1)
        header.setHighlightSections(False)
        for i in range(0, self.m_model.columnCount()) :
            header.setSectionResizeMode(i, qt.QtWidgets.QHeaderView.Stretch)

        self.setMultipleSelection(False)

        #self.setStyleSheet("QTableView {selection-background-color: transparent;}")
        #self.setItemDelegate(misc.StyledItemDelegate(self))

        #self.selectionModel().blockSignals(True)

    '''# ------------------------------------------------------------------------------------------------------------------------------
    def event(self, event):
        if self.m_showToolTip :
            if event.type() == qt.QtCore.QEvent.ToolTip :
                qt.QtWidgets.QToolTip.showText(event.globalPos(), "{0} items, {1} selected".format(self.rowCount(), len(self.selectionModel().selectedRows())))
                return True

        return super(Table, self).event(event)

    # ------------------------------------------------------------------------------------------------------------------------------
    def leaveEvent(self, event):
        if qt.QtWidgets.QToolTip.isVisible() :
            qt.QtWidgets.QToolTip.hideText()

        return super(Table, self).leaveEvent(event)'''

    # ------------------------------------------------------------------------------------------------------------------------------
    '''def mousePressEvent(self, event) :
        super(Table, self).mousePressEvent(event)

        item= self.indexAt(event.pos())
        if not item.isValid() :
            self.selectionModel().clearSelection()'''

    '''# ------------------------------------------------------------------------------------------------------------------------------
    def mousePressEvent(self, event) :
        super(Table, self).mousePressEvent(event)

        item= self.indexAt(event.pos())
        if not item.isValid() :
            self.selectionModel().clearSelection()

        if event.button() == qt.QtCore.Qt.LeftButton :
            self.repaint()
            self.m_pressed= True
        elif event.button() == qt.QtCore.Qt.RightButton :
            self.repaint()
            self.emit_onSelect()

    # ------------------------------------------------------------------------------------------------------------------------------
    def mouseMoveEvent(self, event) :
        super(Table, self).mouseMoveEvent(event)
        if self.m_pressed == True :
            self.repaint()

    # ------------------------------------------------------------------------------------------------------------------------------
    def mouseReleaseEvent(self, event) :
        super(Table, self).mouseReleaseEvent(event)
        if event.button() == qt.QtCore.Qt.LeftButton and self.m_pressed == True :
            self.repaint()
            self.m_pressed= False
            self.emit_onSelect()

    # ------------------------------------------------------------------------------------------------------------------------------
    def emitSignals(self, state) :
        self.m_emitSignals= state'''

    # ------------------------------------------------------------------------------------------------------------------------------
    def setMultipleSelection(self, state) :
        if state :
            self.setSelectionMode(qt.QtWidgets.QAbstractItemView.ExtendedSelection)
        else :
            self.setSelectionMode(qt.QtWidgets.QAbstractItemView.SingleSelection)

    # ------------------------------------------------------------------------------------------------------------------------------
    def setFixed(self, columnIdx) :
        self.horizontalHeader().setSectionResizeMode(columnIdx, qt.QtWidgets.QHeaderView.Fixed)

    # ------------------------------------------------------------------------------------------------------------------------------
    def setWidth(self, columnIdx, width) :
        self.horizontalHeader().setSectionResizeMode(columnIdx, qt.QtWidgets.QHeaderView.Fixed)
        self.setColumnWidth(columnIdx, width)

    # ------------------------------------------------------------------------------------------------------------------------------
    def setRowHeight(self, height) :
        #for i in range(self.rowCount()) :
        #    self.setRowHeight(i, height)
        #self.centerSelection()
        header= self.verticalHeader()
        #header.setVisible(False)
        header.setSectionResizeMode(qt.QtWidgets.QHeaderView.Fixed)
        header.setDefaultSectionSize(height)

    # ------------------------------------------------------------------------------------------------------------------------------
    '''def update(self) :
        #self.selectionModel().blockSignals(True)
        self.m_model.beginResetModel()
        self.m_model.endResetModel()
        #self.selectionModel().blockSignals(False)'''

    # ------------------------------------------------------------------------------------------------------------------------------
    def select(self, idx, emit= False) :
        #self.selectionModel().blockSignals(True)

        self.selectionModel().clearSelection()

        if isinstance(idx, list) :
            for i in idx :
                if i >= 0 and i < self.rowCount() :
                    self.selectionModel().select(self.model().index(i, 0), qt.QtCore.QItemSelectionModel.Select|qt.QtCore.QItemSelectionModel.Rows)
        else :
            if idx >= 0 and idx < self.rowCount() :
                self.selectionModel().select(self.model().index(idx, 0), qt.QtCore.QItemSelectionModel.Select|qt.QtCore.QItemSelectionModel.Rows)

        # too heavy self.repaint()
        super(Table, self).update()

        if emit :
            self.emit_onSelect()
        #self.selectionModel().blockSignals(False)

    # ------------------------------------------------------------------------------------------------------------------------------
    def selection(self) :
        selection= [ item.row() for item in self.selectionModel().selectedRows() ]
        return selection

    # ------------------------------------------------------------------------------------------------------------------------------
    def selectedRow(self) :
        if len(self.selection()) :
            return self.m_rows[self.selection()[0]]

        return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def selectedRows(self) :
        rows= [ self.m_rows[idx] for idx in self.selection() ]
        return rows

    # ------------------------------------------------------------------------------------------------------------------------------
    def centerSelection(self) :
        indexes= self.selectionModel().selectedRows()
        if len(indexes) :
            self.scrollTo(indexes[0], qt.QtWidgets.QAbstractItemView.EnsureVisible)

    # ------------------------------------------------------------------------------------------------------------------------------
    def columnCount(self) : return self.model().columnCount()

    # ------------------------------------------------------------------------------------------------------------------------------
    def columnNames(self) : return self.model().columnNames()

    # ------------------------------------------------------------------------------------------------------------------------------
    def columnName(self, idx) : return self.model().columnName(idx)

    # ------------------------------------------------------------------------------------------------------------------------------
    def columnIndex(self, columnName) : return self.model().columnIndex(columnName)

    # ------------------------------------------------------------------------------------------------------------------------------
    def rowCount(self) : return len(self.m_rows)

    # ------------------------------------------------------------------------------------------------------------------------------
    def row(self, idx) : return self.m_rows[idx]

    # ------------------------------------------------------------------------------------------------------------------------------
    def data(self, columnIdx, rowIdx) : return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def editorData(self, columnIdx, rowIdx) : return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def fgColor(self, columnIdx, rowIdx) : return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def bgColor(self, columnIdx, rowIdx) : return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def icon(self, columnIdx, rowIdx) : return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def alignment(self, columnIdx, rowIdx) : return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def font(self, columnIdx, rowIdx) : return None

    # ------------------------------------------------------------------------------------------------------------------------------
    def setSort(self, columnIdx, reverse= False) :
        self.m_sortColumn= columnIdx
        self.m_sortReverse= reverse

        if reverse : order= qt.QtCore.Qt.AscendingOrder
        else : order= qt.QtCore.Qt.DescendingOrder
        self.horizontalHeader().setSortIndicator(columnIdx, order)

    # ------------------------------------------------------------------------------------------------------------------------------
    def sortColumn(self) : return self.m_sortColumn

    # ------------------------------------------------------------------------------------------------------------------------------
    def sortReverse(self) : return self.m_sortReverse

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onSelect(self, function) :
        model= self.selectionModel()
        model.selectionChanged.connect(function)

    # ------------------------------------------------------------------------------------------------------------------------------
    def set_onSort(self, function) :
        model= self.selectionModel()
        self.s_sort_sig.connect(function)

    # ------------------------------------------------------------------------------------------------------------------------------
    def calc_table_height(self) :
        res = 0
        for i in range(self.verticalHeader().count()):
            if not self.verticalHeader().isSectionHidden(i):
                res += self.verticalHeader().sectionSize(i)
        if self.horizontalScrollBar().isHidden():
            res+= self.horizontalScrollBar().height()
        if not self.horizontalHeader().isHidden():
            res+= self.horizontalHeader().height()
        return res

    # ------------------------------------------------------------------------------------------------------------------------------
    def vertical_resize_table_to_content(self) :
        self.verticalScrollBar().hide()
        content_height= self.calc_table_height()
        self.setFixedHeight(content_height)

    # ------------------------------------------------------------------------------------------------------------------------------
    def closePersistentEditors(self) :
        for c in range(self.columnCount()) :
            if self.itemDelegateForColumn(c) :
                for r in range(self.rowCount()) :
                    index= self.model().index(r, c)
                    widget= self.indexWidget(index)
                    if widget :
                        widget.clearFocus()
                    self.closePersistentEditor(index)
