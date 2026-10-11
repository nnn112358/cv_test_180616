"""Embed the device icons into the game page: python3 game/build.py"""
import base64, json, pathlib
root = pathlib.Path(__file__).resolve().parent
icons = {k: 'data:image/svg+xml;base64,' + base64.b64encode((root.parent / 'icons' / f).read_bytes()).decode()
         for k, f in {'fire': 'm5stack_fire.svg', 'stick': 'm5stickc.svg', 'mp135': 'm5stack_coremp135.svg',
                      'core2': 'm5stack_core2.svg', 'basic': 'm5stack.svg'}.items()}
html = (root / 'template.html').read_text().replace('/*ICONS*/null', json.dumps(icons))
(root / 'stackwars.html').write_text(html)
print(len(html))
