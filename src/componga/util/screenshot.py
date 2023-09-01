import platform
from kivy.logger import Logger
from kivy.clock import Clock
from componga.util.functions import desktop_screenshot

OS = platform.system().lower()

class _BackgroundScreenshotHandlerTrait(object):
    
    def take_screenshot(self, mon, target, win):
        self._hide_window(win)
        bg = self._capture_background(mon)
        self._show_window(win)

        target.background = bg

    def _capture_background(self, mon):
        return desktop_screenshot(mon)


class _OSXBackgroundScreenshotHandler(_BackgroundScreenshotHandlerTrait):
    def _hide_window(self, win):
        # TODO NOT tested on OSX
        win.hide()

        Clock.usleep(200000)

    def _show_window(self, win):
        win.show()


class _WindowsBackgroundScreenshotHandler(_BackgroundScreenshotHandlerTrait):
    
    _prev_style = None

    def _hide_window(self, win):
        # Widows only, to improve performance and avoid issues with native windows
        import win32gui
        import win32con
        
        handle = win32gui.FindWindow(None, win.title)
        Logger.debug(f"[{self.__class__}] _hide_window handle: {handle}")
        
        win32gui.ShowWindow(handle, win32con.SW_HIDE)

        Clock.usleep(300000)

    def _show_window(self, win):
        import win32gui
        import win32con
        
        handle = win32gui.FindWindow(None, win.title)
        Logger.debug(f"[{self.__class__}] _show_window handle: {handle}")

        win32gui.ShowWindow(handle, win32con.SW_SHOW)


class _LinuxBackgroundScreenshotHandler(_BackgroundScreenshotHandlerTrait):
    def _hide_window(self, win):
        # For Linux, given that there are multiple desktop managers, 
        # handling the window in a native way would be too complex
        win.hide()

        Clock.usleep(200000)

    def _show_window(self, win):
        win.show()

class BackgroundScreenshotHandler(object):
    def __init__(self, target):
        from kivy.app import App
        self._target = target
        self._app = App.get_running_app()
        self._mon = self._app.monitor
        self._delegate = None

    def _create_delegate(self):
        if OS == "darwin":
            self._delegate = _OSXBackgroundScreenshotHandler()
        elif OS == "linux":
            self._delegate = _LinuxBackgroundScreenshotHandler()
        elif OS == "windows":
            self._delegate = _WindowsBackgroundScreenshotHandler()
        else:
            raise Exception(f"OS {OS} not supported")

    def take_screenshot(self):
        # Importing the window here to avoid initializing the window 
        # before the app is ready
        try:
            if self._delegate is None:
                self._create_delegate()

            self._delegate.take_screenshot(self._mon, self._target, self._app.root_window)
        except Exception as e:
            Logger.exception(f"Error taking screenshot: {e}")
            raise e