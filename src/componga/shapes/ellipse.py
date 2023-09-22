from kivy.graphics import Line
from kivy.vector import Vector

from .baseshape import BaseShape


class Ellipse(BaseShape):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas:
            self.ellipse_line = Line(
                ellipse=self._compute_ellipse(), width=self.line_width
            )

    def on_touch_move(self, touch):
        super().on_touch_move(touch)

        if touch.button == "left":
            self.ellipse_line.ellipse = self._compute_ellipse()
            return True
        return False

    def _compute_ellipse(self):
        x0, y0 = self.start_point
        x, y = self.end_point

        major_axis = abs(x - x0)
        minor_axis = abs(y - y0)

        left_corner_x = x0 if x0 < x else x
        left_corner_y = y0 if y0 < y else y

        return (left_corner_x, left_corner_y, major_axis, minor_axis)

    def build_shape_preview(self, *args):
        if self.shadow:
            self.shadow.on_pos(*args)

        self.start_point = Vector(*self.parent.pos) + Vector(0, self.parent.height)
        self.end_point = Vector(*self.parent.pos) + Vector(self.parent.width, 0)
        self.ellipse_line.ellipse = self._compute_ellipse()
