SCREEN_TITLE = "componga"

SHAPE_TYPES = ('Blip', 'ArrowPath', 'ArrowStraight', 'LineStraight', 'Ellipse', 'Rectangle', 'Path')
SHAPE_TYPES_LOWER = list(map(lambda t: t.lower(), SHAPE_TYPES))
SHAPE_TYPES_UPPER = list(map(lambda t: t.upper(), SHAPE_TYPES))

DEFAULT_SHAPE = 'ArrowStraight'
DEFAULT_SHAPE_LINE_WIDTH = 5
MIN_SHAPE_LINE_WIDTH = 1
MAX_SHAPE_LINE_WIDTH = 15
DEFAULT_SHAPE_COLOR = (1, 0, 0, 1)
DEFAULT_SHAPE_FADE_DURATION = 5.0

DEFAULT_CONFIG_SECTIONS = [
    {
        'name': 'shapes.attributes',
        'options': {
            'shape_type': DEFAULT_SHAPE,
            'shape_line_width': DEFAULT_SHAPE_LINE_WIDTH,
            'min_shape_line_width': MIN_SHAPE_LINE_WIDTH,
            'max_shape_line_width': MAX_SHAPE_LINE_WIDTH,
            'shape_color': DEFAULT_SHAPE_COLOR,
            'shape_fade_duration': DEFAULT_SHAPE_FADE_DURATION
            }
    },
    {
        'name': 'keyboard.shortcuts',
        'options': {
            'freeze': 'f',
            'update_background': 'u',
            'exit': 'escape',
            'select_blip': 'b',
            'select_arrow_path': 'a',
            'select_arrow_straight': 's',
            'select_line_straight': 'l',
            'select_ellipse': 'e',
            'select_rectangle': 'r',
            'select_path': 'p'
        }
    },
    {
        'name': 'keyboard.shortcuts.help',
        'options': {
            'freeze': 'Disable shape fading',
            'update_background': 'Refresh desktop image',
            'exit': 'Exit Componga',
            'select_blip': 'Select Blip tool',
            'select_arrow_path': 'Select ArrowPath tool',
            'select_arrow_straight': 'Select ArrowStraight tool',
            'select_line_straight': 'Select LineStraight tool',
            'select_ellipse': 'Select Ellipse tool',
            'select_rectangle': 'Select Rectangle tool',
            'select_path': 'Select Path tool'
        }
    }
]


