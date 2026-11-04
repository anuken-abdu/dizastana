# DizAstana (diz-astana.kz) — сайт санитарной службы Астаны

Статический сайт: Python-генератор → папка `dist/` → Vercel.

## Сборка
```
python3 src/gen_chat.py      # ИИ-чат: api/chat.js из данных сайта
python3 src/build.py         # сайт → dist/ (66 страниц, sitemap, robots, llms.txt)
python3 src/banners.py       # OG-картинка assets/og.png (после — снова build.py)
python3 src/ads_editor.py    # Google Ads Editor → google-ads/*.csv
```
Все тексты, вредители, услуги, районы и FAQ — в `src/data.py`. Сменили домен — правьте `SITE_URL` там же и пересоберите.

## Vercel
- Залить весь проект (с папками `api/`, `dist/`, `images/`), Output Directory — `dist` (уже в vercel.json).
- Environment Variables → `ANTHROPIC_API_KEY` — чтобы чат отвечал через ИИ. Без ключа работает встроенный автоответчик.
- Домен: добавить diz-astana.kz и www.diz-astana.kz в Settings → Domains, основной — www (как SITE_URL в data.py).

## Аналитика и конверсии
В `src/data.py` заполнить `GA_ID`, `GADS_ID`, `GADS_CALL_LABEL`, `GADS_WA_LABEL` и пересобрать. Клики по телефону и WhatsApp, а также отправка формы шлют конверсии.

## Фото
Свои фотографии кладите в `images/` (см. images/README.txt).

## Фото вредителей
Лежат в `assets/pests/` (webp, 960×720 и 480×360, без EXIF). Новое фото: положите исходник, обрежьте под 4:3 на белом фоне, назовите по slug вредителя из `data.py` и пропишите `photo="slug"`.

## Фото услуг
Положите `assets/services/<slug-услуги>.webp` (4:3, например 960×720) — фото само встанет в карточку и шапку страницы услуги. Без файла показывается фото вредителя или тёмная плитка с линейной иконкой.

## Google Ads Editor
Аккаунт → Импорт → Из файла: сначала `1-kampaniya-editor.csv`, затем `2-rasshireniya-editor.csv` → Обработать → Сохранить → Опубликовать.
