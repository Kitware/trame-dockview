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
      components (dict):
        Map of components to replate using template names.
        Possible components to override:
            watermarkComponent, rightHeaderActionsComponent,
            prefixHeaderActionsComponent, leftHeaderActionsComponent,
            defaultTabComponent
      default_renderer (string):
        Possible values: always | onlyWhenVisible
      disable_auto_resizing (bool):
        Disable the auto-resizing which is controlled through a ResizeObserver.
        Call .layout(width, height) to manually resize the container.
      disable_dnd (bool):
        Disable drag and drop.
      disable_floating_groups (bool):
        Disable floating groups.
      disable_tabs_overflow_list (bool):
        Disable tabs overflow list.
      dnd_edges (bool):
      floating_group_bounds (dict|string):
        { minimumHeightWithinViewport: number, minimumWidthWithinViewport: number } | 'boundedWithinViewport'
      hide_borders (bool):
        Hide borders
      locked (bool):
      no_panels_overlay (string):
        Define the behaviour of the dock when there are no panels to display. Defaults to watermark.
        Options: watermark | emptyGroup
      popout_url (string):
        Popup url
      scrollbars (string):
        Select native to use built-in scrollbar behaviours and custom to use an internal implementation
        that allows for improved scrollbar overlay UX. This is only applied to the tab header section.
        Defaults to custom.
        Options: custom | native
      single_tab_mode (string):
        Options: default | fullwidth

      ready (event):
        Event emitted when the component is ready.
      active_panel (event):
        Event emitted when a panel is activated.
        The $event will be equal to the id used when creating the panel.
      removePanel (event):
        Event emitted when a panel is removed.
        The $event will be equal to the panel id provided at the panel creation.
    """

    _next_id = 0

    def __init__(self, **kwargs):
        super().__init__(
            "dock-view",
            **kwargs,
        )
        self._attr_names += [
            "theme",
            "components",
            ("default_renderer", "defaultRenderer"),
            ("disable_auto_resizing", "disableAutoResizing"),
            ("disable_dnd", "disableDnd"),
            ("disable_floating_groups", "disableFloatingGroups"),
            ("disable_tabs_overflow_list", "disableTabsOverflowList"),
            ("dnd_edges", "dndEdges"),
            ("floating_group_bounds", "floatingGroupBounds"),
            ("hide_borders", "hideBorders"),
            "locked",
            ("no_panels_overlay", "noPanelsOverlay"),
            ("popout_url", "popoutUrl"),
            "scrollbars",
            ("single_tab_mode", "singleTabMode"),
        ]
        self._event_names += [
            "ready",
            ("active_panel", "activePanel"),
            ("remove_panel", "removePanel"),
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

    def remove_panel(self, id):
        """
        Remove/Close an existing panel within the layout.
        This can only be called once the widget is ready.

        Args:
            id (string):
                Unique identifier for that panel
        """
        self.server.js_call(self.__ref, "removePanel", id)

    def active_panel(self, id):
        """
        Activate an existing panel within the layout.
        This can only be called once the widget is ready.

        Args:
            id (string):
                Unique identifier for that panel
        """
        self.server.js_call(self.__ref, "activePanel", id)
