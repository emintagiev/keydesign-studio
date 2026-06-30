const yearEl = document.getElementById('year');
const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.nav');

if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}

if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });
}
