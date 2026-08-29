/* <name> Built-In Appliance Specialists — Atelier */
(function () {
  'use strict';

  // Mobile navigation
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Current year in the footer
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Quote form: validation + success state.
  // Wire a real destination by setting data-endpoint on the <form>.
  var form = document.getElementById('quote-form');
  if (!form) return;

  var PHONE_RE = /^[\d\s().+-]{10,}$/;

  function setError(field, on) {
    field.classList.toggle('invalid', on);
  }

  function validate() {
    var ok = true;
    form.querySelectorAll('[data-required]').forEach(function (input) {
      var field = input.closest('.field');
      var value = input.value.trim();
      var bad = !value || (input.type === 'tel' && !PHONE_RE.test(value));
      setError(field, bad);
      if (bad && ok) input.focus();
      if (bad) ok = false;
    });
    return ok;
  }

  form.addEventListener('input', function (e) {
    var field = e.target.closest('.field.invalid');
    if (field) setError(field, false);
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.querySelector('[name="company"]').value) return; // honeypot
    if (!validate()) return;

    var button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    button.textContent = 'Sending…';

    var endpoint = form.dataset.endpoint;
    var done = function () {
      form.classList.add('sent');
      form.querySelector('.form-success').focus();
    };

    if (endpoint) {
      fetch(endpoint, { method: 'POST', body: new FormData(form) })
        .then(done)
        .catch(function () {
          button.disabled = false;
          button.textContent = 'Request service';
          alert('Something went wrong. Please call us instead.');
        });
    } else {
      // No endpoint configured yet — show the confirmation so the flow is testable.
      setTimeout(done, 350);
    }
  });
})();
