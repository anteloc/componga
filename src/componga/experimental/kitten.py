from kivy.graphics import RenderContext
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.app import App
from kivy.base import EventLoop


class CustomShaderWidget(Widget):
    def __init__(self, **kwargs):
        #We must do this, if no other widget has been loaded the 
        #GL context may not be fully prepared
        EventLoop.ensure_window() 
        #Most likely you will want to use the parent projection 
        #and modelviev in order for your widget to behave the same
        #as the rest of the widgets
        # Replace canvas with RenderContext, custom shader
        self.canvas = RenderContext(use_parent_projection=True,
            use_parent_modelview=True)
        # Example using a custom shader
        self.canvas.shader.source = 'myshader.glsl'
        super(CustomShaderWidget, self).__init__(**kwargs) 
        

class CustomShaderApp(App):

    def build(self):
        shader_widget = CustomShaderWidget()
        im = Image(source='kitten.png')
        shader_widget.add_widget(im)
        shader_widget.bind(size=im.setter('size'))
        return shader_widget


if __name__ == '__main__':
    CustomShaderApp().run()