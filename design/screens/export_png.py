"""Export design/screens/*.html to design/screens/png/*.png with headless Chrome or Edge (#7).

Usage:
    python design/screens/export_png.py            # all screens
    python design/screens/export_png.py 04-insight # one screen

Set CHROME=/path/to/chrome if the browser is not found automatically.
Headless Chrome cannot make a window narrower than ~500px, so mobile is exported via 08-mobile.html (iframes).
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "png"

# page -> (width, height): heights fit the content of each mockup.
SCREENS = {
    "01-login": (1440, 900),
    "02-home": (1440, 800),
    "03-feed": (1440, 1340),
    "04-insight": (1440, 3150),
    "05-chat": (1440, 1200),
    "06-trace-feedback": (1440, 1250),
    "07-states": (1440, 2000),
    "08-mobile": (1440, 1060),
    "ui-kit": (1440, 2900),
}

CANDIDATES = [
    os.environ.get("CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
]


def browser():
    for path in CANDIDATES:
        if path and Path(path).exists():
            return path
    sys.exit("Chrome/Edge not found: set CHROME=/path/to/chrome")


def export(name, size, exe):
    page = HERE / f"{name}.html"
    target = OUT / f"{name}.png"
    subprocess.run(
        [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
         "--virtual-time-budget=4000", f"--window-size={size[0]},{size[1]}",
         f"--screenshot={target}", page.as_uri()],
        check=True, timeout=90, capture_output=True,
    )
    print(f"{target.relative_to(HERE.parent.parent)}  {size[0]}x{size[1]}")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    exe = browser()
    names = sys.argv[1:] or list(SCREENS)
    for name in names:
        export(name, SCREENS[name], exe)
