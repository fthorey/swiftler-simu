from utils.simobject import SimObject
from PyQt4 import QtGui, QtCore

class Polygon(SimObject):
    """The polygon is a simobject that gets the envelope supplied at construction.
       It draws itself as a filled polygon.
       """
    count = 0

    def __init__(self, envelope, brush_, pen_):
        SimObject.__init__(self, "polygon" + str(self.count), brush_, pen_)
        self.count = self.count + 1

        # Cache the envelope
        self._envelope = envelope

        # Cache the bounding rect
        xmin, ymin, xmax, ymax = self.getBounds()
        self._boundingRect = QtCore.QRectF(QtCore.QPointF(xmin, ymin), QtCore.QPointF(xmax, ymax))

        # Cache the shape
        points = [QtCore.QPointF(p[0], p[1]) for p in self._envelope]
        self._shape = QtGui.QPainterPath()
        self._shape.addPolygon(QtGui.QPolygonF(points))

    def getEnvelope(self):
        return self._envelope

    def boundingRect(self, ):
        """
        """
        return self._boundingRect

    def shape(self, ):
        """
        """
        return self._shape

    # Define how to paint the envelope
    def paint(self, painter, option, widget):
        """Draw the envelope (envelope) filling it with the internal color."""
        painter.setBrush(self._brush)
        painter.setPen(self._pen)

        points = [QtCore.QPointF(p[0], p[1]) for p in self.getEnvelope()]
        painter.drawPolygon(QtGui.QPolygonF(points))
