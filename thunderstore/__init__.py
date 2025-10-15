def createPlugins():
    from .base import ThunderstoreBasePlugin
    from .installer import ThunderstoreInstaller
    from .mod_page import ThunderstoreModPage

    return [ThunderstoreBasePlugin(), ThunderstoreInstaller(), ThunderstoreModPage()]
