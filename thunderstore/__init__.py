from .installer import ThunderstoreInstaller as ThunderstoreInstaller
from .mod_page import ThunderstoreModPage as ThunderstoreModPage


def createPlugins():
    return [ThunderstoreModPage(), ThunderstoreInstaller()]
