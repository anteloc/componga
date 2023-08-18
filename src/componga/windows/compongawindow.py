import sys

sys.path.append("..") 

import arcade
import arcade.gui
import pyglet
import pyglet.window
from PIL import Image
import mss
# from widgets.contextmenu import ContextMenu
from shapes.baseshape import BaseShape
from shapes.arrowpath import ArrowPath
from shapes.arrowstraight import ArrowStraight
from shapes.circumference import Circumference
from shapes.ellipse import Ellipse
from shapes.linestraight import LineStraight
from shapes.path import Path
from shapes.pathsmooth import PathSmooth
from shapes.rectangle import Rectangle


from constants import DEFAULT_SHAPE, DEFAULT_SHAPE_COLOR, DEFAULT_SHAPE_LINE_WIDTH

class CompongaWindow(arcade.Window):
    def __init__(self, screen, width, height, title):
        super().__init__(width,
                         height,
                         title,
                         fullscreen=True,
                         resizable=False,
                         visible=False,
                         screen=screen,
                         style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
        
        self._screen = screen

        self._manager = arcade.gui.UIManager()

        cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        self.set_mouse_cursor(cursor)

        self._line_width = DEFAULT_SHAPE_LINE_WIDTH
        self._shape_color = DEFAULT_SHAPE_COLOR
        self._shape_constructor = None
        self._current_shape = None
        self._fading_shapes = []

        # Capture screenshot
        self._screenshot = None
        self._background = None

        self._menu_widget = None
        self._menu_widget_anchor = None

    def setup(self):
        self._manager.enable()

        # Capture screenshot
        self._screenshot = self._monitor_screenshot()
        
        self._background = arcade.Texture("screenshot", image=self._screenshot)
       
        # FIXME Positioning not working, resorted to using an anchor for now
        # self._menu_widget = ContextMenu(app_window=self,
        #                                 x=1900.0, y=421.0, width=450, height=238)
        
        # self._menu_widget_anchor = arcade.gui.UIAnchorWidget(
        #     anchor_x="right",
        #     align_x=-10,
        #     anchor_y="center_y",
        #     child=self._menu_widget)
        
        self._shape_constructor = eval(DEFAULT_SHAPE)
        self._current_shape = self._shape_constructor(self._shape_color, self._line_width)

        self.set_visible(True)

    def _monitor_screenshot(self):
        with mss.mss() as sct:
            # Get rid of the first, as it represents the "All in One" monitor:
            for num, monitor in enumerate(sct.monitors[1:], 1):
                # Get raw pixels from the screen

                if monitor["left"] == self._screen.x and monitor["top"] == self._screen.y:
                    sct_img = sct.grab(monitor)
                    # Create the Image
                    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
               
                    return img
                
            return None

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        arcade.start_render()

        # Draw the screenshot as a background to simulate transparency
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2,
                                      self.width,  self.height, self._background)
        
        # Draw a red rectangle framing the screenshot
        arcade.draw_rectangle_outline(self.width // 2, self.height // 2,
                                      self.width,  self.height, 
                                      arcade.color.RED, 5)

        # Cleanup shapes that became invisible
        self._fading_shapes = [s for s in self._fading_shapes if not s.faded]

        # Render the current and active shape
        if self._current_shape:
            self._current_shape.draw()

        # Render past active shapes that are still fading away
        for s in self._fading_shapes:
            s.draw()

        # Render menu and widgets, if needed
        self._manager.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.ESCAPE:
            self._exit_app()
        elif key == arcade.key.R:
            # FIXME In theory, when switching to another window, the background screenshot should be updated with changes on the monitor
            self._monitor_screenshot()

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            # self._manager.remove(self._menu_widget_anchor)
            self.set_mouse_visible(False)

            # Move the current shape to the fading shapes, and let it fade away
            if self._current_shape:
                self._fading_shapes.append(self._current_shape)

            # Create a new shape instance of the current type
            self._current_shape = self._shape_constructor(self._shape_color, self._line_width)

            # Forward the click to the new shape, to be handled there
            self._current_shape.mouse_press(x, y, button, modifiers)

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            # FIXME Add the menu widget and show it in mouse position
            # self._manager.add(self._menu_widget_anchor)
            pass
            # self.manager.debug()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """ Called when the user drags the mouse. """
        if buttons == arcade.MOUSE_BUTTON_LEFT:
            self._current_shape.mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        """ Called when the user releases a mouse button. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self._current_shape.mouse_release(x, y, button, modifiers)
            self.set_mouse_visible(True)

    def on_shape_button_click(self, shape_type):
        self._shape_constructor = eval(shape_type)
        # self._manager.remove(self._menu_widget_anchor)

    def on_color_slider_change(self, new_color):
        self._shape_color = new_color

    def on_linew_slider_change(self, new_width):
        self._line_width = new_width

    def on_exit_button_click(self):
        self._exit_app()

    def _exit_app(self):
        arcade.exit()