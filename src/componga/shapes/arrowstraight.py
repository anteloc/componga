import math

from kivy.graphics import Line
from kivy.vector import Vector

from .linestraight import LineStraight


class ArrowStraight(LineStraight):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.arrowhead_length = 15 * self.line_width // 2
        self.arrowhead_angle = math.radians(45)

        barb1_points, barb2_points = self._calculate_arrowhead_points()

        with self.canvas:
            self._barb1 = Line(points=barb1_points, width=self.line_width)
            self._barb2 = Line(points=barb2_points, width=self.line_width)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)

        if touch.button == "left":
            barb1_points, barb2_points = self._calculate_arrowhead_points()

            self._barb1.points = barb1_points
            self._barb2.points = barb2_points
            return True
        return False

    def _calculate_arrowhead_points(self):
        # Calculate the angle of the arrow
        xe, ye = self.end_point
        xs, ys = self.start_point

        angle = math.atan2(ye - ys, xe - xs)

        # Calculate the positions of the two lines that form the arrowhead
        x1 = xe - self.arrowhead_length * math.cos(angle + self.arrowhead_angle)
        y1 = ye - self.arrowhead_length * math.sin(angle + self.arrowhead_angle)
        x2 = xe - self.arrowhead_length * math.cos(angle - self.arrowhead_angle)
        y2 = ye - self.arrowhead_length * math.sin(angle - self.arrowhead_angle)

        barb1_points = [x1, y1, xe, ye]
        barb2_points = [x2, y2, xe, ye]

        return barb1_points, barb2_points

    def build_shape_preview(self, *args):
        if self.shadow:
            self.shadow.on_pos(*args)

        self.start_point = Vector(*self.parent.pos) + Vector(0, self.parent.height / 2)
        self.end_point = Vector(*self.parent.pos) + Vector(
            self.parent.width, self.parent.height / 2
        )

        self.line.points = [*self.start_point, *self.end_point]
        self._barb1.points, self._barb2.points = self._calculate_arrowhead_points()
