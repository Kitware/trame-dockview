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
