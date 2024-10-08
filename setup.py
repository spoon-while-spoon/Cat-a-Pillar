from setuptools import setup

APP = ['snake_game.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame'],
    'iconfile': 'snake.icns',  # Optional
    'compressed': False,       # Komprimierung deaktivieren
    'excludes': ['tkinter', 'numpy', 'unittest', 'email', 'html', 'http', 'xml', 'urllib', 'distutils', 'unnecessary_module'],
    # 'resources': [],         # Fügen Sie hier Ihre Ressourcen hinzu
}

setup(
    app=APP,
    name='Snake 2',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
