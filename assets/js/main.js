/* ============================================================
   Interacciones — Coach Gloria Celis
   Sin dependencias. Progresivo: todo funciona sin JS.
   ============================================================ */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Header sticky ---------- */
  var header = document.getElementById('siteHeader');
  var onScroll = function () {
    if (window.scrollY > 24) header.classList.add('is-stuck');
    else header.classList.remove('is-stuck');
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- 2. Menú móvil ---------- */
  var toggle = document.getElementById('navToggle');
  var menu = document.getElementById('mobileMenu');

  function setMenu(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    menu.classList.toggle('is-open', open);
    menu.setAttribute('aria-hidden', String(!open));
    document.body.style.overflow = open ? 'hidden' : '';
  }

  toggle.addEventListener('click', function () {
    setMenu(toggle.getAttribute('aria-expanded') !== 'true');
  });
  menu.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () { setMenu(false); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setMenu(false);
  });

  /* ---------- 3. Reveals al hacer scroll ---------- */
  var revealItems = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    revealItems.forEach(function (el) { revealObserver.observe(el); });
  } else {
    revealItems.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- 4. Contadores ---------- */
  var counters = document.querySelectorAll('[data-count]');
  var easeOutExpo = function (t) { return t === 1 ? 1 : 1 - Math.pow(2, -10 * t); };

  function animateCounter(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    if (isNaN(target)) return;
    if (reduceMotion) { el.textContent = String(target); return; }

    var duration = 1600;
    var start = null;

    function step(ts) {
      if (!start) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      el.textContent = String(Math.round(easeOutExpo(progress) * target));
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  if ('IntersectionObserver' in window) {
    var counterObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { counterObserver.observe(el); });
  } else {
    counters.forEach(animateCounter);
  }

  /* ---------- 5. Formulario ---------- */
  var form = document.getElementById('contactForm');
  var status = document.getElementById('formStatus');

  function validateField(input) {
    var field = input.closest('.field');
    var value = input.value.trim();
    var valid = true;

    if (input.hasAttribute('required') && !value) valid = false;
    if (valid && input.type === 'email' && value) {
      valid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value);
    }
    field.classList.toggle('has-error', !valid);
    return valid;
  }

  if (form) {
    form.querySelectorAll('input[required], input[type="email"]').forEach(function (input) {
      input.addEventListener('blur', function () { validateField(input); });
      input.addEventListener('input', function () {
        if (input.closest('.field').classList.contains('has-error')) validateField(input);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fields = form.querySelectorAll('input[required], input[type="email"]');
      var ok = true;
      var firstInvalid = null;

      fields.forEach(function (input) {
        var valid = validateField(input);
        if (!valid && !firstInvalid) firstInvalid = input;
        ok = ok && valid;
      });

      if (!ok) {
        if (firstInvalid) firstInvalid.focus();
        status.classList.remove('is-visible');
        return;
      }

      status.classList.add('is-visible');
      form.reset();
      form.querySelectorAll('.field').forEach(function (f) { f.classList.remove('has-error'); });
      status.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
    });
  }

  /* ---------- 6. Año actual ---------- */
  var year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());

  /* ---------- 7. Parallax suave del balón (solo desktop) ---------- */
  var ball = document.querySelector('.ball');
  if (ball && !reduceMotion && window.matchMedia('(min-width: 1024px)').matches) {
    var raf = null;
    window.addEventListener('scroll', function () {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        var y = Math.min(window.scrollY, 600);
        ball.style.setProperty('--ball-shift', (y * 0.08) + 'px');
        ball.style.translate = '0 ' + (y * 0.08) + 'px';
        raf = null;
      });
    }, { passive: true });
  }
})();
