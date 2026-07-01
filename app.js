    (function () {
      "use strict";

      document.documentElement.classList.add("js");

      var root = document.documentElement;

  /* ---------- i18n (RU default, EN ready) ---------- */
      var i18n = {
        ru: {
          "brand.tag": "Студия интерьерного дизайна",
          "nav.about": "О студии",
          "nav.projects": "Проекты",
          "nav.services": "Услуги",
          "nav.approach": "Подход",
          "nav.partners": "Партнёры",
          "nav.contact": "Контакты",
          "nav.home": "На главную",
          "hero.eyebrow": "Москва - Санкт-Петербург",
          "hero.tagline":
            "Создаём продуманные интерьеры, в которых выверены свет, материал и каждая деталь.",
          "hero.cta": "Смотреть проекты",
          "hero.secondary": "Обсудить проект",
          "hero.media": "Скоро - съёмка проектов",
          "hero.stat1": "лет практики",
          "hero.stat2": "реализованных интерьеров",
          "hero.stat3": "города присутствия",
          "hero.scroll": "Проекты",
          "about.label": "О студии",
          "about.p1":
            "Всё началось с искренней любви к пространству и желания создавать то, что остаётся с людьми надолго.",
          "about.p2":
            "Первые проекты, первые ошибки, первые клиенты, которые доверились. Годы практики в разных условиях и форматах - от небольших квартир до сложных объектов - сформировали не просто насмотренность, а собственный язык. Язык, в котором каждая деталь оправдана, каждое решение - осознанно.",
          "about.p3":
            "Сегодня Key-Design - это авторское бюро с чётким видением: архитектурная выверенность, живые материалы и точный баланс формы и тепла. Пространства, которые не кричат о себе, но остаются в памяти.",
          "about.p4":
            "Хороший интерьер - это не про красивые фотографии. Это про то, как вы себя чувствуете в пространстве каждый день. Именно это мы проектируем.",
          "about.role": "основатель и ведущий дизайнер",
          "projects.label": "Проекты",
          "projects.all": "Все проекты",
          "projects.featured": "Избранный проект",
          "project.link": "Смотреть проект",
          "project.1.cat": "Частный дом · Москва · 2025",
          "project.1.name": "Dream House",
          "project.1.desc":
            "Частный дом в тёплой нейтральной палитре: натуральное дерево, мягкие фактуры и выверенный свет - от кухни-гостиной до приватных зон.",
          "project.2.cat": "Квартира · Москва · 2025",
          "project.2.name": "ЖК Пульсар",
          "project.2.desc":
            "Квартира в современном жилом комплексе: светлая палитра, функциональное зонирование и продуманные детали.",
          "project.3.cat": "Студия · Москва · 2025",
          "project.3.name": "Москва Студия",
          "project.3.desc":
            "Компактная студия с выверенной планировкой: каждый метр работает на комфорт, свет и ощущение простора.",
          "project.4.cat": "Салок красоты tati · 2026",
          "project.4.name": "Салок красоты tati",
          "project.4.desc":
            "Интерьер салона красоты tati - мягкий свет, спокойная палитра и продуманная эргономика.",
          "project.5.cat": "Частный дом · Новосибирск · 2025",
          "project.5.name": "г. Новосибирск, Лаки Парк, Дом",
          "project.5.desc": "",
          "project.6.cat": "Квартира · Москва · 2025",
          "project.6.name": "г. Москва, ЖК Архитектор",
          "project.6.desc": "",
          "project.7.cat": "Жилой комплекс · Новосибирск · 2025",
          "project.7.name": "Новосибирск, Академгородок, Жк Пульсар 1",
          "project.7.desc": "",
          "project.8.cat": "Квартира · Новосибирск · 2025",
          "project.8.name": "г. Новосибирск, Квартал Декабристов",
          "project.8.desc": "",
          "project.9.cat": "Частный дом · Новосибирск · 2025",
          "project.9.name": "г. Новосибирск, ул. Невская дом",
          "project.9.desc": "",
          "project.10.cat": "Квартира · Новосибирск · 2025",
          "project.10.name": "г. Новосибирск, Квартира с Восточным вайбом",
          "project.10.desc": "",
          "project.11.cat": "Квартира · Новосибирск · 2025",
          "project.11.name": "г. Новосибирск, Кедровый",
          "project.11.desc": "",
          "project.12.cat": "Кабинет · 2025",
          "project.12.name": "Кабинет-Оружейная Морозово",
          "project.12.desc": "",
          "approach.label": "Подход",
          "approach.title": "Как мы работаем",
          "step.1.title": "Знакомство и бриф",
          "step.1.text":
            "Изучаем образ жизни, задачи и характер пространства, формируем общее видение.",
          "step.2.title": "Концепция",
          "step.2.text":
            "Предлагаем планировочные решения, палитру материалов и атмосферу интерьера.",
          "step.3.title": "Проект и детали",
          "step.3.text":
            "Разрабатываем рабочую документацию, подбираем мебель, свет и отделку.",
          "step.4.title": "Реализация",
          "step.4.text":
            "Ведём проект на площадке и контролируем качество вплоть до финального стайлинга.",
          "partners.label": "Материалы и партнёры",
          "partners.title": "С кем мы работаем",
          "partners.text":
            "Проверенные поставщики мебели, камня, света и отделочных материалов.",
          "partners.cat1": "Мебель",
          "partners.cat2": "Камень и поверхности",
          "partners.cat3": "Свет",
          "partners.cat4": "Текстиль и декор",
          "partners.note":
            "Финальный список партнёров формируется индивидуально под задачи каждого проекта.",
          "contact.label": "Контакты",
          "contact.title": "Обсудим ваш проект",
          "contact.text":
            "Расскажите о пространстве и задачах - предложим первичное видение, сроки и условия сотрудничества.",
          "contact.cta": "Написать нам",
          "contact.phone": "Телефон",
          "contact.email": "Почта",
          "contact.messenger": "Мессенджеры",
          "contact.social": "Соцсети",
          "footer.rights": "Все права защищены.",
          "footer.privacy": "Политика конфиденциальности",
          "footer.cities": "Москва · Санкт-Петербург",
          "privacy.label": "Политика конфиденциальности",
          "brief.consentBefore": "Я согласен(на) на обработку персональных данных в соответствии с",
          "brief.consentLink": "политикой конфиденциальности",
          "brief.title": "Заявка на проект",
          "brief.q1": "Какой метраж пространства мы будем проектировать?",
          "brief.q2": "Какое направление интерьера вам ближе?",
          "brief.q3": "Когда планируете приступить к работам?",
          "brief.q4": "Как с вами связаться?",
          "brief.a1.1": "До 60 м²",
          "brief.a1.2": "60-120 м²",
          "brief.a1.3": "120-200 м²",
          "brief.a1.4": "200-500 м²",
          "brief.a1.5": "500-1000 м²",
          "brief.a1.6": "Больше 1000 м²",
          "brief.a2.1": "Классический",
          "brief.a2.2": "Ар-деко",
          "brief.a2.3": "Минимализм",
          "brief.a2.4": "Современный",
          "brief.a2.5": "Эклектика",
          "brief.a2.6": "Пока выбираю",
          "brief.a3.1": "Уже готов(а) начать",
          "brief.a3.2": "В течение полугода",
          "brief.a3.3": "В течение года",
          "brief.a3.4": "Не раньше чем через год",
          "brief.a3.5": "Пока не определился(лась)",
          "brief.name": "Имя",
          "brief.namePh": "Имя",
          "brief.phone": "Телефон",
          "brief.phonePh": "Телефон",
          "brief.back": "Назад",
          "brief.next": "Продолжить",
          "brief.fillData": "Указать контакты",
          "brief.submit": "Отправить",
          "brief.sending": "Отправляем…",
          "brief.error": "Не удалось отправить. Попробуйте ещё раз или напишите на key-des@mail.ru",
          "brief.doneTitle": "Принято!",
          "brief.doneText": "Мы получили вашу заявку и скоро напишем или позвоним.",
          "services.subtitle": "Что мы делаем для вашего пространства",
          "services.all": "Все услуги",
          "svc.more": "Подробнее",
          "svc.less": "Свернуть",
          "svc.cta": "Оставить заявку",
          "svc.1.title": "Дизайн-проект интерьера",
          "svc.1.lead": "Авторская концепция пространства и полный комплект рабочей документации: стиль, конструктивные решения и технологии отделки. Срок разработки - от двух месяцев, в зависимости от площади и сложности объекта.",
          "svc.1.note": "Отдельно можно заказать консультацию по планировке на этапе выбора квартиры или дома.",
          "svc.1.s1.title": "Техническое задание",
          "svc.1.s1.text": "Фиксируем задачи по каждой зоне, собираем пожелания и референсы по стилю, мебели и оборудованию.",
          "svc.1.s2.title": "Обмеры и фотофиксация",
          "svc.1.s2.text": "Выезжаем на объект, снимаем точные размеры и фиксируем исходное состояние помещений.",
          "svc.1.s3.title": "Планировочное решение",
          "svc.1.s3.text": "Предлагаем несколько вариантов расстановки зон с учётом сценариев жизни и инженерии.",
          "svc.1.s4.title": "3D-визуализация",
          "svc.1.s4.text": "Показываем будущую атмосферу интерьера: свет, материалы, мебель и детали в объёмных рендерах.",
          "svc.1.s5.title": "Рабочий проект",
          "svc.1.s5.text": "Готовим чертежи и спецификации, по которым строители и поставщики реализуют проект без догадок.",
          "svc.2.title": "Менеджмент проектов",
          "svc.2.lead": "Ведём проект как единую систему: координируем поставщиков и подрядчиков, помогаем с комплектацией. Сокращаем время на подбор чистовых материалов, мебели и декора, выстраиваем бюджет и контролируем сроки поставок.",
          "svc.2.s1.title": "Поиск исполнителей",
          "svc.2.s1.text": "Подбираем проверенных поставщиков и подрядчиков под задачи и бюджет проекта.",
          "svc.2.s2.title": "Карта материалов",
          "svc.2.s2.text": "Формируем техническое задание, собираем палитру отделки и согласовываем образцы с вами.",
          "svc.2.s3.title": "Смета и сроки",
          "svc.2.s3.text": "Считаем стоимость материалов, мебели и наполнения по спецификациям проекта с указанием сроков.",
          "svc.2.s4.title": "Утверждение бюджета",
          "svc.2.s4.text": "Согласовываем финальную смету и фиксируем приоритеты закупок.",
          "svc.2.s5.title": "График оплат",
          "svc.2.s5.text": "Связываем платежи с этапами строительства, чтобы закупки шли в нужной последовательности.",
          "svc.2.s6.title": "Закупка и логистика",
          "svc.2.s6.text": "Ведём процесс от проверки коммерческих предложений до доставки и монтажа на объекте.",
          "svc.3.title": "Авторский надзор",
          "svc.3.lead": "Сопровождаем реализацию дизайн-проекта на площадке: следим за качеством, координируем подрядчиков и своевременно вносим уточнения в документацию.",
          "svc.3.s1.title": "Выезды на объект",
          "svc.3.s1.text": "Регулярно приезжаем на площадку и сверяем ход работ с проектом.",
          "svc.3.s2.title": "Консультации бригады",
          "svc.3.s2.text": "Отвечаем на вопросы строителей в процессе отделки и монтажа.",
          "svc.3.s3.title": "Контроль качества",
          "svc.3.s3.text": "Проверяем соответствие узлов, материалов и геометрии рабочим чертежам.",
          "svc.3.s4.title": "Корректировки проекта",
          "svc.3.s4.text": "Оперативно обновляем чертежи, если на объекте появляются уточнения.",
          "svc.3.s5.title": "Смежные подрядчики",
          "svc.3.s5.text": "Согласуем работу инженеров, мебельщиков, декораторов и других специалистов.",
          "svc.3.s6.title": "Отчётность",
          "svc.3.s6.text": "Еженедельно фиксируем статус работ и принятые решения для прозрачности процесса.",
          "svc.4.title": "Архитектурное планирование",
          "svc.4.lead": "Проектируем логику пространства до деталей отделки: перепланировки, зонирование, инженерные вводные и связь интерьера с архитектурой здания.",
          "svc.4.s1.title": "Анализ объекта",
          "svc.4.s1.text": "Изучаем планировку, инсоляцию, инженерные стояки и ограничения застройщика или БТИ.",
          "svc.4.s2.title": "Сценарии использования",
          "svc.4.s2.text": "Описываем, как вы будете жить в пространстве: маршруты, приватность, хранение, зоны отдыха и работы.",
          "svc.4.s3.title": "Планировочные схемы",
          "svc.4.s3.text": "Готовим варианты перепланировки с расстановкой мебели и привязкой инженерии.",
          "svc.4.s4.title": "Согласование изменений",
          "svc.4.s4.text": "Помогаем подготовить документы для согласования перепланировки, если это требуется.",
          "svc.4.s5.title": "Связь с дизайн-проектом",
          "svc.4.s5.text": "Передаём утверждённую планировку в этап проработки материалов, света и деталей интерьера."
        },
        en: {
          "brand.tag": "Interior Design Studio",
          "nav.about": "About",
          "nav.projects": "Projects",
          "nav.services": "Services",
          "nav.approach": "Approach",
          "nav.partners": "Partners",
          "nav.contact": "Contact",
          "nav.home": "Home",
          "hero.eyebrow": "Moscow - Saint Petersburg",
          "hero.tagline":
            "We create thoughtful interiors where light, material and every detail are in balance.",
          "hero.cta": "View projects",
          "hero.secondary": "Discuss a project",
          "hero.media": "Photography coming soon",
          "hero.stat1": "years of practice",
          "hero.stat2": "interiors delivered",
          "hero.stat3": "cities",
          "hero.scroll": "Projects",
          "about.label": "About the studio",
          "about.p1":
            "It started with a genuine love of space and a wish to create interiors that stay with people for years.",
          "about.p2":
            "Early projects, early mistakes, and the first clients who trusted us. Years of practice across scales and formats - from compact apartments to complex sites - shaped more than experience: a language of our own, where every detail is justified and every decision is deliberate.",
          "about.p3":
            "Today Key-Design is an author studio with a clear vision: architectural precision, living materials, and a fine balance of form and warmth. Spaces that do not shout, yet stay in memory.",
          "about.p4":
            "A good interior is not about beautiful photos. It is about how you feel in the space every day. That is what we design.",
          "about.role": "founder & lead designer",
          "projects.label": "Projects",
          "projects.all": "All projects",
          "projects.featured": "Featured project",
          "project.link": "View project",
          "project.1.cat": "Private house · Moscow · 2025",
          "project.1.name": "Dream House",
          "project.1.desc":
            "A private house in a warm neutral palette: natural wood, soft textures and considered light - from the kitchen-living room to the private quarters.",
          "project.2.cat": "Apartment · Moscow · 2025",
          "project.2.name": "Pulsar Residential Complex",
          "project.2.desc":
            "An apartment in a modern residential complex: a light palette, functional zoning and considered details.",
          "project.3.cat": "Studio · Moscow · 2025",
          "project.3.name": "Moscow Studio",
          "project.3.desc":
            "A compact studio with a considered layout: every square metre works for comfort, light and a sense of space.",
          "project.4.cat": "Salok krasoty tati · 2026",
          "project.4.name": "Salok krasoty tati",
          "project.4.desc":
            "Salon interior for tati - soft light, a calm palette, and thoughtful ergonomics.",
          "project.5.cat": "Private house · Novosibirsk · 2025",
          "project.5.name": "Novosibirsk, Laki Park, House",
          "project.5.desc": "",
          "project.6.cat": "Apartment · Moscow · 2025",
          "project.6.name": "Moscow, ZHK Arkhitektor",
          "project.6.desc": "",
          "project.7.cat": "Residential complex · Novosibirsk · 2025",
          "project.7.name": "Novosibirsk, Akademgorodok, ZHK Pulsar 1",
          "project.7.desc": "",
          "project.8.cat": "Apartment · Novosibirsk · 2025",
          "project.8.name": "Novosibirsk, Dekabristov Quarter",
          "project.8.desc": "",
          "project.9.cat": "Private house · Novosibirsk · 2025",
          "project.9.name": "Novosibirsk, Nevskaya St. House",
          "project.9.desc": "",
          "project.10.cat": "Apartment · Novosibirsk · 2025",
          "project.10.name": "Novosibirsk, Eastern Vibe Apartment",
          "project.10.desc": "",
          "project.11.cat": "Apartment · Novosibirsk · 2025",
          "project.11.name": "Novosibirsk, Kedrovy",
          "project.11.desc": "",
          "project.12.cat": "Study · 2025",
          "project.12.name": "Kabinet-Oruzheynaya Morozovo",
          "project.12.desc": "",
          "approach.label": "Approach",
          "approach.title": "How we work",
          "step.1.title": "Intro & brief",
          "step.1.text":
            "We study your lifestyle, goals and the character of the space to shape a shared vision.",
          "step.2.title": "Concept",
          "step.2.text":
            "We propose layouts, a material palette and the overall atmosphere of the interior.",
          "step.3.title": "Design & detail",
          "step.3.text":
            "We develop working documentation and select furniture, lighting and finishes.",
          "step.4.title": "Delivery",
          "step.4.text":
            "We lead the project on site and control quality down to the final styling.",
          "partners.label": "Materials & partners",
          "partners.title": "Who we work with",
          "partners.text":
            "Trusted suppliers of furniture, stone, lighting and finishing materials.",
          "partners.cat1": "Furniture",
          "partners.cat2": "Stone & surfaces",
          "partners.cat3": "Lighting",
          "partners.cat4": "Textile & decor",
          "partners.note":
            "The final list of partners is curated individually for each project.",
          "contact.label": "Contact",
          "contact.title": "Let's discuss your project",
          "contact.text":
            "Tell us about your space and goals - we'll share an initial vision, timeline and terms.",
          "contact.cta": "Get in touch",
          "contact.phone": "Phone",
          "contact.email": "Email",
          "contact.messenger": "Messengers",
          "contact.social": "Social",
          "footer.rights": "All rights reserved.",
          "footer.privacy": "Privacy policy",
          "footer.cities": "Moscow · Saint Petersburg",
          "privacy.label": "Privacy policy",
          "brief.consentBefore": "I agree to the processing of personal data in accordance with the",
          "brief.consentLink": "privacy policy",
          "brief.title": "Project inquiry",
          "brief.q1": "What is the area we will be designing?",
          "brief.q2": "Which interior direction feels closest to you?",
          "brief.q3": "When are you planning to start work?",
          "brief.q4": "How can we reach you?",
          "brief.a1.1": "Up to 60 m²",
          "brief.a1.2": "60-120 m²",
          "brief.a1.3": "120-200 m²",
          "brief.a1.4": "200-500 m²",
          "brief.a1.5": "500-1000 m²",
          "brief.a1.6": "Over 1000 m²",
          "brief.a2.1": "Classic",
          "brief.a2.2": "Art Deco",
          "brief.a2.3": "Minimalism",
          "brief.a2.4": "Modern",
          "brief.a2.5": "Eclectic",
          "brief.a2.6": "Still exploring",
          "brief.a3.1": "Ready to start now",
          "brief.a3.2": "Within six months",
          "brief.a3.3": "Within a year",
          "brief.a3.4": "Not before a year from now",
          "brief.a3.5": "Not decided yet",
          "brief.name": "Name",
          "brief.namePh": "Name",
          "brief.phone": "Phone",
          "brief.phonePh": "Phone",
          "brief.back": "Back",
          "brief.next": "Continue",
          "brief.fillData": "Add contacts",
          "brief.submit": "Send",
          "brief.sending": "Sending…",
          "brief.error": "Could not send. Try again or email key-des@mail.ru",
          "brief.doneTitle": "Received!",
          "brief.doneText": "We have your inquiry and will be in touch soon.",
          "services.subtitle": "What we do for your space",
          "services.all": "All services",
          "svc.more": "Learn more",
          "svc.less": "Show less",
          "svc.cta": "Request a call",
          "svc.1.title": "Interior design project",
          "svc.1.lead": "A bespoke spatial concept and full working documentation: style, structural choices and finishing technologies. Timeline from two months, depending on size and complexity.",
          "svc.1.note": "Planning consultation when choosing a home can be booked separately.",
          "svc.1.s1.title": "Design brief",
          "svc.1.s1.text": "We define tasks for each zone and collect preferences and references for style, furniture and equipment.",
          "svc.1.s2.title": "Site survey",
          "svc.1.s2.text": "We visit the site, take accurate measurements and document the existing condition.",
          "svc.1.s3.title": "Layout options",
          "svc.1.s3.text": "We propose several zoning schemes based on how you live and on engineering constraints.",
          "svc.1.s4.title": "3D visualisation",
          "svc.1.s4.text": "We show the future atmosphere: light, materials, furniture and details in rendered views.",
          "svc.1.s5.title": "Working drawings",
          "svc.1.s5.text": "We prepare drawings and specifications builders and suppliers can follow without guesswork.",
          "svc.2.title": "Project management",
          "svc.2.lead": "We run the project as one system: coordinate suppliers and contractors and help with procurement. Less time on finishes, furniture and decor; clearer budget and delivery dates.",
          "svc.2.s1.title": "Finding partners",
          "svc.2.s1.text": "We select trusted suppliers and contractors for the scope and budget.",
          "svc.2.s2.title": "Material palette",
          "svc.2.s2.text": "We prepare specifications, build a finish palette and approve samples with you.",
          "svc.2.s3.title": "Estimate and lead times",
          "svc.2.s3.text": "We calculate materials, furniture and fittings from project specs with costs and dates.",
          "svc.2.s4.title": "Budget approval",
          "svc.2.s4.text": "We agree the final estimate and set procurement priorities.",
          "svc.2.s5.title": "Payment schedule",
          "svc.2.s5.text": "We align payments with construction stages so orders arrive in the right sequence.",
          "svc.2.s6.title": "Purchasing and logistics",
          "svc.2.s6.text": "From reviewing quotes to delivery and installation on site.",
          "svc.3.title": "Author supervision",
          "svc.3.lead": "We support implementation on site: quality control, contractor coordination and timely updates to documentation.",
          "svc.3.s1.title": "Site visits",
          "svc.3.s1.text": "Regular visits to compare progress with the approved project.",
          "svc.3.s2.title": "Team guidance",
          "svc.3.s2.text": "We answer builders' questions during finishing and installation.",
          "svc.3.s3.title": "Quality control",
          "svc.3.s3.text": "We check details, materials and geometry against working drawings.",
          "svc.3.s4.title": "Drawing updates",
          "svc.3.s4.text": "We revise drawings promptly when the site requires clarifications.",
          "svc.3.s5.title": "Related trades",
          "svc.3.s5.text": "We coordinate engineers, joiners, decorators and other specialists.",
          "svc.3.s6.title": "Reporting",
          "svc.3.s6.text": "Weekly status and decisions documented for a transparent process.",
          "svc.4.title": "Architectural planning",
          "svc.4.lead": "We design spatial logic before finishes: replanning, zoning, engineering inputs and how the interior relates to the building.",
          "svc.4.s1.title": "Site analysis",
          "svc.4.s1.text": "We study layout, daylight, risers and developer or registry constraints.",
          "svc.4.s2.title": "Use scenarios",
          "svc.4.s2.text": "How you will live in the space: routes, privacy, storage, rest and work zones.",
          "svc.4.s3.title": "Layout schemes",
          "svc.4.s3.text": "Replanning options with furniture and engineering layouts.",
          "svc.4.s4.title": "Approvals",
          "svc.4.s4.text": "We help prepare documents for replanning approval when required.",
          "svc.4.s5.title": "Handover to design",
          "svc.4.s5.text": "Approved layout moves into materials, lighting and interior detailing."
        }
      };

      var langButtons = document.querySelectorAll(".lang__btn");

      function applyLang(lang) {
        var dict = i18n[lang] || i18n.ru;
        var nodes = document.querySelectorAll("[data-i18n]");
        nodes.forEach(function (node) {
          var key = node.getAttribute("data-i18n");
          if (dict[key]) node.textContent = dict[key];
        });
        document.querySelectorAll("[data-i18n-placeholder]").forEach(function (node) {
          var pKey = node.getAttribute("data-i18n-placeholder");
          if (dict[pKey]) node.placeholder = dict[pKey];
        });
        root.setAttribute("lang", lang);
        langButtons.forEach(function (b) {
          b.setAttribute(
            "aria-pressed",
            b.getAttribute("data-lang") === lang ? "true" : "false"
          );
        });
        if (window.__kdsBriefUpdateLabels) window.__kdsBriefUpdateLabels();
        try {
          localStorage.setItem("kds-lang", lang);
        } catch (e) {}
      }

      var storedLang = null;
      try {
        storedLang = localStorage.getItem("kds-lang");
      } catch (e) {}
      applyLang(storedLang === "en" ? "en" : "ru");

      langButtons.forEach(function (b) {
        b.addEventListener("click", function () {
          applyLang(b.getAttribute("data-lang"));
        });
      });

      /* ---------- Mobile nav ---------- */
      var nav = document.getElementById("nav");
      var navToggle = document.getElementById("navToggle");
      if (nav && navToggle) {
        var navScrollY = 0;

        function syncHeaderHeight() {
          var hdr = document.getElementById("header");
          if (!hdr) return;
          document.documentElement.style.setProperty(
            "--header-h",
            hdr.offsetHeight + "px"
          );
        }

        function setNavOpen(open) {
          nav.classList.toggle("is-open", open);
          navToggle.setAttribute("aria-expanded", open ? "true" : "false");
          navToggle.setAttribute(
            "aria-label",
            open ? "Закрыть меню" : "Открыть меню"
          );
          document.body.classList.toggle("nav-open", open);
          if (open) {
            navScrollY = window.scrollY || window.pageYOffset || 0;
            document.body.style.top = "-" + navScrollY + "px";
            document.body.style.position = "fixed";
            document.body.style.width = "100%";
            syncHeaderHeight();
          } else {
            document.body.style.top = "";
            document.body.style.position = "";
            document.body.style.width = "";
            window.scrollTo(0, navScrollY);
          }
        }

        function closeNav() {
          setNavOpen(false);
        }

        syncHeaderHeight();
        window.addEventListener("resize", syncHeaderHeight, { passive: true });

        navToggle.addEventListener("click", function () {
          setNavOpen(!nav.classList.contains("is-open"));
        });

        nav.addEventListener("click", function (e) {
          if (e.target.classList.contains("nav__link")) closeNav();
          else if (e.target === nav) closeNav();
        });

        document.addEventListener("keydown", function (e) {
          if (e.key === "Escape" && nav.classList.contains("is-open")) {
            closeNav();
          }
        });
      }

      function queryHashTarget() {
        var hash = location.hash;
        if (!hash || hash === "#") return null;
        try {
          return document.querySelector(hash);
        } catch (e) {
          return null;
        }
      }

      /* ---------- Header scroll state ---------- */
      var header = document.getElementById("header");
      var projectsNavLink = document.querySelector(".nav__link--projects");
      var projectsNavDefault = projectsNavLink
        ? projectsNavLink.querySelector(".nav__link-default")
        : null;
      var projectsNavScrolled = projectsNavLink
        ? projectsNavLink.querySelector(".nav__link-scrolled")
        : null;

      function syncProjectsNavLabel(scrolled) {
        if (!projectsNavDefault || !projectsNavScrolled) return;
        projectsNavDefault.hidden = scrolled;
        projectsNavScrolled.hidden = !scrolled;
      }

      function scrollToHashTarget(id, behavior) {
        var target = document.getElementById(id);
        if (!target) return;
        var headerH = header ? header.offsetHeight : 0;
        var top =
          target.getBoundingClientRect().top + window.scrollY - headerH - 12;
        window.scrollTo({ top: Math.max(0, top), behavior: behavior || "smooth" });
      }

      function onScroll() {
        var scrolled = window.scrollY > 24;
        if (header) {
          header.classList.toggle("is-scrolled", scrolled);
        }
        if (document.body.classList.contains("home")) {
          syncProjectsNavLabel(scrolled);
        }
      }
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });

      document.querySelectorAll('a[href="#projects"]').forEach(function (link) {
        link.addEventListener("click", function (e) {
          if (!document.getElementById("projects")) return;
          e.preventDefault();
          scrollToHashTarget("projects", "smooth");
          if (history.replaceState) {
            history.replaceState(null, "", "#projects");
          } else {
            location.hash = "projects";
          }
        });
      });

      if (location.hash === "#projects" && document.getElementById("projects")) {
        requestAnimationFrame(function () {
          scrollToHashTarget("projects", "auto");
        });
      }

      /* ---------- Hero slideshow (homepage) ---------- */
      var heroScene = document.querySelector(".hero__scene");
      if (heroScene) {
        var heroSlides = heroScene.querySelectorAll(".hero__slide");
        var heroLoaded = [];
        var HERO_MS = 5000;

        function heroSlideUrl(slide) {
          return slide.getAttribute("data-hero-bg") || "";
        }

        function loadHeroSlide(index) {
          if (heroLoaded[index]) {
            return Promise.resolve();
          }
          var slide = heroSlides[index];
          var url = heroSlideUrl(slide);
          if (!url) {
            heroLoaded[index] = true;
            return Promise.resolve();
          }
          return new Promise(function (resolve) {
            var img = new Image();
            img.onload = img.onerror = function () {
              slide.style.backgroundImage = 'url("' + url + '")';
              heroLoaded[index] = true;
              resolve();
            };
            img.src = url;
          });
        }

        heroSlides.forEach(function (slide, i) {
          if (slide.style.backgroundImage) {
            heroLoaded[i] = true;
          }
        });

        if (heroSlides.length > 1) {
          var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
          if (!reduceMotion) {
            var heroIdx = 0;
            var preloadNext = function () {
              var nextIdx = (heroIdx + 1) % heroSlides.length;
              loadHeroSlide(nextIdx);
            };
            setTimeout(preloadNext, 2500);
            setInterval(function () {
              var nextIdx = (heroIdx + 1) % heroSlides.length;
              loadHeroSlide(nextIdx).then(function () {
                heroSlides[heroIdx].classList.remove("is-active");
                heroIdx = nextIdx;
                heroSlides[heroIdx].classList.add("is-active");
                setTimeout(preloadNext, HERO_MS - 1800);
              });
            }, HERO_MS);
          }
        }
      }

      /* ---------- Reveal on scroll ---------- */
      var revealEls = document.querySelectorAll(".reveal");
      if ("IntersectionObserver" in window) {
        var io = new IntersectionObserver(
          function (entries) {
            entries.forEach(function (entry) {
              if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                io.unobserve(entry.target);
              }
            });
          },
          { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
        );
        revealEls.forEach(function (el) {
          io.observe(el);
          var rect = el.getBoundingClientRect();
          if (rect.top < window.innerHeight * 0.92 && rect.bottom > 0) {
            el.classList.add("is-visible");
            io.unobserve(el);
          }
        });
        setTimeout(function () {
          revealEls.forEach(function (el) {
            if (!el.classList.contains("is-visible")) {
              el.classList.add("is-visible");
            }
          });
        }, 2500);
      } else {
        revealEls.forEach(function (el) {
          el.classList.add("is-visible");
        });
      }

      /* ---------- Smooth horizontal scroll (all pages) ----------
         One requestAnimationFrame loop eases scrollLeft toward an
         accumulating target. Wheel events only nudge the target, so
         rapid trackpad / shift+wheel input never spawns competing
         animations (that was the old jerk / freeze). Containers use
         scroll-behavior: auto in CSS so per-frame writes are instant. */
      var H_SCROLL_SEL = ".proj-gallery, .room-rail, .pcar";
      var EASE = 0.16; // glide factor per frame (higher = snappier)

      function initHorizontalScroll(el) {
        if (!el || el.dataset.hScrollInit) return;
        el.dataset.hScrollInit = "1";

        var target = el.scrollLeft;
        var rafId = null;

        function stopAnim() {
          if (rafId) {
            cancelAnimationFrame(rafId);
            rafId = null;
          }
          el.classList.remove("is-wheel-scrolling");
        }

        function tick() {
          var diff = target - el.scrollLeft;
          if (Math.abs(diff) < 0.5) {
            el.scrollLeft = target;
            stopAnim();
            return;
          }
          el.scrollLeft += diff * EASE;
          rafId = requestAnimationFrame(tick);
        }

        function startAnim() {
          if (rafId) return;
          el.classList.add("is-wheel-scrolling");
          rafId = requestAnimationFrame(tick);
        }

        el.addEventListener(
          "wheel",
          function (e) {
            var absX = Math.abs(e.deltaX);
            var absY = Math.abs(e.deltaY);
            var delta = 0;

            if (absX > absY && absX > 0) {
              delta = e.deltaX;
            } else if (e.shiftKey && absY > 0) {
              delta = e.deltaY;
            } else {
              return; // let the page scroll vertically
            }

            var maxScroll = el.scrollWidth - el.clientWidth;
            if (maxScroll <= 0) return;

            // sync target to reality when idle, then accumulate
            if (!rafId) target = el.scrollLeft;
            target = Math.max(0, Math.min(maxScroll, target + delta));
            startAnim();
            e.preventDefault();
          },
          { passive: false }
        );

        var down = false;
        var startX = 0;
        var startLeft = 0;
        el.addEventListener("pointerdown", function (e) {
          if (e.button !== 0) return;
          stopAnim();
          down = true;
          el.dataset.dragged = "0";
          startX = e.clientX;
          startLeft = el.scrollLeft;
          target = startLeft;
        });
        el.addEventListener("pointermove", function (e) {
          if (!down) return;
          var dx = e.clientX - startX;
          if (Math.abs(dx) > 6) el.dataset.dragged = "1";
          el.scrollLeft = startLeft - dx;
          target = el.scrollLeft;
        });
        function endDrag() {
          if (!down) return;
          down = false;
          target = el.scrollLeft;
          setTimeout(function () {
            el.dataset.dragged = "0";
          }, 0);
        }
        el.addEventListener("pointerup", endDrag);
        el.addEventListener("pointercancel", endDrag);
        el.addEventListener("pointerleave", endDrag);
      }

      document.querySelectorAll(H_SCROLL_SEL).forEach(initHorizontalScroll);

      /* ---------- Projects carousel nav (homepage) ---------- */
      var projCar = document.getElementById("projCar");
      if (projCar) {
        projCar.addEventListener(
          "click",
          function (e) {
            if (projCar.dataset.dragged === "1") {
              e.preventDefault();
              e.stopPropagation();
            }
          },
          true
        );

        var projSlide = function (dir) {
          var slides = Array.prototype.slice.call(
            projCar.querySelectorAll(".pcar-slide")
          );
          if (!slides.length) return;
          var center = projCar.scrollLeft + projCar.clientWidth / 2;
          var cur = 0;
          var best = Infinity;
          slides.forEach(function (s, i) {
            var c = s.offsetLeft + s.offsetWidth / 2;
            var d = Math.abs(c - center);
            if (d < best) {
              best = d;
              cur = i;
            }
          });
          var t = Math.max(0, Math.min(slides.length - 1, cur + dir));
          var target = slides[t];
          var left =
            target.offsetLeft + target.offsetWidth / 2 - projCar.clientWidth / 2;
          projCar.scrollTo({ left: left, behavior: "smooth" });
        };

        document.querySelectorAll(".pcar-nav .rail-nav__btn").forEach(function (btn) {
          btn.addEventListener("click", function () {
            projSlide(btn.getAttribute("data-pdir") === "next" ? 1 : -1);
          });
        });
      }

      /* ---------- Room rail nav (project pages) ---------- */
      document.querySelectorAll(".rooms-rail-head .rail-nav__btn").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var rail = document.getElementById("roomRail");
          if (!rail) return;
          var amount = rail.clientWidth * 0.8;
          rail.scrollBy({
            left: btn.getAttribute("data-dir") === "next" ? amount : -amount,
            behavior: "smooth",
          });
        });
      });

      /* ---------- Year ---------- */
      var y = document.getElementById("year");
      if (y) y.textContent = new Date().getFullYear();

      /* ---------- Brief quiz modal (homepage) ---------- */
      var briefRoot = document.getElementById("brief");
      if (briefRoot) {
        var briefForm = document.getElementById("briefForm");
        var briefPanels = briefRoot.querySelectorAll("[data-brief-step]");
        var briefCounter = briefRoot.querySelector("[data-brief-counter]");
        var briefProgress = briefRoot.querySelector("[data-brief-progress]");
        var briefFoot = briefRoot.querySelector("[data-brief-foot]");
        var briefBack = briefRoot.querySelector("[data-brief-back]");
        var briefNext = briefRoot.querySelector("[data-brief-next]");
        var briefNextLabel = briefRoot.querySelector("[data-brief-next-label]");
        var briefStep = 1;
        var briefTotalQuiz = 3;

        function briefDict() {
          var lang = root.getAttribute("lang") === "en" ? "en" : "ru";
          return i18n[lang] || i18n.ru;
        }

        function briefCanAdvance() {
          if (briefStep === 1) {
            return !!briefForm.querySelector('input[name="area"]:checked');
          }
          if (briefStep === 2) {
            return !!briefForm.querySelector('input[name="style"]:checked');
          }
          if (briefStep === 3) {
            return !!briefForm.querySelector('input[name="timeline"]:checked');
          }
          if (briefStep === 4) {
            var name = briefForm.querySelector('input[name="name"]');
            var phone = briefForm.querySelector('input[name="phone"]');
            var consent = briefForm.querySelector('input[name="consent"]');
            return (
              name &&
              phone &&
              name.value.trim() &&
              phone.value.trim() &&
              consent &&
              consent.checked
            );
          }
          return false;
        }

        function briefUpdateUi() {
          briefPanels.forEach(function (panel) {
            var n = Number(panel.getAttribute("data-brief-step"));
            var active = n === briefStep;
            panel.hidden = !active;
            panel.classList.toggle("is-active", active);
          });

          if (briefCounter) {
            briefCounter.hidden = briefStep > briefTotalQuiz || briefStep === 5;
            if (briefStep <= briefTotalQuiz) {
              briefCounter.textContent = briefStep + " / " + briefTotalQuiz;
            }
          }

          if (briefProgress) {
            var pct = briefStep <= briefTotalQuiz ? (briefStep / briefTotalQuiz) * 100 : 100;
            briefProgress.style.width = pct + "%";
          }

          if (briefFoot) briefFoot.hidden = briefStep === 5;
          if (briefBack) briefBack.disabled = briefStep <= 1 || briefStep === 5;

          var dict = briefDict();
          if (briefNextLabel) {
            if (briefStep === 3) briefNextLabel.textContent = dict["brief.fillData"];
            else if (briefStep === 4) briefNextLabel.textContent = dict["brief.submit"];
            else briefNextLabel.textContent = dict["brief.next"];
          }

          if (briefNext) {
            briefNext.disabled = !briefCanAdvance();
            briefNext.type = briefStep === 4 ? "submit" : "button";
          }
        }

        window.__kdsBriefUpdateLabels = briefUpdateUi;

        function briefReset() {
          briefStep = 1;
          briefForm.reset();
          briefForm.querySelectorAll(".is-invalid").forEach(function (el) {
            el.classList.remove("is-invalid");
          });
          briefUpdateUi();
        }

        function briefOpen() {
          briefReset();
          briefRoot.classList.add("is-open");
          briefRoot.setAttribute("aria-hidden", "false");
          document.body.style.overflow = "hidden";
          if (briefNext) briefNext.focus();
        }

        function briefClose() {
          briefRoot.classList.remove("is-open");
          briefRoot.setAttribute("aria-hidden", "true");
          document.body.style.overflow = "";
          if (location.hash === "#brief") {
            history.replaceState(null, "", location.pathname + location.search);
          }
        }

        function briefMailtoFallback(payload) {
          var lines = [
            "Заявка - Key Design Studio",
            "",
            "Метраж: " + payload.area,
            "Направление: " + payload.style,
            "Сроки: " + payload.timeline,
            "Имя: " + payload.name,
            "Телефон: " + payload.phone
          ];

          try {
            var mail = "mailto:key-des@mail.ru?subject=" +
              encodeURIComponent("Заявка с сайта Key Design Studio") +
              "&body=" + encodeURIComponent(lines.join("\n"));
            var mailWin = window.open(mail, "_blank");
            if (!mailWin) window.location.href = mail;
          } catch (e) {}
        }

        function briefShowDone() {
          briefStep = 5;
          briefUpdateUi();
        }

        function briefSubmit() {
          var area = briefForm.querySelector('input[name="area"]:checked');
          var style = briefForm.querySelector('input[name="style"]:checked');
          var timeline = briefForm.querySelector('input[name="timeline"]:checked');
          var name = briefForm.querySelector('input[name="name"]');
          var phone = briefForm.querySelector('input[name="phone"]');
          var consent = briefForm.querySelector('input[name="consent"]');

          if (!name.value.trim() || !phone.value.trim() || !consent || !consent.checked) {
            if (!name.value.trim()) name.classList.add("is-invalid");
            if (!phone.value.trim()) phone.classList.add("is-invalid");
            if (consent && !consent.checked) consent.classList.add("is-invalid");
            briefUpdateUi();
            return;
          }

          var payload = {
            area: area ? area.value : "",
            style: style ? style.value : "",
            timeline: timeline ? timeline.value : "",
            name: name.value.trim(),
            phone: phone.value.trim(),
            _subject: "Заявка с сайта Key Design Studio"
          };

          var endpoint = window.KDS_BRIEF && window.KDS_BRIEF.endpoint;
          if (!endpoint) {
            briefMailtoFallback(payload);
            briefShowDone();
            return;
          }

          var dict = briefDict();
          if (briefNext) {
            briefNext.disabled = true;
            if (briefNextLabel) briefNextLabel.textContent = dict["brief.sending"];
          }

          fetch(endpoint, {
            method: "POST",
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
          })
            .then(function (res) {
              if (!res.ok) throw new Error("submit failed");
              briefShowDone();
            })
            .catch(function () {
              briefMailtoFallback(payload);
              briefShowDone();
            });
        }

        document.querySelectorAll("[data-open-brief]").forEach(function (trigger) {
          trigger.addEventListener("click", function (e) {
            e.preventDefault();
            briefOpen();
          });
        });

        briefRoot.querySelectorAll("[data-close-brief]").forEach(function (el) {
          el.addEventListener("click", briefClose);
        });

        if (briefBack) {
          briefBack.addEventListener("click", function () {
            if (briefStep > 1 && briefStep < 5) {
              briefStep -= 1;
              briefUpdateUi();
            }
          });
        }

        if (briefNext) {
          briefNext.addEventListener("click", function () {
            if (briefNext.disabled) return;
            if (briefStep < 4) {
              briefStep += 1;
              briefUpdateUi();
            }
          });
        }

        briefForm.addEventListener("change", briefUpdateUi);
        briefForm.addEventListener("input", function (e) {
          if (e.target.classList) e.target.classList.remove("is-invalid");
          briefUpdateUi();
        });

        briefForm.querySelectorAll(".brief__consent a").forEach(function (link) {
          link.addEventListener("click", function (e) {
            e.stopPropagation();
          });
        });

        briefForm.addEventListener("submit", function (e) {
          e.preventDefault();
          if (briefStep === 4) briefSubmit();
        });

        document.addEventListener("keydown", function (e) {
          if (e.key === "Escape" && briefRoot.classList.contains("is-open")) {
            briefClose();
          }
        });

        if (location.hash === "#brief") briefOpen();
        window.addEventListener("hashchange", function () {
          if (location.hash === "#brief") briefOpen();
        });

        briefUpdateUi();
      }

      /* ---------- Services page accordion ---------- */
      function svcDict() {
        var lang = root.getAttribute("lang") === "en" ? "en" : "ru";
        return i18n[lang] || i18n.ru;
      }

      function svcClose(svc) {
        svc.classList.remove("is-open");
        var body = svc.querySelector(".svc__body");
        var btn = svc.querySelector("[data-svc-toggle]");
        if (body) body.hidden = true;
        if (btn) {
          btn.setAttribute("aria-expanded", "false");
          var dict = svcDict();
          btn.textContent = dict["svc.more"] || "Подробнее";
        }
      }

      function svcOpenTarget(target) {
        if (!target || !target.classList.contains("svc")) return;
        document.querySelectorAll(".svc.is-open").forEach(function (other) {
          if (other !== target) svcClose(other);
        });
        target.classList.add("is-open");
        var body = target.querySelector(".svc__body");
        var btn = target.querySelector("[data-svc-toggle]");
        if (body) body.hidden = false;
        if (btn) {
          btn.setAttribute("aria-expanded", "true");
          var dict = svcDict();
          btn.textContent = dict["svc.less"] || "Свернуть";
        }
        setTimeout(function () {
          target.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 60);
      }

      document.querySelectorAll("[data-svc-toggle]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var svc = btn.closest(".svc");
          if (!svc) return;
          if (svc.classList.contains("is-open")) svcClose(svc);
          else svcOpenTarget(svc);
        });
      });

      if (location.hash) {
        var hashTarget = queryHashTarget();
        if (hashTarget && hashTarget.classList.contains("svc")) {
          svcOpenTarget(hashTarget);
        }
      }

      window.addEventListener("hashchange", function () {
        var t = queryHashTarget();
        if (t && t.classList.contains("svc")) svcOpenTarget(t);
      });
    })();
