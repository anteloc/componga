import math
from .path import Path
from kivy.graphics import Line
from kivy.vector import Vector

class ArrowPath(Path):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.arrowhead_length = 15 * self.line_width // 2
        self.arrowhead_angle = math.radians(45)

        barb1_points, barb2_points = self._calculate_arrowhead_points()

        with self.canvas:
            self._barb1 = Line(points=barb1_points, 
                               width=self.line_width)
            self._barb2 = Line(points=barb2_points, 
                               width=self.line_width)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)

        if touch.button == 'left':
            barb1_points, barb2_points = self._calculate_arrowhead_points()

            self._barb1.points = barb1_points
            self._barb2.points = barb2_points
            return True
        return False

    def _calculate_arrowhead_points(self):
        # Calculate the angle of the arrow
        xe, ye = self.end_point

        num_points = len(self.path.points) // 2
        last_n_points = min(num_points, 15)
        first_point_idx = -last_n_points
        xs = self.path.points[first_point_idx * 2]
        ys = self.path.points[first_point_idx * 2 + 1]

        angle = math.atan2(ye - ys, xe - xs)

        # Calculate the positions of the two lines that form the arrowhead
        x1 = xe - self.arrowhead_length * math.cos(angle + self.arrowhead_angle)
        y1 = ye - self.arrowhead_length * math.sin(angle + self.arrowhead_angle)
        x2 = xe - self.arrowhead_length * math.cos(angle - self.arrowhead_angle)
        y2 = ye - self.arrowhead_length * math.sin(angle - self.arrowhead_angle)
        
        barb1_points = [x1, y1, xe, ye]
        barb2_points = [x2, y2, xe, ye]

        return barb1_points, barb2_points

    def on_pos(self, *args):
        if self.shadow:
            self.shadow.on_pos(*args)

        x0 = int(self.parent.x)
        y0 = int(self.parent.y)
        y_center = y0 + int(self.parent.height / 2)
        y_max = int(self.parent.height)
        x_max = int(self.parent.width)
        last_n_points = 50
        cos_x_max = x_max - last_n_points

        sh_points = []

        # Curve points
        for x in range(0, cos_x_max, 5):
            rads = (x / cos_x_max) * (2 * math.pi)
            y = y_max * abs(math.cos(rads))
            p = (x + x0, y + y0)
            sh_points.extend(p)

        # Just for fun ;P - Last segment: straight line to allow the arrowhead to be clearly visible
        s0 = Vector(sh_points[-8], sh_points[-7])
        s1 = Vector(sh_points[-2], sh_points[-1])

        m = (s1.y - s0.y) / (s1.x - s0.x)
        s_fun = lambda x: m * (x - s0.x) + s0.y

        for x in range(s0.x, x_max, 2):
            sh_points.extend((x, s_fun(x)))

        self.path.points = [*sh_points]

        self.start_point = Vector(sh_points[0], sh_points[1])
        self.end_point = Vector(sh_points[-2], sh_points[-1])

        self._barb1.points, self._barb2.points = self._calculate_arrowhead_points()
    