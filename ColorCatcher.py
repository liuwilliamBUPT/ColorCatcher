from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QGuiApplication, QColor, QCursor
from PyQt5.QtWidgets import QWidget, QApplication

import ui_colorcatcher

import cv2
import numpy as np


class ColorCatcher(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = ui_colorcatcher.Ui_ColorCatcher()
        self.ui.setupUi(self)
        self.ui.lineEditMark.setText("Press space to mark!")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.catch)
        self.timer.start(100)
        self.nowColor = None
        self.setCursor(Qt.CrossCursor)
        self.show()

    def catch(self):
        x = QCursor.pos().x()
        y = QCursor.pos().y()
        pixmap = QGuiApplication.primaryScreen().grabWindow(QApplication.
                                                            desktop().
                                                            winId(), x, y, 1, 1)
        if not pixmap.isNull():
            image = pixmap.toImage()
            if not image.isNull():
                if image.valid(0, 0):
                    color = QColor(image.pixel(0, 0))
                    r, g, b, _ = color.getRgb()
                    h, s, v = list(cv2.cvtColor(
                        np.array([[[r, g, b]]]).astype(np.uint8),
                        cv2.COLOR_RGB2HSV).reshape(3))
                    self.nowColor = color
                    self.ui.lineEditMove.setText(
                        '(%d, %d, %d) %s \n '
                        'HSV in cv2 (%d, %d, %d)' % (r, g, b,
                                                    color.name().upper(),
                                                    h, s, v))
                    self.ui.lineEditMove.setStyleSheet('QLineEdit{border:2px '
                                                       'solid %s;}' % (
                                                           color.name()))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.ui.lineEditMark.setText(self.ui.lineEditMove.text())
            self.ui.lineEditMark.setStyleSheet(
                'QLineEdit{border:2px solid %s;}' % (self.nowColor.name()))
