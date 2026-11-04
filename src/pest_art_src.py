# -*- coding: utf-8 -*-
"""Реалистичные иллюстрации вредителей, которых нет в наборе Fluent Emoji.
Стиль — мягкие градиенты без обводок, viewBox 32×32."""

def wrap(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none">{body}</svg>'

LEG = 'stroke-linecap="round" stroke-linejoin="round" fill="none"'

CUSTOM = {}

# Постельный клоп — плоский рыже-коричневый овал
CUSTOM["bedbug"] = wrap(f'''
<defs>
<radialGradient id="b1" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="matrix(-1.5 11 -9 -1.2 15 15)"><stop stop-color="#D9774A"/><stop offset=".55" stop-color="#A34522"/><stop offset="1" stop-color="#5E2310"/></radialGradient>
<linearGradient id="b2" x1="16" y1="6" x2="16" y2="12" gradientUnits="userSpaceOnUse"><stop stop-color="#B9593A"/><stop offset="1" stop-color="#6E2A14"/></linearGradient>
</defs>
<g stroke="#5A2412" stroke-width="1.05" {LEG}>
<path d="M10.3 13.6 7 12.2 5 9.6"/><path d="M9.6 18.2 5.8 18.5 3.9 21"/><path d="M10.6 23 7.8 25.6 7.4 28.4"/>
<path d="M21.7 13.6 25 12.2 27 9.6"/><path d="M22.4 18.2 26.2 18.5 28.1 21"/><path d="M21.4 23 24.2 25.6 24.6 28.4"/>
<path d="M14.6 5.2 12.6 2.6 10.2 2.2" stroke-width=".8"/><path d="M17.4 5.2 19.4 2.6 21.8 2.2" stroke-width=".8"/>
</g>
<ellipse cx="16" cy="5.9" rx="2.1" ry="1.9" fill="url(#b2)"/>
<circle cx="14.4" cy="5.4" r=".55" fill="#2B0F06"/><circle cx="17.6" cy="5.4" r=".55" fill="#2B0F06"/>
<path d="M10.2 9.4c1.4-2 3.5-2.6 5.8-2.6s4.4.6 5.8 2.6c-.6 1.3-3 2-5.8 2s-5.2-.7-5.8-2z" fill="url(#b2)"/>
<path d="M16 10.4c6.3 0 8.6 4.6 8.6 9.4 0 5.6-3.9 9.4-8.6 9.4s-8.6-3.8-8.6-9.4c0-4.8 2.3-9.4 8.6-9.4z" fill="url(#b1)"/>
<g stroke="#4E1D0C" stroke-opacity=".55" stroke-width=".55" fill="none">
<path d="M8.4 15.4c4.9 1.5 10.3 1.5 15.2 0"/><path d="M7.6 19.2c5.4 1.7 11.4 1.7 16.8 0"/><path d="M7.9 23c5.3 1.6 10.9 1.6 16.2 0"/><path d="M9.6 26.4c4.3 1.3 8.5 1.3 12.8 0"/>
</g>
<ellipse cx="13" cy="15.5" rx="3.6" ry="2" fill="#fff" fill-opacity=".22" transform="rotate(-18 13 15.5)"/>''')

# Блоха — сжатое с боков тело, мощные задние ноги
CUSTOM["flea"] = wrap(f'''
<defs>
<radialGradient id="f1" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="matrix(9 -2 2 7 14 14)"><stop stop-color="#B5713A"/><stop offset=".6" stop-color="#7A3E17"/><stop offset="1" stop-color="#3E1C08"/></radialGradient>
</defs>
<g stroke="#3A1A08" {LEG}>
<path d="M22.6 19.4 26.5 24.8 24.6 29.4 27.6 29.6" stroke-width="1.5"/>
<path d="M17.4 21.4 18.6 25.8 16.4 29" stroke-width="1.2"/>
<path d="M12 20.8 11 25 8.6 27.4" stroke-width="1.1"/>
</g>
<path d="M5.6 15.2c0-5.8 6-10 13.2-9.4 6.3.5 9.8 5.3 8.8 10.7-1 5.4-6.2 7.5-11.7 7.2-5.8-.3-10.3-3.6-10.3-8.5z" fill="url(#f1)"/>
<path d="M6.2 12.4c-2-.9-3.8-.2-4.4 1.1.6 1.6 2.6 2.3 4.4 1.7z" fill="#5A2A0D"/>
<circle cx="5" cy="12.9" r=".55" fill="#120602"/>
<g stroke="#2E1305" stroke-opacity=".5" stroke-width=".6" fill="none">
<path d="M11.4 8.4c1.6 4.1 1.6 9.2-.3 13.4"/><path d="M15.6 6.4c1.8 4.8 1.8 10.9-.1 16.4"/><path d="M19.8 6.3c1.8 4.6 1.7 10.3-.3 15.7"/><path d="M23.8 8c1.4 3.7 1.3 8.2-.7 12.1"/>
</g>
<ellipse cx="15" cy="9.6" rx="5" ry="1.6" fill="#fff" fill-opacity=".25" transform="rotate(-8 15 9.6)"/>''')

# Иксодовый клещ — каплевидное тело, тёмный щиток
CUSTOM["tick"] = wrap(f'''
<defs>
<radialGradient id="t1" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="matrix(0 10 -8.5 0 16 19)"><stop stop-color="#C2563D"/><stop offset=".6" stop-color="#8A2E1E"/><stop offset="1" stop-color="#4A140B"/></radialGradient>
<linearGradient id="t2" x1="16" y1="9" x2="16" y2="17" gradientUnits="userSpaceOnUse"><stop stop-color="#3E2A22"/><stop offset="1" stop-color="#170C08"/></linearGradient>
</defs>
<g stroke="#2A140C" stroke-width="1.15" {LEG}>
<path d="M11.4 12.6 7.6 9.2 6.6 5.6"/><path d="M10.4 15.4 5.6 13.6 3.2 15.2"/><path d="M10.4 18.6 5.4 20 3.6 23.2"/><path d="M11.6 21.8 8 25.4 8 28.6"/>
<path d="M20.6 12.6 24.4 9.2 25.4 5.6"/><path d="M21.6 15.4 26.4 13.6 28.8 15.2"/><path d="M21.6 18.6 26.6 20 28.4 23.2"/><path d="M20.4 21.8 24 25.4 24 28.6"/>
</g>
<path d="M14.6 6.2h2.8l.6 3.8h-4z" fill="#2A160E"/>
<path d="M15.2 3.6h1.6l.4 2.8h-2.4z" fill="#3B2116"/>
<path d="M16 9.6c5.6 0 7.4 5.1 7.4 9.6 0 6-3.5 10-7.4 10s-7.4-4-7.4-10c0-4.5 1.8-9.6 7.4-9.6z" fill="url(#t1)"/>
<path d="M16 9.6c3.4 0 4.8 2.5 4.6 5.1-.3 2.6-2.3 4-4.6 4s-4.3-1.4-4.6-4c-.2-2.6 1.2-5.1 4.6-5.1z" fill="url(#t2)"/>
<ellipse cx="14.4" cy="12.2" rx="2" ry="1" fill="#fff" fill-opacity=".22" transform="rotate(-20 14.4 12.2)"/>
<ellipse cx="13.2" cy="22" rx="1.8" ry="3" fill="#fff" fill-opacity=".14"/>''')

# Пылевой клещ — полупрозрачное кремовое тело с щетинками
CUSTOM["mite"] = wrap(f'''
<defs>
<radialGradient id="m1" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="matrix(0 10 -9 0 15.5 15)"><stop stop-color="#FFF4DE"/><stop offset=".55" stop-color="#E9C9A0"/><stop offset="1" stop-color="#B58658"/></radialGradient>
</defs>
<g stroke="#9C6E45" stroke-width="1.2" {LEG}>
<path d="M10.6 12.4 6.6 9.6 5.2 6.4"/><path d="M9.8 15.4 5 14.8 2.8 16.6"/><path d="M10.2 20.4 5.6 22.6 4.6 25.6"/><path d="M12 23.6 9.2 27.2 9.6 29.6"/>
<path d="M21.4 12.4 25.4 9.6 26.8 6.4"/><path d="M22.2 15.4 27 14.8 29.2 16.6"/><path d="M21.8 20.4 26.4 22.6 27.4 25.6"/><path d="M20 23.6 22.8 27.2 22.4 29.6"/>
</g>
<g stroke="#B58A62" stroke-width=".5" stroke-linecap="round"><path d="M12 9 10.4 5.6M20 9l1.6-3.4M9.4 18 6.6 18.4M22.6 18l2.8.4M14 26.6 13.4 29M18 26.6l.6 2.4"/></g>
<path d="M14.2 6.4h3.6l.8 3.4h-5.2z" fill="#C79A6C"/>
<ellipse cx="16" cy="17.4" rx="7" ry="9.2" fill="url(#m1)"/>
<path d="M11 14.6c3.2 1 6.8 1 10 0" stroke="#B58658" stroke-opacity=".6" stroke-width=".6"/>
<ellipse cx="13.6" cy="13.4" rx="2.4" ry="1.4" fill="#fff" fill-opacity=".6" transform="rotate(-25 13.6 13.4)"/>''')

# Оса — тонкая талия, полосатое брюшко
CUSTOM["wasp"] = wrap(f'''
<defs>
<linearGradient id="w1" x1="11" y1="18" x2="21" y2="18" gradientUnits="userSpaceOnUse"><stop stop-color="#F2A900"/><stop offset=".5" stop-color="#FFD43B"/><stop offset="1" stop-color="#E39A00"/></linearGradient>
<linearGradient id="w2" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#DDF0FF" stop-opacity=".95"/><stop offset="1" stop-color="#9CC8EC" stop-opacity=".55"/></linearGradient>
<radialGradient id="w3" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="matrix(0 3.2 -3.6 0 16 11)"><stop stop-color="#4A4040"/><stop offset="1" stop-color="#151010"/></radialGradient>
</defs>
<path d="M14.6 10.6C10 5 3.4 4.8 2.6 7.6c-.8 3 4.6 5.4 11.4 5.2z" fill="url(#w2)"/>
<path d="M17.4 10.6C22 5 28.6 4.8 29.4 7.6c.8 3-4.6 5.4-11.4 5.2z" fill="url(#w2)"/>
<path d="M14.6 11.6c-3.6-1.8-7.6-1.4-8.4.2-.6 1.6 3.4 2.6 8.4 1.6zM17.4 11.6c3.6-1.8 7.6-1.4 8.4.2.6 1.6-3.4 2.6-8.4 1.6z" fill="url(#w2)"/>
<g stroke="#1E1714" stroke-width="1" {LEG}><path d="M13.6 12.8 10.4 15.4 9.2 18.6"/><path d="M18.4 12.8l3.2 2.6 1.2 3.2"/><path d="M14 14.2 11.8 18.8 12 22.4"/><path d="M18 14.2l2.2 4.6-.2 3.6"/><path d="M14.8 4.4 13 1.8M17.2 4.4 19 1.8" stroke-width=".85"/></g>
<ellipse cx="16" cy="5.8" rx="2.6" ry="2.4" fill="#F5B800"/>
<ellipse cx="14.4" cy="5.4" rx="1" ry="1.5" fill="#1A1212"/><ellipse cx="17.6" cy="5.4" rx="1" ry="1.5" fill="#1A1212"/>
<ellipse cx="16" cy="10.8" rx="3.4" ry="3.2" fill="url(#w3)"/>
<path d="M14.2 9.4c.8-.6 2.8-.6 3.6 0" stroke="#F5C400" stroke-width=".8" stroke-linecap="round"/>
<rect x="15.3" y="13.6" width="1.4" height="2.2" rx=".6" fill="#1A1212"/>
<path d="M16 15.2c3.6 0 5.2 3.4 5.2 6.6 0 4.2-2.8 7.4-5.2 8.6-2.4-1.2-5.2-4.4-5.2-8.6 0-3.2 1.6-6.6 5.2-6.6z" fill="url(#w1)"/>
<g fill="#1A1212"><path d="M11 20.2c3.2 1.1 6.8 1.1 10 0l.1 1.8c-3.3 1.1-6.9 1.1-10.2 0z"/><path d="M11.4 24.4c3 1 6.2 1 9.2 0l-.5 1.8c-2.8.9-5.4.9-8.2 0z"/><path d="M13.2 28.2c1.8.6 3.8.6 5.6 0L16 30.6z"/></g>
<ellipse cx="14" cy="18.2" rx="1.2" ry="2" fill="#fff" fill-opacity=".35"/>''')

# Платяная моль — пыльные бежевые крылья
CUSTOM["moth"] = wrap(f'''
<defs>
<linearGradient id="o1" x1="5" y1="6" x2="15" y2="22" gradientUnits="userSpaceOnUse"><stop stop-color="#E7D3AE"/><stop offset=".6" stop-color="#C4A577"/><stop offset="1" stop-color="#8F7149"/></linearGradient>
<linearGradient id="o2" x1="27" y1="6" x2="17" y2="22" gradientUnits="userSpaceOnUse"><stop stop-color="#E7D3AE"/><stop offset=".6" stop-color="#C4A577"/><stop offset="1" stop-color="#8F7149"/></linearGradient>
<linearGradient id="o3" x1="16" y1="8" x2="16" y2="27" gradientUnits="userSpaceOnUse"><stop stop-color="#A88A60"/><stop offset="1" stop-color="#6E5636"/></linearGradient>
</defs>
<path d="M15 12.4 3.6 8.2C1.6 8 1.2 12 2.8 16.4c1.6 4.4 5.6 9.2 12.2 8.4z" fill="url(#o1)"/>
<path d="M17 12.4l11.4-4.2c2-.2 2.4 3.8.8 8.2-1.6 4.4-5.6 9.2-12.2 8.4z" fill="url(#o2)"/>
<g fill="#7C5F3B" fill-opacity=".55"><circle cx="8" cy="13.4" r="1.1"/><circle cx="10.8" cy="18" r=".8"/><circle cx="24" cy="13.4" r="1.1"/><circle cx="21.2" cy="18" r=".8"/></g>
<g stroke="#8B6E47" stroke-opacity=".5" stroke-width=".5" fill="none"><path d="M14.6 13.6 4.4 10.4M14.6 16.4 5.2 18.6M14.6 19.4 8.6 23.4M17.4 13.6l10.2-3.2M17.4 16.4l9.4 2.2M17.4 19.4l6 4"/></g>
<path d="M3.2 9.4c1.6-.3 6 1.2 9.6 2.6" stroke="#fff" stroke-opacity=".45" stroke-width=".8" stroke-linecap="round"/>
<path d="M28.8 9.4c-1.6-.3-6 1.2-9.6 2.6" stroke="#fff" stroke-opacity=".45" stroke-width=".8" stroke-linecap="round"/>
<g stroke="#6E5636" stroke-width=".9" {LEG}><path d="M15.2 8.8C13.4 6 11.2 4.4 8.6 4"/><path d="M16.8 8.8C18.6 6 20.8 4.4 23.4 4"/></g>
<g stroke="#6E5636" stroke-width=".45" stroke-linecap="round"><path d="M12.6 5.6l.2-1.2M11 4.9l.1-1.2M14 6.8l.4-1M19.4 5.6l-.2-1.2M21 4.9l-.1-1.2M18 6.8l-.4-1"/></g>
<ellipse cx="16" cy="9.4" rx="1.9" ry="1.7" fill="#9C7E55"/>
<rect x="14.4" y="10.4" width="3.2" height="16.4" rx="1.6" fill="url(#o3)"/>
<g stroke="#5A452A" stroke-opacity=".5" stroke-width=".45"><path d="M14.6 16h2.8M14.6 18.6h2.8M14.6 21.2h2.8M14.6 23.8h2.8"/></g>''')

# Мокрица — серые панцирные сегменты
CUSTOM["woodlouse"] = wrap(f'''
<defs>
<linearGradient id="l1" x1="8" y1="16" x2="24" y2="16" gradientUnits="userSpaceOnUse"><stop stop-color="#5C6670"/><stop offset=".45" stop-color="#9AA6B1"/><stop offset="1" stop-color="#4A535C"/></linearGradient>
</defs>
<g stroke="#3B4148" stroke-width=".95" {LEG}>
<path d="M9.4 10.4 6.6 9M8.6 13.6 5.4 13M8.2 16.8H5M8.2 20l-3 .8M8.8 23.2 6 24.6"/>
<path d="M22.6 10.4 25.4 9M23.4 13.6l3.2-.6M23.8 16.8H27M23.8 20l3 .8M23.2 23.2l2.8 1.4"/>
<path d="M14.4 4.6 12.2 1.8 10 1.6M17.6 4.6l2.2-2.8 2.2-.2" stroke-width=".8"/>
</g>
<path d="M16 4.2c5.6 0 8.2 4.6 8.2 12.6 0 7.4-3.6 12.4-8.2 12.4s-8.2-5-8.2-12.4c0-8 2.6-12.6 8.2-12.6z" fill="url(#l1)"/>
<g stroke="#2F353B" stroke-opacity=".7" stroke-width=".7" fill="none">
<path d="M9.6 8.8c4.2 1.2 8.6 1.2 12.8 0"/><path d="M8.6 12c4.8 1.4 10 1.4 14.8 0"/><path d="M8.1 15.3c5.2 1.5 10.6 1.5 15.8 0"/><path d="M8 18.6c5.3 1.5 10.7 1.5 16 0"/><path d="M8.3 21.8c5 1.4 10.4 1.4 15.4 0"/><path d="M9.2 24.8c4.4 1.2 9.2 1.2 13.6 0"/>
</g>
<path d="M13 9.6c.4 4.4.4 10.8-.2 15.4" stroke="#fff" stroke-opacity=".28" stroke-width="1.4" stroke-linecap="round"/>''')
