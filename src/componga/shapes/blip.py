from .baseshape import BaseShape
from kivy.graphics import Line, Color
from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.vector import Vector

class Blip(BaseShape):
    radius = NumericProperty(10)

    def __init__(self, *args, **kwargs):

        fade_duration = kwargs.pop('fade_duration', None)

        if fade_duration == 0:
            # Fading is disabled
            kwargs['fade_duration'] = 0
        else: 
            kwargs['fade_duration'] = 1

        super().__init__(*args, **kwargs)

        with self.canvas:
            self.blip_circle = Line(circle=[*self.start_point, self.radius], 
                                    width=self.line_width)

        anim = Animation(radius=200, duration=1)
        anim.bind(on_progress=self._update_circle)
        anim.start(self)

    def _update_circle(self, *args):
        self.blip_circle.circle = [*self.start_point, self.radius]
    
    def on_pos(self, *args):
        if self.shadow:
            self.shadow.on_pos(*args)
        # Radius animation will take care of updating the circle
        self.start_point = Vector(*self.parent.pos) + Vector(self.parent.width / 2, self.parent.height / 2)

    

   