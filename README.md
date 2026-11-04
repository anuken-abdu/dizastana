# ТазаДез — сайт санитарной службы Астаны

Статический сайт: Python-генератор → папка `dist/` → Vercel.

## Сборка
```
python3 src/gen_chat.py      # ИИ-чат: api/chat.js из данных сайта
python3 src/build.py         # сайт → dist/ (57 страниц, sitemap, robots, llms.txt)
python3 src/banners.py       # баннеры → google-ads/banners/ и assets/og.png (после — снова build.py)
python3 src/ads.py src/templates/Create_New_Campaigns.xlsx   # Google Ads → google-ads/
```
Все тексты, вредители, услуги, районы и FAQ — в `src/data.py`. Сменили домен — правьте `SITE_URL` там же и пересоберите.

## Vercel
- Залить весь проект (с папками `api/`, `dist/`, `images/`), Output Directory — `dist` (уже в vercel.json).
- Environment Variables → `ANTHROPIC_API_KEY` — чтобы чат отвечал через ИИ. Без ключа работает встроенный автоответчик.
- Домен: добавить в Settings → Domains, основной — с www.

## Аналитика и конверсии
В `src/data.py` заполнить `GA_ID`, `GADS_ID`, `GADS_CALL_LABEL`, `GADS_WA_LABEL` и пересобрать. Клики по телефону и WhatsApp, а также отправка формы шлют конверсии.

## Фото
Свои фотографии кладите в `images/` (см. images/README.txt).
