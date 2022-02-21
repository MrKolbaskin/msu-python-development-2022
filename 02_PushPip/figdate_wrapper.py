import tempfile
import venv
import subprocess
import sys
from pathlib import Path

with tempfile.TemporaryDirectory() as path_temp_dir:
    temp_dir = Path(path_temp_dir)
    venv.create(temp_dir, with_pip=True)
    
    subprocess.run([temp_dir / "bin" / "pip", "install", "pyfiglet"], stdout=subprocess.DEVNULL)
    subprocess.run([temp_dir / "bin" / "python3", "-m", "figdate", *sys.argv[1:]])
