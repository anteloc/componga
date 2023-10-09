from .constants import (
    OS,
    SHAPE_TYPES,
    DEFAULT_CONFIG_SECTIONS,
    DEFAULT_SHAPE,
    DEFAULT_SHAPE_COLOR,
    DEFAULT_SHAPE_FADE_DURATION,
    DEFAULT_SHAPE_LINE_WIDTH,
    MIN_SHAPE_LINE_WIDTH,
    MAX_SHAPE_LINE_WIDTH,
    SCREEN_TITLE,
)

from .functions import get_monitors_info, monitors_unsc_info, find_current_monitor_info, find_shape_type

from .screenshot import BackgroundScreenshotHandler, desktop_screenshot

