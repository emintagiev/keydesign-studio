#!/usr/bin/env python3
"""Тексты для страниц услуг, раздела статей и описаний проектов (RU + EN).

Единый источник: из этого файла берут русский текст генераторы страниц,
а ключи для переключателя языка попадают в app.js (см. patch-i18n.py).
"""

from __future__ import annotations

COST_DESIGN_RU = "Стоимость считаем за квадратный метр и называем после первого разговора о проекте."
COST_OTHER_RU = "Стоимость называем после первого разговора о проекте."

RU = {
    "nav.guides": "Статьи",
    "svc.all": "Все услуги",
    "svc.how": "Как проходит работа",
    "svc.examples": "Примеры проектов",
    "svc.faqTitle": "Вопросы и ответы",
    "svc.others": "Другие услуги",
    "svc.cost.1": COST_DESIGN_RU,
    "svc.cost.n": COST_OTHER_RU,
    "svc.1.faq.1.q": "Что входит в дизайн-проект?",
    "svc.1.faq.1.a": "Техническое задание, обмеры и фотофиксация, планировочное решение, 3D-визуализация и рабочий проект: чертежи и спецификации, по которым строители и поставщики реализуют проект без догадок.",
    "svc.1.faq.2.q": "Сколько занимает разработка проекта?",
    "svc.1.faq.2.a": "Срок разработки - от двух месяцев, в зависимости от площади и сложности объекта.",
    "svc.1.faq.3.q": "Сколько стоит дизайн-проект?",
    "svc.1.faq.3.a": COST_DESIGN_RU,
    "svc.2.faq.1.q": "Что такое проектное сопровождение?",
    "svc.2.faq.1.a": "Ведём проект как единую систему: координируем поставщиков и подрядчиков, помогаем с комплектацией, выстраиваем бюджет и контролируем сроки поставок.",
    "svc.2.faq.2.q": "Как проходит комплектация?",
    "svc.2.faq.2.a": "Формируем карту материалов, считаем смету и сроки по спецификациям проекта, согласовываем бюджет и связываем платежи с этапами строительства. Закупку и логистику ведём от проверки коммерческих предложений до доставки и монтажа на объекте.",
    "svc.2.faq.3.q": "Как выстраивается бюджет?",
    "svc.2.faq.3.a": "Считаем стоимость материалов, мебели и наполнения по спецификациям проекта, согласовываем финальную смету и фиксируем приоритеты закупок.",
    "svc.3.faq.1.q": "Что делает дизайнер на объекте?",
    "svc.3.faq.1.a": "Приезжаем на площадку и сверяем ход работ с проектом, отвечаем на вопросы бригады, проверяем соответствие узлов, материалов и геометрии рабочим чертежам.",
    "svc.3.faq.2.q": "Что, если на объекте что-то меняется?",
    "svc.3.faq.2.a": "Оперативно обновляем чертежи, если на объекте появляются уточнения, и согласуем работу инженеров, мебельщиков, декораторов и других специалистов.",
    "svc.3.faq.3.q": "Как я узнаю, как идут работы?",
    "svc.3.faq.3.a": "Еженедельно фиксируем статус работ и принятые решения для прозрачности процесса.",
    "svc.4.faq.1.q": "Что такое архитектурное планирование?",
    "svc.4.faq.1.a": "Проектируем логику пространства до деталей отделки: перепланировки, зонирование, инженерные вводные и связь интерьера с архитектурой здания.",
    "svc.4.faq.2.q": "Что вы изучаете перед планированием?",
    "svc.4.faq.2.a": "Планировку, инсоляцию, инженерные стояки и ограничения застройщика или БТИ.",
    "svc.4.faq.3.q": "Что я получу в итоге?",
    "svc.4.faq.3.a": "Варианты перепланировки с расстановкой мебели и привязкой инженерии. Утверждённую планировку передаём в этап проработки материалов, света и деталей интерьера.",
    "proj.service.label": "Услуга:",
    "proj.service.name": "дизайн-проект интерьера",
    "guides.title": "Статьи",
    "guides.soon": "Первые статьи скоро появятся",
    "guides.back": "Все статьи",
    "guides.project": "Как это было в проекте",
    "guides.service": "Услуга",
    "guides.faq": "Вопросы и ответы",
    "guides.related": "Читайте также",
    "guides.cta": "Расскажите метраж и когда планируете начать — заявка на сайте.",
}

EN = {
    "nav.guides": "Guides",
    "svc.all": "All services",
    "svc.how": "How we work",
    "svc.examples": "Project examples",
    "svc.faqTitle": "Questions and answers",
    "svc.others": "Other services",
    "svc.cost.1": "We price per square metre and quote the cost after a first conversation about your project.",
    "svc.cost.n": "We quote the cost after a first conversation about your project.",
    "svc.1.faq.1.q": "What does the design project include?",
    "svc.1.faq.1.a": "A design brief, site survey and photo documentation, a layout solution, 3D visualisation and working drawings: drawings and specifications that builders and suppliers can follow without guesswork.",
    "svc.1.faq.2.q": "How long does the design take?",
    "svc.1.faq.2.a": "From two months, depending on the size and complexity of the project.",
    "svc.1.faq.3.q": "How much does a design project cost?",
    "svc.1.faq.3.a": "We price per square metre and quote the cost after a first conversation about your project.",
    "svc.2.faq.1.q": "What is project support?",
    "svc.2.faq.1.a": "We run the project as a single system: we coordinate suppliers and contractors, help with sourcing, build the budget and keep an eye on delivery times.",
    "svc.2.faq.2.q": "How does sourcing work?",
    "svc.2.faq.2.a": "We prepare a materials map, calculate the estimate and timing from the project specifications, agree the budget and tie payments to the stages of construction. We manage purchasing and logistics from checking quotations to delivery and installation on site.",
    "svc.2.faq.3.q": "How is the budget built?",
    "svc.2.faq.3.a": "We calculate the cost of materials, furniture and furnishings from the project specifications, agree the final estimate and fix purchasing priorities.",
    "svc.3.faq.1.q": "What does the designer do on site?",
    "svc.3.faq.1.a": "We visit the site and compare the progress of the work with the project, answer the crew's questions and check that details, materials and geometry match the working drawings.",
    "svc.3.faq.2.q": "What if something changes on site?",
    "svc.3.faq.2.a": "We promptly update the drawings when clarifications arise on site and coordinate the work of engineers, furniture makers, decorators and other specialists.",
    "svc.3.faq.3.q": "How will I know how the work is going?",
    "svc.3.faq.3.a": "Every week we record the status of the work and the decisions made, so the process stays transparent.",
    "svc.4.faq.1.q": "What is architectural planning?",
    "svc.4.faq.1.a": "We design the logic of the space down to finishing details: layout changes, zoning, engineering inputs and the link between the interior and the building's architecture.",
    "svc.4.faq.2.q": "What do you study before planning?",
    "svc.4.faq.2.a": "The layout, sunlight, engineering risers and the constraints set by the developer or the technical inventory bureau (BTI).",
    "svc.4.faq.3.q": "What will I get in the end?",
    "svc.4.faq.3.a": "Layout options with furniture placement and engineering connections. The approved layout goes on to the stage where materials, lighting and interior details are worked out.",
    "proj.service.label": "Service:",
    "proj.service.name": "interior design project",
    "guides.title": "Guides",
    "guides.soon": "The first guides are coming soon",
    "guides.back": "All guides",
    "guides.project": "How it went in the project",
    "guides.service": "Service",
    "guides.faq": "Questions and answers",
    "guides.related": "Read next",
    "guides.cta": "Tell us the size of your space and when you plan to start — send a request on the site.",
}

# Описание проекта: факты только из опубликованных названий и списков комнат.
SUMMARY_HEAD_RU = {
    "moscow-studio": "Дизайн студии 30 м² в ЖК Bauman Haus, Москва.",
    "kvartira-dubay": "Дизайн апартаментов 120 м², Дубай.",
    "zhk-arkhitektor": "Дизайн квартиры 60 м² в ЖК Архитектор, Москва.",
    "oblaka-orhan": "Дизайн квартиры 80 м² в ЖК Облака, Новосибирск.",
    "salon-krasoty-tati": "Дизайн салона красоты Tati, 90 м², Новосибирск.",
    "laki-park-dom": "Дизайн дома 108 м² в Лаки Парк, Новосибирск.",
    "ns-akadem-pulsar": "Дизайн квартиры 62 м² в ЖК Пульсар, Новосибирск.",
    "kvartal-dekabristov": "Дизайн квартиры 140 м² в ЖК Квартал Декабристов, Новосибирск.",
    "nevskaya-dom": "Дизайн загородного дома 160 м², Новосибирск.",
    "vostochny-vayb": "Дизайн квартиры с восточным вайбом, 48 м², Новосибирск.",
    "kedrovy-ns": "Дизайн квартиры 120 м² в ЖК Кедровый, Новосибирск.",
    "dom-sinegore": "Дизайн загородного дома 300 м², Новосибирск.",
    "kabinet-morozovo": "Дизайн кабинета-оружейной 25 м² в загородном доме, с. Морозово.",
    "little-classic": "Дизайн квартиры 48 м² в ЖК Европейский берег, Новосибирск.",
}

SUMMARY_HEAD_EN = {
    "moscow-studio": "Interior design of a 30 sq m studio at Bauman Haus RC, Moscow.",
    "kvartira-dubay": "Interior design of a 120 sq m apartment, Dubai.",
    "zhk-arkhitektor": "Interior design of a 60 sq m apartment at ZHK Arkhitektor, Moscow.",
    "oblaka-orhan": "Interior design of an 80 sq m apartment at Oblaka Residence, Novosibirsk.",
    "salon-krasoty-tati": "Interior design of the Tati beauty salon, 90 sq m, Novosibirsk.",
    "laki-park-dom": "Interior design of a 108 sq m house in Laki Park, Novosibirsk.",
    "ns-akadem-pulsar": "Interior design of a 62 sq m apartment at ZHK Pulsar, Novosibirsk.",
    "kvartal-dekabristov": "Interior design of a 140 sq m apartment at ZHK Dekabristov Quarter, Novosibirsk.",
    "nevskaya-dom": "Interior design of a 160 sq m country house, Novosibirsk.",
    "vostochny-vayb": "Interior design of a 48 sq m apartment with an eastern vibe, Novosibirsk.",
    "kedrovy-ns": "Interior design of a 120 sq m apartment at ZHK Kedrovy, Novosibirsk.",
    "dom-sinegore": "Interior design of a 300 sq m country house, Novosibirsk.",
    "kabinet-morozovo": "Interior design of a 25 sq m gun-room study in a country house, Morozovo.",
    "little-classic": "Interior design of a 48 sq m apartment at ZHK Evropeysky bereg, Novosibirsk.",
}

ROOMS_EN = {
    "Кухня-гостиная": "kitchen and living room",
    "Гостиная-кухня": "living room and kitchen",
    "Спальня": "bedroom",
    "Спальня 1": "bedroom 1",
    "Спальня 2": "bedroom 2",
    "Спальня Серафима": "Serafim's bedroom",
    "Гостевая спальня": "guest bedroom",
    "Мастер-спальня": "master bedroom",
    "Прихожая": "entry hall",
    "Мастер-санузел": "master bathroom",
    "Гостевой санузел": "guest bathroom",
    "Зеленый санузел": "green bathroom",
    "Розовый санузел": "pink bathroom",
    "Санузел": "bathroom",
    "Санузел 1": "bathroom 1",
    "Санузел 2": "bathroom 2",
    "Ванная": "bathroom",
    "Ванная комната": "bathroom",
    "Душевая": "shower room",
    "Детская": "children's room",
    "Детская комната": "children's room",
    "Детская девочки": "girl's room",
    "Кабинет": "study",
    "Мастер-гардеробная": "master dressing room",
}

GENERIC_ROOMS = {"Интерьер", "Фотографии"}


def _lower_first(text: str) -> str:
    return text[:1].lower() + text[1:] if text else text


def summary_ru(slug: str, rooms: list[str]) -> str:
    head = SUMMARY_HEAD_RU[slug]
    names = [r for r in rooms if r not in GENERIC_ROOMS]
    if not names:
        return head
    return f"{head} В проекте: {', '.join(_lower_first(n) for n in names)}."


def summary_en(slug: str, rooms: list[str]) -> str:
    head = SUMMARY_HEAD_EN[slug]
    names = [r for r in rooms if r not in GENERIC_ROOMS]
    if not names:
        return head
    return f"{head} Rooms: {', '.join(ROOMS_EN.get(n, n) for n in names)}."
