[![Build status](https://ci.appveyor.com/api/projects/status/fr7g37cfooy4hq73/branch/main?svg=true)](https://ci.appveyor.com/project/anteloc/componga/branch/main)
[![Build status](https://ci.appveyor.com/api/projects/status/fr7g37cfooy4hq73?svg=true)](https://ci.appveyor.com/project/anteloc/componga)
# componga
Screen drawing app for presentations

## Installation

Linux installation:

Tested with: python v3.10

```
pip install kivy
pip install pyautogui
pip install mss
```

See: requirements.txt for the exact versions used for developing the app.

Now, clone the repo for this project:

```
git clone https://github.com/anteloc/componga.git
```

And checkout the branch:

```
$ git checkout kivy-port
```

## Running 
Start the app by running:

```
cd src/componga-kivy
python kivy___main__.py
```

## Control:
- _Mouse:_
    - **Left click**: draw shape
    - **Right click**: popup menu
    - **Mouse wheel up/down**: select another shape
    - **Shift + mouse wheel up/down**: change line thickness
- _Keyboard defaults:_
    - **f**: freeze
    - **u**: update background
    - **escape**: exit
    - **b**: select blip
    - **a**: select arrow path
    - **s**: select arrow straight
    - **l**: select line straight
    - **e**: select ellipse
    - **r**: select rectangle
    - **p**: select path
- _Configuration:_
    - Last shape selected, color and line width are saved automatically
    - To change the configuration, edit the `componga.ini` file


