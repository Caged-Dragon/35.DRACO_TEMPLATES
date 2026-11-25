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
