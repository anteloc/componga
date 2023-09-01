# componga
Screen drawing app for presentations

## Installation

Linux installation:

```
pip install kivy
pip install pyautogui
pip install mss
```

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


