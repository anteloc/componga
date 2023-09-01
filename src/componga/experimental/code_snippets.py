# Usage:
# res = []
# to_keypaths({'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'f': 4}, keypaths=res)
# print(f"res: {res}")
# Result:
# res: [(['a', 'b', 'c'], 1), (['a', 'b', 'd'], 2), (['a', 'e'], 3), (['f'], 4)]
def to_keypaths(adict, stack=[], keypaths=[]):
    for key, value in adict.items():
        stack.append(key)
        if isinstance(value, dict):
            to_keypaths(value, stack, keypaths)
        else:
            keypaths.append((stack.copy(), value))
        stack.pop()

# Returns the dpi's for each monitor, taking into account that each monitor can have a different dpi
def print_dpi():
    import ctypes
    import win32api

    PROCESS_PER_MONITOR_DPI_AWARE = 2
    MDT_EFFECTIVE_DPI = 0

    shcore = ctypes.windll.shcore
    monitors = win32api.EnumDisplayMonitors()
    # NOTE: This PROCESS_PER_MONITOR_DPI_AWARE configuration affects the whole application!
    # If other part of the application sets a different value before running this,
    # the assert will fail
    hresult = shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    assert hresult == 0
    dpiX = ctypes.c_uint()
    dpiY = ctypes.c_uint()
    for i, monitor in enumerate(monitors):
        shcore.GetDpiForMonitor(
            monitor[0].handle,
            MDT_EFFECTIVE_DPI,
            ctypes.byref(dpiX),
            ctypes.byref(dpiY)
        )
        print(
            f"Monitor {i} (hmonitor: {monitor[0]}) = dpiX: {dpiX.value}, dpiY: {dpiY.value}"
        )

# Makes a window transparent (layered window)
# This is not what we are looking for, because it makes the whole window transparent and
# we want to make only the background transparent.
# Besides that, the window is not clickable anymore.
def make_window_transparent():
    import sys
    import win32gui
    import win32con
    import win32api
    from kivy.core.window import Window
    
    Window.set_title("Componga")
    handle = win32gui.FindWindow(None, "Componga")
    print(f"_setup_window handle: {handle}")

    style = win32gui.GetWindowLong(handle, win32con.GWL_EXSTYLE)
    # style = style | win32con.WS_EX_TRANSPARENT
    style = style | win32con.WS_EX_LAYERED
    # # Make it a layered window
    win32gui.SetWindowLong(handle, win32con.GWL_EXSTYLE,  style)

    flags = win32con.LWA_COLORKEY
    # flags = win32con.LWA_ALPHA | win32con.LWA_COLORKEY
    colorkey = win32api.RGB(0, 0, 0)

    # # make it transparent (alpha between 0 and 255)
    alpha = 125
    win32gui.SetLayeredWindowAttributes(handle, colorkey, alpha , flags)
