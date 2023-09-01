from kivy.graphics import Line
from kivy.vector import Vector
from .baseshape import BaseShape

class LineStraight(BaseShape):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas:
            self.line = Line(points=[*self.start_point, *self.end_point],
                             width=self.line_width)
            
    def on_touch_move(self, touch):
        super().on_touch_move(touch)

        if touch.button == 'left':
            self.line.points = [*self.start_point, *self.end_point]
            return True
        return False
    
    def on_pos(self, *args):
        if self.shadow:
            self.shadow.on_pos(*args)
            
        self.start_point = Vector(*self.parent.pos) + Vector(0, self.parent.height / 2)
        self.end_point = Vector(*self.parent.pos) + Vector(self.parent.width, self.parent.height / 2)
        self.line.points = [*self.start_point, *self.end_point]
