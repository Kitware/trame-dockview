from trame_client.widgets.core import AbstractElement

from .. import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


__all__ = [
    "DockView",
]


class DockView(HtmlElement):
    _next_id = 0

    def __init__(self, **kwargs):
        super().__init__(
            "dock-view",
            **kwargs,
        )
        self._attr_names += [
            "theme",
        ]
        self._event_names += [
            "ready",
        ]

        self.__ref = kwargs.get("ref")
        if self.__ref is None:
            DockView._next_id += 1
            self.__ref = f"_dockview_{DockView._next_id}"
        self._attributes["ref"] = f'ref="{self.__ref}"'

    def add_panel(self, id, title, template_name, **add_on):
        self.server.js_call(self.__ref, "addPanel", id, title, template_name, add_on)
