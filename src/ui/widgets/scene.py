from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtCore import QObject, QRectF, QPointF, Qt
import settings


class GridScene(QGraphicsScene):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.__grid_std_pen = QPen(Qt.GlobalColor.lightGray, 1)
        self.__grid_big_pen = QPen(Qt.GlobalColor.darkGray, 1)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(self.__grid_std_pen)

        for i in range(int(rect.x()), int(rect.width()) + 1, settings.GRID_STEP):
            if int((i / settings.GRID_STEP) % settings.GRID_BIG_STEP) == 0:
                painter.setPen(self.__grid_big_pen)
            painter.drawLine(QPointF(i, rect.y()), QPointF(i, rect.height()))
            painter.setPen(self.__grid_std_pen)

        for i in range(int(rect.y()), int(rect.height()) + 1, settings.GRID_STEP):
            if int((i / settings.GRID_STEP) % settings.GRID_BIG_STEP) == 0:
                painter.setPen(self.__grid_big_pen)
            painter.drawLine(QPointF(rect.x(), i), QPointF(rect.width(), i))
            painter.setPen(self.__grid_std_pen)

        self.update()
        painter.restore()
        return super().drawBackground(painter, rect)
