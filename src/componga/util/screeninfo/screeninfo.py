import typing as T

from componga.util.screeninfo import enumerators
from componga.util.screeninfo.common import Enumerator, Monitor, ScreenInfoError

ENUMERATOR_MAP = {
    Enumerator.Windows: enumerators.windows,
    Enumerator.Cygwin: enumerators.cygwin,
    Enumerator.Xrandr: enumerators.xrandr,
    Enumerator.Xinerama: enumerators.xinerama,
    Enumerator.DRM: enumerators.drm,
    Enumerator.OSX: enumerators.osx,
}

# XXX This is a hack to ensure that the metrics are set for the monitors, just in 
# case componga's screeninfo doesn't report the correct values
def _ensure_metrics(monitors):
    from kivy.metrics import Metrics

    for monitor in monitors:
        if monitor.dpi is None or monitor.density is None:
            from kivy.logger import Logger
            Logger.warn(f"No metrics detected by componga's screeninfo, using kivy's metrics: dpi: {Metrics.dpi}, density: {Metrics.density}")
            monitor.dpi = Metrics.dpi
            monitor.density = Metrics.density


def get_monitors(
    name: T.Union[Enumerator, str, None] = None
) -> T.List[Monitor]:
    """Returns a list of :class:`Monitor` objects based on active monitors."""
    if name is not None:
        return list(ENUMERATOR_MAP[Enumerator(name)].enumerate_monitors())

    for enumerator in ENUMERATOR_MAP.keys():
        try:
            monitors = get_monitors(enumerator)
        except Exception as ex:
            monitors = []

        if monitors:
            from kivy.logger import Logger
            Logger.debug(f"Monitors found by enumerator: {enumerator.value}")

            _ensure_metrics(monitors)
            return monitors

    raise ScreenInfoError("No enumerators available")
