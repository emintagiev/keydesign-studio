    (function () {
      "use strict";

      var root = document.documentElement;

  /* ---------- i18n (RU default, EN ready) ---------- */
      var i18n = {
        ru: {
          "brand.tag": "Студия интерьерного дизайна",
          "nav.about": "О студии",
          "nav.projects": "Проекты",
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
          "footer.cities": "Москва · Санкт-Петербург",
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
          "brief.doneText": "Мы получили вашу заявку и скоро напишем или позвоним."
        },
        en: {
          "brand.tag": "Interior Design Studio",
          "nav.about": "About",
          "nav.projects": "Projects",
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
          "footer.cities": "Moscow · Saint Petersburg",
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
          "brief.doneText": "We have your inquiry and will be in touch soon."
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
      navToggle.addEventListener("click", function () {
        var open = nav.classList.toggle("is-open");
        navToggle.setAttribute("aria-expanded", open ? "true" : "false");
        document.body.style.overflow = open ? "hidden" : "";
      });
      nav.addEventListener("click", function (e) {
        if (e.target.classList.contains("nav__link")) {
          nav.classList.remove("is-open");
          navToggle.setAttribute("aria-expanded", "false");
          document.body.style.overflow = "";
        }
      });

      /* ---------- Header scroll state ---------- */
      var header = document.getElementById("header");
      function onScroll() {
        if (window.scrollY > 24) header.classList.add("is-scrolled");
        else header.classList.remove("is-scrolled");
      }
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });

      /* ---------- Hero slideshow (homepage) ---------- */
      var heroScene = document.querySelector(".hero__scene");
      if (heroScene) {
        var heroSlides = heroScene.querySelectorAll(".hero__slide");
        var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        if (heroSlides.length > 1 && !reduceMotion) {
          var heroIdx = 0;
          setInterval(function () {
            heroSlides[heroIdx].classList.remove("is-active");
            heroIdx = (heroIdx + 1) % heroSlides.length;
            heroSlides[heroIdx].classList.add("is-active");
          }, 5000);
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
            return name && phone && name.value.trim() && phone.value.trim();
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

          if (!name.value.trim() || !phone.value.trim()) {
            if (!name.value.trim()) name.classList.add("is-invalid");
            if (!phone.value.trim()) phone.classList.add("is-invalid");
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
    })();
