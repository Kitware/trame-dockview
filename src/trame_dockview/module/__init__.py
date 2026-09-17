from pathlib import Path

from trame_dockview import __version__

serve_path = str(Path(__file__).with_name("serve").resolve())
server_path = f"__trame_dockview_{__version__}"
serve = {server_path: serve_path}
scripts = [f"{server_path}/trame_dockview.umd.js"]
styles = [f"{server_path}/trame_dockview.css"]
vue_use = ["trame_dockview"]
