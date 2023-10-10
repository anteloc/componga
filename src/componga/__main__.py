import os
# import platform
import sys

from componga.util import OS

# OS = platform.system().lower()

# Workaround for Kivy bug on Windows when using PyInstaller and not using the console
# See: https://github.com/kivy/kivy/issues/8074
if OS == "windows" and hasattr(sys, "_MEIPASS"):
    os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.config import Config

if OS != "windows":
    # On Windows OS, hiding the window causes sometimes
    # crashes due to "0" values in properties like width, height, etc.
    Config.set("graphics", "window_state", "hidden")

# Disable touchpads behaving like touchscreens
Config.set("input", "%(name)s", None)
Config.set("input", "mouse", "mouse,disable_multitouch")
Config.set("graphics", "multisamples", "10")

from kivy.app import App
from kivy.logger import Logger
from kivy.resources import resource_add_path, resource_find
from kivy.clock import Clock

from componga.ui import DrawSurface
from componga.util import find_current_monitor_info, DEFAULT_CONFIG_SECTIONS


class CompongaApp(App):
    def __init__(self, launcher=None):
        self._launcher = launcher
        super(CompongaApp, self).__init__()

    def build(self):
        Config.set("kivy", "log_level", "debug")
        self.title = "Componga"
        self._draw_surface = DrawSurface(pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.monitor = None
        self.monitor_unsc = None

        resource_add_path(os.path.join(os.path.dirname(__file__), "resources"))

        return self._draw_surface

    def set_monitors(self, monitor, monitor_unsc):
        self.monitor = monitor
        self.monitor_unsc = monitor_unsc
        self._draw_surface.set_monitors(monitor, monitor_unsc)

    def on_start(self):
        self.root_window.title = self.title
        Logger.debug(f"self.root_window: {self.root_window}")
        self.config.add_callback(self.on_config_change)
        # self.monitor, self.monitor_unsc = find_current_monitor_info()

        # self._fullscreen()
        # self._setup_keyboard()

        # XXX keep initial background screenshot?
        # self._draw_surface.post_init()

        if self._launcher:
            self._launcher.register_componga_app(self)

    def on_config_change(self, *args, **kwargs):
        self.config.write()

    def build_config(self, config):
        for section in DEFAULT_CONFIG_SECTIONS:
            config.setdefaults(section["name"], section["options"])

    def get_application_config(self):
        self._bootstrap_config()

        return super(CompongaApp, self).get_application_config(
            "~/.componga/%(appname)s.ini"
        )

    def get_resource(self, filename):
        return resource_find(filename)

    def run_launcher_cmd(self, cmd, **kwargs):
        print(f"run_launcher_cmd: {cmd}, {kwargs}")
        clock_callbacks = []

        if cmd == "show":
            clock_callbacks.append(lambda dt: self.set_monitors(kwargs["monitor"], kwargs["monitor_unsc"]))
            clock_callbacks.append(lambda dt: self.show_window())
            # clock_callback = lambda dt: self.root_window.show()
        elif cmd == "hide":
            clock_callbacks.append(lambda dt: self.hide_window())
        elif cmd == "stop":
            clock_callbacks.append(lambda dt: self.stop())
        else:
            raise Exception(f"Unknown command {cmd}")

        # Kivy doesn't allow calling methods from an external thread.
        # Schedule the call to the method in kivy's main thread instead.
        for clock_callback in clock_callbacks:
            Clock.schedule_once(clock_callback, 0)

    def _bootstrap_config(self):
        home_directory = os.path.expanduser("~")
        config_dir = os.path.join(home_directory, ".componga")

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

    def show_window(self):
        print("show_window")
        # TODO Check if a working fullscreen is platform-dependent
        # if OS == "linux":
        #     # pass
        #     # self.root_window.fullscreen = "auto"
        #     # self.root_window.fullscreen = "fake"
        #     # self.root_window.position = "custom"
        # elif OS == "darwin":
        #     # TODO Full screen custom config for OSX
        #     pass
        # elif OS == "windows":
        #     pass
        # else:
        #     raise Exception(
        #         f"OS {OS} not supported - Unable to set window to fullscreen"
        #     )

        # TODO Workaround fullscreen for Linux due to other ways being buggy, verify it works for Windows and several different monitors
        # TODO Review if the usleep calls are still needed
        self.root_window.borderless = True
        Clock.usleep(200000)
        self.root_window.maximize()

        self._position_window()
        Clock.usleep(200000)
        self._resize_window()
        Clock.usleep(200000)
        self._win_info("show_window")

        self._draw_surface.fake_desktop_background()
        self._setup_keyboard()
        self.root_window.raise_window()

    def hide_window(self):

        # TODO Check if the app is still present in the taskbar for Windows, Linux and OSX
        self.root_window.borderless = False
        Clock.usleep(200000)
        self.root_window.minimize()
        Clock.usleep(200000)
        self.root_window.hide()

    def _position_window(self):

        print(f"position_window: monitor: {self.monitor}")

        self.root_window.left, self.root_window.top = (
            self.monitor["left"],
            self.monitor["top"],
        )

        self._win_info("_position_window")

    def _resize_window(self):
        self.root_window.system_size = (
            self.monitor["width"],
            self.monitor["height"],
        )

        self._win_info("_resize_window")

    def _setup_keyboard(self):
        # Bind the keyboard to the on_key_down function
        self._keyboard = self.root_window.request_keyboard(
            self._keyboard_closed, self._draw_surface
        )
        self._keyboard.bind(
            on_key_down=self._draw_surface.on_key_down,
            on_key_up=self._draw_surface.on_key_up,
        )

    def _keyboard_closed(self):
        # Unbind the keyboard
        self._keyboard.unbind(on_key_down=self._draw_surface.on_key_down)
        self._keyboard = None

    def _win_info(self, prefix=""):
        # Used for debugging only
        import kivy.metrics

        dpis = kivy.metrics.Metrics.dpi
        density = kivy.metrics.Metrics.density

        Logger.debug(
            f"""[{prefix}] 
              monitor: {self.monitor or 'N/A'}, monitor_unsc: {self.monitor_unsc or 'N/A'}
              Metrics dpis: {dpis}, Metrics density: {density}, Window dpi: {self.root_window.dpi}
              Window: left: {self.root_window.left}, top: {self.root_window.top}
              width: {self.root_window.width}, height: {self.root_window.height}
              system_size: {self.root_window.system_size}, size: {self.root_window.size}
              position: {self.root_window.position}, fullscreen: {self.root_window.fullscreen}
              """
        )


def main(launcher=None):
    print(f"componga main: {launcher}")
    app = CompongaApp(launcher)
    app.run()


if __name__ == "__main__":
    main()
