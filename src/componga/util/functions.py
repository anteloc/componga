import mouse
# from kivy.logger import Logger


from .constants import SHAPE_TYPES, SHAPE_TYPES_LOWER, SHAPE_TYPES_UPPER
from .screeninfo import get_monitors


# XXX This is a hack to ensure that the metrics are set for the monitors, just in
#   case componga's screeninfo doesn't report the correct values
def _ensure_metrics(monitors):
    for mon in monitors:
        if mon.dpi is None or mon.density is None:
            # Logger.warn(
            #     f"No metrics detected by componga's screeninfo, using kivy's metrics: dpi: {Metrics.dpi}, density: {Metrics.density}"
            # )

            from kivy.metrics import Metrics

            mon.dpi = Metrics.dpi
            mon.density = Metrics.density


def _add_friendly_names(monitors):
    for i, mon in enumerate(monitors):
        mon.friendly_name = f"Monitor {i + 1} - {mon.width}x{mon.height}"


def get_monitors_info():
    monitors = get_monitors()
    _ensure_metrics(monitors)
    _add_friendly_names(monitors)

    mon_infos = [
        {
            "left": mon.x,
            "top": mon.y,
            "width": mon.width,
            "height": mon.height,
            "friendly_name": mon.friendly_name,
            "density": mon.density,
        }
        for mon in monitors
    ]

    return mon_infos


def monitors_unsc_info(mon):
    density = mon["density"]

    mon_unsc = {
        key: int(val / density) if not isinstance(val, str) else val
        for key, val in mon.items()
    }

    return mon, mon_unsc


def find_current_monitor_info():
    monitors = get_monitors_info()

    # Logger.debug(f"monitors screeninfo: {monitors}")

    mouse_x, mouse_y = mouse.get_position()
    # Logger.debug(f"mouse at {mouse_x}, {mouse_y}")

    current_monitor = None

    for mon in monitors:
        scr_x0 = mon["left"]
        scr_x1 = mon["left"] + mon["width"]
        scr_y0 = mon["top"]
        scr_y1 = mon["top"] + mon["height"]

        if (
            mouse_x >= scr_x0
            and mouse_x <= scr_x1
            and mouse_y >= scr_y0
            and mouse_y <= scr_y1
        ):
            current_monitor = mon

        if current_monitor is not None:
            return current_monitor, monitors_unsc_info(current_monitor)
            # density = current_monitor.density
            # mss_monitor = {
            #     "left": current_monitor.x,
            #     "top": current_monitor.y,
            #     "width": current_monitor.width,
            #     "height": current_monitor.height,
            # }
            # mss_monitor_unsc = {
            #     key: int(val / density) for key, val in mss_monitor.items()
            # }
            #
            # return mss_monitor, mss_monitor_unsc

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
