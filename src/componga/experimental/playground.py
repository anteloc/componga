import sys

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
