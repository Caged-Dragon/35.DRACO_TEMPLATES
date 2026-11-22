/* CAGED_DRAGON central product portals. No credentials, analytics, or cross-site session sharing. */
(function () {
  'use strict';
  const app = "Templates";
  const current = "templates";
  const signInPath = "";
  const destinations = [["accounts", "Accounts", "https://draco-accounts.caged-dragon.vercel.app/"], ["feedback", "Feedback", "https://draco-feedback.caged-dragon.vercel.app/"], ["care", "Customer Care", "https://draco-customer-care.caged-dragon.vercel.app/"], ["payment", "Payment (demo)", "https://draco-payment-gateway.caged-dragon.vercel.app/"], ["authenticator", "Authenticator", "https://draco-authenticator.caged-dragon.vercel.app/"], ["portfolio", "Portfolio", "https://draco-portfolio.caged-dragon.vercel.app/"]];
  const translate = document.documentElement.lang.toLowerCase().startsWith('ta');
  function node(tag, attributes, value) {
    const el = document.createElement(tag);
    for (const [key, val] of Object.entries(attributes || {})) el.setAttribute(key, val);
    if (value) el.textContent = value;
    return el;
  }
  function install() {
    if (document.querySelector('[data-cd-portals]')) return;
    const script = document.querySelector('script[src*="cd-central-portals.js"]');
    const prefix = script ? new URL('.', script.src).href : '/';
    const style = node('link', {rel: 'stylesheet', href: prefix + 'cd-central-portals.css'});
    document.head.appendChild(style);
    const details = node('details', {'class':'cd-portals', 'data-cd-portals':'', 'aria-label':'CAGED_DRAGON services'});
    const summary = node('summary', {}, translate ? 'CAGED_DRAGON சேவைகள்' : 'CAGED_DRAGON Portals');
    details.appendChild(summary);
    const nav = node('nav', {'aria-label': translate ? 'மைய சேவைகள்' : 'Central services'});
    const heading = node('p', {'class':'cd-portals-title'}, translate ? app + ' · உதவி இணைப்புகள்' : app + ' · Quick links');
    nav.appendChild(heading);
    if (signInPath) {
      const signIn = node('a', {href:signInPath, 'class':'cd-portals-signin'}, translate ? 'உள்நுழை' : 'Sign in / Login');
      nav.appendChild(signIn);
    }
    for (const [id, label, url] of destinations) {
      if (id === current) continue;
      nav.appendChild(node('a', {href:url, rel:'noopener noreferrer'}, label));
    }
    const note = node('p', {'class':'cd-portals-note'}, translate ? 'பாதுகாப்பான உள்நுழைவு தயாரிப்பில் தொடங்கும்.' : 'Secure sign-in always begins in its product.');
    nav.appendChild(note);
    details.appendChild(nav);
    document.body.appendChild(details);
    details.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') { details.open = false; summary.focus(); }
    });
    document.addEventListener('pointerdown', function(event) {
      if (details.open && !details.contains(event.target)) details.open = false;
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', install, {once:true});
  else install();
})();
