/* Retired product launcher. Retained for existing script references. */
(function () {
  'use strict';
  function loadVercelWebAnalytics() {
    if (document.querySelector('script[data-cd-vercel-analytics], script[src="/_vercel/insights/script.js"]')) return;
    window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
    const script = document.createElement('script');
    script.defer = true;
    script.src = '/_vercel/insights/script.js';
    script.setAttribute('data-cd-vercel-analytics', 'true');
    document.head.appendChild(script);
  }
  if (location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') loadVercelWebAnalytics();
})();
(function () {
  'use strict';
  if (typeof HTMLDialogElement === 'undefined' || typeof HTMLDialogElement.prototype.showModal !== 'function') return;
  const script = document.currentScript;
  if (!script?.src) return;
  const css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = new URL('cd-central-portals.css', script.src).href;
  let observer;
  function install() {
    const nav = document.querySelector(".nav-wrap .nav-links");
    const header = document.querySelector(".nav-wrap .shell.nav");
    if (!nav || !header || document.getElementById('cd-local-navigation')) return false;
    if ("#menuToggle" && !document.querySelector("#menuToggle")) return false;
    const toggle = document.createElement('button');
    toggle.type = 'button'; toggle.className = 'cd-local-nav-trigger';
    toggle.setAttribute('aria-haspopup','dialog'); toggle.setAttribute('aria-controls','cd-local-navigation'); toggle.setAttribute('aria-expanded','false');
    if ("#menuToggle") { const old = document.querySelector("#menuToggle"); old?.remove(); }
    const dialog = document.createElement('dialog'); dialog.id = 'cd-local-navigation'; dialog.className = 'cd-local-nav';
    const panel = document.createElement('div'); panel.className = 'cd-local-nav-panel';
    const heading = document.createElement('div'); heading.className = 'cd-local-nav-heading';
    const title = document.createElement('strong'), close = document.createElement('button');
    close.type = 'button'; close.className = 'cd-local-nav-close';
    function labels() { const ta = (document.documentElement.lang || '').toLowerCase().startsWith('ta'); title.textContent = ta ? 'வழிசெலுத்தல்' : 'Navigation'; toggle.textContent = '☰'; toggle.setAttribute('aria-label', ta ? 'பட்டி' : 'Open navigation'); close.textContent = ta ? 'மூடு' : 'Close'; dialog.setAttribute('aria-label', title.textContent); }
    heading.append(title, close); nav.classList.add('cd-local-nav-source'); panel.append(heading, nav); dialog.append(panel);
    header.prepend(toggle); document.body.append(dialog);
    let before = '';
    function shut() { if (dialog.open) dialog.close(); }
    toggle.addEventListener('click', () => { if (dialog.open) return; labels(); before = document.body.style.overflow; dialog.showModal(); document.body.style.overflow = 'hidden'; toggle.setAttribute('aria-expanded','true'); close.focus(); });
    close.addEventListener('click', shut);
    dialog.addEventListener('click', event => { if (event.target === dialog || (event.target instanceof Element && event.target.closest("nav a[href]"))) shut(); });
    dialog.addEventListener('close', () => { document.body.style.overflow = before; toggle.setAttribute('aria-expanded','false'); toggle.focus(); });
    labels();
    window.dispatchEvent(new Event('resize'));
    return true;
  }
  css.addEventListener('load', () => {
    if (!install()) { observer = new MutationObserver(() => { if (install()) observer.disconnect(); }); observer.observe(document.body,{childList:true,subtree:true}); }
  }, {once:true});
  document.head.append(css);
})();
