import platform

OS = platform.system().lower()

import os
import sys

# Workaround for Kivy bug on Windows when using PyInstaller and not using the console
# See: https://github.com/kivy/kivy/issues/8074
if OS == 'windows' and hasattr(sys, '_MEIPASS'):
    os.environ['KIVY_NO_CONSOLELOG'] = '1'

from componga.app import main
    
if __name__ == "__main__":
    main()
