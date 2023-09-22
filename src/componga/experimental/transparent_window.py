# This will create a window with a custom shape for the window: visible parts
# will be part of the window, transparent parts will not and let the user
# click on underlying windows or desktop
# The main idea is to show the underlying desktop, e. g. ongoing videos, but
# still let the user draw shapes on top of those videos.
# See: kivy git repo: examples/miscellaneous/shapedwindow.py

# Configure the window
from kivy.config import Config

Config.set("graphics", "shaped", 1)

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout


class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # NOTE: The size of the window must be the exact size
        # of the image used for giving shape to the window
        # If not, the window will not behave as expected or will not get the right shape
        Window.size = (800, 600)
        Window.shape_color_key = [0, 0, 0, 1]
        Window.shape_image = "defaultshape.png"
        Window.shape_mode = "colorkey"


class ShapedWindow(App):
    def build(self):
        return Root()


if __name__ == "__main__":
    ShapedWindow().run()
