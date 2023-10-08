from kivy.factory import Factory

from .drawsurface import DrawSurface

mixins = ("HoverAnimationMixin", "HoverSizeMixin", "HoverSizeHintMixin")

# Required for kivy .kv files to recognize the mixins when creating rules and templates
for mixin in mixins:
    Factory.register(mixin, module="componga.ui.mixins")
