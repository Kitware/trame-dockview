from pathlib import Path

serve_path = str(Path(__file__).with_name("serve").resolve())
serve = {"__trame_dockview": serve_path}
scripts = ["__trame_dockview/trame_dockview.umd.js"]
styles = ["__trame_dockview/style.css"]
vue_use = ["trame_dockview"]
