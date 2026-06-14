import sys
import os
import json
import uuid

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QBrush, QPen, QAction, QPixmap, QPainter, QTransform
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QMainWindow,
    QMenu,
    QColorDialog,
    QGraphicsPixmapItem,
    QGraphicsItem,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QLabel,
    QInputDialog,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QCheckBox,
    QComboBox,
)


from data_handler.api_handler import api_handler


# Simple mock DB — replace with real API via get_devices_for_type
MOCK_DB = {
    'Router': [
        {'id': 'r1', 'ip': '10.0.0.1', 'ports': 4, 'subnet': '255.255.255.0', 'description': 'Office edge router'},
        {'id': 'r2', 'ip': '10.0.0.2', 'ports': 8, 'subnet': '255.255.255.0', 'description': 'Backup router'},
    ],
    'Switch': [
        {'id': 'sw1', 'ip': '10.0.1.1', 'ports': 48, 'subnet': '255.255.255.0', 'description': 'Main distribution switch'},
        {'id': 'sw2', 'ip': '10.0.1.2', 'ports': 24, 'subnet': '255.255.255.0', 'description': 'Secondary access switch'},
    ],
    'Server': [
        {'id': 'srv1', 'ip': '10.0.2.10', 'ports': 2, 'subnet': '255.255.255.0', 'description': 'Application server'},
    ],
}


def _load_db_entries():
    if api_handler is None:
        return []
    try:
        client = api_handler()
        return client.fetch_data() or []
    except Exception:
        pass
    return []


def get_db_device_entries():
    if api_handler is None:
        return []
    try:
        client = api_handler()
        return client.fetch_data() or []
    except Exception:
        return []


def get_db_device_types():
    if api_handler is None:
        return []
    try:
        client = api_handler()
        return client.fetch_types() or []
    except Exception:
        return []


def get_devices_for_type(device_type):
    """Pluggable adapter: return list of dicts with keys id, ip, ports, subnet, description."""
    device_type = str(device_type or '').strip()
    if api_handler is not None:
        results = []
        for entry in _load_db_entries():
            if (
                str(entry.get('type', '')).lower() == device_type.lower()
                or str(entry.get('name', '')).lower() == device_type.lower()
                or str(entry.get('id', '')).lower() == device_type.lower()
            ):
                results.append({
                    'id': entry.get('id'),
                    'ip': entry.get('ip'),
                    'ports': int(entry.get('ports') or 0),
                    'subnet': entry.get('subnet'),
                    'description': entry.get('description'),
                })
        if results:
            return results
        return MOCK_DB.get(device_type, [])
    return MOCK_DB.get(device_type, [])


class GraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self._panning = False
        self._pan_start = None

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            angle = event.angleDelta().y()
            factor = 1.0 + (0.001 * angle)
            self.scale(factor, factor)
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._panning = True
            self._pan_start = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning and self._pan_start is not None:
            delta = event.pos() - self._pan_start
            self._pan_start = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)


class PortItem(QGraphicsEllipseItem):
    def __init__(self, x, y, index, parent_node):
        super().__init__(-4, -4, 8, 8, parent_node)
        self.setPos(x, y)
        self.port_index = index
        self.node = parent_node
        self.setBrush(QBrush(QColor('#94a3b8')))
        self.setPen(QPen(QColor('#111827')))
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.AllButtons)

        # small label (1-based)
        self.label = QGraphicsTextItem(str(index + 1), self)
        self.label.setDefaultTextColor(Qt.white)
        self.label.setScale(0.7)
        self.label.setPos(8, -6)
        self.label.setVisible(False)

        try:
            self.setToolTip(f"Port {index + 1}")
        except Exception:
            pass

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(QColor('#60a5fa')))
        self.label.setVisible(True)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(QColor('#94a3b8')))
        if not getattr(self.node, 'show_port_labels', False):
            self.label.setVisible(False)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        scene = self.scene()
        if hasattr(scene, 'port_clicked'):
            scene.port_clicked(self.node, self.port_index)
        event.accept()

    def contextMenuEvent(self, event):
        # Forward context menu to the parent DeviceNode so right-click works
        try:
            if hasattr(self, 'node') and self.node is not None:
                self.node.contextMenuEvent(event)
                return
        except Exception:
            pass
        return super().contextMenuEvent(event)

    def set_connected(self, connected=True):
        if connected:
            self.setBrush(QBrush(QColor('#f97316')))
            self.label.setVisible(True)
        else:
            self.setBrush(QBrush(QColor('#94a3b8')))
            if not getattr(self.node, 'show_port_labels', False):
                self.label.setVisible(False)


class Connection:
    def __init__(self, scene, start_ref, end_ref, color=QColor('#00ff00')):
        # start_ref/end_ref: either DeviceNode or (DeviceNode, port_index)
        self.start_ref = start_ref
        self.end_ref = end_ref
        self.line = QGraphicsLineItem()
        self.line.setPen(QPen(color, 3))
        scene.addItem(self.line)
        self.update()

    def anchor_point(self, ref):
        if isinstance(ref, tuple):
            node, port = ref
            return node.port_scene_pos(port)
        else:
            return ref.mapToScene(QPointF(0, 0))

    def update(self):
        s = self.anchor_point(self.start_ref)
        e = self.anchor_point(self.end_ref)
        self.line.setLine(s.x(), s.y(), e.x(), e.y())

    def mark_connected(self, on=True):
        def mark(ref, state):
            if isinstance(ref, tuple):
                node, port = ref
                try:
                    idx = int(port) % len(node.port_items)
                    node.port_items[idx].set_connected(state)
                except Exception:
                    pass

        mark(self.start_ref, on)
        mark(self.end_ref, on)


class DeviceNode(QGraphicsEllipseItem):
    COLORS = {
        'Router': '#3498db',
        'Switch': '#2ecc71',
        'Server': '#9b59b6',
        'Firewall': '#e74c3c',
    }

    def __init__(self, name, x, y, ports=0, node_id=None):
        super().__init__(-40, -40, 80, 80)
        self.name = name
        self.id = node_id or uuid.uuid4().hex
        self.radius = 40
        self.ports = ports or 0
        self.port_items = []
        self.connections = []
        self.source_id = None
        self.ip = None
        self.subnet = None
        self.description = None
        self.info_label = None
        self.description_label = None

        images_dir = os.path.join(os.path.dirname(__file__), 'images')
        specific = os.path.join(images_dir, f"{name.lower()}.png")
        default = os.path.join(images_dir, 'default.png')
        img = None
        if os.path.exists(specific):
            img = specific
        elif os.path.exists(default):
            img = default
        if img:
            pix = QPixmap(img)
            if not pix.isNull():
                pix = pix.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_item = QGraphicsPixmapItem(pix, self)
                self.image_item.setOffset(-pix.width() / 2, -pix.height() / 2)
                self.setBrush(QBrush(QColor(0, 0, 0, 0)))
        else:
            self.setBrush(QBrush(QColor(self.COLORS.get(name, '#7f8c8d'))))

        self.setPen(QPen(QColor('#ffffff'), 2))
        self.setFlags(QGraphicsEllipseItem.ItemIsMovable | QGraphicsEllipseItem.ItemIsSelectable | QGraphicsEllipseItem.ItemSendsScenePositionChanges)
        self.setAcceptedMouseButtons(Qt.AllButtons)
        self.setAcceptHoverEvents(True)
        self.setPos(x, y)

        self.title = QGraphicsTextItem(name, self)
        self.title.setDefaultTextColor(Qt.white)
        self.title.setPos(-30, 45)

        self.ip_label = None
        if self.ports > 0:
            self._create_ports(self.ports)

        # control whether port labels stay visible
        self.show_port_labels = False

    def _create_ports(self, ports):
        # remove existing
        for p in list(self.port_items):
            try:
                self.scene().removeItem(p)
            except Exception:
                pass
        self.port_items = []
        max_per_row = 16
        rows = (ports + max_per_row - 1) // max_per_row
        spacing_x = 80.0 / (min(max_per_row, ports) + 1)
        spacing_y = 12
        for r in range(rows):
            row_count = min(max_per_row, ports - r * max_per_row)
            start_x = - (row_count - 1) * spacing_x / 2
            y = 18 + r * spacing_y
            for j in range(row_count):
                i = r * max_per_row + j
                px = start_x + j * spacing_x
                p = PortItem(px, y, i, self)
                self.port_items.append(p)

    def set_ports(self, ports):
        self.ports = ports or 0
        self._create_ports(self.ports)

    def _update_info_label(self):
        try:
            if self.info_label and self.info_label.scene() is not None:
                self.scene().removeItem(self.info_label)
        except Exception:
            pass
        self.info_label = None

        text = ''
        if self.ip:
            text = str(self.ip)
        if self.subnet:
            text = f"{text} / {self.subnet}" if text else str(self.subnet)
        if text:
            self.info_label = QGraphicsTextItem(text, self)
            self.info_label.setDefaultTextColor(Qt.lightGray)
            self.info_label.setPos(-30, 58)

    def _update_description_label(self):
        try:
            if self.description_label and self.description_label.scene() is not None:
                self.scene().removeItem(self.description_label)
        except Exception:
            pass
        self.description_label = None
        if self.description:
            self.description_label = QGraphicsTextItem(str(self.description), self)
            self.description_label.setDefaultTextColor(Qt.lightGray)
            font = QFont()
            font.setPointSize(8)
            self.description_label.setFont(font)
            self.description_label.setPos(-30, -58)

    def set_ip(self, ip):
        self.ip = str(ip).strip() if ip else None
        self._update_info_label()

    def set_subnet(self, subnet):
        self.subnet = str(subnet).strip() if subnet else None
        self._update_info_label()

    def set_description(self, description):
        self.description = str(description).strip() if description else None
        self._update_description_label()

    def refresh_from_db(self):
        if not self.source_id:
            return
        entries = get_devices_for_type(self.name)
        for entry in entries:
            if entry.get('id') == self.source_id:
                self.set_ip(entry.get('ip'))
                self.set_subnet(entry.get('subnet'))
                self.set_description(entry.get('description'))
                self.set_ports(entry.get('ports', 0))
                return

    def edit_properties(self):
        dialog = QDialog()
        dialog.setWindowTitle(f"Edit {self.name} properties")
        layout = QFormLayout(dialog)

        ip_edit = QLineEdit(self.ip or '')
        subnet_edit = QLineEdit(self.subnet or '')
        description_edit = QLineEdit(self.description or '')
        ports_edit = QSpinBox()
        ports_edit.setRange(0, 256)
        ports_edit.setValue(self.ports or 0)

        layout.addRow('IP address:', ip_edit)
        layout.addRow('Subnet:', subnet_edit)
        layout.addRow('Description:', description_edit)
        layout.addRow('Port count:', ports_edit)
        if self.source_id:
            source_label = QLineEdit(str(self.source_id))
            source_label.setReadOnly(True)
            layout.addRow('Source ID:', source_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            self.set_ip(ip_edit.text().strip() or None)
            self.set_subnet(subnet_edit.text().strip() or None)
            self.set_description(description_edit.text().strip() or None)
            self.set_ports(ports_edit.value())
            try:
                if getattr(self.scene(), 'history_callback', None):
                    self.scene().history_callback()
            except Exception:
                pass

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for c in list(self.connections):
                c.update()
        return super().itemChange(change, value)

    def port_scene_pos(self, port_index):
        if not self.port_items:
            return self.mapToScene(QPointF(0, 0))
        try:
            idx = int(port_index) % len(self.port_items)
        except Exception:
            idx = 0
        return self.port_items[idx].mapToScene(QPointF(0, 0))

    def nearest_port_to_scene_point(self, point):
        if not self.port_items:
            return None
        best = None
        best_d = None
        for i, p in enumerate(self.port_items):
            pos = p.mapToScene(QPointF(0, 0))
            dx = pos.x() - point.x()
            dy = pos.y() - point.y()
            d = dx * dx + dy * dy
            if best is None or d < best_d:
                best = i
                best_d = d
        return best

    def hoverEnterEvent(self, event):
        self.show_port_labels = True
        for p in self.port_items:
            p.label.setVisible(True)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.show_port_labels = False
        for p in self.port_items:
            p.label.setVisible(False)
        super().hoverLeaveEvent(event)

    def contextMenuEvent(self, event):
        scene = self.scene()
        if scene is None:
            return
        menu = QMenu()
        assign = QAction('Assign from DB')
        refresh = QAction('Refresh from DB')
        edit = QAction('Edit properties')
        clear = QAction('Clear assignment')
        menu.addAction(assign)
        menu.addAction(refresh)
        menu.addAction(edit)
        menu.addAction(clear)
        refresh.setEnabled(bool(self.source_id))
        act = menu.exec(event.screenPos())
        if act == assign:
            entries = get_devices_for_type(self.name)
            if not entries:
                return
            items = [f"{e['id']} {e['ip']} ({e['ports']}p)" for e in entries]
            choice, ok = QInputDialog.getItem(None, 'Select device', 'Devices:', items, 0, False)
            if ok and choice:
                idx = items.index(choice)
                e = entries[idx]
                self.set_ip(e.get('ip'))
                self.set_subnet(e.get('subnet'))
                self.set_description(e.get('description'))
                self.set_ports(e.get('ports', 0))
                self.source_id = e.get('id')
                try:
                    if getattr(self.scene(), 'history_callback', None):
                        self.scene().history_callback()
                except Exception:
                    pass
        elif act == refresh:
            self.refresh_from_db()
        elif act == edit:
            self.edit_properties()
        elif act == clear:
            self.set_ip(None)
            self.source_id = None
            self.set_ports(0)


class NetworkScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setBackgroundBrush(QColor('#13222f'))
        self.nodes = []
        self.connections = []
        self._connecting = None  # (node, port_idx, port_item)
        self.last_click_pos = QPointF(0, 0)
        self.frame = None
        self.debug_mode = True
        self.create_frame()

    def create_frame(self):
        from PySide6.QtWidgets import QGraphicsRectItem
        rect = QGraphicsRectItem(-1000, -600, 2000, 1200)
        rect.setPen(QPen(QColor('#334155'), 2))
        rect.setBrush(QBrush(QColor(0, 0, 0, 0)))
        rect.setZValue(-1)
        self.addItem(rect)
        self.frame = rect

    def _select_device_type(self, parent=None):
        types = ['Router', 'Switch', 'Server', 'Firewall']
        choice, ok = QInputDialog.getItem(parent, 'Select device type', 'Device type:', types, 0, False)
        return choice if ok else None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.scenePos(), QTransform())
            if item is None or item is self.frame:
                self.last_click_pos = event.scenePos()
                choice = self._select_device_type(self.views()[0] if self.views() else None)
                if choice:
                    self.add_device(choice)
                    event.accept()
                    return
        super().mousePressEvent(event)

    def add_device(self, dtype, node_id=None):
        pos = self.last_click_pos
        node = DeviceNode(dtype, pos.x(), pos.y(), ports=48 if 'switch' in dtype.lower() else 4, node_id=node_id)
        self.addItem(node)
        self.nodes.append(node)
        try:
            if getattr(self, 'history_callback', None):
                self.history_callback()
        except Exception:
            pass
        return node

    def contextMenuEvent(self, event):
        self.last_click_pos = event.scenePos()
        menu = QMenu()
        for t in ['Router', 'Switch', 'Server', 'Firewall']:
            menu.addAction(QAction(t))
        act = menu.exec(event.screenPos())
        if not act:
            return
        dtype = act.text()
        if self.debug_mode:
            self.add_device(dtype)
            return
        # DB mode
        entries = get_devices_for_type(dtype)
        if not entries:
            return
        items = [f"{e['id']} {e['ip']} ({e['ports']}p)" for e in entries]
        choice, ok = QInputDialog.getItem(None, 'Select device', 'Devices:', items, 0, False)
        if ok and choice:
            idx = items.index(choice)
            e = entries[idx]
            n = self.add_device(dtype, node_id=e.get('id'))
            n.set_ports(e.get('ports', 0))
            n.set_ip(e.get('ip'))
            n.source_id = e.get('id')

    def port_clicked(self, node, port_index):
        if self._connecting is None:
            # start connection
            pi = None
            for p in node.port_items:
                if getattr(p, 'port_index', None) == port_index:
                    pi = p
                    break
            if pi:
                pi.setBrush(QBrush(QColor('#34d399')))
            self._connecting = (node, port_index, pi)
            return
        # finalize
        start_node, start_port, start_item = self._connecting
        if start_node is node and start_port == port_index:
            if start_item:
                start_item.set_connected(False)
            self._connecting = None
            return
        conn = Connection(self, (start_node, start_port), (node, port_index))
        start_node.connections.append(conn)
        node.connections.append(conn)
        self.connections.append(conn)
        try:
            conn.mark_connected(True)
        except Exception:
            pass
        if start_item:
            start_item.set_connected(True)
        self._connecting = None
        try:
            if getattr(self, 'history_callback', None):
                self.history_callback()
        except Exception:
            pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Network Planner')
        self.resize(1200, 820)
        self.scene = NetworkScene()
        self.scene.history_callback = self.push_history_state
        self._history = []
        self._history_index = -1
        self._history_suppress = False

        container = QWidget()
        layout = QHBoxLayout(container)

        sidebar = QWidget()
        sidebar.setObjectName('sidebar')
        sidebar.setFixedWidth(220)
        s_layout = QVBoxLayout(sidebar)
        s_layout.setContentsMargins(12, 12, 12, 12)
        s_layout.setSpacing(12)
        title = QLabel('Devices')
        title.setStyleSheet('font-size: 16px; font-weight: bold; color: #f8fafc;')
        s_layout.addWidget(title)

        self.device_selector = QComboBox()
        self.device_selector.setEditable(False)
        self.device_selector.setInsertPolicy(QComboBox.NoInsert)
        self.device_selector.addItem('Loading DB devices...')
        s_layout.addWidget(self.device_selector)

        refresh_btn = QPushButton('Refresh DB')
        refresh_btn.clicked.connect(self.load_db_devices)
        s_layout.addWidget(refresh_btn)

        add_btn = QPushButton('Add Selected')
        add_btn.clicked.connect(self.add_selected_device)
        s_layout.addWidget(add_btn)

        self.debug_checkbox = QCheckBox('Debug mode (free place)')
        self.debug_checkbox.setChecked(True)
        self.debug_checkbox.stateChanged.connect(self._on_debug_changed)
        s_layout.addWidget(self.debug_checkbox)

        s_layout.addStretch()
        layout.addWidget(sidebar)

        canvas = QWidget()
        c_layout = QVBoxLayout(canvas)
        c_layout.setContentsMargins(8, 8, 8, 8)

        # Top toolbar for quick actions
        tool_bar = QWidget()
        tool_bar.setObjectName('topToolbar')
        t_layout = QHBoxLayout(tool_bar)
        t_layout.setContentsMargins(0, 0, 0, 0)
        t_layout.setSpacing(8)
        btn_load = QPushButton('Load Mock')
        btn_clear = QPushButton('Clear Scene')
        btn_save = QPushButton('Save')
        btn_undo = QPushButton('Undo')
        btn_redo = QPushButton('Redo')
        btn_zoom_out = QPushButton('-')
        btn_zoom_in = QPushButton('+')
        btn_fit = QPushButton('Fit')
        btn_debug = QPushButton('Debug')
        t_layout.addWidget(btn_load)
        t_layout.addWidget(btn_clear)
        t_layout.addWidget(btn_save)
        t_layout.addWidget(btn_undo)
        t_layout.addWidget(btn_redo)
        t_layout.addStretch()
        t_layout.addWidget(btn_zoom_out)
        t_layout.addWidget(btn_zoom_in)
        t_layout.addWidget(btn_fit)
        t_layout.addWidget(btn_debug)
        c_layout.addWidget(tool_bar)

        self.view = GraphicsView(self.scene)
        self.view.setObjectName('canvasView')
        self.view.setStyleSheet('background: #17212b; border: 1px solid #354154; border-radius: 10px;')
        c_layout.addWidget(self.view)
        canvas.setStyleSheet('background:#13222f; border: 1px solid #2a3a50; border-radius:12px;')
        layout.addWidget(canvas, 1)
        
        # Details panel on the right
        details = QWidget()
        details.setObjectName('detailsPanel')
        details.setFixedWidth(320)
        details.setFixedWidth(300)
        d_layout = QFormLayout(details)
        d_layout.setLabelAlignment(Qt.AlignRight)
        d_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        d_layout.setContentsMargins(16, 16, 16, 16)
        d_layout.setSpacing(14)
        self.detail_id = QLineEdit()
        self.detail_id.setReadOnly(True)
        self.detail_name = QLineEdit()
        self.detail_ip = QLineEdit()
        self.detail_subnet = QLineEdit()
        self.detail_description = QLineEdit()
        self.detail_description.setMinimumHeight(30)
        self.detail_ports = QSpinBox()
        self.detail_ports.setRange(0, 256)
        self.detail_ports.setButtonSymbols(QSpinBox.PlusMinus)
        self.detail_source = QLineEdit()
        self.detail_source.setReadOnly(True)

        d_layout.addRow('ID:', self.detail_id)
        d_layout.addRow('Type / Name:', self.detail_name)
        d_layout.addRow('IP:', self.detail_ip)
        d_layout.addRow('Subnet:', self.detail_subnet)
        d_layout.addRow('Ports:', self.detail_ports)
        d_layout.addRow('Source ID:', self.detail_source)
        d_layout.addRow('Description:', self.detail_description)

        layout.addWidget(details)
        details.setStyleSheet('background:#1f2a34; border:1px solid #3b4b5c; border-radius:14px;')

        # selection/state
        self.selected_node = None
        self._db_devices = []
        self.scene.selectionChanged.connect(self._on_selection_changed)

        self.load_db_devices()

        # wire detail edits
        self.detail_name.editingFinished.connect(self._apply_details_to_node)
        self.detail_ip.editingFinished.connect(self._apply_details_to_node)
        self.detail_subnet.editingFinished.connect(self._apply_details_to_node)
        self.detail_description.editingFinished.connect(self._apply_details_to_node)
        self.detail_ports.valueChanged.connect(self._apply_details_to_node)

        # connect toolbar actions
        btn_load.clicked.connect(self.load_mock_devices)
        btn_clear.clicked.connect(self._clear_scene)
        btn_save.clicked.connect(self.save_state)
        btn_undo.clicked.connect(self.undo)
        btn_redo.clicked.connect(self.redo)
        btn_zoom_in.clicked.connect(lambda: self.view.scale(1.2, 1.2))
        btn_zoom_out.clicked.connect(lambda: self.view.scale(1 / 1.2, 1 / 1.2))
        btn_fit.clicked.connect(lambda: self.view.fitInView(self.scene.frame, Qt.KeepAspectRatio) if self.scene.frame is not None else None)
        btn_debug.clicked.connect(lambda: self.debug_checkbox.setChecked(not self.debug_checkbox.isChecked()))
        self._undo_button = btn_undo
        self._redo_button = btn_redo

        self.setCentralWidget(container)
        container.setStyleSheet('''
            QWidget#sidebar {
                background: #1d2a35;
                border: 1px solid #364552;
                border-radius: 16px;
            }
            QWidget#detailsPanel {
                background: #1c2834;
                border: 1px solid #364552;
                border-radius: 16px;
            }
            QWidget#topToolbar {
                background: transparent;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3e5b61, stop:1 #2f4a50);
                color: #e7ecef;
                border: 1px solid #47656e;
                border-radius: 10px;
                padding: 8px 12px;
                min-width: 70px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #517278, stop:1 #3f5e66);
            }
            QPushButton:pressed {
                background: #2d4e55;
            }
            QListWidget {
                background: #1c2b35;
                border: 1px solid #35607a;
                border-radius: 12px;
                color: #e7ecef;
                padding: 8px;
            }
            QLineEdit, QSpinBox {
                background: #1f2f3b;
                border: 1px solid #3f5662;
                border-radius: 10px;
                color: #e7ecef;
                padding: 8px;
            }
            QLabel {
                color: #cdd6df;
                font-size: 13px;
            }
            QCheckBox {
                color: #cdd6df;
            }
        ''')

        self.state_file = os.path.join(os.path.dirname(__file__), 'scene_state.json')
        self.load_state()
        if self.scene.nodes:
            self.push_history_state()
        # If no saved state, populate the scene with mock devices for convenience
        if not self.scene.nodes:
            try:
                self.load_mock_devices()
            except Exception:
                pass

    def _on_debug_changed(self, state):
        self.scene.debug_mode = bool(state)

    def _capture_scene_state(self):
        data = {'nodes': [], 'connections': []}
        for n in self.scene.nodes:
            p = n.pos()
            data['nodes'].append({
                'id': n.id,
                'name': n.name,
                'x': p.x(),
                'y': p.y(),
                'ports': n.ports,
                'ip': n.ip,
                'subnet': n.subnet,
                'description': n.description,
                'source_id': getattr(n, 'source_id', None),
            })
        for c in self.scene.connections:
            def refdict(ref):
                if isinstance(ref, tuple):
                    node, port = ref
                    return {'id': node.id, 'port': port}
                else:
                    return {'id': ref.id}
            data['connections'].append({
                'start': refdict(c.start_ref),
                'end': refdict(c.end_ref),
                'color': c.line.pen().color().name(),
            })
        return json.dumps(data)

    def push_history_state(self):
        if self._history_suppress:
            return
        if self._history_index < len(self._history) - 1:
            self._history = self._history[:self._history_index + 1]
        self._history.append(self._capture_scene_state())
        self._history_index = len(self._history) - 1
        self._update_undo_redo_buttons()

    def _update_undo_redo_buttons(self):
        if hasattr(self, '_undo_button'):
            self._undo_button.setEnabled(self._history_index > 0)
        if hasattr(self, '_redo_button'):
            self._redo_button.setEnabled(self._history_index < len(self._history) - 1)

    def undo(self):
        if self._history_index <= 0:
            return
        self._history_index -= 1
        self._restore_scene_state(self._history[self._history_index])
        self._update_undo_redo_buttons()

    def redo(self):
        if self._history_index >= len(self._history) - 1:
            return
        self._history_index += 1
        self._restore_scene_state(self._history[self._history_index])
        self._update_undo_redo_buttons()

    def _restore_scene_state(self, state_json):
        try:
            data = json.loads(state_json)
        except Exception:
            return
        self._history_suppress = True
        # clear existing scene items
        for c in list(self.scene.connections):
            try:
                self.scene.removeItem(c.line)
            except Exception:
                pass
        self.scene.connections.clear()
        for n in list(self.scene.nodes):
            try:
                self.scene.removeItem(n)
            except Exception:
                pass
        self.scene.nodes.clear()
        id_map = {}
        for nd in data.get('nodes', []):
            self.scene.last_click_pos = QPointF(nd.get('x', 0), nd.get('y', 0))
            node = self.scene.add_device(nd.get('name', 'Server'), node_id=nd.get('id'))
            node.set_ports(nd.get('ports', 0) or 0)
            node.set_ip(nd.get('ip'))
            node.set_subnet(nd.get('subnet'))
            node.set_description(nd.get('description'))
            node.source_id = nd.get('source_id')
            id_map[nd.get('id')] = node
        for cd in data.get('connections', []):
            s = cd.get('start') or {}
            e = cd.get('end') or {}
            if isinstance(s, dict):
                s_id = s.get('id'); s_port = s.get('port')
            else:
                s_id = s; s_port = None
            if isinstance(e, dict):
                e_id = e.get('id'); e_port = e.get('port')
            else:
                e_id = e; e_port = None
            s_node = id_map.get(s_id)
            e_node = id_map.get(e_id)
            if s_node and e_node:
                start_ref = (s_node, s_port) if s_port is not None else s_node
                end_ref = (e_node, e_port) if e_port is not None else e_node
                conn = Connection(self.scene, start_ref, end_ref, QColor(cd.get('color', '#00ff00')))
                if isinstance(start_ref, tuple):
                    start_ref[0].connections.append(conn)
                else:
                    start_ref.connections.append(conn)
                if isinstance(end_ref, tuple):
                    end_ref[0].connections.append(conn)
                else:
                    end_ref.connections.append(conn)
                self.scene.connections.append(conn)
        self._history_suppress = False
        self._on_selection_changed()

    def load_mock_devices(self):
        """Populate the scene with entries from MOCK_DB for quick testing."""
        self._history_suppress = True
        # Simple grid placement
        x = -240
        y = -160
        dx = 200
        dy = 140
        max_x = 480
        for dtype, entries in MOCK_DB.items():
            for e in entries:
                self.scene.last_click_pos = QPointF(x, y)
                n = self.scene.add_device(dtype, node_id=e.get('id'))
                n.set_ports(e.get('ports', 0))
                n.set_ip(e.get('ip'))
                n.set_subnet(e.get('subnet'))
                n.set_description(e.get('description'))
                n.source_id = e.get('id')
                x += dx
                if x > max_x:
                    x = -240
                    y += dy
        self._history_suppress = False
        self.push_history_state()

    def _clear_scene(self):
        """Remove all devices and connections from the scene."""
        # remove connection lines
        for c in list(self.scene.connections):
            try:
                self.scene.removeItem(c.line)
            except Exception:
                pass
        self.scene.connections.clear()
        # remove nodes
        for n in list(self.scene.nodes):
            try:
                self.scene.removeItem(n)
            except Exception:
                pass
        self.scene.nodes.clear()
        self.push_history_state()

    def _on_selection_changed(self):
        items = [it for it in self.scene.selectedItems() if isinstance(it, DeviceNode)]
        if not items:
            self.selected_node = None
            self._clear_details()
            return
        node = items[0]
        self.selected_node = node
        # populate detail fields
        self.detail_id.setText(str(node.id))
        self.detail_name.setText(str(node.name))
        self.detail_ip.setText(str(node.ip) if node.ip else '')
        self.detail_subnet.setText(str(node.subnet) if node.subnet else '')
        self.detail_description.setText(str(node.description) if node.description else '')
        self.detail_ports.setValue(int(node.ports or 0))
        self.detail_source.setText(str(node.source_id) if node.source_id else '')

    def _clear_details(self):
        self.detail_id.clear()
        self.detail_name.clear()
        self.detail_ip.clear()
        self.detail_subnet.clear()
        self.detail_description.clear()
        self.detail_ports.setValue(0)
        self.detail_source.clear()

    def load_db_devices(self):
        self._db_devices = []
        self.device_selector.clear()
        if api_handler is None:
            self.device_selector.addItem('Database unavailable')
            self.device_selector.setEnabled(False)
            return

        self.device_selector.setEnabled(True)
        try:
            entries = get_db_device_entries()
        except Exception:
            entries = []

        if not entries:
            self.device_selector.addItem('No DB devices found')
            self.device_selector.setEnabled(False)
            return

        self._db_devices = entries
        for entry in entries:
            label = entry.get('name') or entry.get('id')
            entry_id = entry.get('id')
            self.device_selector.addItem(f"{label} ({entry_id})")

    def _apply_details_to_node(self, *args):
        if not self.selected_node:
            return
        node = self.selected_node
        name = self.detail_name.text().strip()
        if name and name != node.name:
            node.name = name
            try:
                node.title.setPlainText(name)
            except Exception:
                pass
        ip = self.detail_ip.text().strip()
        node.set_ip(ip or None)
        subnet = self.detail_subnet.text().strip()
        node.set_subnet(subnet or None)
        desc = self.detail_description.text().strip()
        node.set_description(desc or None)
        ports = int(self.detail_ports.value() or 0)
        if ports != node.ports:
            node.set_ports(ports)
        self.push_history_state()

    def add_selected_device(self):
        if not self._db_devices:
            return
        index = self.device_selector.currentIndex()
        if index < 0 or index >= len(self._db_devices):
            return
        entry = self._db_devices[index]
        name = entry.get('name') or entry.get('id')
        center = self.view.mapToScene(self.view.viewport().rect().center())
        self.scene.last_click_pos = center
        node = self.scene.add_device(name)
        node.source_id = entry.get('id')
        if entry.get('ip'):
            node.set_ip(entry.get('ip'))
        if entry.get('subnet'):
            node.set_subnet(entry.get('subnet'))
        if entry.get('description'):
            node.set_description(entry.get('description'))
        if entry.get('ports') is not None:
            try:
                node.set_ports(int(entry.get('ports') or 0))
            except Exception:
                pass
        if node.ports > 24:
            node.setScale(0.9)

    def keyPressEvent(self, event):
        # connect selected nodes via 'C'
        if event.key() == Qt.Key_C:
            selected = [it for it in self.scene.selectedItems() if isinstance(it, DeviceNode)]
            if len(selected) == 2:
                a, b = selected
                a_center = a.mapToScene(QPointF(0, 0))
                b_center = b.mapToScene(QPointF(0, 0))
                a_port = None
                b_port = None
                if a.ports and b.ports:
                    a_choices = [str(i) for i in range(a.ports)]
                    b_choices = [str(i) for i in range(b.ports)]
                    a_sel, ok_a = QInputDialog.getItem(self, 'Select port', f'Port for {a.name}:', a_choices, 0, False)
                    if not ok_a:
                        return
                    b_sel, ok_b = QInputDialog.getItem(self, 'Select port', f'Port for {b.name}:', b_choices, 0, False)
                    if not ok_b:
                        return
                    try:
                        a_port = int(a_sel)
                        b_port = int(b_sel)
                    except Exception:
                        pass
                else:
                    a_port = a.nearest_port_to_scene_point(b_center)
                    b_port = b.nearest_port_to_scene_point(a_center)
                start = (a, a_port) if a_port is not None else a
                end = (b, b_port) if b_port is not None else b
                color = QColorDialog.getColor(QColor('#00ff00'), self, 'Connection color')
                if color.isValid():
                    conn = Connection(self.scene, start, end, color)
                    if isinstance(start, tuple):
                        start[0].connections.append(conn)
                    else:
                        start.connections.append(conn)
                    if isinstance(end, tuple):
                        end[0].connections.append(conn)
                    else:
                        end.connections.append(conn)
                    if conn not in self.scene.connections:
                        self.scene.connections.append(conn)
                    try:
                        conn.mark_connected(True)
                    except Exception:
                        pass
        elif event.key() == Qt.Key_Delete:
            selected = list(self.scene.selectedItems())
            for item in selected:
                if isinstance(item, DeviceNode):
                    for conn in list(item.connections):
                        try:
                            self.scene.removeItem(conn.line)
                        except Exception:
                            pass
                        # remove from other node
                        def other_node_of(c, node):
                            s = c.start_ref[0] if isinstance(c.start_ref, tuple) else c.start_ref
                            e = c.end_ref[0] if isinstance(c.end_ref, tuple) else c.end_ref
                            return s if s != node else e
                        other = other_node_of(conn, item)
                        if other and conn in other.connections:
                            other.connections.remove(conn)
                        if conn in self.scene.connections:
                            self.scene.connections.remove(conn)
                        try:
                            conn.mark_connected(False)
                        except Exception:
                            pass
                    try:
                        self.scene.removeItem(item)
                    except Exception:
                        pass
                    if item in self.scene.nodes:
                        self.scene.nodes.remove(item)
        elif event.key() == Qt.Key_S and (event.modifiers() & Qt.ControlModifier):
            self.save_state()
        super().keyPressEvent(event)

    def closeEvent(self, event):
        self.save_state()
        return super().closeEvent(event)

    def save_state(self):
        data = {'nodes': [], 'connections': []}
        for n in self.scene.nodes:
            p = n.pos()
            data['nodes'].append({
                'id': n.id,
                'name': n.name,
                'x': p.x(),
                'y': p.y(),
                'ports': n.ports,
                'ip': n.ip,
                'subnet': n.subnet,
                'description': n.description,
                'source_id': getattr(n, 'source_id', None),
            })
        for c in self.scene.connections:
            def refdict(ref):
                if isinstance(ref, tuple):
                    node, port = ref
                    return {'id': node.id, 'port': port}
                else:
                    return {'id': ref.id}
            data['connections'].append({'start': refdict(c.start_ref), 'end': refdict(c.end_ref), 'color': c.line.pen().color().name()})
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print('Failed to save state:', e)

    def load_state(self):
        if not os.path.exists(self.state_file):
            return
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return
        self._history_suppress = True
        # clear
        for c in list(self.scene.connections):
            try:
                self.scene.removeItem(c.line)
            except Exception:
                pass
        self.scene.connections.clear()
        for n in list(self.scene.nodes):
            try:
                self.scene.removeItem(n)
            except Exception:
                pass
        self.scene.nodes.clear()
        id_map = {}
        for nd in data.get('nodes', []):
            self.scene.last_click_pos = QPointF(nd.get('x', 0), nd.get('y', 0))
            node = self.scene.add_device(nd.get('name', 'Server'), node_id=nd.get('id'))
            node.set_ports(nd.get('ports', 0) or 0)
            if nd.get('ip'):
                node.set_ip(nd.get('ip'))
            if nd.get('subnet'):
                node.set_subnet(nd.get('subnet'))
            if nd.get('description'):
                node.set_description(nd.get('description'))
            node.source_id = nd.get('source_id')
            id_map[nd.get('id')] = node
        for cd in data.get('connections', []):
            s = cd.get('start') or {}
            e = cd.get('end') or {}
            if isinstance(s, dict):
                s_id = s.get('id'); s_port = s.get('port')
            else:
                s_id = s; s_port = None
            if isinstance(e, dict):
                e_id = e.get('id'); e_port = e.get('port')
            else:
                e_id = e; e_port = None
            s_node = id_map.get(s_id)
            e_node = id_map.get(e_id)
            if s_node and e_node:
                start_ref = (s_node, s_port) if s_port is not None else s_node
                end_ref = (e_node, e_port) if e_port is not None else e_node
                conn = Connection(self.scene, start_ref, end_ref, QColor(cd.get('color', '#00ff00')))
                if isinstance(start_ref, tuple):
                    start_ref[0].connections.append(conn)
                else:
                    start_ref.connections.append(conn)
                if isinstance(end_ref, tuple):
                    end_ref[0].connections.append(conn)
                else:
                    end_ref.connections.append(conn)
                self.scene.connections.append(conn)
        self._history_suppress = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())