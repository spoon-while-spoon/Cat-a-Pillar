# snake-mf

A modern take on the classic Snake game, developed in Python using Pygame. **snake-mf** offers multiple difficulty levels, a fun mode with unique levels, and a highscore system to keep track of your best games. 
## Table of Contents 

- [Features](#features) 
- [Installation](#installation) 
	- [Prerequisites](#prerequisites) 
	- [Clone the Repository](#clone-the-repository) 
	- [Install Dependencies](#install-dependencies) 
- [Running the Game](#running-the-game) 
- [Controls](#controls) 
- [Game Modes](#game-modes) 
	- [Classic Mode](#classic-mode) 
	- [Fun Mode](#fun-mode) 
- [Highscores](#highscores) 
- [Building an Executable (macOS)](#building-an-executable-macos) 
	- [Prerequisites](#prerequisites-1) 
	- [Setup Script](#setup-script) 
	- [Building the App](#building-the-app) 
	- [Notes](#notes) 
- [License](#license) 
- [Acknowledgments](#acknowledgments) 

## Features 
- **Classic Snake Gameplay**: Enjoy the traditional Snake game with modern enhancements. -
- **Multiple Difficulty Levels**: Choose from Easy, Medium, Hard, and Extreme. 
- **Fun Mode with Unique Levels**: -
	- **Level 1**: Wall around the playing field. 
	- **Level 2**: Obstacles on the playing field. 
	- **Level 3**: Wall & Obstacles. 
	- **Level 4**: Moving Obstacles. 
	- **Level 5**: Random Obstacles. 
- **Highscore System**: Keep track of your top scores. 
- **Sprint Functionality**: Hold down the direction key to speed up. 
- **Pause Functionality**: Pause the game at any time. 
- **Matrix-Style Start Animation**: Cyberpunk-inspired visuals. 
## Installation 
### Prerequisites 
- **Python 3.6** or higher 
- **Pygame** library 
### Clone the Repository 

```bash https://www.github.com/spoon-while-spoon/snake-mf cd snake-mf```

### Install Dependencies

It's recommended to use a virtual environment.

#### Using `venv`

```bash
python3 -m venv venv 
source venv/bin/activate 
pip install pygame
```

#### Using `pipenv`

```bash 
pip install pipenv 
pipenv install 
pygame pipenv shell
```


## Running the Game

After installing the dependencies, you can run the game with:

```bash
python snake-mf.py
```

## Controls

- **Arrow Keys**: Move the snake in the desired direction.
- **Spacebar**: Pause the game.
- **Sprint**: Hold down the arrow key in the direction you're moving to speed up.

## Game Modes

### Classic Mode

- Play the traditional Snake game with a modern twist.
- Choose from four difficulty levels: Easy, Medium, Hard, Extreme.

### Fun Mode

- Offers unique levels with different obstacles and challenges.
- **Levels**:
    1. **Level 1**: Wall around the playing field.
    2. **Level 2**: Obstacles on the playing field.
    3. **Level 3**: Wall & Obstacles.
    4. **Level 4**: Moving Obstacles.
    5. **Level 5**: Random Obstacles.

## Highscores

- The game features a highscore system that saves your top scores.
- Highscores are stored in user-writable directories depending on your operating system:
    - **macOS**: `~/Library/Application Support/snake-mf`
    - **Windows**: `%APPDATA%\snake-mf`
    - **Linux**: `~/.snake-mf`
- You can view and clear highscores from the main menu.

## Building an Executable (macOS)

If you want to create an executable application for macOS, you can use `py2app`.

### Prerequisites

- `py2app` installed in your Python environment

bash

Code kopieren

`pip install py2app`

### Setup Script

Ensure you have a `setup.py` file with the following content:

python

```python
from setuptools import setup  

APP = ['snake-mf.py'] 
OPTIONS = {     
		   'argv_emulation': True,
		   'packages': ['pygame'],     
			   'iconfile': 'snake.icns',  # Optional: Path to your app icon
			   'compressed': False,     
			   'excludes': ['tkinter', 'unittest', 'email', 'html', 'http',
			   'xml', 'urllib', 'distutils'], 
}  

setup(     
	  app=APP,     
	  name='snake-mf',     
	  options={'py2app': OPTIONS},     
	  setup_requires=['py2app'], )`
```

### Building the App

Run the following command to build the application:

```bash 
python setup.py py2app
```

The built application will be located in the `dist` directory.

### Notes

- **Testing**: Make sure to test the application thoroughly.
- **Code Signing and Notarization**: For distribution on macOS, consider code signing and notarization due to Gatekeeper requirements.
- **Dependencies**: Ensure all dependencies are included and paths to resources are correctly set.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
