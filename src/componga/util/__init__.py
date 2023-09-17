from kivy.factory import Factory


mixins = ('HoverAnimationMixin', 
          'HoverSizeMixin', 
          'HoverSizeHintMixin')

for mixin in mixins:
    Factory.register(mixin, module='componga.util.mixins')