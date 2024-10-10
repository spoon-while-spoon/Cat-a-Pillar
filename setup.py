from setuptools import setup
import sys
import os

APP = ['catapillar.py']
DATA_FILES = [
    os.path.join('assets', 'menu.wav'),
    os.path.join('assets', 'game.wav'),
    os.path.join('assets', 'PressStart2P.ttf'),
    os.path.join('assets', 'snake.icns'),
    # Optional: Füge weitere Ressourcen hinzu, z.B. ein Icon
    # os.path.join('assets', 'app_icon.icns'),
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame'],
    'resources': DATA_FILES,  
    # Optional: Füge ein App-Icon hinzu
    'iconfile': 'assets/snake.icns',  # Stelle sicher, dass diese Datei existiert
    'plist': {
        'CFBundleName': 'Cat-a-Pillar',
        'CFBundleShortVersionString': '1.0',
        'CFBundleVersion': '1.0',
        'CFBundleIdentifier': 'com.deinname.catapillar',  # Passe dies an deine Domain an
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
