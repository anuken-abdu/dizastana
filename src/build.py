# -*- coding: utf-8 -*-
"""Генератор сайта DizAstana (санитарная служба, Астана): python3 src/build.py → dist/"""
import html, json, re, shutil, sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from data import *

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
VER = "0511262300"
TODAY = date.today().isoformat()
E = lambda s: html.escape(str(s), quote=True)
PAGES = []
P = {p["slug"]: p for p in PESTS}; S = {s["slug"]: s for s in SERVICES}

def wa(text): return f"https://wa.me/{WA_NUMBER}?text=" + re.sub(r"\s", "%20", html.escape(text))
def wa_attr(text): return f'href="{wa(text)}" target="_blank" rel="noopener"'
PH = json.loads((Path(__file__).parent / "ph_icons.json").read_text(encoding="utf-8"))
def ph(name): return f'<svg class="ph" viewBox="0 0 256 256" aria-hidden="true" focusable="false">{PH[name]}</svg>'
def photo(p, cls="pc-p", big=False, eager=False):
    src = f"/assets/pests/{p['photo']}{'' if big else '-s'}.webp?v={VER}"
    w, h = (960, 720) if big else (480, 360)
    return f'<img class="{cls}" src="{src}" alt="{E(p["name"])}" width="{w}" height="{h}"{"" if eager else " loading=" + chr(34) + "lazy" + chr(34)} decoding="async">'

ICON = {
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 "wa": '<path d="M3.5 20.5l1.2-4.3A8.5 8.5 0 1 1 8 19.4z"/><path d="M9 8.5c0 3 2.5 6.3 6 6.8l1.3-1.6-2-1-1 .9c-1-.5-2-1.5-2.4-2.5l.9-1-1-2z"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>', "up": '<path d="M12 19V5M6 11l6-6 6 6"/>', "back": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>', "close": '<path d="M6 6l12 12M18 6L6 18"/>', "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "chev": '<path d="M6 9l6 6 6-6"/>', "send": '<path d="M4 12l16-8-6 16-2.5-6.5z"/>', "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "spark": '<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M18.5 15l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
 "alert": '<path d="M12 3l9.5 17h-19z"/><path d="M12 10v4M12 17.5v.01"/>',
}
def ui(n, cls="ui"): return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[n]}</g></svg>'

def logo(dark=False):
    return (f'<a class="logo{" logo-d" if dark else ""}" href="/" aria-label="{BRAND} — на главную"><img src="/assets/logo-mark.svg" alt="" width="44" height="44">'
            f'<span class="logo-t">Diz<i>Astana</i></span></a>')

def btns(msg, light=False):
    return (f'<div class="btns"><a class="btn btn-p" href="tel:{PHONE_TEL}">{ui("phone")}Позвонить</a>'
            f'<a class="btn {"btn-l" if light else "btn-o"}" {wa_attr(msg)}>{ui("wa")}Написать в WhatsApp</a></div>')

def sec(title, inner, sub="", alt=False, sid="", link=None, cls=""):
    lk = f'<a class="lnk" href="{link[1]}">{link[0]} {ui("arrow")}</a>' if link else ""
    return (f'<section class="sec{" sec-alt" if alt else ""}{" " + cls if cls else ""}"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}><div class="wrap">'
            f'<div class="sec-h"><div><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>{lk}</div>{inner}</div></section>')

def crumbs_html(cr):
    items = [("Главная", "/")] + cr
    li = "".join(f'<li><a href="{u}">{E(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{E(n)}</li>' for i, (n, u) in enumerate(items))
    return f'<nav class="crumbs" aria-label="Навигация"><ol>{li}</ol></nav>'

def ph_hero(h1, lead, crumbs, msg, art=""):
    side = f'<div class="phd-art">{art}</div>' if art else ""
    return f'<section class="phd"><div class="wrap">{crumbs_html(crumbs)}<div class="phd-in{" has-art" if art else ""}"><div><h1>{h1}</h1><p class="lead-t">{lead}</p>{btns(msg, True)}</div>{side}</div></div></section>'

# ---------------------------------------------------------------- блоки
def pest_cards(items=None, full=False):
    """Фото-карточки вредителей. Без фото — тёмная плитка; крысы и мыши вместе — одна широкая плитка «Крысы и мыши»."""
    items = list(items or [p for p in PESTS if p.get("photo") and p["svc"] != "obrabotka-sada"])
    out = [f'<a class="pc" href="/vrediteli/{p["slug"]}/">{photo(p)}<b>{E(p["name"])}</b></a>' for p in items if p.get("photo")]
    rest = [p for p in items if not p.get("photo")]
    if full or {"krysy", "myshi"} <= {p["slug"] for p in rest}:
        rest = [p for p in rest if p["slug"] not in ("krysy", "myshi")]
        out.append('<a class="pc pc-d pc-w" href="/uslugi/deratizaciya/"><b>Крысы и мыши</b><span>Дератизация</span></a>')
    out += [f'<a class="pc pc-d" href="/vrediteli/{p["slug"]}/"><b>{E(p["name"])}</b><span>Подробнее</span></a>' for p in rest]
    return f'<div class="pests{" pests-4" if len(out) <= 4 and not full else ""}">' + "".join(out) + "</div>"

def svc_media(s, cls="sc-m", big=False):
    f = ROOT / "assets" / "services" / f"{s['slug']}.webp"
    if f.exists():
        return f'<img class="{cls}" src="/assets/services/{s["slug"]}.webp?v={VER}" alt="{E(s["name"])}" width="960" height="720" loading="lazy" decoding="async">'
    if SERVICE_PHOTO.get(s["slug"]):
        return photo(P[SERVICE_PHOTO[s["slug"]]], cls, big=big)
    return f'<span class="{cls} sc-ph">{ph("s-" + s["slug"])}</span>'

def svc_count(s):
    n = len(SERVICE_ITEMS[s["slug"]])
    return f"{n} {plural(n, 'вид', 'вида', 'видов')} услуг"

def svc_cards(items=None):
    items = items or SERVICES
    return f'<div class="svcs{" svcs-4" if len(items) == 4 else ""}">' + "".join(
        f'<a class="sc" href="/uslugi/{s["slug"]}/">{svc_media(s)}<span class="sc-t"><b>{E(s.get("card", s["name"]))}</b><span class="sc-s">{svc_count(s)}</span></span>{ui("arrow", "ui sc-a")}</a>' for s in items) + "</div>"

def items_html(s):
    li = "".join(f'<li><a href="{u}">{E(t)}{ui("arrow")}</a></li>' if u else f'<li><span>{E(t)}</span></li>' for t, u in SERVICE_ITEMS[s["slug"]])
    return f'<ul class="dl dl-3 dl-i">{li}</ul>'

def promo_pair():
    def card(p, title, sub, url):
        return (f'<a class="pr" href="{url}"><span class="pr-t"><b>{title}</b><span>{sub}</span><span class="pr-l">Подробнее {ui("arrow")}</span></span>'
                f'<span class="pr-m">{photo(P[p], "pr-p", big=True)}</span></a>')
    return ('<section class="sec sec-pr"><div class="wrap prs">'
            + card("klopy", "Клопы не&nbsp;уйдут сами", "Обработка спальных мест, мебели и&nbsp;плинтусов", "/vrediteli/klopy/")
            + card("kleshchi", "Клещи на&nbsp;участке", "Акарицидная обработка дач и&nbsp;дворов", "/uslugi/akaricidnaya-obrabotka/")
            + "</div></section>")

def promo_wide():
    imgs = "".join(f'<span class="pw-c">{photo(P[x], "pw-p")}</span>' for x in ("tlya", "gusenicy", "belyanka"))
    return (f'<section class="sec sec-pr"><div class="wrap"><a class="pw" href="/uslugi/obrabotka-sada/"><span class="pw-t"><b>Сад и&nbsp;огород под&nbsp;защитой</b>'
            f'<span>Тля, гусеницы и белянки: обработка деревьев, кустов и&nbsp;грядок</span><span class="pr-l">Обработка сада {ui("arrow")}</span></span><span class="pw-i">{imgs}</span></a></div></section>')

def obj_cards(items=None):
    items = items or OBJECTS
    return '<div class="objs">' + "".join(f'<a class="oc" href="/obekty/{o[0]}/">{ph(o[3])}<b>{E(o[1])}</b></a>' for o in items) + "</div>"

def steps_html():
    return '<ol class="steps">' + "".join(f'<li><span>{i}</span><b>{E(t)}</b><p>{E(d)}</p></li>' for i, (t, d) in enumerate(STEPS, 1)) + "</ol>"

def factors_html():
    return '<div class="fac">' + "".join(f'<div><b>{E(t)}</b><p>{E(d)}</p></div>' for t, d in PRICE_FACTORS) + "</div>"

def prep_html():
    return '<ul class="prep">' + "".join(f"<li>{E(x)}</li>" for x in PREP) + "</ul>"

def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details><summary>{E(q)}{ui("chev")}</summary><p>{E(a)}</p></details>' for q, a in faq) + "</div>"

def districts_html(cur=""):
    city = [d for d in DISTRICTS if not d.get("suburb")]; sub = [d for d in DISTRICTS if d.get("suburb")]
    li = lambda ds: "".join(f'<li><a href="/rayony/{d["slug"]}/"{" aria-current=page" if d["slug"] == cur else ""}>{E(d["short"])}{ui("arrow")}</a></li>' for d in ds)
    return f'<div class="geo"><div><h3>Районы Астаны</h3><ul class="dl dl-3">{li(city)}</ul></div><div><h3>Пригороды</h3><ul class="dl">{li(sub)}</ul></div></div>'

def geo_sec(cur=""):
    return sec("Работаем по всей Астане", districts_html(cur), "Выезжаем во все районы столицы и ближайшие пригороды. Время приезда согласуем при заявке.", alt=True, sid="rayony")

def article_cards():
    return '<div class="arts">' + "".join(f'<a class="art" href="/stati/{a["slug"]}/"><b>{E(a["title"])}</b><span>{E(a["desc"])}</span>{ui("arrow")}</a>' for a in ARTICLES) + "</div>"

def callout(msg="Здравствуйте! Нужна обработка в Астане."):
    return f'''<section class="cta"><div class="wrap"><div class="cta-in"><div><b>Не знаете, какая обработка нужна?</b><p>Расскажите, кто беспокоит и какой объект — подскажем метод и назовём стоимость до выезда.</p></div>{btns(msg, True)}</div></div></section>'''

def lead_form(title="Оставьте заявку на обработку", pest=""):
    popts = "".join(f'<option{" selected" if p["slug"] == pest else ""}>{E(p["name"])}</option>' for p in PESTS)
    dopts = '<option>Не указан</option>' + "".join(f'<option>{E(d["short"])}</option>' for d in DISTRICTS)
    return f'''<section class="sec sec-dark" id="zayavka"><div class="wrap lead">
<div><h2>{title}</h2><p>Заполните форму — заявка откроется в WhatsApp с вашими данными. Или позвоните, ответим на вопросы и назовём стоимость.</p>
<a class="lead-ph" href="tel:{PHONE_TEL}">{ui("phone")}{PHONE_DISPLAY}</a></div>
<form class="form" data-lead novalidate>
<div class="fld"><label for="fN">Имя</label><input id="fN" name="name" autocomplete="name"></div>
<div class="fld"><label for="fP">Телефон</label><input id="fP" name="phone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="+7"></div>
<div class="fld"><label for="fV">Кто беспокоит</label><select id="fV" name="pest"><option>Нужна консультация</option>{popts}<option>Дезинфекция</option><option>Плесень</option><option>Неприятный запах</option></select></div>
<div class="fld"><label for="fD">Район</label><select id="fD" name="area">{dopts}</select></div>
<div class="fld fld-w"><label for="fM">Объект и комментарий</label><textarea id="fM" name="msg" rows="3" placeholder="Например: 2-комнатная квартира, тараканы на кухне"></textarea></div>
<p class="f-err" hidden>Укажите телефон, чтобы мы могли связаться.</p>
<button class="btn btn-p fld-w" type="submit">{ui("wa")}Отправить в WhatsApp</button>
<p class="f-note fld-w">Нажимая кнопку, вы соглашаетесь с <a href="/privacy-policy/">политикой конфиденциальности</a>.</p></form></div></section>'''

# ---------------------------------------------------------------- schema
ORG = {"@type": "Organization", "@id": SITE_URL + "/#org", "name": BRAND, "url": SITE_URL + "/", "telephone": PHONE_TEL, "logo": SITE_URL + "/assets/icon-512.png",
       "areaServed": {"@type": "City", "name": "Астана"}, "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_TEL, "contactType": "customer service", "areaServed": "KZ", "availableLanguage": ["ru", "kk"]}}
def service_schema(name, url, desc, area="Астана"):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name, "url": SITE_URL + url, "description": desc,
            "provider": {"@id": SITE_URL + "/#org"}, "areaServed": {"@type": "City" if area == "Астана" else "Place", "name": area}}
def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

# ---------------------------------------------------------------- шаблон
def nav_html():
    pl = "".join(f'<li><a href="/vrediteli/{p["slug"]}/">{E(p["name"])}</a></li>' for p in PESTS)
    sl = "".join(f'<li><a href="/uslugi/{s["slug"]}/">{E(s["name"])}</a></li>' for s in SERVICES)
    return f'''<nav class="nav" id="nav" aria-label="Меню"><ul>
<li class="has"><a href="/vrediteli/">Вредители</a><ul class="sub sub-3">{pl}</ul></li>
<li class="has"><a href="/uslugi/">Услуги</a><ul class="sub">{sl}</ul></li>
<li><a href="/obekty/">Объекты</a></li><li><a href="/rayony/">Районы</a></li><li><a href="/stoimost/">Стоимость</a></li><li><a href="/stati/">Статьи</a></li><li><a href="/kontakty/">Контакты</a></li></ul>
<div class="nav-m">{btns("Здравствуйте! Нужна обработка в Астане.", True)}</div></nav>'''

def gtag():
    """Единый тег Google — ровно как выдаёт Google («Вручную»), сразу после <head>. Второй тег не добавляем."""
    if not TAG_ID: return ""
    return (f'<script async src="https://www.googletagmanager.com/gtm.js?id={TAG_ID}"></script>\n'
            '<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag(\'js\', new Date());\n</script>\n')

def page(path, title, desc, body, schemas=(), crumbs=None, prio="0.7"):
    PAGES.append((path, prio))
    bc = []
    if crumbs:
        items = [("Главная", "/")] + crumbs
        bc = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + u} for i, (n, u) in enumerate(items)]}]
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in [{"@context": "https://schema.org", **ORG}, *schemas, *bc])
    cfg = json.dumps({"ga": GA_ID, "ads": GADS_ID, "call": GADS_CALL_LABEL, "wa": GADS_WA_LABEL, "wan": WA_NUMBER}, ensure_ascii=False)
    doc = f'''<!doctype html>
<html lang="ru">
<head>
{gtag()}<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="geo.region" content="KZ-AST"><meta name="geo.placename" content="Астана">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_KZ"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:image" content="{SITE_URL}/assets/og.png"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#06183f">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.png" type="image/png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/nunito-sans-cyrillic-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/exo-2-cyrillic-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/styles.css?v={VER}">
{ld}
</head>
<body>
<a class="skip" href="#main">К содержимому</a>
<header class="hdr"><div class="wrap hdr-in">{logo()}{nav_html()}
<div class="hdr-c"><a class="hdr-ph" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
<a class="hdr-call" href="tel:{PHONE_TEL}" aria-label="Позвонить {PHONE_DISPLAY}">{ui("phone")}</a>
<a class="btn btn-p btn-s hdr-wa" {wa_attr("Здравствуйте! Нужна обработка в Астане.")}>{ui("wa")}WhatsApp</a>
<button class="burger" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="nav">{ui("menu")}{ui("close", "ui ui-x")}</button></div></div></header>
<main id="main">
{body}
</main>
<footer class="ftr"><div class="wrap ftr-g">
<div>{logo(True)}<p>Дезинсекция, дератизация, дезинфекция и удаление запахов в Астане и пригородах.</p><a class="ftr-ph" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div>
<div><h4>Вредители</h4><ul>{"".join(f'<li><a href="/vrediteli/{p["slug"]}/">{E(p["name"])}</a></li>' for p in PESTS[:8])}</ul></div>
<div><h4>Услуги</h4><ul>{"".join(f'<li><a href="/uslugi/{s["slug"]}/">{E(s["name"])}</a></li>' for s in SERVICES[:8])}</ul></div>
<div><h4>Компания</h4><ul><li><a href="/obekty/">Объекты</a></li><li><a href="/rayony/">Районы Астаны</a></li><li><a href="/stoimost/">Стоимость</a></li><li><a href="/stati/">Статьи</a></li><li><a href="/o-kompanii/">О компании</a></li><li><a href="/kontakty/">Контакты</a></li><li><a href="/privacy-policy/">Политика конфиденциальности</a></li></ul></div>
</div><div class="wrap ftr-b"><span>© {date.today().year} {BRAND}. Информация на сайте не является публичной офертой.</span><a href="{DEV[1]}" target="_blank" rel="noopener">Разработка сайта — {DEV[0]}</a></div></footer>
<div class="fab"><button class="fab-b" type="button" data-back aria-label="Назад" title="Назад">{ui("back")}</button><button class="fab-b" type="button" data-top aria-label="Наверх" title="Наверх">{ui("up")}</button></div>
<button class="chat-o" type="button" data-chat aria-label="ИИ-консультант"><span class="chat-o-i">{ui("spark")}</span><span class="chat-o-t">ИИ-консультант</span></button>
<div class="chat" id="chat" hidden role="dialog" aria-label="ИИ-консультант"><div class="chat-h"><b>{BRAND}<small>ИИ-консультант</small></b><button type="button" data-chat-x aria-label="Закрыть чат">{ui("close")}</button></div>
<div class="chat-l" aria-live="polite"></div><div class="chat-q"></div>
<form class="chat-f"><input name="q" autocomplete="off" placeholder="Напишите вопрос" aria-label="Ваш вопрос"><button type="submit" aria-label="Отправить">{ui("send")}</button></form>
<a class="chat-wa" {wa_attr("Здравствуйте! Пишу с сайта, нужна обработка.")}>{ui("wa")}Продолжить в WhatsApp</a></div>
<script>window.CFG={cfg};</script>
<script src="/assets/app.js?v={VER}" defer></script>
</body></html>'''
    out = DIST / "404.html" if path == "/404" else DIST / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc, encoding="utf-8")

# ---------------------------------------------------------------- страницы
def build_home():
    hp = [P[x] for x in ("tarakany", "klopy", "muravi", "osy", "blohi", "kleshchi", "mol")]
    cloud = "".join(f'<a class="hc hc-{i}" href="/vrediteli/{p["slug"]}/" title="{E(p["name"])}">{photo(p, "hc-p", eager=True)}</a>' for i, p in enumerate(hp))
    body = f'''<section class="hero"><div class="wrap hero-in"><div class="hero-t">
<h1>Дезинсекция, дератизация и&nbsp;<em>дезинфекция</em> в&nbsp;Астане</h1>
<p class="lead-t">Избавляем от насекомых и грызунов, убираем плесень и стойкие запахи в квартирах, домах и на объектах бизнеса.</p>
{btns("Здравствуйте! Нужна обработка в Астане.", True)}</div>
<div class="hero-v" aria-hidden="true"><div class="hex-cloud">{cloud}</div></div></div></section>
{sec("От кого избавляем", pest_cards(full=True), "Выберите вредителя: признаки, обработка и подготовка.", sid="vrediteli", link=("Все вредители", "/vrediteli/"))}
{sec("Услуги", svc_cards(), "Подбираем метод под задачу и объект.", alt=True, link=("Все услуги", "/uslugi/"))}
{promo_pair()}
{sec("Обрабатываем любые объекты", obj_cards(), link=("Все объекты", "/obekty/"))}
{promo_wide()}
{callout()}
{sec("Как мы работаем", steps_html(), alt=True)}
{sec("От чего зависит стоимость", factors_html(), "Точную цену называем до выезда, после уточнения задачи.", link=("Подробнее о стоимости", "/stoimost/"))}
{sec("Как подготовиться к обработке", prep_html(), alt=True, link=("Памятка", "/stati/kak-podgotovit-kvartiru-k-obrabotke/"))}
{geo_sec()}
{sec("Полезно знать", article_cards(), link=("Все статьи", "/stati/"))}
{sec("Частые вопросы", faq_html(FAQ), alt=True)}
{lead_form()}'''
    page("/", f"Дезинсекция, дератизация и дезинфекция в Астане — {BRAND}",
         "Санитарная служба в Астане: уничтожение тараканов, клопов, блох, крыс и мышей, дезинфекция, удаление плесени и запахов. Все районы и пригороды.",
         body, [service_schema("Дезинсекция, дератизация и дезинфекция", "/", "Санитарная обработка квартир, домов и объектов бизнеса в Астане."), faq_schema(FAQ)], prio="1.0")

def build_pests():
    body = f'''{ph_hero("Уничтожение вредителей в Астане", "Насекомые и грызуны в квартирах, домах и на объектах бизнеса. Выберите вредителя, чтобы узнать подробности.", [("Вредители", "/vrediteli/")], "Здравствуйте! Нужна обработка от вредителей.")}
{sec("Насекомые", pest_cards(full=True))}
{sec("Сад и огород", pest_cards([P[x] for x in ("tlya", "gusenicy", "belyanka", "shchitniki")]), alt=True, link=("Обработка сада", "/uslugi/obrabotka-sada/"))}
{sec("Также обрабатываем", pest_cards([p for p in PESTS if not p.get("photo")]))}{callout()}{lead_form()}'''
    page("/vrediteli/", f"Уничтожение вредителей в Астане — {BRAND}", "Уничтожение тараканов, клопов, блох, муравьёв, моли, ос, клещей, крыс и мышей в Астане.", body, crumbs=[("Вредители", "/vrediteli/")], prio="0.9")
    for p in PESTS:
        url = f"/vrediteli/{p['slug']}/"; s = S[p["svc"]]
        signs = "".join(f"<li>{E(x)}</li>" for x in p["signs"])
        faq = p["faq"] + [FAQ[0], FAQ[2], FAQ[4]]
        ph_list = [x for x in PESTS if x.get("photo") and x is not p]; k = PESTS.index(p) * 3 % len(ph_list)
        others = (ph_list[k:] + ph_list[:k])[:4]
        body = f'''{ph_hero(f"Уничтожение {E(p['gen'])} в Астане", E(p["intro"]), [("Вредители", "/vrediteli/"), (p["name"], url)], f"Здравствуйте! Нужна обработка от: {p['name'].lower()}.", photo(p, "phd-p", big=True, eager=True) if p.get("photo") else "")}
<section class="sec"><div class="wrap two"><div><h2>Признаки</h2><ul class="signs">{signs}</ul></div><div><h2>Как проходит обработка</h2><p class="txt">{E(p["how"])}</p>
<a class="lnk" href="/uslugi/{s['slug']}/">Подробнее об услуге {ui("arrow")}</a></div></div></section>
{sec("Как подготовиться", prep_html(), alt=True)}
{callout(f"Здравствуйте! Нужна обработка от: {p['name'].lower()}.")}
{sec("Вопросы", faq_html(faq))}
{sec("Другие вредители", pest_cards(others), alt=True, link=("Все вредители", "/vrediteli/"))}
{geo_sec()}
{lead_form(f"Заявка: уничтожение {p['gen']}", p["slug"])}'''
        page(url, f"Уничтожение {p['gen']} в Астане — {BRAND}", f"Уничтожение {p['gen']} в Астане: квартиры, дома, кафе и офисы во всех районах. {p['intro'][:90].rsplit(' ', 1)[0]}…",
             body, [service_schema(f"Уничтожение {p['gen']}", url, p["intro"]), faq_schema(faq)], crumbs=[("Вредители", "/vrediteli/"), (p["name"], url)], prio="0.9")

def build_services():
    body = f'''{ph_hero("Услуги санитарной службы", "Дезинсекция, дератизация, дезинфекция, удаление плесени и запахов в Астане.", [("Услуги", "/uslugi/")], "Здравствуйте! Нужна санитарная обработка.")}
{sec("Все услуги", svc_cards())}{promo_pair()}{callout()}{lead_form()}'''
    page("/uslugi/", f"Услуги санитарной службы в Астане — {BRAND}", "Дезинсекция, дератизация, дезинфекция, обработка от плесени, озонирование и удаление запахов в Астане.", body, crumbs=[("Услуги", "/uslugi/")], prio="0.9")
    for s in SERVICES:
        url = f"/uslugi/{s['slug']}/"
        kinds = "".join(f'<div><b>{E(t)}</b><p>{E(d)}</p></div>' for t, d in s["kinds"])
        rel = [P[x] for x in ("tlya", "gusenicy", "belyanka", "shchitniki")] if s["slug"] == "obrabotka-sada" else [p for p in PESTS if p["svc"] == s["slug"] and p.get("photo")][:8]
        rel = rel if len(rel) in (4, 8) else []
        media = svc_media(s, "phd-p", big=True)
        body = f'''{ph_hero(f"{E(s['name'])} в Астане", E(s["lead"]), [("Услуги", "/uslugi/"), (s["name"], url)], f"Здравствуйте! Нужна услуга: {s['name'].lower()}.", media if "sc-ph" not in media else "")}
{sec(f"{svc_count(s)[0].upper()}{svc_count(s)[1:]}", items_html(s))}
<section class="sec sec-alt"><div class="wrap two"><div class="prose">{"".join(f"<p>{E(x)}</p>" for x in s["body"])}</div><div class="kinds">{kinds}</div></div></section>
{sec("От кого избавляем", pest_cards(rel)) if rel else ""}
{sec("Как мы работаем", steps_html(), alt=bool(rel))}
{callout(f"Здравствуйте! Нужна услуга: {s['name'].lower()}.")}
{sec("Вопросы", faq_html(FAQ[:6]), alt=not rel)}
{sec("Другие услуги", svc_cards([x for x in SERVICES if x is not s][:4]), alt=bool(rel))}
{lead_form(f"Заявка: {s['name'].lower()}")}'''
        page(url, f"{s['name']} в Астане — {BRAND}", f"{s['name']} в Астане: {s['lead'][:120].rsplit(' ', 1)[0]}…",
             body, [service_schema(s["name"], url, s["lead"])], crumbs=[("Услуги", "/uslugi/"), (s["name"], url)], prio="0.9")

def build_objects():
    body = f'''{ph_hero("Обрабатываем любые объекты", "Квартиры, частные дома, кафе, офисы, склады, школы, гостиницы и подвалы многоквартирных домов в Астане.", [("Объекты", "/obekty/")], "Здравствуйте! Нужна обработка объекта.")}
{sec("Объекты", obj_cards())}{lead_form()}'''
    page("/obekty/", f"Санитарная обработка объектов в Астане — {BRAND}", "Дезинсекция и дезинфекция квартир, домов, кафе, офисов, складов, школ, гостиниц и подвалов в Астане.", body, crumbs=[("Объекты", "/obekty/")], prio="0.8")
    for slug, name, gen, icon, text, pests in OBJECTS:
        url = f"/obekty/{slug}/"
        body = f'''{ph_hero(f"Обработка {E(gen)} в Астане", E(text), [("Объекты", "/obekty/"), (name, url)], f"Здравствуйте! Нужна обработка: {name.lower()}.")}
{sec("Частые вредители", pest_cards([P[x] for x in pests]))}
{sec("Услуги", svc_cards(), alt=True)}
{callout(f"Здравствуйте! Нужна обработка: {name.lower()}.")}
{sec("Вопросы", faq_html(FAQ[:6]))}
{lead_form()}'''
        page(url, f"Дезинсекция и дезинфекция {gen} в Астане — {BRAND}", f"Санитарная обработка {gen} в Астане: {text[:110].rsplit(' ', 1)[0]}…", body,
             [service_schema(f"Обработка {gen}", url, text)], crumbs=[("Объекты", "/obekty/"), (name, url)], prio="0.7")

def build_districts():
    body = f'''{ph_hero("Районы Астаны", "Работаем во всех районах столицы и в пригородах. Выберите свой район.", [("Районы", "/rayony/")], "Здравствуйте! Нужна обработка, мой район:")}
{sec("Районы и пригороды", districts_html())}{lead_form()}'''
    page("/rayony/", f"Санитарная обработка по районам Астаны — {BRAND}", "Дезинсекция и дезинфекция в районах Алматы, Байконыр, Есиль, Нура, Сарыарка, Сарайшык и в пригородах Астаны.", body, crumbs=[("Районы", "/rayony/")], prio="0.8")
    for d in DISTRICTS:
        url = f"/rayony/{d['slug']}/"
        spots = "".join(f"<li>{E(x)}</li>" for x in d["spots"])
        faq = [(f"Выезжаете {d['loc']}?", f"Да, работаем {d['loc']}. Время приезда согласуем при заявке."),
               (f"Сколько стоит обработка {d['loc']}?", "Стоимость зависит от вида вредителя, площади и типа объекта. Точную цену называем до выезда.")] + FAQ[2:5]
        body = f'''{ph_hero(f"Дезинсекция и дезинфекция {E(d['loc'])}", E(d["about"]), [("Районы", "/rayony/"), (d["short"], url)], f"Здравствуйте! Нужна обработка, {d['name']}.")}
<section class="sec"><div class="wrap two"><div><h2>Где работаем</h2><ul class="bl">{spots}</ul></div><div><h2>Как проходит заявка</h2><p class="txt">Позвоните или напишите в WhatsApp, укажите адрес {d['loc']}, вид вредителя и объект. Назовём стоимость и согласуем время.</p></div></div></section>
{sec(f"Вредители {d['loc']}", pest_cards(full=True), alt=True)}
{sec("Услуги", svc_cards())}
{callout(f"Здравствуйте! Нужна обработка, {d['name']}.")}
{sec("Вопросы", faq_html(faq), alt=True)}
{sec("Другие районы", districts_html(d["slug"]))}
{lead_form(f"Заявка — {d['short']}")}'''
        page(url, f"Дезинсекция и дезинфекция {d['loc']} (Астана) — {BRAND}", f"Уничтожение тараканов, клопов, крыс и мышей, дезинфекция {d['loc']}: {', '.join(d['spots'])}.",
             body, [service_schema(f"Санитарная обработка {d['loc']}", url, d["about"], d["name"]), faq_schema(faq)], crumbs=[("Районы", "/rayony/"), (d["short"], url)], prio="0.8")

def build_articles():
    for a in ARTICLES:
        url = f"/stati/{a['slug']}/"
        parts = ["<ul>" + "".join(f"<li>{E(i)}</li>" for i in x) + "</ul>" if t == "ul" else f"<{t}>{E(x)}</{t}>" for t, x in a["body"]]
        body = f'''<section class="phd phd-s"><div class="wrap">{crumbs_html([("Статьи", "/stati/"), (a["title"], url)])}<h1>{E(a["title"])}</h1><p class="lead-t">{E(a["desc"])}</p></div></section>
<section class="sec"><div class="wrap"><article class="prose">{"".join(parts)}{btns("Здравствуйте! Прочитал статью, нужна обработка.")}</article></div></section>
{sec("Другие статьи", article_cards(), alt=True)}{lead_form()}'''
        sch = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": TODAY, "dateModified": TODAY,
               "author": {"@id": SITE_URL + "/#org"}, "publisher": {"@id": SITE_URL + "/#org"}, "mainEntityOfPage": SITE_URL + url, "inLanguage": "ru"}
        page(url, f"{a['title']} — {BRAND}", a["desc"], body, [sch], crumbs=[("Статьи", "/stati/"), (a["title"], url)], prio="0.6")
    body = f'''{ph_hero("Статьи", "Памятки и советы: как подготовиться к обработке, что делать с клопами, плесенью и грызунами.", [("Статьи", "/stati/")], "Здравствуйте! Есть вопрос по обработке.")}
{sec("Все статьи", article_cards())}'''
    page("/stati/", f"Статьи о дезинсекции и дезинфекции — {BRAND}", "Как подготовить квартиру к обработке, что делать с клопами, плесенью и грызунами.", body, crumbs=[("Статьи", "/stati/")], prio="0.6")

def build_misc():
    body = f'''{ph_hero("Стоимость обработки", "Цену называем до выезда — после того как уточним вид вредителя, площадь и объект.", [("Стоимость", "/stoimost/")], "Здравствуйте! Хочу узнать стоимость обработки.")}
{sec("От чего зависит цена", factors_html())}{sec("Как мы работаем", steps_html(), alt=True)}{sec("Вопросы", faq_html(FAQ[:6]))}{lead_form("Узнать стоимость")}'''
    page("/stoimost/", f"Стоимость дезинсекции и дезинфекции в Астане — {BRAND}", "От чего зависит стоимость дезинсекции, дератизации и дезинфекции в Астане. Цену называем до выезда.", body, [faq_schema(FAQ[:6])], crumbs=[("Стоимость", "/stoimost/")], prio="0.8")
    body = f'''{ph_hero(f"О компании {BRAND}", "Санитарная служба в Астане: дезинсекция, дератизация, дезинфекция, удаление плесени и запахов.", [("О компании", "/o-kompanii/")], "Здравствуйте! Нужна обработка.")}
<section class="sec"><div class="wrap two"><div class="prose"><h2>Чем занимаемся</h2><p>Избавляем от насекомых и грызунов, проводим дезинфекцию, убираем плесень и стойкие запахи в квартирах, частных домах и на объектах бизнеса.</p><p>Работаем по всем районам Астаны и в пригородах: Косшы, Коянды, Талапкер.</p></div><div><ul class="dl">{"".join(f'<li><a href="/uslugi/{x["slug"]}/">{E(x["name"])}{ui("arrow")}</a></li>' for x in SERVICES)}</ul></div></div></section>
{sec("Как мы работаем", steps_html(), alt=True)}{lead_form()}'''
    page("/o-kompanii/", f"О компании {BRAND} — санитарная служба Астаны", f"{BRAND}: дезинсекция, дератизация и дезинфекция в Астане и пригородах.", body, crumbs=[("О компании", "/o-kompanii/")], prio="0.5")
    body = f'''{ph_hero("Контакты", "Позвоните или напишите в WhatsApp — ответим на вопросы и назовём стоимость.", [("Контакты", "/kontakty/")], "Здравствуйте! Нужна обработка.")}
<section class="sec"><div class="wrap cont"><div><span>Телефон и WhatsApp</span><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div><div><span>Где работаем</span><b>Астана и пригороды</b></div><div><span>Написать</span><a {wa_attr("Здравствуйте! Нужна обработка.")}>WhatsApp</a></div></div></section>
{geo_sec()}{lead_form()}'''
    page("/kontakty/", f"Контакты {BRAND} — санитарная служба Астаны", f"Телефон и WhatsApp {PHONE_DISPLAY}. Дезинсекция, дератизация и дезинфекция в Астане.", body, crumbs=[("Контакты", "/kontakty/")], prio="0.6")
    body = f'''<section class="phd phd-s"><div class="wrap">{crumbs_html([("Политика конфиденциальности", "/privacy-policy/")])}<h1>Политика конфиденциальности</h1></div></section>
<section class="sec"><div class="wrap"><div class="prose"><p>Сайт не хранит персональные данные на своих серверах. Имя, телефон и комментарий из формы заявки передаются в WhatsApp только после того, как вы сами нажмёте кнопку отправки.</p>
<p>Для статистики посещений могут использоваться сервисы Google Analytics и Google Ads, обрабатывающие обезличенные данные. Вопросы о данных можно задать по телефону {PHONE_DISPLAY}.</p></div></div></section>'''
    page("/privacy-policy/", f"Политика конфиденциальности — {BRAND}", "Как сайт обрабатывает данные из формы заявки и статистику посещений.", body, crumbs=[("Политика конфиденциальности", "/privacy-policy/")], prio="0.2")
    body = f'''<section class="phd"><div class="wrap"><h1>Страница не найдена</h1><p class="lead-t">Возможно, адрес изменился. Перейдите на главную или выберите вредителя.</p><div class="btns"><a class="btn btn-p" href="/">На главную</a><a class="btn btn-l" href="/vrediteli/">Вредители</a></div></div></section>'''
    page("/404", f"Страница не найдена — {BRAND}", "Страница не найдена.", body, prio="0")

def build_files():
    PAGES[:] = [p for p in PAGES if p[0] != "/404"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + \
         [f"<url><loc>{SITE_URL}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>" for u, p in PAGES] + ["</urlset>"]
    (DIST / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "YandexBot", "Bingbot"]
    (DIST / "robots.txt").write_text("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    llms = [f"# {BRAND} — {BRAND_SUB}", "", "> Дезинсекция, дератизация, дезинфекция, обработка от плесени, озонирование и удаление запахов в Астане и пригородах (Косшы, Коянды, Талапкер).", "",
            f"- Телефон и WhatsApp: {PHONE_DISPLAY}", f"- Сайт: {SITE_URL}/", "- Стоимость называется до выезда и зависит от вида вредителя, площади, объекта и степени заражения.", "",
            "## Вредители"] + [f"- {p['name']}: {SITE_URL}/vrediteli/{p['slug']}/" for p in PESTS] + ["", "## Услуги"] + [f"- {s['name']} — {s['sub']}: {SITE_URL}/uslugi/{s['slug']}/" for s in SERVICES] + \
           ["", "## Объекты"] + [f"- {o[1]}: {SITE_URL}/obekty/{o[0]}/" for o in OBJECTS] + ["", "## Районы"] + [f"- {d['name']}: {SITE_URL}/rayony/{d['slug']}/" for d in DISTRICTS] + \
           ["", "## Частые вопросы"] + [f"- {q} {a}" for q, a in FAQ] + ["", "## Статьи"] + [f"- {a['title']}: {SITE_URL}/stati/{a['slug']}/" for a in ARTICLES]
    (DIST / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    (DIST / "site.webmanifest").write_text(json.dumps({"name": f"{BRAND} — {BRAND_SUB}", "short_name": BRAND, "start_url": "/", "display": "standalone", "background_color": "#06183f", "theme_color": "#06183f",
        "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")
    shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)
    css = (ROOT / "src" / "fonts.css").read_text(encoding="utf-8") + (ROOT / "src" / "styles.css").read_text(encoding="utf-8")
    (DIST / "assets" / "styles.css").write_text(css, encoding="utf-8")
    kb = {"phone": PHONE_DISPLAY, "pests": [[p["name"], p["gen"], f"/vrediteli/{p['slug']}/", p["slug"]] for p in PESTS], "services": [[s["name"], f"/uslugi/{s['slug']}/"] for s in SERVICES],
          "districts": [[d["short"], d["loc"], f"/rayony/{d['slug']}/"] for d in DISTRICTS]}
    js = (ROOT / "src" / "app.js").read_text(encoding="utf-8").replace("/*__KB__*/{}", json.dumps(kb, ensure_ascii=False))
    (DIST / "assets" / "app.js").write_text(js, encoding="utf-8")
    for f in ("favicon.png", "favicon.ico"):
        if (ROOT / "assets" / f).exists(): shutil.copy(ROOT / "assets" / f, DIST / f)

if __name__ == "__main__":
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    build_home(); build_pests(); build_services(); build_objects(); build_districts(); build_articles(); build_misc(); build_files()
    print("pages:", len(PAGES))
