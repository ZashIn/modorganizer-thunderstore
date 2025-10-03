from .base import ThunderstoreBasePlugin as ThunderstoreBasePlugin
from .installer import ThunderstoreInstaller as ThunderstoreInstaller
from .mod_page import ThunderstoreModPage as ThunderstoreModPage


def createPlugins():
    return [ThunderstoreBasePlugin(), ThunderstoreInstaller(), ThunderstoreModPage()]
