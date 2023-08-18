import sys
import tempfile
from mss import mss, tools
import mss.tools
import pyautogui

# FIXME This is a hack to import from the parent directory
sys.path.append("..") 

from constants.constants import (SHAPE_TYPES, SHAPE_TYPES_LOWER, SHAPE_TYPES_UPPER)

def find_current_monitor():
        
    mouse_x, mouse_y = pyautogui.position()

    print(f"mouse at {mouse_x}, {mouse_y}")

    # Monitors are considered as part of the same (big) display
    with mss.mss() as sct:
        monitors = sct.monitors

        # Start at 1 because the first monitor is the whole display 
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

def desktop_screenshot(mon, attempts=1):

    print(f"mon: {mon}")

    if attempts > 3:
        return None

    tmp_file = tempfile.NamedTemporaryFile(suffix='.png')
    
    with mss.mss() as sct:
        monitors = sct.monitors
        mon_number = monitors.index(mon) if mon in monitors else None
        # Maybe the previous monitor was disconnected
        if mon_number is None:
            new_mon = find_current_monitor()
            attempts += 1
            return desktop_screenshot(new_mon, attempts)

        # Generator, requires next() to actually save the screenshot
        next(sct.save(mon=mon_number, output=tmp_file.name))

        print(f"tmp_file: {tmp_file.name}")

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
        print(f"hint: {hint}")
        if hint in SHAPE_TYPES:
            shape_type = hint    
        elif hint in SHAPE_TYPES_LOWER:
            shape_type = _shape_type_at(SHAPE_TYPES_LOWER.index(hint))
        elif hint in SHAPE_TYPES_UPPER:
            shape_type = _shape_type_at(SHAPE_TYPES_UPPER.index(hint))
    elif type(hint) is int:
        shape_type = _shape_type_at(hint)

    return shape_type

# filename = mss.mss().shot(mon=1, output='screenshot.png')
