from PyQt6 import QtCore
import settings
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsSceneHoverEvent,
    QGraphicsTextItem,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)
from PyQt6.QtCore import Qt, QPointF, QRectF, QVariant
from PyQt6.QtGui import QTextOption, QFocusEvent, QPainter, QBrush
from ui.utils.point import DynamicPoint, ResizePoint


class TextItem(QGraphicsTextItem):
    def __init__(self, parent: QGraphicsItem):
        super().__init__(parent)
        self.__parent = parent
        self.__edit_mode = False
        super().setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        super().document().setDefaultTextOption(
            QTextOption(Qt.AlignmentFlag.AlignHCenter)
        )
        super().setTextWidth(self.__parent.boundingRect().width())

        self.updatePosition()
        self.document().contentsChanged.connect(lambda: self.updatePosition())

    def updatePosition(self):
        self.setTextWidth(-1)
        parent_rectangle = self.__parent.boundingRect()
        my_rectange = self.boundingRect()
        delta_x = (parent_rectangle.width() - my_rectange.width()) / 2
        delta_y = (parent_rectangle.height() - my_rectange.height()) / 2
        self.setPos(parent_rectangle.x() + delta_x, parent_rectangle.y() + delta_y)
        self.setTextWidth(my_rectange.width())

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.__edit_mode = True
        return super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        super().setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.__edit_mode = False
        return super().focusOutEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.__edit_mode == False:
            super().setTextInteractionFlags(
                Qt.TextInteractionFlag.TextEditorInteraction
            )
            super().setFocus()
        return super().mouseDoubleClickEvent(event)


class AlgorithmItem(QGraphicsRectItem):
    def __init__(self, rectangle: QRectF) -> None:
        super().__init__(rectangle)
        super().setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        super().setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        super().setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        super().setAcceptHoverEvents(True)
        self.__shift_mouse_coords = QPointF(0, 0)
        self.text_item = TextItem(self)
        self.resize_points: list[ResizePoint] = []
        self.white_brush = QBrush(Qt.GlobalColor.white)

        def transform_top_left(delta: QPointF):
            delta_x = delta.x()
            delta_y = delta.y()

            if (
                delta.x() > 0
                and self.rect().width() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_x = 0

            if (
                delta.y() > 0
                and self.rect().height() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_y = 0

            self.prepareGeometryChange()
            self.setRect(self.rect().adjusted(delta_x, delta_y, 0, 0))
            self.text_item.updatePosition()

        self.resize_points.append(
            ResizePoint(
                self,
                DynamicPoint(
                    lambda: self.boundingRect().topLeft().x(),
                    lambda: self.boundingRect().topLeft().y(),
                ),
                Qt.CursorShape.SizeFDiagCursor,
                transform_top_left,
                ResizePoint.Direction.All,
            )
        )

        def transform_top_rigth(delta: QPointF):
            delta_x = delta.x()
            delta_y = delta.y()

            if (
                delta.x() < 0
                and self.rect().width() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_x = 0

            if (
                delta.y() > 0
                and self.rect().height() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_y = 0

            self.prepareGeometryChange()
            self.setRect(self.rect().adjusted(0, delta_y, delta_x, 0))
            self.text_item.updatePosition()

        self.resize_points.append(
            ResizePoint(
                self,
                DynamicPoint(
                    lambda: self.boundingRect().topRight().x(),
                    lambda: self.boundingRect().topRight().y(),
                ),
                Qt.CursorShape.SizeBDiagCursor,
                transform_top_rigth,
                ResizePoint.Direction.All,
            )
        )

        def transform_bottom_left(delta: QPointF):
            delta_x = delta.x()
            delta_y = delta.y()

            if (
                delta.x() > 0
                and self.rect().width() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_x = 0

            if (
                delta.y() < 0
                and self.rect().height() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_y = 0

            self.prepareGeometryChange()
            self.setRect(self.rect().adjusted(delta_x, 0, 0, delta_y))
            self.text_item.updatePosition()

        self.resize_points.append(
            ResizePoint(
                self,
                DynamicPoint(
                    lambda: self.boundingRect().bottomLeft().x(),
                    lambda: self.boundingRect().bottomLeft().y(),
                ),
                Qt.CursorShape.SizeBDiagCursor,
                transform_bottom_left,
                ResizePoint.Direction.All,
            )
        )

        def trasform_bottom_rigth(delta: QPointF):
            delta_x = delta.x()
            delta_y = delta.y()

            if (
                delta.x() < 0
                and self.rect().width() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_x = 0

            if (
                delta.y() < 0
                and self.rect().height() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_y = 0

            self.prepareGeometryChange()
            self.setRect(self.rect().adjusted(0, 0, delta_x, delta_y))
            self.text_item.updatePosition()

        self.resize_points.append(
            ResizePoint(
                self,
                DynamicPoint(
                    lambda: self.boundingRect().bottomRight().x(),
                    lambda: self.boundingRect().bottomRight().y(),
                ),
                Qt.CursorShape.SizeFDiagCursor,
                trasform_bottom_rigth,
                ResizePoint.Direction.All,
            )
        )

        def transform_top_middle(delta: QPointF):
            delta_y = delta.y()

            if (
                delta.y() > 0
                and self.rect().height() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_y = 0

            self.prepareGeometryChange()
            self.setRect(self.rect().adjusted(0, delta_y, 0, 0))
            self.text_item.updatePosition()

        self.resize_points.append(
            ResizePoint(
                self,
                DynamicPoint(
                    lambda: self.boundingRect().topLeft().x()
                    + self.boundingRect().width() / 2,
                    lambda: self.boundingRect().topLeft().y(),
                ),
                Qt.CursorShape.SizeVerCursor,
                transform_top_middle,
                ResizePoint.Direction.Vertical,
            )
        )

        def transform_botton_middle(delta: QPointF):
            delta_y = delta.y()

            if (
                delta.y() < 0
                and self.rect().height() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_y = 0

            self.prepareGeometryChange()
            self.setRect(self.rect().adjusted(0, 0, 0, delta_y))
            self.text_item.updatePosition()

        self.resize_points.append(
            ResizePoint(
                self,
                DynamicPoint(
                    lambda: self.boundingRect().bottomLeft().x()
                    + self.boundingRect().width() / 2,
                    lambda: self.boundingRect().bottomLeft().y(),
                ),
                Qt.CursorShape.SizeVerCursor,
                transform_botton_middle,
                ResizePoint.Direction.Vertical,
            )
        )

        def transform_left_middle(delta: QPointF):
            delta_x = delta.x()

            if (
                delta.x() > 0
                and self.rect().width() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_x = 0

            self.prepareGeometryChange()
            self.setRect(self.rect().adjusted(delta_x, 0, 0, 0))
            self.text_item.updatePosition()

        self.resize_points.append(
            ResizePoint(
                self,
                DynamicPoint(
                    lambda: self.boundingRect().topLeft().x(),
                    lambda: self.boundingRect().topLeft().y()
                    + self.boundingRect().height() / 2,
                ),
                Qt.CursorShape.SizeHorCursor,
                transform_left_middle,
                ResizePoint.Direction.Horizontal,
            )
        )

        def transform_right_middle(delta: QPointF):
            delta_x = delta.x()

            if (
                delta.x() < 0
                and self.rect().width() < settings.DEFAULT_RESIZE_POINT_SIZE * 2
            ):
                delta_x = 0

            self.prepareGeometryChange()
            self.setRect(self.rect().adjusted(0, 0, delta_x, 0))
            self.text_item.updatePosition()

        self.resize_points.append(
            ResizePoint(
                self,
                DynamicPoint(
                    lambda: self.boundingRect().topRight().x(),
                    lambda: self.boundingRect().topRight().y()
                    + self.boundingRect().height() / 2,
                ),
                Qt.CursorShape.SizeHorCursor,
                transform_right_middle,
                ResizePoint.Direction.Horizontal,
            )
        )

    def boundingRect(self) -> QRectF:
        bounding_rect = super().boundingRect()
        bounding_rect_x = bounding_rect.x()
        bounding_rect_y = bounding_rect.y()
        bounding_rect_width = bounding_rect.width()
        bounding_rect_height = bounding_rect.height()
        bounding_rect_x = (
            round(bounding_rect_x / settings.GRID_STEP) * settings.GRID_STEP
        )
        bounding_rect_y = (
            round(bounding_rect_y / settings.GRID_STEP) * settings.GRID_STEP
        )
        bounding_rect_width = (
            round(bounding_rect_width / settings.GRID_STEP) * settings.GRID_STEP
        )
        bounding_rect_height = (
            round(bounding_rect_height / settings.GRID_STEP) * settings.GRID_STEP
        )
        return QRectF(
            bounding_rect_x, bounding_rect_y, bounding_rect_width, bounding_rect_height
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

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == event.buttons().LeftButton:
            self.__shift_mouse_coords = super().pos() - super().mapToScene(event.pos())
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == event.buttons().LeftButton:
            self.setPos(event.pos() + super().mapToScene(self.__shift_mouse_coords))
        return super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == event.buttons().LeftButton:
            self.text_item.mouseDoubleClickEvent(event)
        return super().mouseDoubleClickEvent(event)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        super().setCursor(Qt.CursorShape.SizeAllCursor)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        super().setCursor(Qt.CursorShape.ArrowCursor)
        return super().hoverLeaveEvent(event)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.isSelected():
            painter.setPen(Qt.GlobalColor.blue)
            painter.drawRect(self.boundingRect())
        widget.update()
        painter.restore()


class ActionItem(AlgorithmItem):
    def __init__(self, rectangle: QRectF) -> None:
        super().__init__(rectangle)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self.white_brush)
        painter.drawRect(self.boundingRect())
        widget.update()
        painter.restore()
        return super().paint(painter, option, widget)


class ConditionItem(AlgorithmItem):
    def __init__(self, rectangle: QRectF) -> None:
        super().__init__(rectangle)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self.white_brush)
        rectangle = self.boundingRect()
        painter.drawConvexPolygon(
            QPointF(rectangle.x() + rectangle.width() / 2, rectangle.y()),
            QPointF(rectangle.right(), rectangle.y() + rectangle.height() / 2),
            QPointF(rectangle.x() + rectangle.width() / 2, rectangle.bottom()),
            QPointF(rectangle.x(), rectangle.y() + rectangle.height() / 2),
        )
        widget.update()
        painter.restore()
        super().paint(painter, option, widget)


class EllipseItem(AlgorithmItem):
    def __init__(self, rectangle: QRectF) -> None:
        super().__init__(rectangle)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self.white_brush)
        rectangle = self.boundingRect()
        painter.drawEllipse(rectangle)
        widget.update()
        painter.restore()
        super().paint(painter, option, widget)


class IOItem(AlgorithmItem):
    def __init__(self, rectangle: QRectF) -> None:
        super().__init__(rectangle)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self.white_brush)
        rectangle = self.boundingRect()
        painter.drawConvexPolygon(
            QPointF(rectangle.x() + settings.DELAULT_RECT_OFFSET, rectangle.y()),
            QPointF(rectangle.right(), rectangle.y()),
            QPointF(
                rectangle.right() - settings.DELAULT_RECT_OFFSET, rectangle.bottom()
            ),
            QPointF(rectangle.x(), rectangle.bottom()),
        )
        widget.update()
        painter.restore()
        super().paint(painter, option, widget)
