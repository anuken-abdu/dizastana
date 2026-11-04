# -*- coding: utf-8 -*-
"""Google Ads Editor: CSV для импорта (Аккаунт → Импорт → Из файла).
1-kampaniya-editor.csv — кампания, местоположение, группы, ключи, минус-слова, объявления.
2-rasshireniya-editor.csv — быстрые ссылки, уточнения, структурированные описания, звонок.
Запуск: python3 src/ads_editor.py"""
import csv, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ads
from ads import G, NEG, COMMON_D, CAMP, GEO, BUDGET, headlines, chk, ERR
from data import SITE_URL, PHONE_TEL

OUT = Path(__file__).resolve().parent.parent / "google-ads"
H = [f"Headline {i}" for i in range(1, 16)]; D = [f"Description {i}" for i in range(1, 5)]
COLS = ["Campaign", "Campaign Type", "Networks", "Budget", "Budget type", "Bid Strategy Type", "Campaign Status", "EU political ads", "Location",
        "Ad Group", "Ad Group Status", "Keyword", "Criterion Type", "Status", "Ad type"] + H + D + ["Path 1", "Path 2", "Final URL"]

rows = [{"Campaign": CAMP, "Campaign Type": "Search", "Networks": "Google search", "Budget": BUDGET, "Budget type": "Daily",
         "Bid Strategy Type": "Maximize clicks", "Campaign Status": "Paused", "EU political ads": "No"},
        {"Campaign": CAMP, "Location": GEO}]
seen = set(); nkw = 0
for name, path, base, exact, hs, ds, p1 in G:
    rows.append({"Campaign": CAMP, "Ad Group": name, "Ad Group Status": "Enabled"})
    kws = []
    for b in base:
        for c in ads.CITY: kws += [(f"{b} {c}", "Phrase"), (f"{b} {c}", "Exact")]
    kws += [(e, "Exact") for e in exact]
    for kw, mt in dict.fromkeys(kws):
        if (kw, mt) in seen: ERR.append(f"дубль {kw} {mt}")
        seen.add((kw, mt)); nkw += 1
        for ng in NEG:
            if f" {ng} " in f" {kw} ": ERR.append(f"минус «{ng}» режет «{kw}»")
        rows.append({"Campaign": CAMP, "Ad Group": name, "Keyword": kw, "Criterion Type": mt, "Status": "Enabled"})
    heads = headlines(hs); descs = ds + COMMON_D
    if len(heads) != 15: ERR.append(f"{name}: заголовков {len(heads)}")
    r = {"Campaign": CAMP, "Ad Group": name, "Ad type": "Responsive search ad", "Status": "Enabled", "Final URL": SITE_URL + path,
         "Path 1": chk(p1, 15, "path1"), "Path 2": "астана"}
    for i, h in enumerate(heads): r[H[i]] = chk(h, 30, "headline")
    for i, d in enumerate(descs): r[D[i]] = chk(d, 90, "description")
    rows.append(r)
for ng in NEG:
    rows.append({"Campaign": CAMP, "Keyword": ng, "Criterion Type": "Campaign Negative Phrase"})

SL = [("Уничтожение клопов", "Спальные места и мебель", "Квартиры и гостиницы", "/vrediteli/klopy/"),
      ("Уничтожение тараканов", "Кухня, санузел, щели", "Квартиры, кафе, офисы", "/vrediteli/tarakany/"),
      ("Крысы и мыши", "Дератизация домов", "Подвалы и склады", "/uslugi/deratizaciya/"),
      ("Обработка сада", "Тля, гусеницы, белянки", "Деревья и огород", "/uslugi/obrabotka-sada/"),
      ("Для бизнеса", "Кафе, магазины, склады", "Разово и по графику", "/uslugi/dlya-biznesa/"),
      ("Стоимость обработки", "От чего зависит цена", "Назовём до выезда", "/stoimost/")]
CO = ["Все районы Астаны", "Выезд в пригороды", "Квартиры и бизнес", "Стоимость до выезда", "Поможем подготовиться", "Сады и участки"]
SN = ["Дезинсекция", "Дератизация", "Дезинфекция", "Озонирование", "Обработка сада", "Удаление запахов"]
ACOLS = ["Campaign", "Link text", "Description line 1", "Description line 2", "Final URL", "Callout text", "Header", "Snippet values", "Phone number", "Country code"]
arows = [{"Campaign": CAMP, "Link text": chk(t, 25, "sitelink"), "Description line 1": chk(a, 35, "sl d1"), "Description line 2": chk(b, 35, "sl d2"), "Final URL": SITE_URL + u} for t, a, b, u in SL]
arows += [{"Campaign": CAMP, "Callout text": chk(x, 25, "callout")} for x in CO]
arows += [{"Campaign": CAMP, "Header": "Services", "Snippet values": ";".join(chk(x, 25, "snippet") for x in SN)}]
arows += [{"Campaign": CAMP, "Phone number": PHONE_TEL, "Country code": "KZ"}]

if ERR: print("\n".join(ERR[:30])); raise SystemExit(1)
OUT.mkdir(exist_ok=True)
for f in OUT.glob("*"):
    if f.is_file(): f.unlink()
def write(path, cols, rs):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in rs: w.writerow({c: r.get(c, "") for c in cols})
write(OUT / "1-kampaniya-editor.csv", COLS, rows)
write(OUT / "2-rasshireniya-editor.csv", ACOLS, arows)
txt = [f"КАМПАНИЯ: {CAMP} (на паузе) | {GEO} | бюджет {BUDGET}/день в валюте аккаунта", f"Групп: {len(G)}, ключей: {nkw}, минус-слов: {len(NEG)}", ""]
for name, path, base, exact, hs, ds, p1 in G:
    txt += [f"Группа: {name}", f"URL: {SITE_URL}{path}", "Заголовки: " + " | ".join(headlines(hs)), "Описания: " + " | ".join(ds + COMMON_D), ""]
(OUT / "3-teksty-dlya-proverki.txt").write_text("\n".join(txt), encoding="utf-8")
print("групп", len(G), "ключей", nkw, "минус", len(NEG), "строк", len(rows), "расширений", len(arows))
