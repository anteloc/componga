import sys
import tempfile
import math
import mss.tools
from util.functions import find_current_monitor, desktop_screenshot, find_shape_type

# Capture desktop screen first, to avoid capturing the kivy windows themselves
app_monitor = find_current_monitor()
desktop_background = desktop_screenshot(app_monitor)

from kivy.config import Config
# Disable config: %(name)s = probesysfs
# since it causes touchpad behave like it's a touchscreen
Config.set('input', '%(name)s', None)
Config.set('input', 'mouse', 'mouse,disable_multitouch')
# These are problematic, for some configurations they don't work for multiple monitors
# Config.set('graphics', 'left', mon['left'])
# Config.set('graphics', 'top', mon['top'])
# Config.set('graphics', 'width', mon['width'])
# Config.set('graphics', 'height', mon['height'])
# Config.set('graphics', 'fullscreen', 1)

from PIL import Image as PImage
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty, BooleanProperty, OptionProperty, DictProperty, AliasProperty, BoundedNumericProperty, VariableListProperty, ReferenceListProperty, NumericProperty
from kivy.graphics import Color, Rectangle as KivyRectangle, Ellipse as KivyEllipse
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker, ColorWheel
from kivy.graphics import Line, Color
from kivy.graphics.instructions import InstructionGroup
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from constants.constants import *
from shapes.linestraight import LineStraight
from shapes.arrowstraight import ArrowStraight
from shapes.arrowpath import ArrowPath
from shapes.ellipse import Ellipse
from shapes.path import Path
from shapes.rectangle import Rectangle
from shapes.blip import Blip


class ShapeViewport(FloatLayout):
    shape = ObjectProperty(None)
    
class PopupMenu(Popup):
    shape_color = ListProperty((0, 0, 0, 1))
    shape_type = StringProperty(DEFAULT_SHAPE)
    line_width = NumericProperty(DEFAULT_SHAPE_LINE_WIDTH)
    min_line_width = NumericProperty(MIN_SHAPE_LINE_WIDTH)
    max_line_width = NumericProperty(MAX_SHAPE_LINE_WIDTH)
    
    def __init__(self, shape_color, shape_type, line_width, min_line_width, max_line_width, **kwargs):
        super(PopupMenu, self).__init__(**kwargs)
        self.shape_color = shape_color
        self.shape_type = shape_type
        self.line_width = line_width
        self.min_line_width = min_line_width
        self.max_line_width = max_line_width


class DrawSurface(FloatLayout):
    
    def __init__(self, monitor, desktop_background, **kwargs):
        super(DrawSurface, self).__init__(**kwargs)
        self._monitor = monitor
        self._menu = None
        self._desktop_bg = None
        self._pressed_keycodes = set()

        self._prev_shapes = []
        self._current_shape = None
        self._shape_viewport = None
        self._freeze = False
        self._prev_freeze = None

        self._shape_type = None
        self._shape_constructor = None
        self._shape_line_width = None
        self._shape_color = None
        self._shape_fade_duration = None
        self._global_shortcuts = None
        self._shape_shortcuts = None

        self._load_shortcuts()
        self._load_shape_attributes()

        self._update_background(new_background=desktop_background)

    def _load_shortcuts(self):
        # Is there a better way to do this? Get the options as a dict?
        sect = 'keyboard.shortcuts'
        shortcuts_opts = app.config.options(sect)

        # One map per shortcut type: global and shape
        # Inverted maps: shortcut -> action

        self._global_shortcuts = {}
        self._shape_shortcuts = {}

        for key in shortcuts_opts:
            val = app.config.get(sect, key)

            if key.startswith('select_'):
                sh_hint = key[len('select_'):]
                self._shape_shortcuts[val] = find_shape_type(sh_hint)
            else:
                self._global_shortcuts[val] = key

    def _load_shape_attributes(self):
        sect = 'shapes.attributes'

        self._shape_type = app.config.get(sect, 'shape_type')
        self._shape_constructor = eval(self._shape_type)
        self._shape_line_width = app.config.getint(sect, 'shape_line_width')
        self._min_shape_line_width = app.config.getint(sect, 'min_shape_line_width')
        self._max_shape_line_width = app.config.getint(sect, 'max_shape_line_width')
        self._shape_color = eval(app.config.get(sect, 'shape_color'))
        self._shape_fade_duration = app.config.getfloat(sect, 'shape_fade_duration')

    def _update_background(self, new_background=None):

        # Remove the previous background temp file, if needed
        if self._desktop_bg:
            self._desktop_bg.close()
        
        if new_background:
            bg = new_background
        else:
            # This is a workaround: the events on_hide, on_minimize, etc.
            # are not working as expected: the OS window reports that it's 
            # hidden or minimized, but the Kivy window is still visible
            # and the kivy window is also captured in the screenshot

            # Window.bind(on_minimize=self._desktop_screenshot)
            Window.minimize()
            # XXX If the OS takes longer than 0.25 seconds to minimize the window,
            # the kivy window will be captured in the screenshot.
            # OTOH, increasing the delay will make the app less responsive
            Clock.schedule_once(self._desktop_screenshot, 0.25)
            return
                                    
        bg_size = PImage.open(bg.name).size
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            KivyRectangle(source=bg.name, pos=(0, 0), size=bg_size)
            Color(1, 0, 0, 1)
            Line(rectangle=(0, 0, *bg_size), width=5)

        self._desktop_bg = bg

    def _win_info(self):
        # Used for debugging only
        print(f"self.size: {self.size}. self.pos: {self.pos}. ")
        print(f"size: {Window.system_size}. position: {Window.position} fullscreen: {Window.fullscreen}")

    def _desktop_screenshot(self, *args):
        bg = desktop_screenshot(self._monitor)
        Window.restore()
        self._update_background(new_background=bg)

    def on_key_down(self, _keyboard, keycode, _text, _modifiers):
        kcode = keycode[1]
        glob_shortc = self._global_shortcuts
        shape_shortc = self._shape_shortcuts

        self._pressed_keycodes.add(kcode)

        cmd = None

        if kcode in glob_shortc:
            cmd = glob_shortc[kcode]
            # Global shortcut
            if cmd == 'freeze':
                self._toggle_freeze()
            elif cmd == 'update_background':
                self._desktop_screenshot()
            elif cmd == 'exit':
                self.exit_app()
                
        elif kcode in shape_shortc:
            # Shape shortcut
            shape_type = shape_shortc[kcode]
            self.on_shape_type(None, shape_type)
            self._show_shape_preview()

        return True
    
    def exit_app(self):
        # Cleanup resources before exiting
        if self._desktop_bg:
            self._desktop_bg.close()

        app.stop()
    
    def on_key_up(self, _, keycode):
        self._pressed_keycodes.remove(keycode[1])
        return True

    def on_touch_down(self, touch):

        if touch.button == 'left':
            if self._menu:
                return super(DrawSurface, self).on_touch_down(touch)
            else:
                self._close_shape_preview()
                self._create_current_shape(touch.pos)
                return True
        elif touch.button == 'right':
            self._open_menu()
            self._show_shape_preview()
            return True
        elif touch.button in ('scrollup', 'scrolldown'):
            self._handle_mouse_wheel(touch.button)
            return True
        
        return super(DrawSurface, self).on_touch_down(touch)
    
    def _handle_mouse_wheel(self, wheel_direction):

        if 'shift' in self._pressed_keycodes:
            new_line_width = None

            if wheel_direction == 'scrollup':
                new_line_width = self._shape_line_width + 1
            elif wheel_direction == 'scrolldown':
                new_line_width = self._shape_line_width - 1

            self.on_line_width(None, new_line_width)
        else:
            shape_index = SHAPE_TYPES.index(self._shape_type)

            if wheel_direction == 'scrollup':
                shape_index += 1
            elif wheel_direction == 'scrolldown':
                shape_index -= 1

            next_shape = find_shape_type(shape_index)
            
            self.on_shape_type(None, next_shape)

        self._show_shape_preview()

    def on_touch_move(self, touch):
        # XXX Maybe this method is not needed because the shape takes care of on_touch_move itself
        # Kept just in case other touch move events need to be handled when there is no current shape
        if touch.button == 'left' and self._current_shape:
            self._current_shape.on_touch_move(touch)
            return True
        return super(DrawSurface, self).on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if touch.button == 'left' and self._current_shape:
            self._current_shape.on_touch_up(touch)
            self._prev_shapes.append(self._current_shape)
            self._current_shape = None
            return True
        return super(DrawSurface, self).on_touch_up(touch)
    
    def _create_current_shape(self, start_point):
        # Current shape is finished, add it to the list of previous shapes
        if self._current_shape:
            self._prev_shapes.append(self._current_shape)
        
        # Create a new shape instance of the current type
        self._current_shape = self._shape_constructor(start_point, 
                                                        self._shape_color, 
                                                        self._shape_line_width,
                                                        fade_duration=self._shape_fade_duration,
                                                        is_shadowed=True,
                                                        is_frozen=self._freeze)
        
        self._current_shape.bind(shape_faded=self.on_shape_faded)

        # TODO See: comments in chroma.py module
        # from experimental.chroma import wrap_with_chroma, DraggableEffectWidget
        # self._current_shape = DraggableEffectWidget(self._current_shape)
        # self._current_shape = wrap_with_chroma(self._current_shape, self._shape_color)
        
        self.add_widget(self._current_shape)
    
    def _open_menu(self):
        # Pause fading shapes in order to compare the existing ones 
        # with the menu options for the new shapes
        self._prev_freeze = self._freeze
        self._toggle_freeze(True)

        self._menu = PopupMenu(shape_color=self._shape_color, 
                               shape_type=self._shape_type,
                               line_width=self._shape_line_width,
                               min_line_width=self._min_shape_line_width,
                               max_line_width=self._max_shape_line_width)
        
        self._menu.bind(shape_color=self.on_shape_color)
        self._menu.bind(shape_type=self.on_shape_type)
        self._menu.bind(line_width=self.on_line_width)
        self._menu.bind(on_dismiss=self.on_menu_dismiss)

        self._menu.open()

    def _show_shape_preview(self):
        if not self._shape_viewport:
            self._shape_viewport = ShapeViewport()
            self.add_widget(self._shape_viewport)

        shape_prev = self._build_shape_preview()
        self._shape_viewport.shape = shape_prev
    
    def _close_shape_preview(self, *args):
        if self._shape_viewport:
            self.remove_widget(self._shape_viewport)
            self._shape_viewport = None
                   
    def _toggle_freeze(self, freeze=None):
        # Set the provided value or toggle the current state
        self._freeze = freeze if freeze else not self._freeze

        if self._current_shape:
            self._current_shape.freeze(self._freeze)

        for s in self._prev_shapes:
            s.freeze(self._freeze)

    def on_menu_dismiss(self, _):
        # FIXME Maybe unbind methods are not needed
        # Restore the previous freeze state 
        self._menu = None

        self._toggle_freeze(self._prev_freeze)
        self._close_shape_preview()

    def on_shape_color(self, _, value):
        self._shape_color = value
        app.config.set('shapes.attributes', 'shape_color', value)

        if self._shape_viewport:
            self._build_shape_preview()

    def on_shape_type(self, _, value):
        self._shape_type = value
        self._shape_constructor = eval(value)
        app.config.set('shapes.attributes', 'shape_type', value)

        if self._shape_viewport:
            self._build_shape_preview()

    def _build_shape_preview(self):
        # FIXME Shadows in preview shapes are not working

        return self._shape_constructor((0,0), 
                                        self._shape_color, 
                                        self._shape_line_width, 
                                        fade_duration=0, 
                                        is_shadowed=True,
                                        is_frozen=True)

    def on_shape_faded(self, instance, _):
        if instance in self._prev_shapes:
            self._prev_shapes.remove(instance)

    def on_line_width(self, _, value):
        
        if value < self._min_shape_line_width:
            value = self._min_shape_line_width
        elif value > self._max_shape_line_width:
            value = self._max_shape_line_width
            
        self._shape_line_width = value
        app.config.set('shapes.attributes', 'shape_line_width', value)

        if self._shape_viewport:
            self._build_shape_preview()


class CompongaApp(App):

    def build(self):
        self.config.add_callback(self.on_config_change)
        self._setup_window()

        self._draw_surface = DrawSurface(monitor=app_monitor, 
                                         desktop_background=desktop_background,
                                         pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        self._setup_keyboard()

        return self._draw_surface
    
    def build_config(self, config):
        # FIXME: this is initial config should be created in the user's config dir, not in the app's dir
        for section in DEFAULT_CONFIG_SECTIONS:
            config.setdefaults(section['name'], section['options'])

    def on_config_change(self, *args, **kwargs):
        print(f"on_config_change: {args}, {kwargs}")
        self.config.write()
    
    def _setup_window(self):
        Window.fullscreen = True 
        Window.left, Window.top = app_monitor['left'], app_monitor['top']
        Window.size = (app_monitor['width'], app_monitor['height'])

    def _setup_keyboard(self):
        # Bind the keyboard to the on_key_down function
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self._draw_surface)
        self._keyboard.bind(on_key_down=self._draw_surface.on_key_down,
                            on_key_up=self._draw_surface.on_key_up)

    def _keyboard_closed(self):
        # Unbind the keyboard
        self._keyboard.unbind(on_key_down=self._draw_surface.on_key_down)
        self._keyboard = None

app = None  
    
if __name__ == "__main__":
    app = CompongaApp()
    app.run()
