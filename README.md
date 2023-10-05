[![Build status](https://ci.appveyor.com/api/projects/status/fr7g37cfooy4hq73/branch/main?svg=true)](https://ci.appveyor.com/project/anteloc/componga/branch/main)
[![Build status](https://ci.appveyor.com/api/projects/status/fr7g37cfooy4hq73?svg=true)](https://ci.appveyor.com/project/anteloc/componga)
# componga
Screen drawing app for presentations

## Installation - Linux

### 1. Clone the repo for this project:

```
git clone https://github.com/anteloc/componga.git
```

### 2. Checkout the ```main``` branch:

```
$ git checkout main
```

### 3. Install Python if required

Tested with Python v3.10 *only*, feedback on other Python versions is welcome!

### 4. Install dependencies
**RECOMMENDED:** create a virtual environment for this project, e.g.:

```
pip install virtualenv
python -m venv componga-venv
source componga-venv/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

Have a look at requirements.txt for the exact versions used for developing the app.

## Running 
Start the app by running:

```
cd componga/src
python main.py
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
    - **o**: select ellipse
    - **r**: select rectangle
    - **p**: select path
- _Configuration:_
    - Last shape selected, color and line width are saved automatically
    - To change the configuration, edit the `componga.ini` file:
      - Linux: ```$HOME/.componga/componga.ini```
      - Windows: TBD
