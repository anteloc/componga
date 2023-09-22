from kivy.factory import Factory

from .constants import (
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

from .functions import find_current_monitor_info, find_shape_type

from .mixins import HoverSizeMixin

from .screenshot import BackgroundScreenshotHandler

mixins = ("HoverAnimationMixin", "HoverSizeMixin", "HoverSizeHintMixin")

# Required for kivy .kv files to recognize the mixins when creating rules and templates
for mixin in mixins:
    Factory.register(mixin, module="componga.util.mixins")
