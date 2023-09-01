import os
import sys
import time
import tempfile
import mss
import mss.tools
import mouse
from componga.util.screeninfo import get_monitors
import kivy.metrics
from kivy.logger import Logger

from componga.util.constants import (SHAPE_TYPES, SHAPE_TYPES_LOWER, SHAPE_TYPES_UPPER)

class BackgroundScreenshot(object):
    def __init__(self):
        ts = time.time() * 1000
        tmp_dir = tempfile.gettempdir()
        filename = f"componga-background-{ts}.png"
        self.name = os.path.join(tmp_dir, filename)
        Logger.debug(f"image tmp file: {self.name}")

    def close(self):
        if os.path.exists(self.name):
            os.remove(self.name)

def unscale_monitor(mon):
    density = kivy.metrics.Metrics.density
    unscaled_mon = {key: int(val / density) for key, val in mon.items()}

    return unscaled_mon

def find_current_monitor():

    mons = get_monitors()
    Logger.debug(f"mons screeninfo: {mons}")
    
    mouse_x, mouse_y = mouse.get_position()
    Logger.debug(f"mouse at {mouse_x}, {mouse_y}")

    # Monitors are considered as part of the same (big) display
    with mss.mss() as sct:
        monitors = sct.monitors
        Logger.debug(f"monitors: {monitors}")

        # Start at 1 because the first monitor is the whole virtual display 
        # and the mouse pointer is always included in monitor[0]
        for mon in monitors[1:]:
            scr_x0 = mon['left']
            scr_x1 = mon['left'] + mon['width']
            scr_y0 = mon['top']
            scr_y1 = mon['top'] + mon['height']

            if mouse_x >= scr_x0 \
                and mouse_x <= scr_x1 \
                and mouse_y >= scr_y0 \
                and mouse_y <= scr_y1:
                return mon
        return None
    
def find_current_monitor_info():

    monitors = get_monitors()
    Logger.debug(f"monitors screeninfo: {monitors}")
    
    mouse_x, mouse_y = mouse.get_position()
    Logger.debug(f"mouse at {mouse_x}, {mouse_y}")

    current_monitor = None
    for mon in monitors:
        scr_x0 = mon.x
        scr_x1 = mon.x + mon.width
        scr_y0 = mon.y
        scr_y1 = mon.y + mon.height

        if mouse_x >= scr_x0 \
            and mouse_x <= scr_x1 \
            and mouse_y >= scr_y0 \
            and mouse_y <= scr_y1:
            current_monitor = mon

        if current_monitor is not None:
            density = current_monitor.density
            mss_monitor = {
                'left': current_monitor.x ,
                'top': current_monitor.y,
                'width': current_monitor.width,
                'height': current_monitor.height
            }
            mss_monitor_unsc = {key: int(val / density) for key, val in mss_monitor.items()}

            return mss_monitor, mss_monitor_unsc
        
    return None, None

def desktop_screenshot(mon, attempts=1):

    Logger.debug(f"taking screenshot for mon: {mon}")

    if attempts > 3:
        return None
 
    tmp_file = BackgroundScreenshot()
    
    with mss.mss() as sct:
        monitors = sct.monitors
        mon_number = monitors.index(mon) if mon in monitors else None
        # Maybe the previous monitor was disconnected
        if mon_number is None:
            new_mon = find_current_monitor()
            attempts += 1
            return desktop_screenshot(new_mon, attempts)

        sct_img = sct.grab(mon)
        mss.tools.to_png(sct_img.rgb, sct_img.size, level=1, output=tmp_file.name)

    return tmp_file

def _shape_type_at(index):
    index = index % len(SHAPE_TYPES)
    return SHAPE_TYPES[index]

def _sanitize_shape_hint(hint):
    # Remove all non-alphanumeric characters, including spaces and underscores
    sanitized = ''.join(letter for letter in hint if letter.isalnum())
    return sanitized

def find_shape_type(hint):
    shape_type = None
    
    if type(hint) is str:
        hint = _sanitize_shape_hint(hint)
        if hint in SHAPE_TYPES:
            shape_type = hint    
        elif hint in SHAPE_TYPES_LOWER:
            shape_type = _shape_type_at(SHAPE_TYPES_LOWER.index(hint))
        elif hint in SHAPE_TYPES_UPPER:
            shape_type = _shape_type_at(SHAPE_TYPES_UPPER.index(hint))
    elif type(hint) is int:
        shape_type = _shape_type_at(hint)

    return shape_type
