/* CAGED_DRAGON central product portals. No credentials, analytics, or cross-site session sharing. */
(function () {
  'use strict';
  const app = "Templates";
  const current = "templates";
  const signInPath = "";
  // CAGED_DRAGON searchable ecosystem 2026-11-22
  const destinations = [["accounts","Accounts","https://draco-accounts.caged-dragon.vercel.app/","கணக்குகள்"],["feedback","Feedback","https://draco-feedback.caged-dragon.vercel.app/","கருத்துகள்"],["care","Customer Care","https://draco-customer-care.caged-dragon.vercel.app/","வாடிக்கையாளர் உதவி"],["payment","Payment (demo)","https://draco-payment-gateway.caged-dragon.vercel.app/","மாதிரி கட்டணம்"],["authenticator","Authenticator","https://draco-authenticator.caged-dragon.vercel.app/","அங்கீகாரச் செயலி"],["portfolio","Portfolio","https://draco-portfolio.caged-dragon.vercel.app/","திட்டங்களின் தொகுப்பு"],["chat","Draco Chat","https://draco-chat.caged-dragon.vercel.app/","டிராகோ அரட்டை"],["mail","Draco Mail","https://draco-mail.caged-dragon.vercel.app/","டிராகோ அஞ்சல்"],["meet","Draco Meet","https://draco-meet.caged-dragon.vercel.app/","டிராகோ சந்திப்பு"],["calendar","Draco Calendar","https://draco-calender.caged-dragon.vercel.app/","டிராகோ நாள்காட்டி"],["timeforge","Draco TimeForge","https://draco-timeforge.caged-dragon.vercel.app/","டிராகோ நேர மேலாண்மை"],["office","Draco Office","https://draco-office.caged-dragon.vercel.app/","டிராகோ அலுவலகம்"],["drive","Draco Drive","https://draco-drive.caged-dragon.vercel.app/","டிராகோ இயக்ககம்"],["files","Draco Files","https://draco-files.caged-dragon.vercel.app/","டிராகோ கோப்புகள்"],["docs","Draco Docs","https://draco-docs.caged-dragon.vercel.app/","டிராகோ ஆவணங்கள்"],["sheets","Draco Sheets","https://draco-sheets.caged-dragon.vercel.app/","டிராகோ தாள்கள்"],["slides","Draco Slides","https://draco-slides.caged-dragon.vercel.app/","டிராகோ விளக்கக்காட்சிகள்"],["code","Draco Code","https://draco-code.caged-dragon.vercel.app/","டிராகோ குறியீடு"],["webhub","Draco WebHub","https://draco-webhub.caged-dragon.vercel.app/","டிராகோ இணைய மையம்"],["store","Draco Store","https://draco-store.caged-dragon.vercel.app/","டிராகோ கடை"],["cart","Draco Cart","https://draco-cart.caged-dragon.vercel.app/","டிராகோ வண்டி"],["templates","Draco Templates","https://draco-template.caged-dragon.vercel.app/","டிராகோ வார்ப்புருக்கள்"],["gamehub","Draco Game Hub","https://draco-game-hub.caged-dragon.vercel.app/","டிராகோ விளையாட்டு மையம்"],["2042","Draco 2042","https://draco-2042.caged-dragon.vercel.app/","டிராகோ 2042"],["tic-tac-toe","Tic-Tac-Toe","https://draco-tic-tac-toe.caged-dragon.vercel.app/","டிக் டாக் டோ"],["sudoku","Sudoku","https://draco-soduku.caged-dragon.vercel.app/","சுடோகு"],["serpant","Serpent","https://draco-serpant.caged-dragon.vercel.app/","பாம்பு விளையாட்டு"],["breaker","Breaker","https://draco-breaker.caged-dragon.vercel.app/","பிரேக்கர்"],["flight","Flight","https://draco-flight.caged-dragon.vercel.app/","விமான விளையாட்டு"],["strike","Strike","https://draco-strike.caged-dragon.vercel.app/","ஸ்ட்ரைக்"],["fire-clash","Fire Clash","https://draco-fire-clash.caged-dragon.vercel.app/","நெருப்பு மோதல்"],["chess","Chess","https://draco-chess.caged-dragon.vercel.app/","சதுரங்கம்"]];
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
    const search = node('input', {type:'search', 'aria-label':translate?'செயலிகளைத் தேடுக':'Search products', placeholder:translate?'செயலிகளைத் தேடுக':'Search products'});
    search.style.cssText='width:100%;min-height:44px;padding:10px;border-radius:8px;border:1px solid #94a3b8;color:#172237;background:#fff';
    nav.appendChild(search);
    const links=[];
    for (const [id, label, url, tamil] of destinations) {
      if (id === current) continue;
      const link=node('a',{href:url,rel:'noopener noreferrer'},translate?tamil:label);
      link.dataset.search=(label+' '+tamil+' '+id).toLowerCase();
      nav.appendChild(link);links.push(link);
    }
    const result=node('p',{role:'status','aria-live':'polite','class':'cd-portals-note'},links.length+' products');
    nav.appendChild(result);
    search.addEventListener('input',()=>{const q=search.value.trim().toLowerCase();let count=0;
      for(const link of links){const visible=link.dataset.search.includes(q);link.style.display=visible?'':'none';if(visible)count++;}
      result.textContent=count?count+' products':(translate?'பொருந்தும் செயலிகள் இல்லை':'No matching products');
    });
    details.addEventListener('toggle',()=>{if(details.open)search.focus();});
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


/* Shared CAGED_DRAGON cinematic introduction, supplied landscape/portrait MP4.
 * Works with existing cd-central-portals.js; never alters authentication, routing or product data.
 * Browsers may reject unmuted autoplay. Do not bypass their playback permissions.
 */
(function () {
  'use strict';
  if (typeof window === 'undefined' || window.top !== window.self || window.__cdIntroInstalled) return;
  if (location.pathname !== '/' && location.pathname !== '/index.html') return;
  if (/[?&](?:code|state|error|token|invite|recover|access_token|refresh_token)=/i.test(location.search)) return;
  window.__cdIntroInstalled = true;
  const seenKey = 'cd:cinematic-intro:seen:v1';
  try { if (sessionStorage.getItem(seenKey) === '1') return; } catch { /* storage disabled */ }

  // The exact supplied ZIP media already exists in TimeForge, verified using Git blob SHA-1.
  const rootUrl = 'https://draco-timeforge.caged-dragon.vercel.app/intro/';
  const portrait = Boolean(window.matchMedia && window.matchMedia('(orientation: portrait)').matches);
  const source = rootUrl + (portrait ? 'caged-dragon-portrait.mp4' : 'caged-dragon-landscape.mp4');
  const poster = rootUrl + (portrait ? 'portrait-poster.jpg' : 'landscape-poster.jpg');

  function install() {
    if (!document.body || document.getElementById('cd-cinematic-intro')) return;
    const css = document.createElement('style');
    css.textContent = [
      '.cd-cinematic-intro{position:fixed!important;inset:0!important;z-index:2147483646!important;background:#08090e!important;color:white!important;isolation:isolate;font:16px/1.45 system-ui,sans-serif;overflow:hidden}',
      '.cd-cinematic-intro video{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}',
      '.cd-cinematic-intro .cd-intro-blur{object-fit:cover;transform:scale(1.1);filter:blur(35px) brightness(.36);opacity:.8}',
      '.cd-cinematic-intro .cd-intro-film{object-fit:contain;z-index:1}',
      '.cd-cinematic-intro button{font:600 14px/1.2 system-ui,sans-serif;min-height:44px;padding:12px 18px;border-radius:10px;border:1px solid #f3cf8b;background:#e4b862;color:#16120c;cursor:pointer}',
      '.cd-cinematic-intro button:focus-visible{outline:3px solid white;outline-offset:3px}',
      '.cd-cinematic-intro .cd-intro-skip{position:absolute;z-index:5;top:18px;right:18px;background:#13151bdf;color:white;border:1px solid #ffffff8c}',
      '.cd-cinematic-intro .cd-intro-launch{position:absolute;z-index:4;inset:0;display:grid;place-items:center;padding:20px;background:#080a11ba}',
      '.cd-cinematic-intro .cd-intro-launch[hidden]{display:none}',
      '.cd-cinematic-intro .cd-intro-panel{width:min(480px,100%);padding:clamp(20px,4vw,34px);border:1px solid #ffffff55;border-radius:20px;background:#10111bed;text-align:center;box-shadow:0 22px 70px #000a}',
      '.cd-cinematic-intro .cd-intro-panel h2{color:white!important;font:bold clamp(24px,4vw,34px)/1.15 system-ui,sans-serif;margin:0 0 12px}',
      '.cd-cinematic-intro .cd-intro-panel p{color:#f2e7d3!important;margin:0 0 22px}',
      '.cd-cinematic-intro .cd-intro-actions{display:flex;justify-content:center;gap:10px;flex-wrap:wrap}',
      '.cd-cinematic-intro .cd-intro-enter{background:#262836;color:white;border-color:#ffffff70}',
      '@media(max-width:480px){.cd-cinematic-intro .cd-intro-actions{flex-direction:column}.cd-cinematic-intro .cd-intro-actions button{width:100%}}',
      '@media(prefers-reduced-motion:reduce){.cd-cinematic-intro .cd-intro-blur{display:none}}'
    ].join('\n');
    document.head.appendChild(css);

    const root = document.createElement('section');
    root.id = 'cd-cinematic-intro';
    root.className = 'cd-cinematic-intro';
    root.setAttribute('role', 'dialog');
    root.setAttribute('aria-modal', 'true');
    root.setAttribute('aria-label', 'Caged Dragon opening film');
    const blur = document.createElement('video');
    blur.className = 'cd-intro-blur';
    blur.muted = true; blur.playsInline = true; blur.tabIndex = -1;
    blur.setAttribute('aria-hidden', 'true');
    blur.src = source;
    const film = document.createElement('video');
    film.className = 'cd-intro-film';
    film.playsInline = true; film.preload = 'auto'; film.poster = poster; film.src = source;
    film.muted = false; film.volume = 1;
    const skip = document.createElement('button');
    skip.type = 'button'; skip.className = 'cd-intro-skip'; skip.textContent = 'Skip intro';
    const launch = document.createElement('div');
    launch.className = 'cd-intro-launch'; launch.hidden = true;
    const panel = document.createElement('div');
    panel.className = 'cd-intro-panel';
    const heading = document.createElement('h2');
    heading.textContent = 'CAGED DRAGON';
    const note = document.createElement('p');
    note.setAttribute('role', 'status');
    const actions = document.createElement('div');
    actions.className = 'cd-intro-actions';
    const play = document.createElement('button');
    play.type = 'button'; play.textContent = 'Play intro with sound';
    const enter = document.createElement('button');
    enter.type = 'button'; enter.className = 'cd-intro-enter'; enter.textContent = 'Enter product';
    actions.append(play, enter); panel.append(heading, note, actions); launch.append(panel);
    root.append(blur, film, skip, launch);
    document.body.appendChild(root);
    // A strict CSP that disallows inline styles should fail open, never block the product.
    if (getComputedStyle(root).position !== 'fixed') { root.remove(); css.remove(); return; }

    let ended = false;
    const priorFocus = document.activeElement;
    function finish() {
      if (ended) return;
      ended = true; film.pause(); blur.pause();
      root.remove(); css.remove();
      try { sessionStorage.setItem(seenKey, '1'); } catch { /* storage disabled */ }
      if (priorFocus && priorFocus.isConnected && typeof priorFocus.focus === 'function')
        priorFocus.focus({ preventScroll: true });
    }
    function prompt(message) {
      if (ended) return;
      note.textContent = message; launch.hidden = false;
      play.focus({ preventScroll: true });
    }
    function playing() {
      if (ended) return;
      launch.hidden = true;
      try { blur.currentTime = film.currentTime; } catch { /* decoration only */ }
      void Promise.resolve(blur.play()).catch(() => {});
    }
    function playWithSound() {
      if (ended) return;
      film.muted = false; film.volume = 1;
      try { film.currentTime = 0; } catch { /* media not ready */ }
      void Promise.resolve(film.play()).then(playing)
        .catch(() => prompt('Your browser blocked audio. Try Play intro with sound, or enter the product.'));
    }
    film.addEventListener('ended', finish);
    film.addEventListener('error', () => prompt('The video could not load. You can enter the product.'));
    skip.addEventListener('click', finish);
    enter.addEventListener('click', finish);
    play.addEventListener('click', playWithSound);
    root.addEventListener('keydown', e => { if (e.key === 'Escape') finish(); });
    window.addEventListener('pagehide', () => { film.pause(); blur.pause(); }, { once: true });
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      prompt('Play the opening film with sound, or enter the product.');
    } else {
      void Promise.resolve(film.play()).then(playing)
        .catch(() => prompt('Your browser requires one click to play the original soundtrack.'));
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', install, { once: true });
  else install();
})();
