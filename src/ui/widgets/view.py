from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsView,
)
from PyQt6.QtGui import QMouseEvent, QWheelEvent
from PyQt6.QtCore import QPoint, QPointF, Qt
import settings


class SceneView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, parent: QWidget = None):
        super().__init__(scene, parent)
        self.__shift_mouse_coords: QPointF = None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == event.buttons().RightButton:
            self.__shift_mouse_coords = event.pos().toPointF()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.__shift_mouse_coords is not None:
            delta: QPointF = self.__shift_mouse_coords - event.pos().toPointF()
            trasform = self.transform()
            delta_x = delta.x() / trasform.m11()
            delta_y = delta.y() / trasform.m22()
            self.setSceneRect(self.sceneRect().translated(delta_x, delta_y))
            self.__shift_mouse_coords = event.pos().toPointF()
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == event.buttons().RightButton:
            self.__shift_mouse_coords = None
        return super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        previous_position = self.mapToScene(event.position().toPoint())

        zoom_factor = settings.ZOOM_IN_FACTOR
        if event.angleDelta().y() < 0:
            zoom_factor = settings.ZOOM_OUT_FACTOR
        self.scale(zoom_factor, zoom_factor)

        new_position = self.mapToScene(event.position().toPoint())

        delta: QPointF = new_position - previous_position
        delta_x = delta.x()
        delta_y = delta.y()
        self.translate(delta_x, delta_y)
        return super().wheelEvent(event)
