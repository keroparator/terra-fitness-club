const header = document.querySelector('[data-header]');
const menuToggle = document.querySelector('[data-menu-toggle]');
const nav = document.querySelector('[data-nav]');
const navLinks = [...document.querySelectorAll('[data-nav] a[href^="#"]')];
const sections = [...document.querySelectorAll('main section[id]')];
const mobileMenu = window.matchMedia('(max-width: 900px)');

const updateMenuAvailability = (isOpen) => {
  const isUnavailable = mobileMenu.matches && !isOpen;
  nav.toggleAttribute('inert', isUnavailable);

  if (isUnavailable) {
    nav.setAttribute('aria-hidden', 'true');
  } else {
    nav.removeAttribute('aria-hidden');
  }
};

const closeMenu = () => {
  menuToggle.setAttribute('aria-expanded', 'false');
  nav.classList.remove('is-open');
  header.classList.remove('menu-active');
  document.body.classList.remove('menu-open');
  updateMenuAvailability(false);

  if (nav.contains(document.activeElement)) menuToggle.focus();
};

menuToggle.addEventListener('click', () => {
  const willOpen = menuToggle.getAttribute('aria-expanded') !== 'true';
  menuToggle.setAttribute('aria-expanded', String(willOpen));
  nav.classList.toggle('is-open', willOpen);
  header.classList.toggle('menu-active', willOpen);
  document.body.classList.toggle('menu-open', willOpen);
  updateMenuAvailability(willOpen);
});

navLinks.forEach((link) => link.addEventListener('click', closeMenu));

window.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeMenu();
});

mobileMenu.addEventListener('change', closeMenu);
updateMenuAvailability(false);

const updateHeader = () => {
  header.classList.toggle('scrolled', window.scrollY > 24);
};

updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

const revealObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('is-visible');
    observer.unobserve(entry.target);
  });
}, { threshold: 0.12, rootMargin: '0px 0px -45px' });

document.querySelectorAll('.hero .reveal').forEach((element) => {
  element.classList.add('is-visible');
});

document.querySelectorAll('.reveal').forEach((element, index) => {
  if (element.classList.contains('is-visible')) return;
  element.style.transitionDelay = `${Math.min(index % 4, 3) * 70}ms`;
  revealObserver.observe(element);
});

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    navLinks.forEach((link) => {
      link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`);
    });
  });
}, { rootMargin: '-35% 0px -60%', threshold: 0 });

sections.forEach((section) => sectionObserver.observe(section));

document.querySelectorAll('[data-year]').forEach((element) => {
  element.textContent = new Date().getFullYear();
});
