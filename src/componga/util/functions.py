import mouse
from kivy.logger import Logger
from kivy.metrics import Metrics

from .constants import SHAPE_TYPES, SHAPE_TYPES_LOWER, SHAPE_TYPES_UPPER
from .screeninfo import get_monitors


# XXX This is a hack to ensure that the metrics are set for the monitors, just in
#   case componga's screeninfo doesn't report the correct values
def _ensure_metrics(monitors):
    for monitor in monitors:
        if monitor.dpi is None or monitor.density is None:
            Logger.warn(
                f"No metrics detected by componga's screeninfo, using kivy's metrics: dpi: {Metrics.dpi}, density: {Metrics.density}"
            )
            monitor.dpi = Metrics.dpi
            monitor.density = Metrics.density


def find_current_monitor_info():
    monitors = get_monitors()
    _ensure_metrics(monitors)

    Logger.debug(f"monitors screeninfo: {monitors}")

    mouse_x, mouse_y = mouse.get_position()
    Logger.debug(f"mouse at {mouse_x}, {mouse_y}")

    current_monitor = None

    for mon in monitors:
        scr_x0 = mon.x
        scr_x1 = mon.x + mon.width
        scr_y0 = mon.y
        scr_y1 = mon.y + mon.height

        if (
            mouse_x >= scr_x0
            and mouse_x <= scr_x1
            and mouse_y >= scr_y0
            and mouse_y <= scr_y1
        ):
            current_monitor = mon

        if current_monitor is not None:
            density = current_monitor.density
            mss_monitor = {
                "left": current_monitor.x,
                "top": current_monitor.y,
                "width": current_monitor.width,
                "height": current_monitor.height,
            }
            mss_monitor_unsc = {
                key: int(val / density) for key, val in mss_monitor.items()
            }

            return mss_monitor, mss_monitor_unsc

    return None, None


def _shape_type_at(index):
    index = index % len(SHAPE_TYPES)
    return SHAPE_TYPES[index]


def _sanitize_shape_hint(hint):
    # Remove all non-alphanumeric characters, including spaces and underscores
    sanitized = "".join(letter for letter in hint if letter.isalnum())
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
