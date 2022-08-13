import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
CLEAR_IMAGE = os.path.join(IMAGES_DIR, 'clear.png')
FOLDER_IMAGE = os.path.join(IMAGES_DIR, 'folder.png')
ICON_IMAGE = os.path.join(IMAGES_DIR, 'icon.png')