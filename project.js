/* ============================================================
   Project page interactions
   - multi-room: room selector rail, then full-screen carousel
   - single-zone: gallery shown immediately (no "Комнаты" step)
   - big side arrows (‹ ›) move one photo at a time
   - lightbox (click a photo to enlarge, arrows / esc to navigate)
   - horizontal scroll: see app.js (all pages)
   ============================================================ */
(function () {
  "use strict";

  /* ---------- move one photo at a time, keeping it centered ---------- */
  function slide(gallery, dir) {
    var figs = Array.prototype.slice.call(gallery.querySelectorAll("figure"));
    if (!figs.length) return;
    var center = gallery.scrollLeft + gallery.clientWidth / 2;
    var current = 0;
    var best = Infinity;
    figs.forEach(function (f, i) {
      var c = f.offsetLeft + f.offsetWidth / 2;
      var d = Math.abs(c - center);
      if (d < best) {
        best = d;
        current = i;
      }
    });
    var next = Math.max(0, Math.min(figs.length - 1, current + dir));
    var target = figs[next];
    var left = target.offsetLeft + target.offsetWidth / 2 - gallery.clientWidth / 2;
    gallery.scrollTo({ left: left, behavior: "smooth" });
  }

  function initGalleryArrows(scope) {
    scope.querySelectorAll(".gallery-arrow").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var stage = btn.closest(".room-stage");
        var gallery = stage ? stage.querySelector(".proj-gallery") : null;
        if (gallery) slide(gallery, btn.getAttribute("data-dir") === "next" ? 1 : -1);
      });
    });
  }

  function initLightbox(containers) {
    var lb = document.getElementById("lightbox");
    if (!lb) return;

    var lbImg = lb.querySelector(".lightbox__img");
    var lbCounter = lb.querySelector(".lightbox__counter");
    var list = [];
    var index = 0;

    function render() {
      lbImg.setAttribute("src", list[index]);
      lbCounter.textContent = index + 1 + " / " + list.length;
    }
    function openLb(images, i) {
      list = images;
      index = i;
      render();
      lb.classList.add("is-open");
      lb.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    }
    function closeLb() {
      lb.classList.remove("is-open");
      lb.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }
    function step(dir) {
      index = (index + dir + list.length) % list.length;
      render();
    }

    containers.forEach(function (container) {
      var gallery = container.querySelector(".proj-gallery");
      var imgs = Array.prototype.slice.call(
        container.querySelectorAll(".proj-gallery figure img")
      );
      var sources = imgs.map(function (img) {
        return img.getAttribute("data-full") || img.getAttribute("src");
      });
      imgs.forEach(function (img, i) {
        img.addEventListener("click", function () {
          if (gallery && gallery.dataset.dragged === "1") return;
          openLb(sources, i);
        });
      });
    });

    lb.querySelector(".lightbox__close").addEventListener("click", closeLb);
    lb.querySelector(".lightbox__nav--next").addEventListener("click", function (e) {
      e.stopPropagation();
      step(1);
    });
    lb.querySelector(".lightbox__nav--prev").addEventListener("click", function (e) {
      e.stopPropagation();
      step(-1);
    });
    lbImg.addEventListener("click", function (e) {
      e.stopPropagation();
      step(1);
    });
    lb.addEventListener("click", function (e) {
      if (e.target === lb) closeLb();
    });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") closeLb();
      else if (e.key === "ArrowRight") step(1);
      else if (e.key === "ArrowLeft") step(-1);
    });
  }

  /* ---------- single-zone project: gallery only ---------- */
  var singleRoot = document.querySelector(".project-single");
  if (singleRoot) {
    initGalleryArrows(singleRoot);
    initLightbox([singleRoot]);
    return;
  }

  /* ---------- multi-room project ---------- */
  var selector = document.getElementById("rooms");
  var rail = document.getElementById("roomRail");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".room-card"));
  var views = Array.prototype.slice.call(document.querySelectorAll(".room-view"));
  if (!selector || !rail) return;

  initGalleryArrows(document);

  /* ---------- open / close rooms ---------- */
  function showSelector() {
    selector.style.display = "";
    document.body.classList.remove("room-open");
    views.forEach(function (v) {
      v.classList.remove("is-open");
    });
    if (location.hash) {
      history.replaceState(null, "", location.pathname + location.search);
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function openRoom(slug) {
    var match = document.getElementById("view-" + slug);
    if (!match) return;
    selector.style.display = "none";
    document.body.classList.add("room-open");
    views.forEach(function (v) {
      v.classList.toggle("is-open", v === match);
    });
    var gallery = match.querySelector(".proj-gallery");
    if (gallery) gallery.scrollLeft = 0;
    history.replaceState(null, "", "#" + slug);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  cards.forEach(function (card) {
    card.addEventListener("click", function () {
      if (rail.dataset.dragged === "1") return;
      openRoom(card.getAttribute("data-room"));
    });
  });

  document.querySelectorAll("[data-back]").forEach(function (btn) {
    btn.addEventListener("click", showSelector);
  });

  initLightbox(views);

  /* ---------- deep link: open a room from the URL hash ---------- */
  var hash = location.hash.replace("#", "");
  if (hash) {
    openRoom(hash);
  }
})();
