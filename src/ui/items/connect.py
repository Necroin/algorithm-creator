import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsLineItem,
    QStyleOptionGraphicsItem,
    QWidget,
    QGraphicsSceneMouseEvent,
    QGraphicsSceneHoverEvent,
)
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QPointF, QLineF, QRectF, QVariant, Qt
from ui.utils.point import DynamicPoint, ResizePoint
import settings


class ConnectLineItem(QGraphicsLineItem):
    def __init__(self, line: QLineF, parent: QGraphicsItem = None):
        super().__init__(line, parent)
        super().setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        super().setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        super().setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        super().setAcceptHoverEvents(True)
        self.__shift_mouse_coords = QPointF(0, 0)
        self.delta_accum = QPointF(0, 0)
        self.resize_points: list[ResizePoint] = []

        def transform1(delta: QPointF):
            # delta_x = (
            #    round((delta.x() + self.delta_accum.x()) / settings.GRID_STEP)
            #    * settings.GRID_STEP
            # )
            # delta_y = (
            #    round((delta.y() + self.delta_accum.y()) / settings.GRID_STEP)
            #    * settings.GRID_STEP
            # )
            #
            # if delta_x == 0 and delta.x() != 0:
            #    self.delta_accum.setX(self.delta_accum.x() + delta.x())
            # if delta_x != 0:
            #    self.delta_accum.setX(self.delta_accum.x() - delta_x)
            #
            # if delta_y == 0 and delta.y() != 0:
            #    self.delta_accum.setY(self.delta_accum.y() + delta.y())
            # if delta_y != 0:
            #    self.delta_accum.setY(self.delta_accum.y() - delta_y)

            line = self.line()
            line.setP1(line.p1() + delta)
            self.prepareGeometryChange()
            self.setLine(line)

        self.resize_points.append(
            ResizePoint(
                self,
                DynamicPoint(
                    lambda: self.boundingLine().x1(),
                    lambda: self.boundingLine().y1(),
                ),
                Qt.CursorShape.PointingHandCursor,
                transform1,
                ResizePoint.Direction.All,
            )
        )

        def transform2(delta: QPointF):
            line = self.line()
            line.setP2(line.p2() + delta)
            self.prepareGeometryChange()
            self.setLine(line)

        self.resize_points.append(
            ResizePoint(
                self,
                DynamicPoint(
                    lambda: self.boundingLine().x2(),
                    lambda: self.boundingLine().y2(),
                ),
                Qt.CursorShape.PointingHandCursor,
                transform2,
                ResizePoint.Direction.All,
            )
        )

    def boundingLine(self) -> QLineF:
        bounding_rect = super().line()
        bounding_rect_x1 = bounding_rect.x1()
        bounding_rect_y1 = bounding_rect.y1()
        bounding_rect_x2 = bounding_rect.x2()
        bounding_rect_y2 = bounding_rect.y2()
        bounding_rect_x1 = (
            round(bounding_rect_x1 / settings.GRID_STEP) * settings.GRID_STEP
        )
        bounding_rect_y1 = (
            round(bounding_rect_y1 / settings.GRID_STEP) * settings.GRID_STEP
        )
        bounding_rect_x2 = (
            round(bounding_rect_x2 / settings.GRID_STEP) * settings.GRID_STEP
        )
        bounding_rect_y2 = (
            round(bounding_rect_y2 / settings.GRID_STEP) * settings.GRID_STEP
        )
        return QLineF(
            bounding_rect_x1, bounding_rect_y1, bounding_rect_x2, bounding_rect_y2
        )

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: QVariant
    ) -> QVariant:
        if change == change.ItemSelectedHasChanged:
            if value == True:
                for resize_point in self.resize_points:
                    resize_point.show()
            else:
                for resize_point in self.resize_points:
                    if not resize_point.isSelected():
                        resize_point.hide()

        if change == change.ItemPositionChange:
            delta: QPointF = value
            delta_x = round(delta.x() / settings.GRID_STEP) * settings.GRID_STEP
            delta_y = round(delta.y() / settings.GRID_STEP) * settings.GRID_STEP
            return QPointF(delta_x, delta_y)
        return super().itemChange(change, value)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        super().setCursor(Qt.CursorShape.SizeAllCursor)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        super().setCursor(Qt.CursorShape.ArrowCursor)
        return super().hoverLeaveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == event.buttons().LeftButton:
            self.__shift_mouse_coords = super().pos() - super().mapToScene(event.pos())
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == event.buttons().LeftButton:
            self.setPos(event.pos() + super().mapToScene(self.__shift_mouse_coords))
        return super().mouseMoveEvent(event)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawLine(self.boundingLine())
        widget.update()
        painter.restore()
