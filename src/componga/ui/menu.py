from collections import OrderedDict

from kivy.app import App
from kivy.metrics import sp
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
    ListProperty,
    StringProperty,
    BooleanProperty,
)

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from componga.util import (
    DEFAULT_SHAPE,
    DEFAULT_SHAPE_LINE_WIDTH,
    MIN_SHAPE_LINE_WIDTH,
    MAX_SHAPE_LINE_WIDTH,
)


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

    def __init__(
        self,
        shape_color,
        shape_type,
        line_width,
        min_line_width,
        max_line_width,
        **kwargs,
    ):
        super(PopupMenu, self).__init__(**kwargs)
        self.shape_color = shape_color
        self.shape_type = shape_type
        self.line_width = line_width
        self.min_line_width = min_line_width
        self.max_line_width = max_line_width

    def on_show_help(self, *args):
        App.get_running_app().open_settings()
        # if self.show_help:
        #     help_popup = PopupHelp()
        #     help_popup.open()
        #     self.show_help = False


class PopupHelp(Popup):
    font_size = NumericProperty(sp(18))

    def __init__(self, *args, **kwargs):
        super(PopupHelp, self).__init__(*args, **kwargs)

        app = App.get_running_app()
        shortcuts_opts = app.config.options("keyboard.shortcuts")

        exit_key = app.config.get("keyboard.shortcuts", "exit")
        exit_help = app.config.get("keyboard.shortcuts.help", "exit")

        lbl = Label(
            text=f"[b]{exit_key}:[/b] {exit_help}",
            size_hint_y=None,
            height=44,
            markup=True,
        )
        self.ids.scroll_content.add_widget(lbl)

        mouse_opts = OrderedDict(
            [
                ("Mouse Left Click", "Draw shape"),
                ("Mouse Right Click", "Popup menu"),
                ("Mouse Wheel Up/Down", "Select another shape"),
                ("Mouse Shift + Mouse Wheel Up/Down", "Change line thickness"),
            ]
        )

        for mouse_key, mouse_help in mouse_opts.items():
            lbl = Label(
                text=f"[b]{mouse_key}:[/b] {mouse_help}",
                size_hint_y=None,
                height=44,
                markup=True,
            )
            self.ids.scroll_content.add_widget(lbl)

        for key in shortcuts_opts:
            if key == "exit":
                continue
            shortcut_key = app.config.get("keyboard.shortcuts", key)
            shortcut_help = app.config.get("keyboard.shortcuts.help", key)

            lbl = Label(
                text=f"[b]{shortcut_key}:[/b] {shortcut_help}",
                size_hint_y=None,
                height=44,
                markup=True,
            )
            self.ids.scroll_content.add_widget(lbl)
