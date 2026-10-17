#!/usr/bin/env python3
"""Wrap index.html (an artifact body) into a standalone page you can open locally.

  python3 tools/build_standalone.py          -> dist/standalone.html
  python3 tools/build_standalone.py --mock   -> same, plus canned replies so the UI works offline
"""
import pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
body = (root / "index.html").read_text(encoding="utf-8")
shim = ""
if "--mock" in sys.argv:
    shim = "<script>\n" + (root / "tools" / "dev-shim.js").read_text(encoding="utf-8") + "\n</script>\n"
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<style>html,body{margin:0;background:#0A0C10}</style>\n</head>\n<body>\n'
        + shim + body + "\n</body>\n</html>\n")
out = root / "dist"
out.mkdir(exist_ok=True)
(out / "standalone.html").write_text(page, encoding="utf-8")
print("wrote", out / "standalone.html")
