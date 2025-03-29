import subprocess
from pathlib import Path
import shutil
import os

def install_font(widget, path: str):
    if not os.path.exists(Path.home() / '.local' / 'share' / 'fonts'):
        os.makedirs(Path.home() / '.local' / 'share' / 'fonts')

    shutil.copy(path, Path.home() / '.local' / 'share' / 'fonts')
    subprocess.run(['fc-cache', '-fv'])

    widget.set_label('Installed')
    widget.set_sensitive(False)
