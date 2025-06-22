from trame_dockview.widgets.dockview import *  # noqa: F403


def initialize(server):
    from trame_dockview import module

    server.enable_module(module)
