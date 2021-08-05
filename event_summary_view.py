import logging

from PyQt5 import QtWidgets

log = logging.getLogger(__name__)


def sip_is_deleted(obj):
    """
    :return: True if object no longer exists
    """
    if obj is None or (isinstance(obj, sip.simplewrapper) and sip.isdeleted(obj)):
        return True
    return False


def qslot(func):
    """
    Decorated slot are protected against already destroyed element
    in SIP but not in Python
    """

    def func_wrapper(*args, **kwargs):
        if len(args) > 0:
            if sip_is_deleted(args[0]):
                return lambda: True
        return func(*args, **kwargs)

    return func_wrapper


class EventSummaryView(QtWidgets.QTreeWidget):
    """
    Topology summary view implementation.
    :param parent: parent widget
    """

    def __init__(self, parent):

        super().__init__(parent)
        self.nodes_id = set()
        # self._topology = Topology.instance()
        self._topology.node_added_signal.connect(self._nodeAddedSlot)
        self._topology.project_changed_signal.connect(self._projectChangedSlot)
        self.itemSelectionChanged.connect(self._itemSelectionChangedSlot)
        self.show_only_devices_with_capture = False
        self.show_only_devices_with_filters = False
        self.setExpandsOnDoubleClick(False)
        self.itemDoubleClicked.connect(self._itemDoubleClickedSlot)

    @qslot
    def _projectChangedSlot(self, *args):
        """
        Clears all the topology summary.
        """

        self.clear()

    def refreshAllLinks(self, source_child=None):
        """
        Refreshes all links for all items.
        """

        root = self.invisibleRootItem()
        for index in range(0, root.childCount()):
            child = root.child(index)
            if source_child and source_child == child:
                continue
            child.refreshLinks()

    @qslot
    def _nodeAddedSlot(self, base_node_id, *args):
        """
        Received events for node creation.
        :param base_node_id: base node identifier
        """

        if not base_node_id:
            log.error("node ID is null")
            return

        node = self._topology.getNode(base_node_id)
        if not node:
            log.error("could not find node with ID {}".format(base_node_id))
            return

        # We check if we don't already have this node because it seem
        # sometimes we can get twice the signal
        if node.id() in self.nodes_id:
            return
        self.nodes_id.add(node.id())
        # TopologyNodeItem(self, node)
        self.resizeColumnToContents(0)

    # @qslot
    # def _itemSelectionChangedSlot(self, *args):
    #     """
    #     Slot called when an item is selected in the TreeWidget.
    #     """
    #
    #     current_item = self.currentItem()
    #     if current_item:
    #         from .main_window import MainWindow
    #         view = MainWindow.instance().uiGraphicsView
    #         for item in view.scene().items():
    #             if isinstance(item, NodeItem):
    #                 item.setSelected(False)
    #                 if isinstance(current_item, TopologyNodeItem) and item.node().id() == current_item.node().id():
    #                     item.setSelected(True)
    #             elif isinstance(item, LinkItem):
    #                 item.setHovered(False)
    #                 if not isinstance(current_item, TopologyNodeItem):
    #                     link = current_item.data(0, QtCore.Qt.UserRole)
    #                     if item.link() == link:
    #                         item.setHovered(True)
    #
    # @qslot
    # def _itemDoubleClickedSlot(self, current_item, *args):
    #     """
    #     When user double click on an element we center the topology on it
    #     """
    #     if current_item != 0:
    #         from .main_window import MainWindow
    #         view = MainWindow.instance().uiGraphicsView
    #         for item in view.scene().items():
    #             if isinstance(item, NodeItem):
    #                 if isinstance(current_item, TopologyNodeItem) and item.node().id() == current_item.node().id():
    #                     view.centerOn(item)
    #             elif isinstance(item, LinkItem):
    #                 if not isinstance(current_item, TopologyNodeItem):
    #                     link = current_item.data(0, QtCore.Qt.UserRole)
    #                     if item.link() == link:
    #                         view.centerOn(item)

    def contextMenuEvent(self, event):
        """
        Handles all context menu events.
        :param event: QContextMenuEvent instance
        """

        self._showContextualMenu(event.globalPos())

    # def _showContextualMenu(self, pos):
    #     """
    #     Contextual menu to expand and collapse the tree.
    #     """
    #
    #     menu = QtWidgets.QMenu()
    #     expand_all = QtWidgets.QAction("Expand all", menu)
    #     # expand_all.setIcon(get_icon("plus.svg"))
    #     expand_all.triggered.connect(self._expandAllSlot)
    #     menu.addAction(expand_all)
    #
    #     collapse_all = QtWidgets.QAction("Collapse all", menu)
    #     # collapse_all.setIcon(get_icon("minus.svg"))
    #     collapse_all.triggered.connect(self._collapseAllSlot)
    #     menu.addAction(collapse_all)
    #
    #     if self.show_only_devices_with_capture is False and self.show_only_devices_with_filters is False:
    #         devices_with_capture = QtWidgets.QAction("Show devices with capture(s)", menu)
    #         # devices_with_capture.setIcon(get_icon("inspect.svg"))
    #         devices_with_capture.triggered.connect(self._devicesWithCaptureSlot)
    #         menu.addAction(devices_with_capture)
    #
    #         devices_with_filters = QtWidgets.QAction("Show devices with packet filter(s)", menu)
    #         # devices_with_filters.setIcon(get_icon("filter.svg"))
    #         devices_with_filters.triggered.connect(self._devicesWithFiltersSlot)
    #         menu.addAction(devices_with_filters)
    #
    #     else:
    #         show_all_devices = QtWidgets.QAction("Show all devices", menu)
    #         # show_all_devices.setIcon(QtGui.QIcon(":/icons/inspect.svg"))
    #         show_all_devices.triggered.connect(self._showAllDevicesSlot)
    #         menu.addAction(show_all_devices)
    #
    #     stop_all_captures = QtWidgets.QAction("Stop all captures", menu)
    #     # stop_all_captures.setIcon(get_icon("capture-stop.svg"))
    #     stop_all_captures.triggered.connect(self._stopAllCapturesSlot)
    #     menu.addAction(stop_all_captures)
    #
    #     reset_all_filters = QtWidgets.QAction("Reset all packet filters", menu)
    #     # reset_all_filters.setIcon(get_icon("filter-reset.svg"))
    #     reset_all_filters.triggered.connect(self._resetAllFiltersSlot)
    #     menu.addAction(reset_all_filters)
    #
    #     resume_suspended_links = QtWidgets.QAction("Resume all suspended links", menu)
    #     # resume_suspended_links.setIcon(get_icon("start.svg"))
    #     resume_suspended_links.triggered.connect(self._resumeAllLinksSlot)
    #     menu.addAction(resume_suspended_links)
    #
    #     current_item = self.currentItem()
    #     from .main_window import MainWindow
    #     view = MainWindow.instance().uiGraphicsView
    #     if current_item and not current_item.isHidden():
    #         menu.addSeparator()
    #         if isinstance(current_item, TopologyNodeItem):
    #             view.populateDeviceContextualMenu(menu)
    #         else:
    #             link = current_item.data(0, QtCore.Qt.UserRole)
    #             for item in view.scene().items():
    #                 if isinstance(item, LinkItem) and item.link() == link:
    #                     item.populateLinkContextualMenu(menu)
    #                     break
    #
    #     menu.exec_(pos)

    @qslot
    def _expandAllSlot(self, *args):
        """
        Expands all items.
        """

        self.expandAll()

    @qslot
    def _collapseAllSlot(self, *args):
        """
        Collapses all items.
        """

        self.collapseAll()

    @qslot
    def _devicesWithCaptureSlot(self, *args):
        """
        Show only devices with captures.
        """

        self.show_only_devices_with_capture = True
        self.refreshAllLinks()

    @qslot
    def _devicesWithFiltersSlot(self, *args):
        """
        Show only devices with filters.
        """

        self.show_only_devices_with_filters = True
        self.refreshAllLinks()

    @qslot
    def _showAllDevicesSlot(self, *args):
        """
        Show all devices items.
        """

        self.show_only_devices_with_capture = False
        self.show_only_devices_with_filters = False
        self.refreshAllLinks()

    @qslot
    def _stopAllCapturesSlot(self, *args):
        """
        Stop all packet captures.
        """

        for link in self._topology.links():
            if link.capturing():
                PacketCapture.instance().stopCapture(link)

    @qslot
    def _resetAllFiltersSlot(self, *args):
        """
        Reset all packet filters
        """

        for link in self._topology.links():
            if len(link.filters()) > 0:
                filters = {}
                link.setFilters(filters)
                link.update()

    @qslot
    def _resumeAllLinksSlot(self, *args):
        """
        Resume all suspended links.
        """

        for link in self._topology.links():
            if link.suspended():
                link.toggleSuspend()
