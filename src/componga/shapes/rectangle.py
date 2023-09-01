from kivy.graphics import Line
from kivy.vector import Vector
from .baseshape import BaseShape

class Rectangle(BaseShape):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas:
            self.rectangle_line = Line(rounded_rectangle=self._compute_rectangle(), 
                                       width=self.line_width)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)

        if touch.button == 'left':
            self.rectangle_line.rounded_rectangle= self._compute_rectangle()
            return True
        return False
    
    def _compute_rectangle(self):
        x0, y0 = self.start_point
        x, y = self.end_point

        width = abs(x - x0)
        height = abs(y - y0)

        left_corner_x = x0 if x0 < x else x
        left_corner_y = y0 if y0 < y else y

        return (left_corner_x, left_corner_y, width, height, 10)
    
    def on_pos(self, *args):
        if self.shadow:
            self.shadow.on_pos(*args)
            
        self.start_point = Vector(*self.parent.pos)
        self.end_point = Vector(*self.parent.pos) + Vector(self.parent.width, self.parent.height)
        self.rectangle_line.rounded_rectangle= self._compute_rectangle()
