# -*- coding: utf-8 -*-
"""Однократная генерация иконок assets/ic: Fluent Emoji Flat (MIT) + свои плоские иллюстрации вредителей."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pest_art_src import CUSTOM
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "ic"; OUT.mkdir(parents=True, exist_ok=True)
F = json.load(open(sys.argv[1]))
MAP = {"cockroach": "cockroach", "ant": "ant", "fly": "fly", "mosquito": "mosquito", "rat": "rat", "mouse": "mouse", "spider": "spider",
       "beetle": "beetle", "microbe": "microbe", "mold": "mushroom", "ozone": "cloud", "odor": "wind-face", "biz": "office-building",
       "flat": "house", "house": "house-with-garden", "office": "office-building", "cafe": "fork-and-knife-with-plate", "shop": "convenience-store",
       "warehouse": "package", "factory": "factory", "school": "school", "hospital": "hospital", "hotel": "hotel", "dorm": "department-store",
       "basement": "derelict-house", "shield": "shield", "doc": "clipboard", "check": "check-mark-button", "time": "alarm-clock",
       "map": "round-pushpin", "family": "baby", "pet": "paw-prints", "leaf": "herb", "drop": "droplet", "bubbles": "bubbles", "garden": "deciduous-tree",
       "people": "handshake", "bed": "bed", "biohazard": "biohazard", "cart": "shopping-cart"}
def fluent(n, prefix):
    body = F["icons"][n]["body"]
    for i in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{i}"', f'id="{prefix}{i}"').replace(f"url(#{i})", f"url(#{prefix}{i})")
    return body
def flat(svg):
    """Градиенты → сплошной цвет средней точки, блики убираем: плоский стиль как у Fluent Flat."""
    grads = {}
    for m in re.finditer(r'<(radialGradient|linearGradient) id="([^"]+)".*?</\1>', svg, re.S):
        stops = re.findall(r'stop-color="([^"]+)"', m.group(0)); grads[m.group(2)] = stops[len(stops) // 2] if stops else "#888"
    svg = re.sub(r"<defs>.*?</defs>", "", svg, flags=re.S)
    svg = re.sub(r'url\(#([^)]+)\)', lambda m: grads.get(m.group(1), "#888"), svg)
    svg = re.sub(r'<ellipse[^>]*fill="#fff" fill-opacity="[^"]+"[^>]*/>', "", svg)
    return svg
for k, n in MAP.items():
    (OUT / f"{k}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">{fluent(n, k[:3])}</svg>', encoding="utf-8")
for k, v in CUSTOM.items():
    (OUT / f"{k}.svg").write_text(flat(v), encoding="utf-8")
# чешуйница — своя плоская иллюстрация
(OUT / "silverfish.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none"><g stroke="#6B7A86" stroke-width="1" stroke-linecap="round" fill="none">
<path d="M13 6.5 10 2.5M15.5 6 15 1.8"/><path d="M14 27.5l-3.5 3.2M16 28l.2 3.6M18 27.4l3.6 2.8"/><path d="M10.5 11 6.5 9.5M10 15.5 5.8 16M11 20 7 22.5M21.5 11l4-1.5M22 15.5l4.2.5M21 20l4 2.5"/></g>
<path d="M16 5.5c4.2 0 6.4 4 6.4 9.2 0 6.1-3 12.3-6.4 12.3s-6.4-6.2-6.4-12.3c0-5.2 2.2-9.2 6.4-9.2z" fill="#A9B6C0"/>
<g stroke="#7E8C97" stroke-width=".7"><path d="M10.4 11.5h11.2M10 15h12M10.4 18.5h11.2M11.2 22h9.6M12.4 25h7.2"/></g></svg>''', encoding="utf-8")
print(len(list(OUT.iterdir())), "иконок")
