import sys

sys.path.append("..") 

# import arcade
# from arcade import Texture
# from arcade.gui import UIBoxLayout, UIFlatButton, UILabel
# from arcade.experimental.uislider import UISlider
# from constants import SHAPE_TYPES, SHAPE_COLORS

class ContextMenu(arcade.gui.UITexturePane, arcade.gui.UIWindowLikeMixin):

    DEFAULT_BUTTON_STYLE = {
            "font_name": ("calibri", "arial"),
            "font_size": 11,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": (21, 19, 21),

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }

    def __init__(self,
                 app_window,
                 x: float = 100,
                 y: float = 100,
                 width: float = 100,
                 height: float = 100):

        self._app_window = app_window

        # Create a vertical BoxGroup to align buttons
        self._v_box = UIBoxLayout()

        # Add buttons to the group
        self._add_shape_buttons()
        self._add_line_width_slider()
        self._add_color_slider()
        self._add_exit_button()

        # bg_tex = arcade.load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        bg_tex = Texture.create_empty("menu background", (0, 0))
        
        super().__init__(child=self._v_box, tex=bg_tex)

    def _add_shape_buttons(self):
        style = dict(self.DEFAULT_BUTTON_STYLE, bg_color=arcade.color.CHARCOAL)

        for st in SHAPE_TYPES:
            # Keep the value of st as constant
            def build_closure(shape_type=st):
                return lambda event: self._app_window.on_shape_button_click(shape_type)

            # FIXME: Buttons should show an icon, not text
            shape_button = UIFlatButton(text=st, width=100, style=style)
            shape_button.on_click = build_closure()

            self._v_box.add(shape_button.with_space_around(bottom=2))

    def _add_line_width_slider(self):
        linew_slider = UISlider(value=5, min_value=1, max_value=20, width=300, height=30)
        label = UILabel(text=f"Width: {int(linew_slider.value)}")

        @linew_slider.event()
        def on_change(event):
            label.text = f"Width: {int(linew_slider.value)}"
            label.fit_content()
            self._app_window.on_linew_slider_change(linew_slider.value)

        self._v_box.add(label.with_space_around(bottom=2))
        self._v_box.add(linew_slider.with_space_around(bottom=2))

    def _add_color_slider(self):
        color_index = SHAPE_COLORS.index(self._app_window._shape_color)
        color_slider = UISlider(value=color_index, min_value=0, max_value=len(SHAPE_COLORS) - 1, width=300, height=30)
        
        self._update_color_slider(color_slider, self._app_window._shape_color)

        @color_slider.event()
        def on_change(event):
            color_index = int(color_slider.value)
            new_color = SHAPE_COLORS[color_index]

            self._update_color_slider(color_slider, new_color)
            
            self._app_window.on_color_slider_change(new_color)

        self._v_box.add(color_slider.with_space_around(bottom=2))

    def _update_color_slider(self, slider, new_color):
        states = ("normal", "hovered", "pressed")

        for state in states:
            # slider.style[f"{state}_bg"] = new_color
            slider.style[f"{state}_unfilled_bar"] = new_color
            slider.style[f"{state}_filled_bar"] = new_color
    
    def _add_exit_button(self):
        style = dict(self.DEFAULT_BUTTON_STYLE, bg_color=arcade.color.DARK_RED)

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=100, style=style)
        exit_button.on_click = lambda event: self._app_window.on_exit_button_click()

        self._v_box.add(exit_button.with_space_around(bottom=20))
