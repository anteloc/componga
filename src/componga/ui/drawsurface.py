from PIL import Image
from kivy.app import App
from kivy.graphics import Color, Line, Rectangle as KivyRectangle
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

# Required for eval(shape_type)
from componga.shapes import *
from componga.util import BackgroundScreenshotHandler, find_shape_type, SHAPE_TYPES
from .menu import PopupMenu, ShapeViewport


class DrawSurface(FloatLayout):
    background = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DrawSurface, self).__init__(**kwargs)

        self._app = App.get_running_app()

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
        sect = "keyboard.shortcuts"
        config = self._app.config

        shortcuts_opts = config.options(sect)

        # One map per shortcut type: global and shape
        # Inverted maps: shortcut -> action
        self._global_shortcuts = {}
        self._shape_shortcuts = {}

        for key in shortcuts_opts:
            val = config.get(sect, key)

            if key.startswith("select_"):
                sh_hint = key[len("select_") :]
                self._shape_shortcuts[val] = find_shape_type(sh_hint)
            else:
                self._global_shortcuts[val] = key

    def _load_shape_attributes(self):
        sect = "shapes.attributes"

        config = self._app.config

        self._shape_type = config.get(sect, "shape_type")
        self._shape_line_width = config.getint(sect, "shape_line_width")
        self._min_shape_line_width = config.getint(sect, "min_shape_line_width")
        self._max_shape_line_width = config.getint(sect, "max_shape_line_width")
        self._shape_fade_duration = config.getfloat(sect, "shape_fade_duration")

        self._shape_constructor = eval(self._shape_type)
        self._shape_color = eval(config.get(sect, "shape_color"))

    def on_background(self, *args):
        self._set_background(self.background)

    def on_key_down(self, _keyboard, keycode, _text, _modifiers):
        # FIXME Take into account the modifiers, to avoid executing the same command
        #   when the user presses the same key but with a modifier
        #   e. g., 'e' and 'Ctrl+e' are not the same thing!
        kcode = keycode[1]
        glob_shortc = self._global_shortcuts
        shape_shortc = self._shape_shortcuts

        self._pressed_keycodes.add(kcode)

        cmd = None

        if kcode in glob_shortc:
            cmd = glob_shortc[kcode]
            # Global shortcut
            if cmd == "freeze":
                self._toggle_freeze()
            elif cmd == "update_background":
                self._update_background()
            elif cmd == "exit":
                self.exit_app()
            return True

        elif kcode in shape_shortc:
            # Shape shortcut
            shape_type = shape_shortc[kcode]
            self.on_shape_type(None, shape_type)
            self._show_shape_preview()
            return True

        return False

    def on_key_up(self, _, keycode):
        try:
            self._pressed_keycodes.remove(keycode[1])
        except KeyError:
            pass
        return True

    def on_touch_down(self, touch):
        if touch.button == "left":
            if self._menu:
                return super(DrawSurface, self).on_touch_down(touch)
            else:
                self._close_shape_preview()
                self._create_current_shape(touch.pos)
                return True
        elif touch.button == "right":
            self._open_menu()
            self._show_shape_preview()
            return True
        elif touch.button in ("scrollup", "scrolldown"):
            self._handle_mouse_wheel(touch.button)
            return True

        return super(DrawSurface, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        # XXX Maybe this method is not needed because the shape takes care of on_touch_move itself
        # Kept just in case other touch move events need to be handled when there is no current shape
        if touch.button == "left" and self._current_shape:
            self._current_shape.on_touch_move(touch)
            return True
        return super(DrawSurface, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.button == "left" and self._current_shape:
            self._current_shape.on_touch_up(touch)
            self._prev_shapes.append(self._current_shape)
            self._current_shape = None
            return True
        return super(DrawSurface, self).on_touch_up(touch)

    def on_menu_dismiss(self, _):
        # FIXME Maybe unbind methods are not needed
        # Restore the previous freeze state
        self._menu = None

        self._toggle_freeze(self._prev_freeze)
        self._close_shape_preview()

    def on_shape_color(self, _, value):
        self._shape_color = value
        self._app.config.set("shapes.attributes", "shape_color", value)

        self._show_shape_preview()

    def on_shape_type(self, _, value):
        self._shape_type = value
        self._shape_constructor = eval(value)
        self._app.config.set("shapes.attributes", "shape_type", value)

        self._show_shape_preview()

    def on_shape_faded(self, instance, _):
        if instance in self._prev_shapes:
            self._prev_shapes.remove(instance)

    def on_line_width(self, _, value):
        if value < self._min_shape_line_width:
            value = self._min_shape_line_width
        elif value > self._max_shape_line_width:
            value = self._max_shape_line_width

        self._shape_line_width = value
        self._app.config.set("shapes.attributes", "shape_line_width", value)

        self._show_shape_preview()

    def exit_app(self):
        # Cleanup resources before exiting
        if self.background:
            self.background.close()

        self._app.stop()

    def _set_background(self, new_background):
        bg = new_background
        bg_size = Image.open(bg.name).size

        with self.canvas.before:
            Color(1, 1, 1, 1)
            KivyRectangle(source=bg.name, pos=(0, 0), size=bg_size)
            Color(1, 0, 0, 1)
            Line(rectangle=(0, 0, *bg_size), width=5)

        self.background = bg

    def _update_background(self):
        if self.background:
            self.background.close()

        self._bg_handler.take_screenshot()

    def _handle_mouse_wheel(self, wheel_direction):
        if "shift" in self._pressed_keycodes:
            new_line_width = None

            if wheel_direction == "scrollup":
                new_line_width = self._shape_line_width + 1
            elif wheel_direction == "scrolldown":
                new_line_width = self._shape_line_width - 1

            self.on_line_width(None, new_line_width)
        else:
            shape_index = SHAPE_TYPES.index(self._shape_type)

            if wheel_direction == "scrollup":
                shape_index += 1
            elif wheel_direction == "scrolldown":
                shape_index -= 1

            next_shape = find_shape_type(shape_index)

            self.on_shape_type(None, next_shape)

        self._show_shape_preview()

    def _create_current_shape(self, start_point):
        # Current shape is finished, add it to the list of previous shapes
        if self._current_shape:
            self._prev_shapes.append(self._current_shape)

        # Create a new shape instance of the current type
        self._current_shape = self._shape_constructor(
            start_point,
            self._shape_color,
            self._shape_line_width,
            fade_duration=self._shape_fade_duration,
            is_shadowed=True,
            is_frozen=self._freeze,
        )

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

        self._menu = PopupMenu(
            shape_color=self._shape_color,
            shape_type=self._shape_type,
            line_width=self._shape_line_width,
            min_line_width=self._min_shape_line_width,
            max_line_width=self._max_shape_line_width,
        )

        self._menu.bind(
            shape_color=self.on_shape_color,
            shape_type=self.on_shape_type,
            line_width=self.on_line_width,
            on_dismiss=self.on_menu_dismiss,
        )

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

    def _build_shape_preview(self):
        # FIXME Shadows in preview shapes are not working
        return self._shape_constructor(
            (0, 0),
            self._shape_color,
            self._shape_line_width,
            fade_duration=0,
            is_shadowed=True,
            is_frozen=True,
        )
