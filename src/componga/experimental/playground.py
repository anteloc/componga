import sys
from kivy.config import Config
# Disable config: %(name)s = probesysfs
# since it causes touchpad behave like it's a touchscreen
Config.set('input', '%(name)s', None)
############################################
from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder

# Load the kv string
Builder.load_string("""
<TouchAwareButton@Button>:
    on_touch_down:
        self.collide_point(*args[1].pos) and self.dispatch('on_press')
""")

class AnimatedScatterApp(App):
    def build(self):
        # Create a ScatterLayout
        scatter = ScatterLayout(size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Add a Label and two TouchAwareButtons to the ScatterLayout
        scatter.add_widget(Button(text="This is a regular button"))
        scatter.add_widget(Button(text="Touch Aware Button 1", cls='TouchAwareButton'))
        scatter.add_widget(Button(text="Touch Aware Button 2", cls='TouchAwareButton'))

        # Schedule the animation
        Clock.schedule_once(lambda dt: self.animate_scatter(scatter), 1)

        return scatter

    def animate_scatter(self, scatter):
        # Animate the position and scale of the ScatterLayout
        anim = Animation(pos=(100, 100), scale=1.5, duration=2) + \
               Animation(pos=(0, 0), scale=1, duration=2)  # Revert to original state

        anim.repeat = True  # Make the animation repeat indefinitely
        anim.start(scatter)

if __name__ == "__main__":
    AnimatedScatterApp().run()



sys.exit(0)

from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.lang import Builder

Window.size = (500, 500)

KV_STRING = '''
<HoverTextButton>:
    size_hint: 0.5, 0.2
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    font_size: 20
'''

Builder.load_string(KV_STRING)

class HoverTextButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_motion=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        pos = args[2]
        if self.collide_point(*pos):
            self.animate_size((0.6, 0.3))
        else:
            self.animate_size((0.5, 0.2))

    def animate_size(self, new_size_hint):
        anim = Animation(size_hint=new_size_hint, duration=0.2)
        anim.start(self)

class HoverApp(App):
    def build(self):
        return HoverTextButton(text='Hover Me!')

if __name__ == "__main__":
    HoverApp().run()


sys.exit(0)

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from collections import OrderedDict
from kivy.properties import BooleanProperty

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
from collections import OrderedDict

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
from collections import OrderedDict

# KV language string
kv = '''
<PopupHelp>:
    title: 'Help'
    title_align: 'center'
    size_hint: .5, .5
    BoxLayout:
        id: content
        orientation: 'vertical'
        padding: 10
        spacing: 10
        ScrollView:
            id: scroll
            bar_width: 10
            scroll_type: ['bars', 'content']
            BoxLayout:
                id: scroll_content
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height

BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Show Popup'
        size_hint: (None, None)
        size: (200, 50)
        pos_hint: {'center_x': 0.5}
        on_press: app.show_popup()
'''

# Load the KV string
Builder.load_string(kv)

class PopupHelp(Popup):
    pass

class MainApp(App):
    def build(self):
        return Builder.load_string(kv)  # Return the root widget defined in the kv string

    def show_popup(self):
        popup = PopupHelp()
        items = OrderedDict([
            ('Item 1', 'Help for [color=ff3333]Item 1[/color]'),
            ('Item 2', 'Help for [i]Item 2[/i]'),
            ('Item 3', 'Help for [b]Item 3[/b]'),
            # ... Add more items as required ...
        ])
        
        for key, value in items.items():
            lbl = Label(text=f"{key}: {value}", size_hint_y=None, height=44, markup=True)
            popup.ids.scroll_content.add_widget(lbl)
        
        popup.open()

if __name__ == '__main__':
    MainApp().run()


sys.exit(0)

# KV language string
kv = '''
<PopupHelp>:
    title: 'Help'
    title_align: 'center'
    size_hint: .5, .5
    BoxLayout:
        id: content
        orientation: 'vertical'
        padding: 10
        spacing: 10
        ScrollView:
            id: scroll
            bar_width: 10
            scroll_type: ['bars', 'content']
            BoxLayout:
                id: scroll_content
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height

BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Show Popup'
        size_hint: (None, None)
        size: (200, 50)
        pos_hint: {'center_x': 0.5}
        on_press: app.show_popup()
'''

# Load the KV string
Builder.load_string(kv)

class PopupHelp(Popup):
    pass

class MainApp(App):
    def build(self):
        return self.root

    def show_popup(self):
        popup = PopupHelp()
        items = OrderedDict([
            ('Item 1', 'Help for [color=ff3333]Item 1[/color]'),
            ('Item 2', 'Help for [i]Item 2[/i]'),
            ('Item 3', 'Help for [b]Item 3[/b]'),
            # ... Add more items as required ...
        ])
        
        for key, value in items.items():
            lbl = Label(text=f"{key}: {value}", size_hint_y=None, height=44, markup=True)
            popup.ids.scroll_content.add_widget(lbl)
        
        popup.open()

if __name__ == '__main__':
    MainApp().run()

sys.exit(0)

# Define custom MarkupLabel
class MarkupLabel(Label):
    markup = BooleanProperty(True)

class PopupHelp(Popup):
    pass

class MainApp(App):
    
    def build(self):
        layout = BoxLayout(orientation='vertical')
        btn = Button(text='Show Popup', size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
        btn.bind(on_press=self.show_popup)
        layout.add_widget(btn)
        return layout

    def show_popup(self, instance):
        popup = PopupHelp()

        # Using OrderedDict to maintain the order
        items = OrderedDict([
            ('Item 1', 'Help for [color=ff3333]Item 1[/color]'),
            ('Item 2', 'Help for [i]Item 2[/i]'),
            ('Item 3', 'Help for [b]Item 3[/b]'),
            # ... Add more items as required ...
        ])
        
        for key, value in items.items():
            lbl = Label(text=f"[b]{key}:[/b] {value}", size_hint_y=None, height=44, markup=True)
            # lbl = MarkupLabel(text=f"{key}: {value}", size_hint_y=None, height=44)
            popup.ids.scroll_content.add_widget(lbl)
        
        popup.open()

if __name__ == '__main__':
    MainApp().run()




sys.exit(0)

class MainApp(App):
    
    def build(self):
        layout = BoxLayout(orientation='vertical')
        btn = Button(text='Show Popup', size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
        btn.bind(on_press=self.show_popup)
        layout.add_widget(btn)
        
        return layout

    def show_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Create a scrollable list of items
        scroll_content = BoxLayout(orientation='vertical', size_hint_y=None)
        items = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5',
                 'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10']
        
        # The height should be adjusted based on the number of items and their individual height.
        scroll_content.bind(minimum_height=scroll_content.setter('height'))
        
        for item in items:
            lbl = Label(text=item, size_hint_y=None, height=44)
            scroll_content.add_widget(lbl)
        
        scroll_view = ScrollView()
        scroll_view.bar_width = 10
        scroll_view.scroll_type = ['bars', 'content']

        scroll_view.add_widget(scroll_content)
        content.add_widget(scroll_view)
        
        close_btn = Button(text='Close', size_hint=(None, None), size=(150, 50))
        content.add_widget(close_btn)
        
        popup = Popup(title='List of Items', content=content, size_hint=(None, None), size=(400, 500))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    MainApp().run()


sys.exit(0)

# from kivy.app import App
# from kivy.lang import Builder
# from kivy.core.window import Window
# from kivy.metrics import sp, Metrics
# from kivy.properties import NumericProperty

# # Make the function available in KV language.
# resizabletext = """
# BoxLayout:
#     orientation: 'vertical'
#     Label:
#         text: 'Dynamically resizing text'
#         font_size: app.font_size
#     Button:
#         text: 'Another widget'
#         size_hint_y: None
#         height: app.font_size * 2

# """



# class ResizableTextApp(App):
#     font_size = NumericProperty(sp(15))  # Default value

#     def build(self):
#         # Bind to the window's size change event
#         Window.bind(size=self.update_font_size)
#         return Builder.load_string(resizabletext)

#     def update_font_size(self, instance, value):
#         base_font_size = 15  # A default base size
#         scale_factor = Metrics.density  # Assuming 1000 is the width at which base_font_size looks best
#         self.font_size = sp(base_font_size * scale_factor)

# ResizableTextApp().run()



# sys.exit(0)

# from pynput.mouse import Button, Controller

# mouse = Controller()

# # Read pointer position
# print('The current pointer position is {0}'.format(
#     mouse.position))

# sys.exit(0)


def print_dpi():
    import ctypes
    import win32api
    import screeninfo

    PROCESS_PER_MONITOR_DPI_AWARE = 2
    MDT_EFFECTIVE_DPI = 0

    monitors_info = screeninfo.get_monitors()

    # monitors_info = screeninfo.get_monitors()
    shcore = ctypes.windll.shcore
    monitors = win32api.EnumDisplayMonitors()
    # hresult = shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    # assert hresult == 0
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


if __name__ == "__main__":
    print_dpi()

sys.exit(0)
from kivy.config import Config
Config.set('graphics', 'multisamples', '4')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line

class LineApp(App):
    def build(self):
        root = Widget()
        with root.canvas:
            Line(points=[10, 10, 300, 300], width=20)
        return root

LineApp().run()


sys.exit(0)

from screeninfo import get_monitors
import pyautogui

# Get monitor information
monitors = get_monitors()

# Loop through all available monitors and take screenshots
for i, monitor in enumerate(monitors):
    left = monitor.x
    top = monitor.y
    width = monitor.width
    height = monitor.height
    
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save(f"screenshot_monitor_{i + 1}.png")


sys.exit(0)

from kivy.app import App
from kivy.uix.label import Label
from kivy.metrics import Metrics

class MyApp(App):

    def build(self):
        return Label(text=f'DPI: {Metrics.dpi}')

if __name__ == '__main__':
    MyApp().run()

sys.exit(0)

class Person:
    def greet(self, greeting="salutations"):
        print(f"{greeting}, !")

# Create an instance of the Person class
p = Person()

# Pack the arguments into a dictionary
args = {'greeting': 'Hello'}

# Use getattr to get the method and invoke it with the unpacked dictionary
method_to_call = getattr(p, 'greet')
method_to_call(**args)


sys.exit(0)

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from PIL import Image as PILImage
import mss
import io

class ScreenshotApp(App):

    def build(self):
        # Create a BoxLayout to hold the Image widget
        self.layout = BoxLayout()
        
        # Take initial screenshot and set it as the window background
        self.set_background_from_screenshot()
        
        # Bind the "u" key to update the background
        Window.bind(on_key_down=self.key_action)
        
        # Bind the on_hide event to update the background
        Window.bind(on_hide=self.update_background)
        
        return self.layout

    def key_action(self, *args):
        key = args[1]
        
        # Check if the "u" key is pressed
        if key == 117:
            # Minimize the window
            Window.minimize()
    
    def update_background(self, *args):
        # Take a new screenshot and set it as the window background
        self.set_background_from_screenshot()
        
        # Restore the window
        Window.restore()

    def set_background_from_screenshot(self):
        # Take a screenshot using mss
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
        
        # Convert the screenshot to a PIL Image
        pil_image = PILImage.frombytes(
            "RGB",
            screenshot.size,
            screenshot.bgra,
            "raw",
            "BGRX"
        )
        
        # Convert the PIL Image to a Kivy Texture
        img_data = io.BytesIO()
        pil_image.save(img_data, format='png')
        img_data.seek(0)
        img_texture = Texture.create(size=(pil_image.width, pil_image.height), colorfmt='rgb')
        img_texture.blit_buffer(img_data.read(), colorfmt='rgb', bufferfmt='ubyte')
        
        # Create an Image widget with the texture
        img = Image(texture=img_texture)
        
        # Clear the layout and add the new Image widget
        self.layout.clear_widgets()
        self.layout.add_widget(img)

if __name__ == '__main__':
    ScreenshotApp().run()

# from kivy.core.window import Window
# from kivy.uix.widget import Widget

# class MyKeyboardListener(Widget):

#     def __init__(self, **kwargs):
#         super(MyKeyboardListener, self).__init__(**kwargs)
#         self._keyboard = Window.request_keyboard(
#             self._keyboard_closed, self, 'text')
#         if self._keyboard.widget:
#             # If it exists, this widget is a VKeyboard object which you can use
#             # to change the keyboard layout.
#             pass
#         self._keyboard.bind(on_key_down=self._on_keyboard_down)
#         self._keyboard.bind(on_key_up=self._on_keyboard_up)  # Bind the on_key_up event

#     def _keyboard_closed(self):
#         print('My keyboard has been closed!')
#         self._keyboard.unbind(on_key_down=self._on_keyboard_down)
#         self._keyboard.unbind(on_key_up=self._on_keyboard_up)  # Unbind the on_key_up event
#         self._keyboard = None

#     def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
#         print(f"keycode: {keycode}, text: {text}, modifiers: {modifiers}")

#         if keycode[1] == 'shift':
#             print("Shift key pressed")

#         if keycode[1] == 'escape':
#             keyboard.release()

#         return True

#     def _on_keyboard_up(self, keyboard, keycode):
#         print(f"keycode: {keycode}")

#         if keycode[1] == 'shift':
#             print("Shift key released")

#         if keycode[1] == 'escape':
#             keyboard.release()

#         return True

# if __name__ == '__main__':
#     from kivy.base import runTouchApp
#     runTouchApp(MyKeyboardListener())


# # import kivy
# # kivy.require('1.0.8')

# # from kivy.core.window import Window
# # from kivy.uix.widget import Widget


# # class MyKeyboardListener(Widget):

# #     def __init__(self, **kwargs):
# #         super(MyKeyboardListener, self).__init__(**kwargs)
# #         self._keyboard = Window.request_keyboard(
# #             self._keyboard_closed, self, 'text')
# #         if self._keyboard.widget:
# #             # If it exists, this widget is a VKeyboard object which you can use
# #             # to change the keyboard layout.
# #             pass
# #         self._keyboard.bind(on_key_down=self._on_keyboard_down)

# #     def _keyboard_closed(self):
# #         print('My keyboard have been closed!')
# #         self._keyboard.unbind(on_key_down=self._on_keyboard_down)
# #         self._keyboard = None

# #     def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
# #         print(f"keycode: {keycode}, text: {text}, modifiers: {modifiers}")

# #         # Keycode is composed of an integer + a string
# #         # If we hit escape, release the keyboard
# #         if keycode[1] == 'escape':
# #             keyboard.release()

# #         # Return True to accept the key. Otherwise, it will be used by
# #         # the system.
# #         return True
    
# #     def _on_keyboard_up(self, keyboard, keycode):
# #         print(f"keycode: {keycode}")

# #         # Keycode is composed of an integer + a string
# #         # If we hit escape, release the keyboard
# #         if keycode[1] == 'escape':
# #             keyboard.release()

# #         # Return True to accept the key. Otherwise, it will be used by
# #         # the system.
# #         return True


# # if __name__ == '__main__':
# #     from kivy.base import runTouchApp
# #     runTouchApp(MyKeyboardListener())

# # from kivy.app import App
# # from kivy.uix.relativelayout import RelativeLayout
# # from kivy.uix.effectwidget import *
# # from kivy.uix.button import Button

# # from kivy.app import App
# # from kivy.uix.relativelayout import RelativeLayout
# # from kivy.uix.effectwidget import EffectWidget, MonochromeEffect
# # from kivy.uix.button import Button

# # class DraggableEffectWidget(EffectWidget):
# #     def __init__(self, **kwargs):
# #         super(DraggableEffectWidget, self).__init__(**kwargs)
# #         self.effects = [ScanlinesEffect()]
# #         self.dragging = False
# #         self.button = Button(text="Drag Me!", size_hint=(None, None), size=(100, 50))
# #         self.add_widget(self.button)

# #     def on_touch_down(self, touch):
# #         if self.button.collide_point(*touch.pos):
# #             self.dragging = True
# #             touch.grab(self)
# #             return True
# #         return super(DraggableEffectWidget, self).on_touch_down(touch)

# #     def on_touch_move(self, touch):
# #         if touch.grab_current is self:
# #             self.button.center_x = touch.x
# #             self.button.center_y = touch.y
# #             return True
# #         return super(DraggableEffectWidget, self).on_touch_move(touch)

# #     def on_touch_up(self, touch):
# #         if touch.grab_current is self:
# #             self.dragging = False
# #             touch.ungrab(self)
# #             return True
# #         return super(DraggableEffectWidget, self).on_touch_up(touch)

# # class MyApp(App):
# #     def build(self):
# #         root = RelativeLayout()
# #         draggable_effect_widget = DraggableEffectWidget(size_hint=(1, 1))
# #         root.add_widget(draggable_effect_widget)
# #         return root

# # if __name__ == '__main__':
# #     MyApp().run()


# # from kivy.app import App
# # from kivy.uix.boxlayout import BoxLayout
# # from kivy.uix.effectwidget import *
# # from kivy.uix.button import Button

# # class MyApp(App):
# #     def build(self):
# #         self.layout = BoxLayout(orientation='vertical')
        
# #         self.effect_widget = EffectWidget()
# #         self.effect_widget.effects = [ScanlinesEffect()]
# #         self.effect_widget.add_widget(Button(text='I am monochrome!'))
        
# #         move_button = Button(text='Move Effect')
# #         move_button.bind(on_press=self.move_effect)
        
# #         self.layout.add_widget(self.effect_widget)
# #         self.layout.add_widget(move_button)
        
# #         return self.layout

# #     def move_effect(self, instance):
# #         self.layout.remove_widget(self.effect_widget)
# #         self.layout.add_widget(self.effect_widget)

# # if __name__ == '__main__':
# #     MyApp().run()
