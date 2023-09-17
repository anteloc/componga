import math
import platform

OS = platform.system().lower()


from kivy.config import Config

if OS != "windows":
    # On Windows OS, hiding the window causes sometimes
    # crashes due to "0" values in properties like width, height, etc.
    Config.set('graphics', 'window_state', 'hidden')
# Disable config: %(name)s = probesysfs
# since it causes touchpad behave like it's a touchscreen
Config.set('input', '%(name)s', None)
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'multisamples', '10')


from PIL import Image as PImage
from collections import OrderedDict
from componga.shapes import *
from componga.util.constants import *
from componga.util.functions import *
from componga.util.screenshot import BackgroundScreenshotHandler
import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Line, Color, Rectangle as KivyRectangle, Ellipse as KivyEllipse
from kivy.graphics.svg import Svg
from kivy.logger import Logger
from kivy.metrics import sp, Metrics
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty, BooleanProperty, \
    NumericProperty, OptionProperty, DictProperty, AliasProperty, BoundedNumericProperty, VariableListProperty, ReferenceListProperty
from kivy.resources import resource_add_path, resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker, ColorWheel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.vector import Vector


class ShapeViewport(FloatLayout):
    shape = ObjectProperty(None)


class PopupMenu(Popup):
    font_size = NumericProperty(sp(15))
    shape_color = ListProperty((0, 0, 0, 0))
    shape_type = StringProperty(DEFAULT_SHAPE)
    line_width = NumericProperty(DEFAULT_SHAPE_LINE_WIDTH)
    min_line_width = NumericProperty(MIN_SHAPE_LINE_WIDTH)
    max_line_width = NumericProperty(MAX_SHAPE_LINE_WIDTH)
    show_help = BooleanProperty(False)

    def __init__(self, shape_color, shape_type, line_width, min_line_width, max_line_width, **kwargs):
        super(PopupMenu, self).__init__(**kwargs)
        self.shape_color = shape_color
        self.shape_type = shape_type
        self.line_width = line_width
        self.min_line_width = min_line_width
        self.max_line_width = max_line_width

    def on_show_help(self, *args):
        if self.show_help:
            help_popup = PopupHelp()
            help_popup.open()
            self.show_help = False


class PopupHelp(Popup):
    font_size = NumericProperty(sp(18))

    def __init__(self, *args, **kwargs):
        super(PopupHelp, self).__init__(*args, **kwargs)
        shortcuts_opts = app.config.options('keyboard.shortcuts')

        exit_key = app.config.get('keyboard.shortcuts', 'exit')
        exit_help = app.config.get('keyboard.shortcuts.help', 'exit')

        lbl = Label(text=f"[b]{exit_key}:[/b] {exit_help}", size_hint_y=None, height=44, markup=True)
        self.ids.scroll_content.add_widget(lbl)

        mouse_opts = OrderedDict([
            ('Mouse Left Click', 'Draw shape'),
            ('Mouse Right Click', 'Popup menu'),
            ('Mouse Wheel Up/Down', 'Select another shape'),
            ('Mouse Shift + Mouse Wheel Up/Down', 'Change line thickness')
        ])

        for mouse_key, mouse_help in mouse_opts.items():
            lbl = Label(text=f"[b]{mouse_key}:[/b] {mouse_help}", size_hint_y=None, height=44, markup=True)
            self.ids.scroll_content.add_widget(lbl)

        for key in shortcuts_opts:
            if key == 'exit':
                continue
            shortcut_key = app.config.get('keyboard.shortcuts', key)
            shortcut_help = app.config.get('keyboard.shortcuts.help', key)

            lbl = Label(text=f"[b]{shortcut_key}:[/b] {shortcut_help}", size_hint_y=None, height=44, markup=True)
            self.ids.scroll_content.add_widget(lbl)


class DrawSurface(FloatLayout):
    background = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DrawSurface, self).__init__(**kwargs)
        self._menu = None
        self.background = None
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

        self._bg_handler = None

    def post_init(self):
        # Take the first background screenshot here, after app window is created and properly initialized
        self._bg_handler = BackgroundScreenshotHandler(self)
        self._bg_handler.take_screenshot()

    def _load_shortcuts(self):
        # XXX Is there a better way to do this? Get the options as a dict?
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

    def _update_background(self):
        if self.background:
            self.background.close()

        self._bg_handler.take_screenshot()

    def on_background(self, *args):
        self._set_background(self.background)

    def _set_background(self, new_background):

        bg = new_background
        bg_size = PImage.open(bg.name).size

        with self.canvas.before:
            Color(1, 1, 1, 1)
            KivyRectangle(source=bg.name, pos=(0, 0), size=bg_size)
            Color(1, 0, 0, 1)
            Line(rectangle=(0, 0, *bg_size), width=5)

        self.background = bg

    def on_key_down(self, _keyboard, keycode, _text, _modifiers):
        # FIXME Take into account the modifiers, to avoid executing the same command
        # when the user presses the same key but with a modifier 
        # e. g., 'e' and 'Ctrl+e' are not the same thing!
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
                self._update_background()
            elif cmd == 'exit':
                self.exit_app()
            return True

        elif kcode in shape_shortc:
            # Shape shortcut
            shape_type = shape_shortc[kcode]
            self.on_shape_type(None, shape_type)
            self._show_shape_preview()
            return True

        elif kcode == '1':
            app._win_info("on_key_down")
            return True

        return False

    def exit_app(self):
        # Cleanup resources before exiting
        if self.background:
            self.background.close()

        app.stop()

    def on_key_up(self, _, keycode):
        try:
            self._pressed_keycodes.remove(keycode[1])
        except KeyError:
            pass
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

        self._show_shape_preview()

    def on_shape_type(self, _, value):
        self._shape_type = value
        self._shape_constructor = eval(value)
        app.config.set('shapes.attributes', 'shape_type', value)

        self._show_shape_preview()

    def _build_shape_preview(self):
        # FIXME Shadows in preview shapes are not working
        return self._shape_constructor((0, 0),
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

        self._show_shape_preview()


class CompongaApp(App):

    def on_start(self):
        self.root_window.title = self.title
        Logger.debug(f"self.root_window: {self.root_window}")
        self.config.add_callback(self.on_config_change)
        self.monitor, self.monitor_unsc = find_current_monitor_info()

        self._fullscreen()
        self._setup_keyboard()

        self._draw_surface.post_init()

    def build(self):
        Config.set('kivy', 'log_level', 'debug')
        self.title = "Componga"
        self._draw_surface = DrawSurface(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.monitor = None
        self.monitor_unsc = None

        resource_add_path(os.path.join(os.path.dirname(__file__), 'resources'))

        return self._draw_surface

    def build_config(self, config):
        # FIXME: this is initial config should be created in the user's config dir, not in the app's dir
        for section in DEFAULT_CONFIG_SECTIONS:
            config.setdefaults(section['name'], section['options'])

    def get_application_config(self):
        self._bootstrap_config()

        return super(CompongaApp, self).get_application_config('~/.componga/%(appname)s.ini')

    def get_resource(self, filename):
        return resource_find(filename)

    def _bootstrap_config(self):
        home_directory = os.path.expanduser('~')
        config_dir = os.path.join(home_directory, '.componga')

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

    def on_config_change(self, *args, **kwargs):
        self.config.write()

    def _fullscreen(self):
        if OS == "linux":
            self.root_window.fullscreen = 'auto'
        elif OS == "darwin":
            # TODO Fullscreen custom config for OSX
            pass
        elif OS == "windows":
            pass
        else:
            raise Exception(f"OS {OS} not supported - Unable to set window to fullscreen")

        self._position_window()
        self._resize_window()
        # self.root_window.show()
        self._win_info("on_start")

    def _position_window(self):
        self.root_window.left, self.root_window.top = self.monitor['left'], self.monitor['top']

    def _resize_window(self):
        self.root_window.system_size = (self.monitor_unsc['width'], self.monitor_unsc['height'])

    def _setup_keyboard(self):
        # Bind the keyboard to the on_key_down function
        self._keyboard = self.root_window.request_keyboard(self._keyboard_closed, self._draw_surface)
        self._keyboard.bind(on_key_down=self._draw_surface.on_key_down,
                            on_key_up=self._draw_surface.on_key_up)

    def _keyboard_closed(self):
        # Unbind the keyboard
        self._keyboard.unbind(on_key_down=self._draw_surface.on_key_down)
        self._keyboard = None

    def _win_info(self, prefix=""):
        # Used for debugging only
        import kivy.metrics

        dpis = kivy.metrics.Metrics.dpi
        density = kivy.metrics.Metrics.density

        Logger.debug(f"""[{prefix}] 
              monitor: {self.monitor or 'N/A'}, monitor_unsc: {self.monitor_unsc or 'N/A'}
              Metrics dpis: {dpis}, Metrics density: {density}, Window dpi: {self.root_window.dpi}
              Window: left: {self.root_window.left}, top: {self.root_window.top}
              width: {self.root_window.width}, height: {self.root_window.height}
              system_size: {self.root_window.system_size}, size: {self.root_window.size}
              position: {self.root_window.position}, fullscreen: {self.root_window.fullscreen}
              """)


def main():
    global app
    app = CompongaApp()
    app.run()
