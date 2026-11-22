/*!
 * CagedDragon auth enhancements — shared by every template in this library.
 *
 * Adds, without changing a template's markup or design:
 *   - inline validation with accessible error messages (aria-invalid / aria-describedby / role="alert")
 *   - loading + success states on submit buttons
 *   - password strength meter, Caps Lock hint, accessible show/hide toggles
 *   - OTP auto-submit and a resend countdown, PIN pad keyboard support
 *   - autocomplete / inputmode attributes, labels for unlabeled fields
 *   - visible keyboard focus, a skip link, and reduced-motion support
 *   - a backend hook: listen for the `cd:submit` event (see README)
 *
 * Backend hook:
 *   form.addEventListener('cd:submit', function (e) {
 *     e.preventDefault();                       // take over from the demo
 *     fetch('/api/login', { method: 'POST', body: JSON.stringify(e.detail.values) })
 *       .then(function (r) { e.detail.done(r.ok, r.ok ? 'Signed in' : 'Check your details'); })
 *       .catch(function () { e.detail.done(false, 'Network error, try again'); });
 *   });
 * Without a listener that calls preventDefault(), a demo success message is shown.
 */
(function () {
  'use strict';
  if (window.__cdEnhance) return;
  window.__cdEnhance = true;

  var doc = document;
  var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var uid = 0;

  function qs(s, r) { return (r || doc).querySelector(s); }
  function qsa(s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); }

  /* ------------------------------------------------------------ styles */
  var CSS = [
    'html{--cd-err:#ba1a1a}',
    'html[data-cd-mode="dark"],html.dark{--cd-err:#ffb4ab}',
    '.cd-err{display:flex;gap:6px;align-items:flex-start;margin-top:6px;font:600 12px/1.4 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--cd-err)}',
    '.cd-err::before{content:"!";display:inline-grid;place-items:center;flex:none;width:15px;height:15px;border-radius:50%;background:var(--cd-err);color:#fff;font-size:10px;font-weight:800;margin-top:1px}',
    'html[data-cd-mode="dark"] .cd-err::before,html.dark .cd-err::before{color:#410002}',
    '.cd-hint{margin-top:6px;font:500 12px/1.4 system-ui,-apple-system,"Segoe UI",sans-serif;color:rgb(var(--cd-on-surface-variant,113 113 122))}',
    'input[aria-invalid="true"]{border-color:var(--cd-err)!important;box-shadow:0 0 0 3px color-mix(in srgb,var(--cd-err) 22%,transparent)!important}',
    '.ws:has(input[aria-invalid="true"]){border-color:var(--cd-err)!important}',
    '.cd-shake{animation:cd-shake .36s}',
    '@keyframes cd-shake{10%,90%{transform:translateX(-2px)}20%,80%{transform:translateX(4px)}30%,50%,70%{transform:translateX(-6px)}40%,60%{transform:translateX(6px)}}',
    '.cd-spin{display:inline-block;width:16px;height:16px;border:2px solid currentColor;border-right-color:transparent;border-radius:50%;animation:cd-spin .7s linear infinite;flex:none}',
    '@keyframes cd-spin{to{transform:rotate(360deg)}}',
    '[aria-busy="true"]{cursor:progress;opacity:.85}',
    '#cd-toast{position:fixed;top:16px;left:50%;z-index:2147483000;max-width:min(420px,calc(100vw - 32px));transform:translate(-50%,-12px);opacity:0;pointer-events:none;',
    'padding:12px 16px;border-radius:12px;background:rgb(var(--cd-surface-container-highest,39 39 42));color:rgb(var(--cd-on-surface,250 250 250));',
    'border:1px solid rgb(var(--cd-outline,113 113 122) / .5);box-shadow:0 14px 40px rgb(0 0 0 / .3);font:600 13px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;transition:opacity .2s,transform .2s}',
    '#cd-toast.show{opacity:1;transform:translate(-50%,0)}',
    '.cd-skip{position:fixed;left:16px;top:-80px;z-index:2147483001;padding:10px 16px;border-radius:10px;background:rgb(var(--cd-primary,37 99 235));color:rgb(var(--cd-on-primary,255 255 255));font:700 14px system-ui,sans-serif;text-decoration:none}',
    '.cd-skip:focus{top:16px}',
    'a:focus-visible,button:focus-visible,summary:focus-visible,[role="button"]:focus-visible{outline:2px solid rgb(var(--cd-primary,37 99 235));outline-offset:2px}',
    '@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}'
  ].join('\n');

  function injectStyle() {
    var s = doc.createElement('style');
    s.id = 'cd-enhance-style';
    s.textContent = CSS;
    (doc.head || doc.documentElement).appendChild(s);
  }

  /* ------------------------------------------------------------ toast */
  var toastEl, toastTimer;
  function toast(msg) {
    if (!toastEl) {
      toastEl = doc.createElement('div');
      toastEl.id = 'cd-toast';
      toastEl.setAttribute('role', 'status');
      toastEl.setAttribute('aria-live', 'polite');
      doc.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    // force reflow so repeated toasts re-trigger the transition
    void toastEl.offsetWidth;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 3600);
  }

  /* ------------------------------------------------------------ helpers */
  function labelText(el) {
    var t = '';
    if (el.labels && el.labels[0]) t = el.labels[0].textContent;
    else t = el.getAttribute('aria-label') || el.placeholder || el.name || el.id || 'this field';
    return t.replace(/\s+/g, ' ').trim();
  }

  function kindOf(el) {
    var t = (el.type || 'text').toLowerCase();
    var k = ((el.id || '') + ' ' + (el.name || '')).toLowerCase();
    if (t === 'email' || /e-?mail/.test(k)) return 'email';
    if (t === 'password') return 'password';
    if (t === 'tel') return 'tel';
    if (el.id === 'ws') return 'workspace';
    if (el.id === 'org') return 'domain';
    return 'text';
  }

  function isSignup(scope) {
    var form = (scope.closest && scope.closest('form')) || scope;
    if (qs('.meter', form) || qs('#fn', form)) return true;
    var btn = qs('button[type="submit"],button:not([type])', form);
    return !!(btn && /create|sign\s?up|register|join/i.test(btn.textContent || ''));
  }

  /* ------------------------------------------------------------ errors */
  function hostFor(el) {
    var otp = el.closest('[data-otp]');
    if (otp) return { node: otp, where: 'afterend' };
    var chk = el.closest('.chk');
    if (chk) return { node: chk, where: 'afterend' };
    var field = el.closest('.field');
    if (field) return { node: field, where: 'beforeend' };
    var p = el.parentElement;
    return { node: p, where: 'afterend' };
  }

  function showErr(el, msg) {
    var otp = el.closest('[data-otp]');
    var target = otp ? qs('input', otp) : el;
    var err = target.__cdErr;
    if (!err) {
      err = doc.createElement('p');
      err.className = 'cd-err';
      err.id = 'cd-err-' + (++uid);
      err.setAttribute('role', 'alert');
      var h = hostFor(el);
      h.node.insertAdjacentElement(h.where, err);
      target.__cdErr = err;
    }
    err.textContent = msg;
    target.setAttribute('aria-invalid', 'true');
    var d = (target.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean);
    if (d.indexOf(err.id) < 0) d.push(err.id);
    target.setAttribute('aria-describedby', d.join(' '));
    if (otp) qsa('input', otp).forEach(function (i) { i.setAttribute('aria-invalid', 'true'); });
  }

  function clearErr(el) {
    var otp = el.closest('[data-otp]');
    var target = otp ? qs('input', otp) : el;
    var err = target.__cdErr;
    target.removeAttribute('aria-invalid');
    if (otp) qsa('input', otp).forEach(function (i) { i.removeAttribute('aria-invalid'); });
    if (err) {
      var d = (target.getAttribute('aria-describedby') || '').split(/\s+/).filter(function (x) { return x && x !== err.id; });
      if (d.length) target.setAttribute('aria-describedby', d.join(' ')); else target.removeAttribute('aria-describedby');
      if (err.parentNode) err.parentNode.removeChild(err);
      target.__cdErr = null;
    }
  }

  /* ------------------------------------------------------------ validation */
  function fieldMsg(el, signup, strict) {
    var v = (el.value || '').trim();
    var k = kindOf(el);
    if (!v) {
      var optional = /optional/i.test(labelText(el) + ' ' + (el.placeholder || ''));
      if (optional && !el.required) return '';
      if (!strict && !el.__cdTouched) return '';
      switch (k) {
        case 'email': return 'Enter your email address.';
        case 'password': return 'Enter your password.';
        case 'tel': return 'Enter your phone number.';
        case 'workspace': return 'Enter your workspace address.';
        case 'domain': return 'Enter your organisation domain.';
        default: return 'Please fill in ' + labelText(el).toLowerCase() + '.';
      }
    }
    if (k === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return 'Enter a valid email, like name@company.com.';
    if (k === 'password' && signup) {
      var min = qs('.meter', el.closest('form') || doc) ? 10 : 8;
      if (v.length < min) return 'Use at least ' + min + ' characters.';
    }
    if (k === 'workspace' && !/^[a-z0-9][a-z0-9-]{2,}$/i.test(v)) return 'Use 3 or more letters, numbers or hyphens.';
    if (k === 'domain' && !/^[^\s@]+\.[a-z]{2,}$/i.test(v)) return 'Enter a domain like yourcompany.com.';
    if (k === 'tel' && v.replace(/\D/g, '').length < 7) return 'Enter a valid phone number.';
    return '';
  }

  function validate(scope) {
    var signup = isSignup(scope);
    var first = null, ok = true, values = {}, n = 0;

    qsa('input,textarea,select', scope).forEach(function (el) {
      var t = (el.type || '').toLowerCase();
      if (el.disabled || t === 'hidden' || t === 'submit' || t === 'button' || t === 'radio') return;
      if (el.closest('[data-otp]')) return;
      if (el.offsetParent === null && getComputedStyle(el).position !== 'fixed' && t !== 'checkbox') return;
      var key = el.name || el.id || ('field' + (++n));
      if (t === 'checkbox') {
        var needs = signup && /agree|terms|privacy/i.test((el.closest('label') || {}).textContent || '');
        values[key] = el.checked;
        if (needs && !el.checked) {
          showErr(el, 'Please accept the Terms and Privacy Policy to continue.');
          ok = false; if (!first) first = el;
        } else clearErr(el);
        return;
      }
      values[key] = el.value;
      var msg = fieldMsg(el, signup, true);
      if (msg) { showErr(el, msg); ok = false; if (!first) first = el; }
      else clearErr(el);
    });

    qsa('[data-otp]', scope).forEach(function (g) {
      var ins = qsa('input', g);
      var code = ins.map(function (i) { return i.value; }).join('');
      values.code = code;
      if (code.length < ins.length) {
        showErr(ins[0], 'Enter all ' + ins.length + ' digits of your code.');
        ok = false; if (!first) first = ins[Math.max(0, code.length)] || ins[0];
      } else clearErr(ins[0]);
    });

    return { ok: ok, first: first, values: values };
  }

  function shake(el) {
    if (reduce || !el) return;
    var box = el.closest('.card,.glass,.term,.plain,.fp-in,.pinbox,form') || el;
    box.classList.remove('cd-shake');
    void box.offsetWidth;
    box.classList.add('cd-shake');
    setTimeout(function () { box.classList.remove('cd-shake'); }, 450);
  }

  /* ------------------------------------------------------------ submit flow */
  function submitButton(f) {
    var s = qs('button[type="submit"]', f) || qs('input[type="submit"]', f);
    if (s) return s;
    // no explicit submit button: pick the last untyped button that isn't a password toggle
    var c = qsa('button:not([type])', f).filter(function (b) {
      return !/password|visibility|toggle|eye/i.test((b.id || '') + ' ' + (b.getAttribute('aria-label') || '') + ' ' + b.className) && (b.textContent || '').trim().length > 2;
    });
    return c[c.length - 1] || null;
  }

  function announce(msg) {
    var l = doc.getElementById('cd-live');
    if (!l) {
      l = doc.createElement('div');
      l.id = 'cd-live';
      l.setAttribute('role', 'status');
      l.setAttribute('aria-live', 'polite');
      l.style.cssText = 'position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap';
      doc.body.appendChild(l);
    }
    l.textContent = '';
    setTimeout(function () { l.textContent = msg; }, 30);
  }

  /* The button's own markup is never replaced, because some templates keep
     references to elements inside it. We only add a spinner and aria-busy. */
  function setBusy(btn) {
    if (!btn || btn.__cdBusy) return;
    btn.__cdBusy = true;
    btn.setAttribute('aria-busy', 'true');
    var sp = doc.createElement('span');
    sp.className = 'cd-spin';
    sp.setAttribute('aria-hidden', 'true');
    sp.style.marginRight = '8px';
    btn.insertBefore(sp, btn.firstChild);
    btn.__cdSpin = sp;
    btn.disabled = true;
    announce('Please wait');
  }

  function clearBusy(btn) {
    if (!btn || !btn.__cdBusy) return;
    btn.__cdBusy = false;
    if (btn.__cdSpin && btn.__cdSpin.parentNode) btn.__cdSpin.parentNode.removeChild(btn.__cdSpin);
    btn.__cdSpin = null;
    btn.removeAttribute('aria-busy');
    btn.disabled = false;
  }

  function run(form, values, e) {
    if (form.__cdBusy) return;
    form.__cdBusy = true;
    var btn = submitButton(form);
    setBusy(btn);
    var settled = false;
    function done(ok, msg) {
      if (settled) return;
      settled = true;
      form.__cdBusy = false;
      clearBusy(btn);
      toast(msg || (ok ? 'Done.' : 'Something went wrong. Please try again.'));
      if (btn && btn.focus) btn.focus({ preventScroll: true });
    }
    var ev = new CustomEvent('cd:submit', { bubbles: true, cancelable: true, detail: { form: form, values: values, done: done } });
    form.dispatchEvent(ev);
    if (!ev.defaultPrevented) {
      setTimeout(function () { done(true, 'Demo mode: no backend is connected. Listen for the cd:submit event to wire one up.'); }, reduce ? 200 : 1100);
    }
  }

  function onSubmit(e) {
    var f = e.target;
    if (!f || f.tagName !== 'FORM') return;
    var r = validate(f);
    e.preventDefault();
    if (!r.ok) {
      e.stopImmediatePropagation();
      if (r.first && r.first.focus) r.first.focus();
      shake(f);
      return;
    }
    run(f, r.values, e);
  }

  /* wizard: validate the current pane before moving on */
  function onClick(e) {
    var t = e.target;
    if (!t || !t.closest) return;

    var next = t.closest('[data-next]');
    if (next) {
      var pane = next.closest('.pane') || next.closest('form');
      if (pane) {
        var r = validate(pane);
        if (!r.ok) {
          e.stopImmediatePropagation();
          e.preventDefault();
          if (r.first && r.first.focus) r.first.focus();
          shake(pane);
        }
      }
      return;
    }

    var resend = t.closest('a[href="#resend"]');
    if (resend) {
      e.preventDefault();
      startResend(resend);
      return;
    }

    var eye = t.closest('.eye,[data-toggle],#togglePassword');
    if (eye) setTimeout(function () { syncEye(eye); }, 0);
  }

  /* ------------------------------------------------------------ passwords */
  function eyeInput(btn) {
    var id = btn.getAttribute('data-toggle');
    if (id) return doc.getElementById(id);
    var wrap = btn.parentElement;
    return wrap && qs('input', wrap);
  }
  function syncEye(btn) {
    var i = eyeInput(btn);
    if (!i) return;
    var shown = i.type === 'text';
    btn.setAttribute('aria-pressed', shown ? 'true' : 'false');
    btn.setAttribute('aria-label', shown ? 'Hide password' : 'Show password');
  }

  var STRENGTH = [
    { t: 'Too short', c: 'var(--cd-err)' },
    { t: 'Weak', c: 'var(--cd-err)' },
    { t: 'Fair', c: 'rgb(var(--cd-secondary,217 119 6))' },
    { t: 'Good', c: 'rgb(var(--cd-tertiary,22 163 74))' },
    { t: 'Strong', c: 'rgb(var(--cd-primary,37 99 235))' }
  ];
  function scorePw(v) {
    if (!v) return -1;
    if (v.length < 8) return 0;
    var s = 0;
    if (v.length >= 10) s++;
    if (/[a-z]/.test(v) && /[A-Z]/.test(v)) s++;
    if (/\d/.test(v)) s++;
    if (/[^A-Za-z0-9]/.test(v)) s++;
    return Math.max(1, s);
  }
  function updateMeter(input) {
    var form = input.closest('form');
    var meter = form && qs('.meter', form);
    if (!meter) return;
    var s = scorePw(input.value);
    qsa('i', meter).forEach(function (bar, k) {
      bar.style.background = (s > 0 && k < s) ? STRENGTH[s].c : 'rgb(var(--cd-surface-container-highest,228 228 231))';
    });
    var lab = meter.__cdLabel;
    if (!lab && s < 0) return;
    if (!lab) {
      lab = doc.createElement('p');
      lab.className = 'cd-hint';
      lab.setAttribute('aria-live', 'polite');
      meter.insertAdjacentElement('afterend', lab);
      meter.__cdLabel = lab;
    }
    lab.textContent = s < 0 ? '' : 'Password strength: ' + STRENGTH[s].t;
  }

  function capsHint(e) {
    var i = e.target;
    if (!i || i.tagName !== 'INPUT' || i.type !== 'password' || !e.getModifierState) return;
    var on = e.getModifierState('CapsLock');
    var h = i.__cdCaps;
    if (on && !h) {
      h = doc.createElement('p');
      h.className = 'cd-hint';
      h.setAttribute('aria-live', 'polite');
      h.textContent = 'Caps Lock is on.';
      var host = hostFor(i);
      host.node.insertAdjacentElement(host.where, h);
      i.__cdCaps = h;
    } else if (!on && h) {
      h.remove();
      i.__cdCaps = null;
    }
  }

  /* ------------------------------------------------------------ OTP + PIN */
  function startResend(a) {
    if (a.__cdTimer) return;
    var left = 30, orig = a.textContent;
    a.setAttribute('aria-disabled', 'true');
    function tick() {
      a.textContent = 'Resend in ' + left + 's';
      if (left-- <= 0) {
        clearInterval(a.__cdTimer);
        a.__cdTimer = null;
        a.textContent = orig;
        a.removeAttribute('aria-disabled');
      }
    }
    toast('A new code has been sent (demo).');
    tick();
    a.__cdTimer = setInterval(tick, 1000);
  }

  function setupOtp() {
    qsa('[data-otp]').forEach(function (g) {
      var ins = qsa('input', g);
      ins.forEach(function (i, k) {
        i.setAttribute('inputmode', 'numeric');
        i.setAttribute('pattern', '[0-9]*');
        i.setAttribute('autocomplete', k === 0 ? 'one-time-code' : 'off');
      });
      g.addEventListener('input', function () {
        var code = ins.map(function (i) { return i.value; }).join('');
        if (code.length === ins.length) {
          clearErr(ins[0]);
          var f = g.closest('form');
          if (f) setTimeout(function () { f.requestSubmit ? f.requestSubmit() : f.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true })); }, 150);
        }
      });
    });
  }

  function setupPin() {
    qsa('[data-pin]').forEach(function (w) {
      var v = '';
      var live = doc.createElement('p');
      live.className = 'cd-hint';
      live.setAttribute('role', 'status');
      live.style.minHeight = '18px';
      var dots = qs('.dots', w);
      if (dots) dots.insertAdjacentElement('afterend', live);
      function say() { live.textContent = v.length ? v.length + ' of 4 digits entered' : ''; }
      w.addEventListener('click', function (e) {
        var b = e.target.closest('[data-k]');
        if (!b) return;
        var k = b.getAttribute('data-k');
        if (k === 'del') v = v.slice(0, -1);
        else if (v.length < 4) v += k;
        say();
        if (v.length === 4) {
          var pin = v;
          var ev = new CustomEvent('cd:submit', {
            bubbles: true, cancelable: true,
            detail: {
              form: w, values: { pin: pin },
              done: function (ok, msg) {
                toast(msg || (ok ? 'PIN accepted.' : 'Incorrect PIN. Try again.'));
                v = '';
                qsa('[data-k="del"]', w).forEach(function (d) { for (var n = 0; n < 4; n++) d.click(); });
                v = ''; say();
              }
            }
          });
          w.dispatchEvent(ev);
          if (!ev.defaultPrevented) setTimeout(function () { ev.detail.done(true, 'Demo mode: PIN ' + 'accepted. Listen for cd:submit to verify it.'); }, reduce ? 150 : 500);
        }
      });
      doc.addEventListener('keydown', function (e) {
        if (e.ctrlKey || e.metaKey || e.altKey) return;
        var sel = null;
        if (/^[0-9]$/.test(e.key)) sel = '[data-k="' + e.key + '"]';
        else if (e.key === 'Backspace') sel = '[data-k="del"]';
        if (!sel) return;
        var tgt = e.target && e.target.tagName;
        if (tgt === 'INPUT' || tgt === 'TEXTAREA') return;
        var b = qs(sel, w);
        if (b) { e.preventDefault(); b.click(); }
      });
    });
  }

  /* ------------------------------------------------------------ attributes */
  function setupFields() {
    if (!doc.documentElement.getAttribute('lang')) doc.documentElement.setAttribute('lang', 'en');
    qsa('form').forEach(function (f) { f.setAttribute('novalidate', ''); });

    qsa('input,textarea').forEach(function (el) {
      var t = (el.type || 'text').toLowerCase();
      if (t === 'hidden' || t === 'checkbox' || t === 'radio' || t === 'submit' || t === 'button') return;
      var k = kindOf(el);
      var signup = isSignup(el);
      if (!el.getAttribute('autocomplete') && !el.closest('[data-otp]')) {
        var ac = null;
        if (k === 'email') ac = signup ? 'email' : 'username';
        else if (k === 'password') ac = signup ? 'new-password' : 'current-password';
        else if (k === 'tel') ac = 'tel';
        else if (el.id === 'fn') ac = 'given-name';
        else if (el.id === 'ln') ac = 'family-name';
        else if (el.id === 'ws' || el.id === 'org') ac = 'organization';
        if (ac) el.setAttribute('autocomplete', ac);
      }
      if (k === 'email') { el.setAttribute('autocapitalize', 'none'); el.setAttribute('spellcheck', 'false'); }
      if (!el.name && el.id) el.name = el.id;
      var labelled = (el.labels && el.labels.length) || el.getAttribute('aria-label') || el.getAttribute('aria-labelledby');
      if (!labelled) el.setAttribute('aria-label', labelText(el));
    });

    qsa('.eye,[data-toggle],#togglePassword').forEach(syncEye);
    qsa('input[type="password"]').forEach(updateMeter);
  }

  function setupSkip() {
    var target = qs('form') || qs('[data-pin]') || qs('main') || qs('.card');
    if (!target) return;
    if (!target.id) target.id = 'cd-main';
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    var a = doc.createElement('a');
    a.className = 'cd-skip';
    a.href = '#' + target.id;
    a.textContent = 'Skip to sign-in';
    a.addEventListener('click', function (e) { e.preventDefault(); target.focus(); });
    doc.body.insertBefore(a, doc.body.firstChild);
  }

  /* ------------------------------------------------------------ live validation */
  function onInput(e) {
    var el = e.target;
    if (!el || el.tagName !== 'INPUT') return;
    el.__cdTouched = true;
    if (el.type === 'password') updateMeter(el);
    if (el.getAttribute('aria-invalid') === 'true') {
      if (el.closest('[data-otp]')) return;
      var msg = fieldMsg(el, isSignup(el), true);
      if (!msg) clearErr(el); else showErr(el, msg);
    }
  }
  function onBlur(e) {
    var el = e.target;
    if (!el || el.tagName !== 'INPUT' || el.closest('[data-otp]')) return;
    var t = (el.type || '').toLowerCase();
    if (t === 'checkbox' || t === 'radio') return;
    if (!(el.value || '').trim()) return; // don't nag on empty fields until submit
    var msg = fieldMsg(el, isSignup(el), true);
    if (msg) showErr(el, msg); else clearErr(el);
  }

  /* screen_20 calls this from an inline oninput but never defines it; a no-op
     fallback keeps typing from throwing. Real implementations are left alone. */
  if (typeof window.evaluatePassStrength !== 'function') window.evaluatePassStrength = function () {};

  /* ------------------------------------------------------------ boot */
  function init() {
    injectStyle();
    setupFields();
    setupOtp();
    setupPin();
    setupSkip();
    doc.addEventListener('submit', onSubmit, true);
    doc.addEventListener('click', onClick, true);
    doc.addEventListener('input', onInput, true);
    doc.addEventListener('focusout', onBlur, true);
    doc.addEventListener('keydown', capsHint, true);
    doc.addEventListener('keyup', capsHint, true);
  }

  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', init);
  else init();
})();
