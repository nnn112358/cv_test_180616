"""Embed the device icons into the game page: python3 game/build.py"""
import base64, json, pathlib
root = pathlib.Path(__file__).resolve().parent
icons = {k: 'data:image/svg+xml;base64,' + base64.b64encode((root.parent / 'icons' / f).read_bytes()).decode()
         for k, f in {'basic': 'm5stack.svg', 'fire': 'm5stack_fire.svg', 'core2': 'm5stack_core2.svg',
                      'cores3': 'm5stack_cores3.svg', 'atoms3': 'm5atoms3.svg', 'stick': 'm5stickc.svg',
                      'sticks3': 'm5sticks3.svg', 'mp135': 'm5stack_coremp135.svg'}.items()}
html = (root / 'template.html').read_text().replace('/*ICONS*/null', json.dumps(icons))
(root / 'stackwars.html').write_text(html)
print(len(html))
