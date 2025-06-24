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
    """
    DockView component.

    Args:
      theme (string):
        Theme to use for the layout manager.
        Possible values are: [
            Abyss, AbyssSpaced, Dark, Dracula, Light,
            LightSpaced, Replit, VisualStudio,
        ]

      ready (event):
        Event emitted when the component is ready.
      active_panel (event):
        Event emitted when a panel is activated.
        The $event will be equal to the id used when creating the panel.
    """

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
            ("active_panel", "activePanel"),
        ]

        self.__ref = kwargs.get("ref")
        if self.__ref is None:
            DockView._next_id += 1
            self.__ref = f"_dockview_{DockView._next_id}"
        self._attributes["ref"] = f'ref="{self.__ref}"'

    def add_panel(self, id, title, template_name, **add_on):
        """
        Add a new panel to the layout.
        This can only be called once the widget is ready.

        Args:
            id (string):
                Unique identifier for that panel
            title (string):
                Title showing up in the tab.
            template_name (string):
                Name of the trame layout to be placed inside the panel.
            **kwargs:
                Additional parameter to control where the panel should be added.
                (https://dockview.dev/docs/core/panels/add#positioning-the-panel)
        """
        self.server.js_call(self.__ref, "addPanel", id, title, template_name, add_on)
