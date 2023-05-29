from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtCore import QObject, QRectF, QPointF, Qt
import settings


class GridScene(QGraphicsScene):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.__grid_std_pen = QPen(Qt.GlobalColor.lightGray, 0)
        self.__grid_big_pen = QPen(Qt.GlobalColor.darkGray, 0)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(self.__grid_std_pen)
        area = rect

        for i in range(
            round(area.x() / settings.GRID_STEP) * settings.GRID_STEP,
            round(area.width()) + 1,
            settings.GRID_STEP,
        ):
            if int((i / settings.GRID_STEP) % settings.GRID_BIG_STEP) == 0:
                painter.setPen(self.__grid_big_pen)
            painter.drawLine(QPointF(i, area.y()), QPointF(i, area.height()))
            painter.setPen(self.__grid_std_pen)

        for i in range(
            round(area.y() / settings.GRID_STEP) * settings.GRID_STEP,
            round(area.height()) + 1,
            settings.GRID_STEP,
        ):
            if int((i / settings.GRID_STEP) % settings.GRID_BIG_STEP) == 0:
                painter.setPen(self.__grid_big_pen)
            painter.drawLine(QPointF(area.x(), i), QPointF(area.width(), i))
            painter.setPen(self.__grid_std_pen)

        self.update()
        painter.restore()
        return super().drawBackground(painter, rect)
