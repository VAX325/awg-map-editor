import sys

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

# UI
import map_editor

# Loader
import MapLoader

# Main class
class MapEditor(QtWidgets.QMainWindow, map_editor.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionExit.triggered.connect(self.Exit)
        self.actionOpen.triggered.connect(self.OpenRaw)
        self.actionNew.triggered.connect(self.New)
        self.EntityProps.setDisabled(True)

        self.model = QtGui.QStandardItemModel()
        # self.populateTree(tree, model.invisibleRootItem())
        self.EntityList.setModel(self.model)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, '')
        self.EntityList.expandAll()
        self.EntityList.selectionModel().selectionChanged.connect(self.onSelectionChanged)

        #self.labNpix = []
        self.objs = []

        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setWidget(self.Workspace)
        self.scroll_area.resize(self.Workspace.width(), self.Workspace.height())
        self.scroll_area.show()

        self.workspace_background = QtWidgets.QLabel(self.Workspace)
        self.workspace_background_pixmap = QtGui.QPixmap("data/Textures/background.jpeg")
        self.workspace_background.setPixmap(self.workspace_background_pixmap)
        self.workspace_background.move(0, 0)
        self.workspace_background_pixmap = self.workspace_background_pixmap.scaled(1366*10, 768*10)
        self.workspace_background.setPixmap(self.workspace_background_pixmap)
        self.workspace_background.resize(1366*10, 768*10)

        #self.labNpix.append((pixmap_test ,label))

        self.groups = []
        self.elements = []

        self.scale = 0.5
        self.scale_label.setText("Scale is: {0}".format(self.scale))

        self.scale_plus.clicked.connect(self.scale_plus_action)
        self.scale_minus.clicked.connect(self.scale_minus_action)

        self.Workspace.setMinimumWidth(1366 * 10)
        self.Workspace.setMinimumHeight(768 * 10)

       # self.Workspace.paintEvent = self.paintEvent

        #END
        #timer = QtCore.QTimer(self, timeout=self.draw, interval=100)
        #timer.start()

    def populateTree(self, children, parent):
        for child in children:
            for group in self.groups:
                if child == group[0]:
                    obj = children[child]
                    for obj_real in obj:
                        child_item = QtGui.QStandardItem(obj_real)
                        group[1].appendRow(child_item)
                        return

            child_item = QtGui.QStandardItem(child)
            parent.appendRow(child_item)
            if isinstance(children, dict):
                self.groups.append([child ,child_item])
                self.populateTree(children[child], child_item)

    def change_current_action(self, action):
        self.CurrentAction.setText(action)

    def change_current_action_procent(self, procent):
        self.CurrentActionProgress.setValue(procent)

    def current_action_done(self):
        self.CurrentAction.setText("None")

    def scale_plus_action(self):
        if self.scale > 1.4:
            self.scale = 1.5
        else:
            self.scale = self.scale + 0.1
        self.scale = round(self.scale, 1)
        self.apply_scale()

    def scale_minus_action(self):
        if self.scale < 0.2:
            self.scale = 0.1
        else:
            self.scale = self.scale - 0.1
        self.scale = round(self.scale, 1)
        self.apply_scale()

    def apply_scale(self):
        for element in self.elements:
            # element[1][0]  # Label
            # element[1][1]  # Pixmap

            # element[2][0][0] - orig x
            # element[2][0][1] - curr x

            # element[2][1][0] - orig y
            # element[2][1][1] - curr y

            # element[2][2][0] - orig w
            # element[2][2][1] - curr w

            # element[2][3][0] - orig h
            # element[2][3][1] - curr h

            x = element[2][0][0] * self.scale + (1366*10 / 2)
            y = element[2][1][0] * self.scale + (768*10 / 2)
            w = element[2][2][0] * self.scale
            h = element[2][3][0] * self.scale

            element[2][0][1] = x
            element[2][1][1] = y
            element[2][2][1] = w
            element[2][3][1] = h

            pixmap = element[1][1].scaled(w, h)
            element[1][0].setPixmap(pixmap)
            element[1][0].resize(w, h)
            element[1][0].move(x, y)
            element[1][0].show()

        #if len(self.elements) >= 1:
        #    width = self._update_width_area()
        #    height = self._update_height_area()

        #    self.workspace_background.resize(width, height)

        self.scale_label.setText("Scale is: {0}".format(self.scale))

    def onSelectionChanged(self, *args):
        for sel in self.EntityList.selectedIndexes():
            val = "/"+sel.data()
            while sel.parent().isValid():
                sel = sel.parent()
                val = "/"+ sel.data()+ val
            print(val)

    def Exit(self):
        buttonReply = QtWidgets.QMessageBox.question(self, "Are you sure", "You sure wan't to exit?\nAll unsaved data will be erased from existense!")
        if buttonReply == QtWidgets.QMessageBox.Yes:
            sys.exit(0)

    #def draw(self):
    #    for pixmap_orig, label in self.labNpix:
    #        pixmap = pixmap_orig.copy()
    #        painter = QtGui.QPainter(pixmap)
    #        painter.setRenderHints(
    #            QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform
    #        )
    #        painter.translate(pixmap.rect().center())
    #        painter.rotate(0)
    #        painter.translate(-pixmap.rect().center())
    #        painter.drawPixmap(QtCore.QPoint(), pixmap_orig)
    #        painter.end()
    #        label.setPixmap(pixmap)
    #    self.update()
        
    def New(self):
        label = QtWidgets.QLabel(self.Workspace)
        pixmap = QtGui.QPixmap("data/Textures/r_devs_1.png")
        label.setPixmap(pixmap)
        label.move(110, 100)
        label.show()
        self.objs.append(label)
        #self.labNpix.append((pixmap, label))

    def add_image_to_workspace(self, image, x, y, w, h, id):
        label = QtWidgets.QLabel(self.Workspace)
        pixmap = QtGui.QPixmap(image)

        _w = w * self.scale
        _h = h * self.scale
        _x = x * self.scale + (1366*10 / 2)
        _y = y * self.scale + (768*10 / 2)

        pixmap = pixmap.scaled(_w, _h)
        label.setPixmap(pixmap)
        label.resize(_w, _h)
        label.move(_x, _y)
        label.show()

        self.elements.append([id, (label, pixmap), ([x, _x], [y, _y], [w, _w], [h, _h])])
        self.objs.append(label)

    def OpenRaw(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Select raw map file...", "","Raw Map Files (*.rlvl);;All Files (*)", options=options)
        if filename:
            self.my_map, self.params = MapLoader.LoadMap(filename)

        for element in self.my_map:
            lst = {element[1][2]: {(element[1][0] + element[1][1])}}
            self.populateTree(lst, self.model.invisibleRootItem())

            if element[0] == 1:  # WorldRectangleRigid
                self.add_image_to_workspace("data/Textures/r_devs_1.png", int(element[1][3]), int(element[1][4]), int(element[1][5]), int(element[1][6]), (element[1][0] + element[1][1]))
            elif element[0] == 2:
                w = 128
                h = 128
                self.add_image_to_workspace("data/Textures/r_devs_1.png", int(element[1][3]), int(element[1][4]), h, w, (element[1][0] + element[1][1]))

        #width = self._update_width_area()
        #height = self._update_height_area()

        #self.workspace_background.resize(width, height)

        #Refocusing
        self.scroll_area.horizontalScrollBar().setValue(1366*10/2)
        self.scroll_area.verticalScrollBar().setValue(768*10/2)

    def _calculate_width(self, widget):
        widget_width = widget.sizeHint().width()
        sb_width = self.scroll_area.verticalScrollBar().sizeHint().width()
        return widget_width + sb_width + 20

    def _calculate_height(self, widget):
        widget_height = widget.sizeHint().height()
        sb_height = self.scroll_area.verticalScrollBar().sizeHint().height()
        return widget_height + sb_height + 20
 
    def _update_width_area(self):
        new_width = [self._calculate_width(i) for i in self.objs]
        self.Workspace.setMinimumWidth(max(new_width))
        return max(new_width)

    def _update_height_area(self):
        new_height = [self._calculate_height(i) for i in self.objs]
        self.Workspace.setMinimumHeight(max(new_height))
        return max(new_height)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MapEditor()
    window.showMaximized()
    sys.exit(app.exec_())
