def createPlugins():
    from .base import ThunderstoreBasePlugin
    from .installer import ThunderstoreInstaller
    from .mod_page import ThunderstoreModPage
    from .tool_register_protocol import ThunderstoreRegisterTool

    return [
        ThunderstoreBasePlugin(),
        ThunderstoreInstaller(),
        ThunderstoreModPage(),
        ThunderstoreRegisterTool(),
    ]
