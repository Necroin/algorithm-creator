import settings
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsSceneHoverEvent,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)
from PyQt6.QtCore import Qt, QPointF, QRectF, QVariant
from PyQt6.QtGui import QPainter, QBrush, QPen
from collections.abc import Callable
import typing
from enum import Enum


class DynamicPoint:
    def __init__(self, x: Callable[[], float], y: Callable[[], float]):
        self.__x = x
        self.__y = y

    def x(self) -> float:
        return self.__x()

    def y(self) -> float:
        return self.__y()


class ResizePoint(QGraphicsItem):
    Direction = Enum("Direction", ["Vertical", "Horizontal", "All"])

    def __init__(
        self,
        parent: QGraphicsItem,
        point: DynamicPoint,
        cursor: Qt.CursorShape,
        transform: Callable[[QPointF], None],
        direction: Direction,
    ):
        super().__init__(parent)
        self.__parent = parent
        self.__point = point
        self.__transform = transform
        self.__cursor = cursor
        self.__size = settings.DEFAULT_RESIZE_POINT_SIZE
        self.__direction = direction
        super().setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        super().setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        super().setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        super().setAcceptHoverEvents(True)
        self.hide()
        self.pen = QPen(Qt.GlobalColor.darkBlue)
        self.brush = QBrush(Qt.GlobalColor.blue)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ):
        painter.save()
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawEllipse(
            QPointF(
                self.__point.x() - self.pos().x(), self.__point.y() - self.pos().y()
            ),
            self.__size,
            self.__size,
        )
        widget.update()
        painter.restore()

    def boundingRect(self) -> QRectF:
        return QRectF(
            self.__point.x() - self.__size - self.pos().x(),
            self.__point.y() - self.__size - self.pos().y(),
            self.__size * 2,
            self.__size * 2,
        )

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        super().setCursor(self.__cursor)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        super().setCursor(Qt.CursorShape.ArrowCursor)
        return super().hoverLeaveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == event.buttons().LeftButton:
            self.setSelected(True)
            self.__parent.setSelected(False)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == event.buttons().LeftButton:
            self.setSelected(False)
            self.__parent.setSelected(True)
        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return super().mouseMoveEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverMoveEvent(event)

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: QVariant
    ) -> QVariant:
        if change == change.ItemPositionChange:
            if not self.isHorizontal():
                typing.cast(QPointF, value).setX(0)
            if not self.isVertical():
                typing.cast(QPointF, value).setY(0)
            if self.isSelected():
                self.__transform(value - self.pos())
        return super().itemChange(change, value)

    def isVertical(self) -> bool:
        if (
            self.__direction == self.Direction.Vertical
            or self.__direction == self.Direction.All
        ):
            return True
        return False

    def isHorizontal(self) -> bool:
        if (
            self.__direction == self.Direction.Horizontal
            or self.__direction == self.Direction.All
        ):
            return True
        return False
