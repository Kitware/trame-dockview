.. |pypi_download| image:: https://img.shields.io/pypi/dm/trame-dockview

trame-dockview: Docking layout system for trame |pypi_download|
===========================================================================

.. image:: https://github.com/Kitware/trame-dockview/actions/workflows/test_and_release.yml/badge.svg
    :target: https://github.com/Kitware/trame-dockview/actions/workflows/test_and_release.yml
    :alt: Test and Release

Trame-dockview extend trame **widgets** with `dockview <https://dockview.dev/>`_ capabilities tuned so it can easily be used within trame.
Dockview is a fully featured Docking Layout Manager with customizable themes and controls.

This package is not supposed to be used by itself but rather should come as a dependency of **trame**.
For any specificity, please refer to `the trame documentation <https://kitware.github.io/trame/>`_.


Installing
-----------------------------------------------------------

trame-dockview can be installed with `pip <https://pypi.org/project/trame-dockview/>`_:

.. code-block:: bash

    pip install --upgrade trame-dockview


Usage
-----------------------------------------------------------

The `Trame Tutorial <https://kitware.github.io/trame/guide/tutorial>`_ is the place to go to learn how to use the library and start building your own application.

The `API Reference <https://trame.readthedocs.io/en/latest/index.html>`_ documentation provides API-level documentation.

The `Dockview website <https://dockview.dev/>`_ is very well made for exploring capabilities that the library is providing.

DockView Widget
```````````````````````````````````````````````````````````

First you need to import the **dockview** module so you can instantiate the layout manager like illustrated below.

.. code-block:: python

    from trame.app import TrameApp
    from trame.ui.html import DivLayout
    from trame.ui.vuetify3 import SinglePageLayout
    from trame.widgets import dockview, html
    from trame.widgets import vtk as vtk_widgets
    from trame.widgets import vuetify3 as v3

    THEMES = [
        "Abyss",
        "AbyssSpaced",
        "Dark",
        "Dracula",
        "Light",
        "LightSpaced",
        "Replit",
        "VisualStudio",
    ]


    class Demo(TrameApp):
        def __init__(self, server=None):
            super().__init__(server)
            self._panel_count = 0
            self._build_ui()

            # init vtk.js
            vtk_widgets.VtkView(trame_server=server)

        def _build_ui(self):
            with SinglePageLayout(self.server, full_height=True) as self.ui:
                with self.ui.toolbar:
                    v3.VSpacer()
                    v3.VSelect(
                        v_model=("theme", "Abyss"),
                        items=("themes", THEMES),
                        hide_details=True,
                        density="compact",
                        style="max-width:200px;",
                    )
                    v3.VBtn(icon="mdi-plus", click=self.add_panel, density="compact")

                with self.ui.content:
                    with v3.VContainer(classes="pa-0 ma-0 fill-height", fluid=True):
                        dockview.DockView(
                            ctx_name="dock_view",
                            theme=("theme",),
                        )

        def add_panel(self):
            self._panel_count += 1
            panel_id = f"panel_{self._panel_count}"
            title = f"Panel {self._panel_count}"
            template_name = f"dock_{panel_id}"
            resolution_key = f"{template_name}_resolution"

            with DivLayout(self.server, template_name) as layout:
                layout.root.style = "height:100%;position:relative;"
                with vtk_widgets.VtkView() as view:
                    with html.Div(
                        style="position:absolute;top:1rem;right:1rem;z-index:1;display:flex;flex-align:center;"
                    ):
                        html.Input(
                            type="range",
                            v_model_number=(resolution_key, 6),
                            min=3,
                            max=60,
                            step=1,
                        )
                        html.Button(
                            "Reset",
                            style="padding:0 5px;margin:10px;background:white;",
                            click=view.reset_camera,
                        )

                    with vtk_widgets.VtkGeometryRepresentation():
                        vtk_widgets.VtkAlgorithm(
                            vtk_class="vtkConeSource",
                            state=(f"{{ resolution: {resolution_key} }}",),
                        )

            self.ctx.dock_view.add_panel(panel_id, title, template_name)


    def main():
        app = Demo()
        app.server.start()


    if __name__ == "__main__":
        main()



License
-----------------------------------------------------------

trame-dockview is made available under the MIT License. For more details, see `LICENSE <https://github.com/Kitware/trame-dockview/blob/master/LICENSE>`_
This license has been chosen to match the one use by `DockView License <https://github.com/mathuo/dockview/blob/master/LICENSE>`_ which is instrumental for making that library possible.


Community
-----------------------------------------------------------

`Trame <https://kitware.github.io/trame/>`_ | `Discussions <https://github.com/Kitware/trame/discussions>`_ | `Issues <https://github.com/Kitware/trame/issues>`_ | `Contact Us <https://www.kitware.com/contact-us/>`_

.. image:: https://zenodo.org/badge/410108340.svg
    :target: https://zenodo.org/badge/latestdoi/410108340


Enjoying trame?
-----------------------------------------------------------

Share your experience `with a testimonial <https://github.com/Kitware/trame/issues/18>`_ or `with a brand approval <https://github.com/Kitware/trame/issues/19>`_.

JavaScript dependency
-----------------------------------------------------------

This Python package bundle the following **dockview-vue@4.4.0** library.
If you would like us to upgrade its dependency or expose more capabilities provided by the underlying library, `please reach out <https://www.kitware.com/trame/>`_.
