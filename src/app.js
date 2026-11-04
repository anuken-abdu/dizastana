(function () {
  "use strict";
  var KB = /*__KB__*/{};
  var CFG = window.CFG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function waUrl(t) { return "https://wa.me/" + CFG.wan + "?text=" + encodeURIComponent(t); }

  /* ---------- конверсии Google Ads / GA4 ---------- */
  function conv(kind) {
    if (typeof window.gtag !== "function") return;
    var label = kind === "call" ? CFG.call : CFG.wa;
    if (CFG.ads && label) window.gtag("event", "conversion", { send_to: CFG.ads + "/" + label, value: 1.0, currency: "USD", transport_type: "beacon" });
    if (CFG.ga) window.gtag("event", kind === "call" ? "phone_click" : "whatsapp_click", { page_path: location.pathname, transport_type: "beacon" });
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;
    var h = a.getAttribute("href") || "";
    if (h.indexOf("tel:") === 0) conv("call");
    else if (h.indexOf("wa.me") > -1) conv("wa");
  });

  /* ---------- меню ---------- */
  var burger = $(".burger"), nav = $("#nav");
  function setNav(o) {
    if (!burger || !nav) return;
    nav.classList.toggle("open", o); burger.setAttribute("aria-expanded", o ? "true" : "false");
    burger.setAttribute("aria-label", o ? "Закрыть меню" : "Открыть меню"); document.body.classList.toggle("lock", o);
  }
  if (burger) burger.addEventListener("click", function () { setNav(!nav.classList.contains("open")); });
  if (nav) nav.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
  window.addEventListener("resize", function () { if (window.innerWidth > 1180) setNav(false); });

  /* ---------- назад / наверх ---------- */
  var fab = $(".fab");
  var ftr = $(".ftr");
  function onScroll() {
    if (fab) fab.classList.toggle("on", window.pageYOffset > 500);
    // у самого низа страницы плавающие кнопки становятся полупрозрачными, чтобы не закрывать подвал
    var end = ftr ? ftr.getBoundingClientRect().top < window.innerHeight - 40 : false;
    document.body.classList.toggle("at-end", end);
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  $$("[data-top]").forEach(function (b) { b.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); }); });
  $$("[data-back]").forEach(function (b) {
    b.addEventListener("click", function () {
      var ref = document.referrer, same = ref && ref.indexOf(location.host) > -1;
      if (same && history.length > 1) history.back(); else location.href = "/";
    });
  });

  /* ---------- заявка → WhatsApp ---------- */
  $$("form[data-lead]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var ph = (f.elements.phone.value || "").replace(/[^\d+]/g, ""), err = $(".f-err", f);
      if (ph.replace(/\D/g, "").length < 10) { err.hidden = false; f.elements.phone.focus(); return; }
      err.hidden = true;
      var t = "Здравствуйте! Заявка с сайта.\nПроблема: " + f.elements.pest.value + "\nРайон: " + f.elements.area.value +
        (f.elements.msg.value.trim() ? "\nОбъект: " + f.elements.msg.value.trim() : "") +
        (f.elements.name.value.trim() ? "\nИмя: " + f.elements.name.value.trim() : "") + "\nТелефон: " + ph;
      conv("wa");
      window.open(waUrl(t), "_blank", "noopener");
    });
  });

  /* ---------- чат: ИИ через /api/chat, без ключа — встроенный автоответчик ---------- */
  var chat = $("#chat"), list = chat && $(".chat-l", chat), qbox = chat && $(".chat-q", chat), opener = $(".chat-o");
  var hist = [], started = false, busy = false;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function add(text, who, html) {
    var d = document.createElement("div"); d.className = "msg " + (who === "u" ? "msg-u" : "msg-b");
    if (html) d.innerHTML = html; else d.textContent = text;
    list.appendChild(d); list.scrollTop = list.scrollHeight; return d;
  }
  function quick(items) {
    qbox.innerHTML = "";
    items.forEach(function (q) { var b = document.createElement("button"); b.type = "button"; b.textContent = q; b.addEventListener("click", function () { ask(q); }); qbox.appendChild(b); });
  }
  function low(s) { return s.toLowerCase().replace(/ё/g, "е"); }
  // встроенный автоответчик: работает без ИИ-ключа и при сбое сети
  var INTENTS = [
    [/цен|стоим|сколько стоит|прайс|почем|по чем|тариф|сколько будет|дорого/, "Стоимость зависит от вредителя и степени заселения, площади и типа объекта, метода и препарата, нужна ли повторная обработка. Напишите, кто беспокоит и площадь, — специалист назовёт цену до выезда.", "/stoimost/"],
    [/дет|ребен|ребён|малыш|беремен|животн|кошк|собак|питом|попуга|аквариум|рыб|безопас|вредно|аллерг|запах после/, "На время обработки и проветривания из помещения выводят людей и животных, аквариум накрывают и выключают компрессор. Когда можно возвращаться и как проветрить, специалист скажет по препарату, которым обрабатывали. Обязательно предупредите при заявке о детях, беременных, аллергиках и питомцах.", "/stati/kak-podgotovit-kvartiru-k-obrabotke/"],
    [/подготов|что убрать|что делать до|перед обработ|собрать вещ|посуд/, "Перед обработкой уберите продукты и посуду, отодвиньте мебель от стен, освободите доступ к плинтусам и щелям, выведите людей и питомцев. Подробный список — по ссылке.", "/stati/kak-podgotovit-kvartiru-k-obrabotke/"],
    [/после обработ|когда убир|мыть пол|сколько не|вернуться|проветр/, "После обработки помещение проветривают, а влажную уборку делают через срок, который назовёт специалист: слишком ранняя уборка смывает защитный слой. Плинтусы и щели обычно не моют дольше."],
    [/повтор|снова появ|опять|вернулись|не помогл|сколько раз|гаранти/, "Если вредители ещё появляются после обработки, часто нужна повторная — так бывает с клопами и тараканами из-за яиц, на которые препараты действуют хуже. Нужна ли повторная и на каких условиях, специалист скажет по результату осмотра."],
    [/юр\.|юрлиц|юридич|компан|тоо|(^|\s)ип(\s|$)|организац|договор|акт|ндс|счет|счёт|санпин|сэс|проверк|журнал|ежемесяч|абонент/, "Для бизнеса — разовые и регулярные обработки кафе, магазинов, складов, офисов и производств. По договору, актам и документам для проверок подскажет менеджер.", "/uslugi/dlya-biznesa/"],
    [/оплат|налич|безнал|kaspi|каспи|перевод/, "Способ оплаты уточнит менеджер при заявке."],
    [/район|адрес|выезд|приед|куда|левый берег|правый берег|пригород|косшы|коянды|талапкер/, "Выезжаем по всем районам Астаны: Алматинский, Байконыр, Есиль, Нура, Сарыарка, Сарайшык, а также в Косшы, Коянды и Талапкер.", "/rayony/"],
    [/срочн|сегодня|завтра|как быстро|когда можете|выходн|вечер|ночь/, "Время выезда согласуем по телефону или в WhatsApp — напишите адрес и удобное время."],
    [/холодн|горяч|туман|генератор/, "Холодный туман — мелкодисперсная обработка, хорошо проникает в щели; горячий туман — ещё более мелкие частицы, применяют при сильном заселении и в больших помещениях. Метод специалист выбирает по вредителю и объекту."],
    [/препарат|химия|средств|чем обрабат|ядовит/, "Применяются профессиональные препараты, разрешённые к использованию; какой выбрать, решает специалист по вредителю, объекту и наличию детей и животных."],
    [/умерш|умер|трупн|после смерти|покойн|морг/, "Дезинфекция после умершего: обеззараживание поверхностей, устранение трупного запаха, при необходимости — озонирование.", "/uslugi/dezinfekciya-posle-umershego/"],
    [/плесен|грибок|грибк|черн.{0,6}(угл|стен)|откос/, "Обработка от плесени и грибка: удаление налёта, фунгицидная обработка поверхностей. Без устранения причины — сырости, промерзания, плохой вентиляции — плесень может вернуться.", "/uslugi/ot-pleseni-i-griba/"],
    [/озон/, "Озонирование устраняет запахи и обеззараживает воздух и поверхности. Во время работы озонатора в помещении не должно быть людей, животных и растений.", "/uslugi/ozonirovanie/"],
    [/запах|вонь|воня|дым|гар|табак|кошач/, "Устранение запахов: табака, гари, кошачьих меток, сырости, трупного запаха — дезодорация и озонирование.", "/uslugi/dezodoraciya/"],
    [/вирус|бактер|ковид|covid|инфекц|санобработ|дезинфекц/, "Дезинфекция помещений от вирусов и бактерий — квартиры, офисы, детские и медицинские учреждения, после болезни.", "/uslugi/dezinfekciya/"],
    [/участ|газон|дач|двор|акарицид|клещ.{0,10}(трав|сад|участ)/, "Акарицидная обработка участков от клещей — сад, газон, территория детских лагерей и баз отдыха.", "/uslugi/akaricidnaya-obrabotka/"],
    [/грызун|дератиз/, "Дератизация — уничтожение крыс и мышей в домах, подвалах, складах и на предприятиях.", "/uslugi/deratizaciya/"],
    [/насеком|дезинсек/, "Дезинсекция — уничтожение тараканов, клопов, блох, муравьёв, моли, комаров, пауков и других насекомых.", "/uslugi/dezinsekciya/"],
    [/(^|\s)бот|робот|ты кто|живой|человек|оператор/, "Я онлайн-консультант сайта. Живой специалист ответит по телефону или в WhatsApp — кнопка ниже."],
    [/спасиб|рахмет|благодар/, "Пожалуйста! Оставьте номер или напишите в WhatsApp — специалист свяжется."],
    [/привет|здравств|салем|сәлем|добрый|ассалам/, "Здравствуйте! Подскажу по дезинсекции, дератизации и дезинфекции в Астане. Кто беспокоит и какой у вас объект?"]
  ];
  // ключи для распознавания вредителей (основы слов)
  var PKEY = { tarakany: "таракан|прусак", klopy: "^(?!.*щитн).*клоп", blohi: "блох", muravi: "муравь|муравей", mol: "(^|\\s)мол[ьи]|моль", mokricy: "мокриц", cheshuynicy: "чешуйниц|серебрянк", osy: "(^|\\s)ос(ы|а|иное|иного|ин)|шершн|пчел|(^|\\s)ро[йя]", kleshchi: "^(?!.*пыл).*клещ", "pylevye-kleshchi": "пылев", krysy: "крыс", myshi: "(^|\\s)мыш|мыши", muhi: "(^|\\s)мух|мошк", komary: "комар", pauki: "паук|паутин", vshi: "(^|\\s)вш|гнид|педикул", drevotochcy: "древоточ|короед|жук", shchitniki: "щитник|вонюч" };
  function local(q) {
    var s = low(q);
    if (s.replace(/\D/g, "").length >= 10) return { t: "Спасибо! Чтобы заявка точно дошла, отправьте номер специалисту в WhatsApp кнопкой ниже." };
    var ps = KB.pests || [];
    var pr = /цен|стоим|сколько|почем|прайс/.test(s);
    for (var i = 0; i < ps.length; i++) {
      var key = PKEY[ps[i][3]]; if (!key || !new RegExp(key).test(s)) continue;
      if (pr) return { t: "Цена обработки от " + ps[i][1] + " зависит от площади, степени заселения и метода. Напишите площадь и район — специалист назовёт стоимость.", u: ps[i][2] };
      return { t: "Да, выполняем обработку от " + ps[i][1] + " в Астане. Специалист уточнит объект и площадь, подберёт метод и препарат. Подробно — на странице.", u: ps[i][2] };
    }
    var ds = KB.districts || [];
    for (var j = 0; j < ds.length; j++) {
      var n = low(ds[j][0]).slice(0, Math.max(4, ds[j][0].length - 2));
      if (s.indexOf(n) > -1) return { t: "Да, выезжаем " + ds[j][1] + ". Кто беспокоит и какой объект?", u: ds[j][2] };
    }
    for (var k = 0; k < INTENTS.length; k++) if (INTENTS[k][0].test(s)) return { t: INTENTS[k][1], u: INTENTS[k][2] };
    return { t: "Уточню у специалиста. Напишите, кто беспокоит, тип объекта и район — или позвоните " + KB.phone + "." };
  }
  function reply(r) {
    var h = esc(r.t) + (r.u ? '<br><a href="' + r.u + '">Открыть страницу</a>' : "");
    add("", "b", h);
  }
  function ask(q) {
    q = String(q || "").trim(); if (!q || busy) return;
    add(q, "u"); hist.push({ role: "user", content: q });
    busy = true; var wait = add("…", "b");
    var done = function (txt) { busy = false; wait.remove(); hist.push({ role: "assistant", content: txt }); add(txt, "b"); };
    var ctrl = window.AbortController ? new AbortController() : null; var to = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);
    fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages: hist.slice(-12), page: location.pathname }), signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { clearTimeout(to); if (!r.ok) throw 0; return r.json(); })
      .then(function (d) { if (!d || !d.text) throw 0; done(d.text); })
      .catch(function () { busy = false; wait.remove(); var r = local(q); hist.push({ role: "assistant", content: r.t }); reply(r); if (qbox) qbox.innerHTML = ""; });
  }
  function openChat() {
    chat.hidden = false; if (opener) opener.hidden = true;
    if (!started) { started = true; add("Здравствуйте! Я ИИ-консультант DizAstana. Подскажу по обработке от насекомых, грызунов, плесени и запахов, по подготовке и безопасности. Кто беспокоит?", "b"); quick(["Сколько стоит?", "Клопы в квартире", "Тараканы", "Безопасно для детей?", "Как подготовиться?", "Для бизнеса"]); }
    setTimeout(function () { var i = $("input", chat); if (i && window.innerWidth > 767) i.focus(); }, 50);
  }
  if (chat) {
    $$("[data-chat]").forEach(function (b) { b.addEventListener("click", openChat); });
    $("[data-chat-x]", chat).addEventListener("click", function () { chat.hidden = true; if (opener) opener.hidden = false; });
    $(".chat-f", chat).addEventListener("submit", function (e) { e.preventDefault(); var i = this.elements.q; ask(i.value); i.value = ""; });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (chat && !chat.hidden) { chat.hidden = true; if (opener) opener.hidden = false; }
    setNav(false);
  });
})();
