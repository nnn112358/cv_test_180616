"""Embed the device icons into the game pages: python3 game/build.py"""
import base64, json, pathlib
root = pathlib.Path(__file__).resolve().parent
ICON_FILES = {'basic': 'm5stack.svg', 'fire': 'm5stack_fire.svg', 'core2': 'm5stack_core2.svg',
              'cores3': 'm5stack_cores3.svg', 'atoms3': 'm5atoms3.svg', 'stick': 'm5stickc.svg',
              'sticks3': 'm5sticks3.svg', 'mp135': 'm5stack_coremp135.svg', 'llm': 'm5stack_module_llm.svg'}
icons = {k: 'data:image/svg+xml;base64,' + base64.b64encode((root.parent / 'icons' / f).read_bytes()).decode()
         for k, f in ICON_FILES.items()}
for template, out in [('template.html', 'stackwars.html'), ('tower-template.html', 'tower.html')]:
    html = (root / template).read_text().replace('/*ICONS*/null', json.dumps(icons))
    (root / out).write_text(html)
    print(out, len(html))
