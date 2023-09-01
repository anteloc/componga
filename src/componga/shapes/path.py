import math
from kivy.graphics import Line
from kivy.vector import Vector
from .baseshape import BaseShape

class Path(BaseShape):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas:
            self.path = Line(points=self.start_point, 
                             joint='round', 
                             cap='round',
                             width=self.line_width)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)

        if touch.button == 'left':
            self.path.points += [*touch.pos]
            return True
        return False

    def on_pos(self, *args):
        if self.shadow:
            self.shadow.on_pos(*args)
            
        x0 = int(self.parent.x)
        y0 = int(self.parent.y)
        y_max = int(self.parent.height)
        x_max = int(self.parent.width)

        cos_points = []

        # Curve points
        for x in range(0, x_max, 10):
            rads = (x / x_max) * (2 * math.pi)
            y = y_max * abs(math.cos(rads))
            p = (x + x0, y + y0)
            cos_points.extend(p)

        self.path.points = [*cos_points]

        self.start_point = Vector(cos_points[0], cos_points[1])
        self.end_point = Vector(cos_points[-2], cos_points[-1])
   