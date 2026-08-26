/* <name> Air Conditioning & Heating — Red Alert */
(function () {
  'use strict';

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  var PHONE_RE = /^[\d\s().+-]{10,}$/;

  // Both the hero quick-bar and the full form below use the same handling.
  // Set data-endpoint on a form to POST it somewhere real.
  function wire(form) {
    if (!form) return;

    function validate() {
      var ok = true;
      Array.prototype.forEach.call(form.querySelectorAll('[data-required]'), function (input) {
        var value = input.value.trim();
        var bad = !value || (input.type === 'tel' && !PHONE_RE.test(value));
        input.closest('.field').classList.toggle('invalid', bad);
        if (bad) {
          if (ok) input.focus();
          ok = false;
        }
      });
      return ok;
    }

    form.addEventListener('input', function (e) {
      var field = e.target.closest('.field.invalid');
      if (field) field.classList.remove('invalid');
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var trap = form.querySelector('[name="company"]');
      if (trap && trap.value) return;
      if (!validate()) return;

      var button = form.querySelector('button[type="submit"]');
      var label = button.textContent;
      button.disabled = true;
      button.textContent = 'Sending…';

      function finish() {
        if (form.querySelector('.form-success')) {
          form.classList.add('sent');
          form.querySelector('.form-success').focus();
        } else {
          // The hero quick-bar has no success panel of its own — hand the
          // visitor down to the full form, pre-filled with what they typed.
          var full = document.getElementById('quote-form');
          if (full) {
            Array.prototype.forEach.call(form.elements, function (el) {
              var twin = full.elements[el.name];
              if (el.name && twin && !twin.value) twin.value = el.value;
            });
            (full.closest('section') || full).scrollIntoView({ behavior: 'smooth' });
            full.querySelector('[name="name"]').focus({ preventScroll: true });
          }
          button.disabled = false;
          button.textContent = label;
        }
      }

      if (form.dataset.endpoint) {
        fetch(form.dataset.endpoint, { method: 'POST', body: new FormData(form) })
          .then(finish)
          .catch(function () {
            button.disabled = false;
            button.textContent = label;
            alert('Something went wrong. Please call us instead.');
          });
      } else {
        setTimeout(finish, 300);
      }
    });
  }

  wire(document.getElementById('callback-form'));
  wire(document.getElementById('quote-form'));
})();
