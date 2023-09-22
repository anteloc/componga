from kivy.uix.effectwidget import EffectWidget

from kivy.uix.effectwidget import (
    EffectBase,
    MonochromeEffect,
    InvertEffect,
    ChannelMixEffect,
    ScanlinesEffect,
    FXAAEffect,
    PixelateEffect,
    HorizontalBlurEffect,
    VerticalBlurEffect,
)

from kivy.uix.effectwidget import shader_header, shader_uniforms, shader_footer_effect

# Taking examples/widgets/effectwidget.py as a starting point, develop a "chroma" effect
# That applies an effect only to a certain color range
# maybe effect_postprocessing is a good place to start, because the effect is applied to colors...
# maybe modify that effect to check if-statement the original colors are to be excluded
# or else apply the effect to the color

# effect_chroma = '''
# vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
# {
#     vec4 result;
#     if (color.r == 0.0 && color.g == 1.0 && color.b == 0.0) {
#         result = vec4(0.0, 0.0, 1.0, 1.0);
#     } else {
#         result = color;
#     }

#     return result;
# }
# '''

# effect_chroma = '''
# vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
# {
#     if (color.r == 0.0 && color.g == 1.0 && color.b == 0.0) {
#         vec2 q = tex_coords * vec2(1, -1);
#         vec2 uv = 0.5 + (q-0.5);//*(0.9);// + 0.1*sin(0.2*time));

#         vec3 oricol = texture2D(texture,vec2(q.x,1.0-q.y)).xyz;
#         vec3 col;

#         col.r = texture2D(texture,vec2(uv.x+0.003,-uv.y)).x;
#         col.g = texture2D(texture,vec2(uv.x+0.000,-uv.y)).y;
#         col.b = texture2D(texture,vec2(uv.x-0.003,-uv.y)).z;

#         col = clamp(col*0.5+0.5*col*col*1.2,0.0,1.0);

#         //col *= 0.5 + 0.5*16.0*uv.x*uv.y*(1.0-uv.x)*(1.0-uv.y);

#         col *= vec3(0.8,1.0,0.7);

#         col *= 0.9+0.1*sin(10.0*time+uv.y*1000.0);

#         col *= 0.97+0.03*sin(110.0*time);

#         float comp = smoothstep( 0.2, 0.7, sin(time) );
#         //col = mix( col, oricol, clamp(-2.0+2.0*q.x+3.0*comp,0.0,1.0) );

#         return vec4(col, color.w);
#     } else {
#         return color;
#     }
# }
# '''

# effect_chroma_blur = '''
# vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
# {{
#     if (color.r == 0.0 && color.g == 1.0 && color.b == 0.0) {{
#         float dt = ({} / 4.0) * 1.0 / resolution.x;
#         vec4 sum = vec4(0.0);
#         sum += texture2D(texture, vec2(tex_coords.x - 4.0*dt, tex_coords.y))
#                         * 0.05;
#         sum += texture2D(texture, vec2(tex_coords.x - 3.0*dt, tex_coords.y))
#                         * 0.09;
#         sum += texture2D(texture, vec2(tex_coords.x - 2.0*dt, tex_coords.y))
#                         * 0.12;
#         sum += texture2D(texture, vec2(tex_coords.x - dt, tex_coords.y))
#                         * 0.15;
#         sum += texture2D(texture, vec2(tex_coords.x, tex_coords.y))
#                         * 0.16;
#         sum += texture2D(texture, vec2(tex_coords.x + dt, tex_coords.y))
#                         * 0.15;
#         sum += texture2D(texture, vec2(tex_coords.x + 2.0*dt, tex_coords.y))
#                         * 0.12;
#         sum += texture2D(texture, vec2(tex_coords.x + 3.0*dt, tex_coords.y))
#                         * 0.09;
#         sum += texture2D(texture, vec2(tex_coords.x + 4.0*dt, tex_coords.y))
#                         * 0.05;
#         return vec4(sum.xyz, color.w);
#     }} else {{
#         return color;
#     }}
# }}
# '''

# FIXME Maybe consider include/exclude alpha channel? Currently, fading combined with this does not work as expected
shader_footer_chroma_effect = """
void main (void) {{
    vec4 normal_color = frag_color * texture2D(texture0, tex_coord0);

    // Define target color and tolerance
    vec4 target_color = vec4({}, {}, {}, {});
    vec4 tolerance = vec4({}, {}, {}, {});

    // Check if normal_color is within the tolerance range of target_color
    bool is_within_range = all(lessThanEqual(abs(normal_color - target_color), tolerance));

    if (is_within_range) {{
        vec4 effect_color = effect(normal_color, texture0, tex_coord0, gl_FragCoord.xy);
        gl_FragColor = effect_color;
    }} else {{
        gl_FragColor = normal_color;
    }}
}}
"""


# XXX How to avoid the mixin requiring an initialization?
class ChromaShapeEffectMixin:
    def __init__(self, chroma_color, chroma_tolerance, **kwargs):
        self._shape = None

        # Tolerance allows to define a range of colors to be affected by the effect
        self._chroma_color = tuple(map(float, chroma_color))
        self._chroma_tolerance = tuple(map(float, chroma_tolerance))

    def set_fbo_shader(self, *args):
        shader_footer_chroma = shader_footer_chroma_effect.format(
            *self._chroma_color, *self._chroma_tolerance
        )

        print(shader_footer_chroma)

        if self.fbo is None:
            return

        self.fbo.set_fs(
            shader_header + shader_uniforms + self.glsl + shader_footer_chroma
        )

    # XXX These two methods are required in order to delegate the "fading" to the actual shape, not to the mixin
    # Maybe find another way in order to avoid these two methods to be delegated to the shape?
    def fade_shape(self):
        if self._shape:
            self._shape.fade_shape()

    def cancel_fade(self):
        if self._shape:
            self._shape.cancel_fade()


# XXX Is there a better way to add the mixin to the class?
class ChromaScanlinesEffect(ChromaShapeEffectMixin, ScanlinesEffect):
    def __init__(
        self,
        *args,
        #  shape=None,
        chroma_color=(1, 1, 1, 1),
        chroma_tolerance=(0.1, 0.1, 0.1, 0.1),
        **kwargs
    ):
        ChromaShapeEffectMixin.__init__(self, chroma_color, chroma_tolerance)
        ScanlinesEffect.__init__(self, *args, **kwargs)

        # self.add_widget(self._shape)

    def add_widget(self, widget):
        self._shape = widget
        super(ScanlinesEffect, self).add_widget(widget)

        # super(ScanlinesEffect, self).add_widget(self._shape)


class ChromaHorizontalBlurEffect(ChromaShapeEffectMixin, HorizontalBlurEffect):
    pass


class ChromaVerticalBlurEffect(ChromaShapeEffectMixin, VerticalBlurEffect):
    pass


class ShapeEffect(EffectWidget):
    def add_widget(self, shape, *args, **kwargs):
        self.shape = shape
        self.bind(on_touch_down=shape.on_touch_down)
        self.bind(on_touch_move=shape.on_touch_move)
        self.bind(on_touch_up=shape.on_touch_up)
        self.cancel_fade = shape.cancel_fade
        self.fade_shape = shape.fade_shape

        return super().add_widget(shape, *args, **kwargs)


class DraggableEffectWidget(EffectWidget):
    def __init__(self, shape, **kwargs):
        super(DraggableEffectWidget, self).__init__(**kwargs)
        self.effects = [MonochromeEffect()]
        # self.effects = [ChromaScanlinesEffect(chroma_color=(1, 0, 0, 1))]
        # self.dragging = False
        # self.button = Button(text="Drag Me!", size_hint=(None, None), size=(100, 50))
        # self.add_widget(self.button)

        self.shape = shape
        self.add_widget(self.shape)

    def on_touch_down(self, touch):
        self.shape.on_touch_down(touch)
        return True
        # if self.button.collide_point(*touch.pos):
        #     self.dragging = True
        #     touch.grab(self)
        #     return True
        # return super(DraggableEffectWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        self.shape.on_touch_move(touch)
        return True
        # if touch.grab_current is self:
        #     self.button.center_x = touch.x
        #     self.button.center_y = touch.y
        #     return True
        # return super(DraggableEffectWidget, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        self.shape.on_touch_up(touch)
        return True
        # if touch.grab_current is self:
        #     self.dragging = False
        #     touch.ungrab(self)
        #     return True
        # return super(DraggableEffectWidget, self).on_touch_up(touch)


# FIXME There are quite some issues here:
# 1. The returned widget is not a shape, but an effect
# 2. As it is right now, combining effects does not work as expected,
# maybe the combination of two effects causes the 1st one to alter the chroma color
# and the 2nd one not to work on the altered color, because its not the same as the specified chroma?
def wrap_with_chroma(shape, chroma_color):
    shape_effect = EffectWidget()
    # shape_effect.effects = [ScanlinesEffect()]
    shape_effect.effects = [ChromaScanlinesEffect(chroma_color=chroma_color)]
    # shape_effect.effects = [ChromaHorizontalBlurEffect(shape=shape, chroma_color=chroma_color, size=10.0)]
    shape_effect.add_widget(shape)
    return shape_effect


# Taken from kivy examples, plays a video and applies an effect to it in real time.
# Performance is good, but not enough for the effect to be applied to 100% of the frames: some frames and
# fragments of the video are not modified by the effect.
if __name__ == "__main__":
    from kivy.app import App
    import sys

    if len(sys.argv) != 2:
        print("usage: %s file" % sys.argv[0])
        sys.exit(1)

    class VideoApp(App):
        def build(self):
            from kivy.uix.effectwidget import EffectWidget

            from kivy.uix.effectwidget import (
                EffectBase,
                MonochromeEffect,
                InvertEffect,
                ChannelMixEffect,
                ScanlinesEffect,
                FXAAEffect,
                PixelateEffect,
                HorizontalBlurEffect,
                VerticalBlurEffect,
            )

            from kivy.uix.effectwidget import (
                shader_header,
                shader_uniforms,
                shader_footer_effect,
            )
            from kivy.uix.video import Video

            self.v = Video(source=sys.argv[1], state="play")
            self.v.bind(state=self.replay)
            self.v.bind(on_touch_down=self.on_touch_down)

            shape_effect = EffectWidget()
            shape_effect.effects = [ScanlinesEffect()]
            chroma_color = (1, 1, 1, 1)
            chroma_tolerance = (0.3, 0.3, 0.3, 0.3)
            shape_effect.effects = [
                ChromaScanlinesEffect(
                    chroma_color=chroma_color, chroma_tolerance=chroma_tolerance
                )
            ]
            # shape_effect.effects = [ChromaHorizontalBlurEffect(shape=shape, chroma_color=chroma_color, size=10.0)]
            shape_effect.add_widget(self.v)

            # return self.v
            return shape_effect

        def replay(self, *args):
            if self.v.state == "stop":
                self.v.state = "play"

        def on_touch_down(self, instance, touch, *args):
            if touch.button == "left" and self.v:
                # print(f"on_touch_down: {args}")
                self.v.state = "play" if self.v.state == "pause" else "pause"
                return True
                return super(VideoApp, self).on_touch_down(touch)

    VideoApp().run()
