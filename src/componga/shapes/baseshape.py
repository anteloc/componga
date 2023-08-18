from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.animation import Animation
from kivy.graphics.boxshadow import BoxShadow
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.vector import Vector
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.effectwidget import EffectWidget

from kivy.uix.effectwidget import (MonochromeEffect,
                                   InvertEffect,
                                   ChannelMixEffect,
                                   ScanlinesEffect,
                                   FXAAEffect,
                                   PixelateEffect,
                                   HorizontalBlurEffect,
                                   VerticalBlurEffect)
import sys
sys.path.append("..") 

from experimental.chroma import *

class ShapeEffect(EffectWidget):
    def add_widget(self, shape, *args, **kwargs):
        self.shape = shape
        self.bind(on_touch_down=shape.on_touch_down)
        self.bind(on_touch_move=shape.on_touch_move)
        self.bind(on_touch_up=shape.on_touch_up)
        self.cancel_fade = shape.cancel_fade
        self.fade_shape = shape.fade_shape

        return super().add_widget(shape, *args, **kwargs)


class BaseShape(Widget):
    shape_faded = BooleanProperty(False)

    def __init__(self, start_point, 
                 initial_color, 
                 line_width, 
                 fade_duration=5.0, 
                 pos_offset=(0, 0),
                 is_shadowed=False,
                 is_frozen=False, 
                 **kwargs):
        
        super().__init__(**kwargs)

        self._kwargs = kwargs

        self.initial_color = initial_color
        self.line_width = line_width
        self.fade_duration = fade_duration
        self.pos_offset = Vector(*pos_offset)
        self.is_shadowed = is_shadowed
        self.is_frozen = is_frozen
        self.shadow = None

        self.start_point = Vector(*start_point) + self.pos_offset
        self.end_point = self.start_point
        self._anim = None

        if self.is_shadowed:
            shadow = self.build_shadow()

            # No effects - OK
            self.shadow = shadow
            self.add_widget(self.shadow)

            # from experimental.chroma import wrap_with_chroma
            # chroma_color=(1, 1, 0, 1)
            # wrapped = DraggableEffectWidget(self)
            # wrapped = wrap_with_chroma(self.shadow , chroma_color=chroma_color)

            # self.shadow = wrapped
            # self.add_widget(wrapped)

        # Doing this with canvas.before instead of with canvas 
        # causes EffectWidget to not work
        with self.canvas:
            self.shape_color = Color(*self.initial_color)

    def build_shadow(self):
        shadow_color=(0, 0, 0, .3)
        pos_offset=(-5, -5)

        shape_subclass = type(self)
       
        shadow = shape_subclass(self.start_point,
                            shadow_color,
                            self.line_width, 
                            fade_duration=self.fade_duration,
                            pos_offset=pos_offset,
                            is_shadowed=False,
                            is_frozen=self.is_frozen,
                            **self._kwargs) # XXX Is this correct?

        # self.shadow = shadow
        # self.add_widget(shadow, 1)

        # from experimental.chroma import wrap_with_chroma
        # wrapped = wrap_with_chroma(shadow, chroma_color=chroma_color)

        # layout = FloatLayout()
        # layout.add_widget(wrapped)

        # self.add_widget(layout)

        return shadow

    def can_draw(self):
        return True
    
    # FIXME This method is for positioning a widget, but it's used as 
    # a way to create a shape preview.
    # Delegate calls to this method to another one, overriden by subclasses, with
    # a more appropriate name.
    #
    # def on_pos(self, *args):
    #     pass

    def on_touch_move(self, touch):
        """ Called when the user drags the mouse. """

        if self.shadow:
            self.shadow.on_touch_move(touch)

        if touch.button == 'left':
            self.end_point = Vector(*touch.pos) + self.pos_offset
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        """ Called when the user releases a mouse button. """
        if self.shadow:
            self.shadow.on_touch_up(touch)

        if touch.button == 'left' and not self.is_frozen:
            self.fade_shape()
            return True
        return super().on_touch_up(touch)
    
    def freeze(self, is_frozen):
        self.is_frozen = is_frozen

        if self.is_frozen:
            self.cancel_fade()
        else:
            self.fade_shape()

    def fade_shape(self):

        if self.shadow:
            self.shadow.fade_shape()

        if not self._anim:
            self._anim = Animation(a=0, duration=self.fade_duration)
            self._anim.bind(on_complete=self.on_fade_complete)
            self._anim.start(self.shape_color)

    def cancel_fade(self):

        if self.shadow:
            self.shadow.cancel_fade()

        if self._anim:
            self._anim.cancel(self.shape_color)
            self._anim = None

    def on_fade_complete(self, *_):
        self.shape_faded = True
        self._anim = None