"""Copy the committed entry image to the requested output directory.

The finished image is committed as entry.png. draw_image.py is the offline
Pillow generator that produced it; this entrypoint only copies the image, so
it runs with stock Python and needs neither Pillow nor fonts.
"""

import os
import shutil
from pathlib import Path

source = Path(__file__).resolve().with_name("entry.png")
if not source.is_file():
    raise FileNotFoundError(f"Required image not found next to main.py: {source}")
output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
output_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, output_dir / "entry.png")
