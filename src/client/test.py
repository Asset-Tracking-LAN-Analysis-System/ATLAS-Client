import sys
import os
import json
import uuid

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QBrush, QPen, QAction, QPixmap, QPainter
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
    QCheckBox,
)

# Simple mock DB — replace with real API via get_devices_for_type
MOCK_DB = {
    'Router': [
        {'id': 'r1', 'ip': '10.0.0.1', 'ports': 4},
        {'id': 'r2', 'ip': '10.0.0.2', 'ports': 8},
    ],
    'Switch': [
        {'id': 'sw1', 'ip': '10.0.1.1', 'ports': 48},
        {'id': 'sw2', 'ip': '10.0.1.2', 'ports': 24},
    ],
    'Server': [
        {'id': 'srv1', 'ip': '10.0.2.10', 'ports': 2},
    ],
}


def get_devices_for_type(device_type):
    """Pluggable adapter: return list of dicts with keys id, ip, ports."""
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

    def set_ip(self, ip):
        self.ip = ip
        try:
            if self.ip_label and self.ip_label.scene() is not None:
                self.scene().removeItem(self.ip_label)
        except Exception:
            pass
        self.ip_label = QGraphicsTextItem(str(ip), self)
        self.ip_label.setDefaultTextColor(Qt.lightGray)
        self.ip_label.setPos(-30, 58)

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
        clear = QAction('Clear assignment')
        menu.addAction(assign)
        menu.addAction(clear)
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
                self.set_ports(e.get('ports', 0))
                self.source_id = e.get('id')
        elif act == clear:
            try:
                if self.ip_label and self.ip_label.scene() is not None:
                    self.scene().removeItem(self.ip_label)
            except Exception:
                pass
            self.ip = None
            self.source_id = None
            self.set_ports(0)


class NetworkScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setBackgroundBrush(QColor('#0f172a'))
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

    def add_device(self, dtype, node_id=None):
        pos = self.last_click_pos
        node = DeviceNode(dtype, pos.x(), pos.y(), ports=48 if 'switch' in dtype.lower() else 4, node_id=node_id)
        self.addItem(node)
        self.nodes.append(node)
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Network Planner')
        self.resize(1200, 800)
        self.scene = NetworkScene()

        container = QWidget()
        layout = QHBoxLayout(container)

        sidebar = QWidget()
        s_layout = QVBoxLayout(sidebar)
        s_layout.setContentsMargins(6, 6, 6, 6)
        s_layout.addWidget(QLabel('Devices'))

        self.device_list = QListWidget()
        for t in ['Router', 'Switch', 'Server', 'Firewall']:
            self.device_list.addItem(QListWidgetItem(t))
        s_layout.addWidget(self.device_list)

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
        self.view = GraphicsView(self.scene)
        c_layout.addWidget(self.view)
        canvas.setStyleSheet('background:#0b1220; border: 2px solid #334155; border-radius:4px;')
        layout.addWidget(canvas, 1)

        self.setCentralWidget(container)

        self.state_file = os.path.join(os.path.dirname(__file__), 'scene_state.json')
        self.load_state()

    def _on_debug_changed(self, state):
        self.scene.debug_mode = bool(state)

    def add_selected_device(self):
        item = self.device_list.currentItem()
        if not item:
            return
        center = self.view.mapToScene(self.view.viewport().rect().center())
        self.scene.last_click_pos = center
        node = self.scene.add_device(item.text())
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
            data['nodes'].append({'id': n.id, 'name': n.name, 'x': p.x(), 'y': p.y(), 'ports': n.ports, 'ip': n.ip, 'source_id': getattr(n, 'source_id', None)})
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())