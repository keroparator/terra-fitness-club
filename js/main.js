const header = document.querySelector('[data-header]');
const menuToggle = document.querySelector('[data-menu-toggle]');
const nav = document.querySelector('[data-nav]');
const navLinks = [...document.querySelectorAll('[data-nav] a[href^="#"]')];
const sections = [...document.querySelectorAll('main section[id]')];
const mobileMenu = window.matchMedia('(max-width: 900px)');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const navGroups = [...nav.querySelectorAll('.nav-group')];
const menuLabel = menuToggle.querySelector('.sr-only');

const updateMenuAvailability = (isOpen) => {
  const isUnavailable = mobileMenu.matches && !isOpen;
  nav.toggleAttribute('inert', isUnavailable);

  if (isUnavailable) {
    nav.setAttribute('aria-hidden', 'true');
  } else {
    nav.removeAttribute('aria-hidden');
  }
};

const groupAnimations = new Map();
const setNavGroup = (group, open, animate = false) => {
  if (!open && !group.open && !groupAnimations.has(group)) return;
  const startHeight = group.getBoundingClientRect().height;
  groupAnimations.get(group)?.cancel();
  groupAnimations.delete(group);
  group.classList.remove('is-closing');
  group.style.removeProperty('overflow');
  const submenu = group.querySelector('.nav-submenu');
  submenu.toggleAttribute('inert', !open);
  if (!animate || !mobileMenu.matches || reducedMotion.matches) {
    group.open = open;
    return;
  }
  group.open = true;
  group.classList.toggle('is-closing', !open);
  const endHeight = open ? group.scrollHeight : group.querySelector('summary').getBoundingClientRect().height;
  group.style.overflow = 'hidden';
  const animation = group.animate([
    { height: `${startHeight}px` },
    { height: `${endHeight}px` }
  ], { duration: 320, easing: 'cubic-bezier(0.22, 1, 0.36, 1)' });
  groupAnimations.set(group, animation);
  animation.onfinish = () => {
    group.open = open;
    group.classList.remove('is-closing');
    group.style.removeProperty('overflow');
    groupAnimations.delete(group);
  };
};

const closeMenu = () => {
  menuToggle.setAttribute('aria-expanded', 'false');
  menuLabel.textContent = 'Menüyü aç';
  navGroups.forEach((group) => setNavGroup(group, false));
  nav.classList.remove('is-open');
  header.classList.remove('menu-active');
  document.body.classList.remove('menu-open');
  updateMenuAvailability(false);

  if (nav.contains(document.activeElement)) menuToggle.focus();
};

menuToggle.addEventListener('click', () => {
  const willOpen = menuToggle.getAttribute('aria-expanded') !== 'true';
  menuToggle.setAttribute('aria-expanded', String(willOpen));
  menuLabel.textContent = willOpen ? 'Menüyü kapat' : 'Menüyü aç';
  nav.classList.toggle('is-open', willOpen);
  header.classList.toggle('menu-active', willOpen);
  document.body.classList.toggle('menu-open', willOpen);
  updateMenuAvailability(willOpen);
});

navLinks.forEach((link) => link.addEventListener('click', closeMenu));
navGroups.forEach((group) => {
  group.querySelector('summary').addEventListener('click', (event) => {
    if (!mobileMenu.matches) return;
    event.preventDefault();
    const willOpen = !group.open || group.classList.contains('is-closing');
    if (willOpen) navGroups.filter((other) => other !== group).forEach((other) => setNavGroup(other, false, true));
    setNavGroup(group, willOpen, true);
  });
  group.addEventListener('toggle', () => {
    if (!mobileMenu.matches) {
      group.querySelector('.nav-submenu').removeAttribute('inert');
      if (group.open) navGroups.filter((other) => other !== group).forEach((other) => setNavGroup(other, false));
    }
  });
});
document.addEventListener('click', (event) => {
  if (!nav.contains(event.target) && !menuToggle.contains(event.target)) {
    navGroups.forEach((group) => setNavGroup(group, false));
  }
});

window.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    const openGroup = navGroups.find((group) => group.open);
    if (!mobileMenu.matches && openGroup) openGroup.querySelector('summary').focus();
    closeMenu();
  }
  if (event.key !== 'Tab' || !mobileMenu.matches || !nav.classList.contains('is-open')) return;
  const focusable = [menuToggle, ...nav.querySelectorAll('a, summary')].filter((element) => element.getClientRects().length && !element.closest('[inert]'));
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
});

mobileMenu.addEventListener('change', closeMenu);
reducedMotion.addEventListener('change', () => navGroups.forEach((group) => setNavGroup(group, group.open && !group.classList.contains('is-closing'))));
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
  element.style.transitionDelay = `${Math.min(index % 3, 2) * 90}ms`;
  revealObserver.observe(element);
});

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    navLinks.forEach((link) => {
      if (link.dataset.package) return;
      const active = link.getAttribute('href') === `#${entry.target.id}`;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    navGroups[0].querySelector('summary').classList.toggle('active', entry.target.id === 'branslar');
    navGroups[1].querySelector('summary').classList.toggle('active', entry.target.id === 'uyelikler');
  });
}, { rootMargin: '-35% 0px -60%', threshold: 0 });

sections.forEach((section) => sectionObserver.observe(section));

const ticker = document.querySelector('.ticker');
const tickerTrack = ticker.querySelector('.ticker-track');
const tickerGroup = ticker.querySelector('.ticker-group');
const tickerItems = [...tickerGroup.children].map((item) => item.cloneNode(true));

const updateTicker = () => {
  const group = tickerGroup.cloneNode(false);
  group.append(...tickerItems.map((item) => item.cloneNode(true)));
  tickerTrack.replaceChildren(group);

  // Fill a whole viewport before duplicating the identical animation half.
  while (group.offsetWidth < ticker.clientWidth) {
    group.append(...tickerItems.map((item) => {
      const copy = item.cloneNode(true);
      copy.setAttribute('aria-hidden', 'true');
      return copy;
    }));
  }

  const duplicate = group.cloneNode(true);
  duplicate.setAttribute('aria-hidden', 'true');
  tickerTrack.append(duplicate);
};

new ResizeObserver(updateTicker).observe(ticker);
document.fonts.ready.then(updateTicker);

document.querySelectorAll('[data-year]').forEach((element) => {
  element.textContent = new Date().getFullYear();
});


const membershipTrack = document.querySelector('[data-membership-track]');
const membershipCards = [...membershipTrack.querySelectorAll('[data-membership]')];
const packageButtons = [...document.querySelectorAll('[data-select-package]')];
const previousPackage = document.querySelector('[data-carousel-prev]');
const nextPackage = document.querySelector('[data-carousel-next]');
const carouselStatus = document.querySelector('[data-carousel-status]');
let selectedPackage = 0;
let carouselFrame = 0;

const updateCardDepth = () => {
  const center = membershipTrack.scrollLeft + membershipTrack.clientWidth / 2;
  membershipCards.forEach((card) => {
    const surface = card.querySelector('.membership-surface');
    const distance = mobileMenu.matches && !reducedMotion.matches
      ? Math.max(-1, Math.min(1, (card.offsetLeft + card.offsetWidth / 2 - center) / card.offsetWidth))
      : 0;
    surface.style.setProperty('--card-angle', `${-distance * 24}deg`);
    surface.style.setProperty('--card-pitch', `${Math.abs(distance) * 5}deg`);
    surface.style.setProperty('--card-scale', String(1 - Math.abs(distance) * 0.09));
    surface.style.setProperty('--light-position', `${25 + distance * 35}%`);
  });
};

const updatePackageSelection = (index) => {
  selectedPackage = index;
  membershipCards.forEach((card, cardIndex) => card.classList.toggle('is-selected', cardIndex === index));
  packageButtons.forEach((button, buttonIndex) => button.setAttribute('aria-pressed', String(buttonIndex === index)));
  document.querySelectorAll('[data-package]').forEach((link) => {
    link.classList.toggle('active', link.dataset.package === membershipCards[index].dataset.membership);
  });
  previousPackage.disabled = index === 0;
  nextPackage.disabled = index === membershipCards.length - 1;
  carouselStatus.textContent = `${membershipCards[index].dataset.membership} aylık üyelik, ${index + 1} / ${membershipCards.length}`;
};

const showPackage = (months) => {
  const index = membershipCards.findIndex((card) => card.dataset.membership === String(months));
  if (index < 0) return;
  updatePackageSelection(index);
  updateCardDepth();
  if (!mobileMenu.matches) return;
  const card = membershipCards[index];
  membershipTrack.scrollTo({
    left: card.offsetLeft - (membershipTrack.clientWidth - card.offsetWidth) / 2,
    behavior: reducedMotion.matches ? 'instant' : 'smooth'
  });
};

packageButtons.forEach((button) => button.addEventListener('click', () => showPackage(button.dataset.selectPackage)));
previousPackage.addEventListener('click', () => showPackage(membershipCards[Math.max(0, selectedPackage - 1)].dataset.membership));
nextPackage.addEventListener('click', () => showPackage(membershipCards[Math.min(membershipCards.length - 1, selectedPackage + 1)].dataset.membership));

document.querySelectorAll('[data-package]').forEach((link) => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    showPackage(link.dataset.package);
    document.querySelector('#uyelikler').scrollIntoView({ behavior: reducedMotion.matches ? 'instant' : 'smooth', block: 'start' });
    document.querySelector('#memberships-title').focus({ preventScroll: true });
    history.replaceState(null, '', '#uyelikler');
  });
});
document.querySelector('#memberships-title').setAttribute('tabindex', '-1');

membershipTrack.addEventListener('scroll', () => {
  if (!mobileMenu.matches || carouselFrame) return;
  carouselFrame = requestAnimationFrame(() => {
    carouselFrame = 0;
    const center = membershipTrack.scrollLeft + membershipTrack.clientWidth / 2;
    const distances = membershipCards.map((card) => Math.abs(card.offsetLeft + card.offsetWidth / 2 - center));
    const nearest = distances.indexOf(Math.min(...distances));
    if (nearest !== selectedPackage) updatePackageSelection(nearest);
    updateCardDepth();
  });
}, { passive: true });

let carouselResizeFrame = 0;
new ResizeObserver(() => {
  cancelAnimationFrame(carouselResizeFrame);
  carouselResizeFrame = requestAnimationFrame(() => showPackage(membershipCards[selectedPackage].dataset.membership));
}).observe(membershipTrack);
updatePackageSelection(0);

reducedMotion.addEventListener('change', updateCardDepth);
updateCardDepth();
