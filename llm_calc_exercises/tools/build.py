"""content/*.py の例題をすべて SVG にして ../svg/ に書き出す。

使い方: python3 llm_calc_exercises/tools/build.py
"""
import importlib.util
import pathlib
import re
import sys

from svgkit import render

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "svg"
README = ROOT.parent / "README.md"


def load_problems():
    probs = []
    for f in sorted((ROOT / "content").glob("ch*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        probs += mod.PROBLEMS
    return probs


def main():
    warns, done = [], []
    for p in load_problems():
        svg, w = render(p)
        name = "{}_{}.svg".format(*p["id"].split("-"))
        (OUT / name).write_text(svg, encoding="utf-8")
        warns += w
        done.append(p["id"])
        print("wrote", name)
    # README の状態欄を更新し、ファイル名をリンクにする
    text = README.read_text(encoding="utf-8")
    for pid in done:
        name = "{}_{}.svg".format(*pid.split("-"))
        text = re.sub(rf"^\| {pid} \| (.+?) \| `svg/{name}` \| ⬜ \|$",
                      rf"| {pid} | \1 | [`svg/{name}`](svg/{name}) | ✅ |", text, flags=re.M)
    README.write_text(text, encoding="utf-8")
    for w in warns:
        print("WARN", w, file=sys.stderr)
    return 1 if warns else 0


if __name__ == "__main__":
    sys.exit(main())
