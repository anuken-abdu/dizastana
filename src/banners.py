# -*- coding: utf-8 -*-
"""Баннеры для Google Ads и рассылки → google-ads/banners/ + OG-картинка сайта → assets/og.png
Без текста — для изображений в поиске и PMax (Google не принимает наложенный текст и логотипы).
С текстом — для КМС и PMax. Для рассылки — крупный текст, без контактов. Логотипы 1:1 и 4:1.
Запуск: python3 src/banners.py (нужен собранный dist/), затем снова python3 src/build.py — чтобы og.png попал в dist."""
import http.server, socketserver, threading, functools, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"; OUT = ROOT / "google-ads" / "banners"
OUT.mkdir(parents=True, exist_ok=True)
for f in OUT.glob("*"): f.unlink()

BASE = """<html><head><meta charset="utf-8"><link rel="stylesheet" href="/assets/styles.css"><style>
html,body{margin:0;background:#0d2b33}
.b{position:relative;overflow:hidden;width:%(w)spx;height:%(h)spx;color:#fff;font-family:"Nunito Sans";
 background:radial-gradient(%(gw)spx %(gh)spx at %(gx)s %(gy)s,rgba(25,194,181,.36),transparent 70%%),radial-gradient(%(gw)spx %(gh)spx at 0 100%%,rgba(123,104,245,.32),transparent 70%%),var(--hex-w),#0d2b33;
 background-size:auto,auto,%(hx)spx %(hy)spx,auto}
.b.light{color:#0d2b33;background:radial-gradient(%(gw)spx %(gh)spx at %(gx)s %(gy)s,rgba(25,194,181,.22),transparent 70%%),radial-gradient(%(gw)spx %(gh)spx at 0 100%%,rgba(123,104,245,.16),transparent 70%%),var(--hex),#f4fafa;background-size:auto,auto,%(hx)spx %(hy)spx,auto}
.cl{position:relative;aspect-ratio:1/1}
.cl .h{position:absolute;display:grid;place-items:center;width:27%%;aspect-ratio:1;background:#fff;clip-path:polygon(50%% 0,100%% 25%%,100%% 75%%,50%% 100%%,0 75%%,0 25%%)}
.light .cl .h{background:#fff}
.light .cl{filter:drop-shadow(0 10px 24px rgba(13,43,51,.14))}
.b.white{background:#fff}
.cl .h img{width:58%%;height:58%%}
.h0{left:36%%;top:0}.h1{left:8%%;top:16%%}.h2{left:64%%;top:16%%}.h3{left:36%%;top:33%%;width:30%%!important}.h4{left:8%%;top:50%%}.h5{left:64%%;top:50%%}.h6{left:36%%;top:67%%}
.col{position:absolute;inset:0;display:flex;flex-direction:column;padding:%(pad)s}
.col .cl{flex:1;min-height:0;align-self:center;margin:24px 0}
.row{position:absolute;inset:0;display:grid;grid-template-columns:1.15fr .85fr;align-items:center;padding:%(pad)s;gap:30px}
.row>div:first-child{display:flex;flex-direction:column;gap:22px;align-items:flex-start}
.row .cl{height:min(100%%,%(clh)spx);justify-self:center}
.t{font:800 %(fs)spx/1.08 "Exo 2";letter-spacing:-.01em}
.t em{font-style:normal;color:#5ff0e2}
.light .t em{color:#0b8a8f}
.s{font:600 %(ss)spx/1.35 "Nunito Sans";opacity:.85}
.bt{display:inline-flex;align-items:center;font:700 %(bs)spx/1 "Nunito Sans";background:linear-gradient(135deg,#19c2b5,#0b8a8f);color:#fff;border-radius:999px;padding:%(bp)s}
.lg{display:flex;align-items:center;gap:%(lgg)spx;font:800 %(lgs)spx/1 "Exo 2"}
.lg img{width:%(lgi)spx;height:%(lgi)spx}
.lg small{display:block;font:600 %(lgss)spx/1 "Nunito Sans";opacity:.7;margin-top:.35em}
</style></head><body><div class="b %(cls)s">%(body)s</div></body></html>"""

def page(w, h, body, cls="", **k):
    d = dict(w=w, h=h, gw=int(w * .75), gh=int(h * .75), gx="80%", gy="45%", hx=max(56, w // 20), hy=int(max(56, w // 20) * 97 / 56), fs=60, ss=26,
             bs=26, bp="20px 32px", lgg=16, lgs=34, lgss=16, lgi=70, pad="60px 64px", clh=520, cls=cls, body=body)
    d.update(k)
    return BASE % d

def cloud(icons, style=""):
    return f'<div class="cl" style="{style}">' + "".join(f'<span class="h h{i}"><img src="/assets/ic/{n}.svg"></span>' for i, n in enumerate(icons)) + "</div>"

LOGO = '<div class="lg"><img src="/assets/logo-mark.svg"><span>ТазаДез<small>санитарная служба Астаны</small></span></div>'
ALL = ["cockroach", "bedbug", "flea", "ant", "moth", "woodlouse", "rat"]
SETS = {"obshchiy": ALL, "klopy": ["bedbug", "flea", "moth", "bedbug", "mite", "cockroach", "woodlouse"],
        "tarakany": ["cockroach", "ant", "silverfish", "cockroach", "woodlouse", "fly", "bedbug"],
        "gryzuny": ["mouse", "rat", "basement", "rat", "warehouse", "mouse", "house"],
        "plesen": ["mold", "microbe", "odor", "ozone", "flat", "mold", "microbe"],
        "biznes": ["cafe", "warehouse", "office", "biz", "factory", "hotel", "cart"]}
TEXT = [("obshchiy", "Дезинсекция и&nbsp;дезинфекция <em>в&nbsp;Астане</em>", "Квартиры, дома, кафе, офисы и склады"),
        ("klopy", "Уничтожение <em>клопов</em> в&nbsp;Астане", "Спальные места, мебель, щели и плинтусы"),
        ("tarakany", "Избавим от <em>тараканов</em>", "Кухня, санузел, щели и места у труб"),
        ("gryzuny", "Уничтожение <em>крыс и&nbsp;мышей</em>", "Частные дома, подвалы, склады"),
        ("plesen", "Удаление <em>плесени и&nbsp;запахов</em>", "Обработка от грибка, озонирование"),
        ("biznes", "Санобработка <em>для&nbsp;бизнеса</em>", "Кафе, магазины, склады, офисы")]

def text_banner(w, h, slug, title, sub):
    if w / h > 1.5:
        return page(w, h, f'<div class="row"><div>{LOGO}<div class="t">{title}</div><div class="s">{sub}</div><div class="bt">Узнать стоимость</div></div>{cloud(SETS[slug])}</div>',
                    fs=62, ss=27, bs=24, bp="18px 28px", lgs=30, lgi=62, lgss=14, pad="44px 56px", clh=540)
    fs, ss = (84, 34) if w == h else (76, 32)
    return page(w, h, f'<div class="col">{LOGO}<div class="t" style="margin-top:44px">{title}</div><div class="s" style="margin-top:20px">{sub}</div>'
                + cloud(SETS[slug]) + '<div><span class="bt">Узнать стоимость</span></div></div>', fs=fs, ss=ss, bs=30, gy="72%", gx="70%", pad="64px 68px")

def plain_banner(w, h, slug, light=False):
    """Без текста и логотипа — только графика (требование Google к изображениям в поиске)."""
    pad = "50px" if w / h > 1.5 else "90px 60px"
    return page(w, h, f'<div class="col" style="justify-content:center;align-items:center">{cloud(SETS[slug], "flex:1;margin:0")}</div>', "light" if light else "", gx="50%", gy="50%", pad=pad)

def mailing(title, sub, slug):
    """Для рассылки в мессенджерах: крупный текст, без контактов."""
    return page(1080, 1080, f'<div class="col"><div class="t">{title}</div>' + (f'<div class="s" style="margin-top:26px">{sub}</div>' if sub else "")
                + cloud(SETS[slug]) + "</div>", fs=104, ss=44, gy="74%", pad="80px 76px 70px")

def logo_png(w, h):
    if w == h:
        return page(w, h, '<img src="/assets/favicon.svg" style="position:absolute;left:10%;top:10%;width:80%;height:80%">', "light white")
    return page(w, h, f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);white-space:nowrap">{LOGO}</div>', "light white", lgs=78, lgss=30, lgi=170, lgg=32)

def og():
    return page(1200, 630, f'<div class="row"><div>{LOGO}<div class="t">Дезинсекция, дератизация и&nbsp;дезинфекция <em>в&nbsp;Астане</em></div>'
                '<div class="s">Тараканы, клопы, грызуны, плесень и запахи · все районы и пригороды</div></div>' + cloud(ALL) + "</div>",
                fs=54, ss=24, lgs=30, lgi=60, lgss=14, pad="50px 60px", clh=540)

JOBS = [("_og.png", 1200, 630, og())]
for w, h in [(1200, 628), (1200, 1200), (960, 1200)]:
    for slug, t, s in TEXT: JOBS.append((f"s-tekstom-{slug}-{w}x{h}.jpg", w, h, text_banner(w, h, slug, t, s)))
    for slug in ["obshchiy", "klopy", "gryzuny", "plesen"]:
        JOBS.append((f"bez-teksta-{slug}-tyomnyy-{w}x{h}.jpg", w, h, plain_banner(w, h, slug)))
        JOBS.append((f"bez-teksta-{slug}-svetlyy-{w}x{h}.jpg", w, h, plain_banner(w, h, slug, True)))
for i, (t, s, slug) in enumerate([("Тараканы, клопы, грызуны? <em>Решим</em>", "Санитарная обработка в Астане", "obshchiy"),
                                  ("Клопы <em>не&nbsp;уйдут</em> сами", "Обработка квартир и домов в Астане", "klopy"),
                                  ("Плесень и&nbsp;запах <em>— уберём</em>", "Обработка от грибка и озонирование", "plesen"),
                                  ("Санобработка <em>для&nbsp;бизнеса</em>", "Кафе, магазины, склады в Астане", "biznes")], 1):
    JOBS.append((f"rassylka-{i}-1080x1080.jpg", 1080, 1080, mailing(t, s, slug)))
JOBS += [("logo-1200x1200.png", 1200, 1200, logo_png(1200, 1200)), ("logo-1200x300.png", 1200, 300, logo_png(1200, 300))]

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
with socketserver.TCPServer(("127.0.0.1", 0), handler) as srv:
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, w, h, html in JOBS:
            (DIST / "_bn.html").write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(f"http://127.0.0.1:{port}/_bn.html"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
            kw = {"type": "png"} if name.endswith(".png") else {"type": "jpeg", "quality": 90}
            pg.screenshot(path=str(OUT / name), **kw); pg.close()
        b.close()
    srv.shutdown()
(DIST / "_bn.html").unlink(missing_ok=True)
shutil.move(str(OUT / "_og.png"), str(ROOT / "assets" / "og.png"))
print("баннеров:", len(JOBS) - 1, "+ og.png")
