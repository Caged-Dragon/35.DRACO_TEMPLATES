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

/* CAGED_DRAGON opening film v2. Asset SHA-1 matches ANIMATION.zip; no analytics. */
(function () {
  'use strict';
  const BASE = 'https://draco-timeforge.caged-dragon.vercel.app/intro/';
  const SEEN = 'cd:intro:v2:seen';
  function installIntro() {
    if (!document.body || (location.pathname !== '/' && location.pathname !== '/index.html')) return;
    if (window.self !== window.top || document.querySelector('[data-cd-intro-v2]')) return;
    const params = new URLSearchParams(location.search);
    if (['code', 'access_token', 'refresh_token', 'token_hash', 'error', 'error_description'].some(key => params.has(key)) ||
        /(?:^|[&#])(access_token|refresh_token|code|error)=/i.test(location.hash)) return;
    try { if (sessionStorage.getItem(SEEN) === '1') return; } catch { /* private mode */ }
    const portrait = window.matchMedia && window.matchMedia('(orientation: portrait)').matches;
    const film = document.createElement('video');
    film.className = 'cd-intro-v2-film';
    film.src = BASE + (portrait ? 'caged-dragon-portrait.mp4' : 'caged-dragon-landscape.mp4');
    film.poster = BASE + (portrait ? 'portrait-poster.jpg' : 'landscape-poster.jpg');
    film.preload = 'auto';
    film.playsInline = true;
    film.defaultMuted = false;
    film.muted = false;
    film.volume = 1;
    film.setAttribute('aria-label', 'CAGED DRAGON cinematic opening with soundtrack');
    const root = document.createElement('section');
    root.className = 'cd-intro-v2';
    root.setAttribute('data-cd-intro-v2', '');
    root.setAttribute('role', 'dialog');
    root.setAttribute('aria-modal', 'true');
    root.setAttribute('aria-label', 'CAGED DRAGON opening film');
    const panel = document.createElement('div');
    panel.className = 'cd-intro-v2-panel';
    const kicker = document.createElement('p');
    kicker.className = 'cd-intro-v2-kicker';
    kicker.textContent = 'CAGED DRAGON';
    const heading = document.createElement('h2');
    heading.textContent = 'The dragon awakens';
    const message = document.createElement('p');
    message.className = 'cd-intro-v2-message';
    message.setAttribute('role', 'status');
    message.textContent = 'Preparing the opening film with its original soundtrack…';
    const actions = document.createElement('div');
    actions.className = 'cd-intro-v2-actions';
    const play = document.createElement('button');
    play.type = 'button';
    play.className = 'cd-intro-v2-play';
    play.textContent = 'Play intro with sound';
    const skip = document.createElement('button');
    skip.type = 'button';
    skip.className = 'cd-intro-v2-enter';
    skip.textContent = 'Enter product';
    const playingSkip = document.createElement('button');
    playingSkip.type = 'button';
    playingSkip.className = 'cd-intro-v2-skip';
    playingSkip.textContent = 'Skip intro';
    const note = document.createElement('small');
    note.textContent = 'The product opens as soon as the film finishes.';
    actions.append(play, skip);
    panel.append(kicker, heading, message, actions, note);
    root.append(film, panel, playingSkip);
    const focusBefore = document.activeElement;
    let finished = false;
    function finish() {
      if (finished) return;
      finished = true;
      film.pause();
      film.removeAttribute('src');
      film.load();
      try { sessionStorage.setItem(SEEN, '1'); } catch { /* storage may be blocked */ }
      root.remove();
      if (focusBefore && focusBefore.isConnected && typeof focusBefore.focus === 'function') {
        try { focusBefore.focus({ preventScroll: true }); } catch { /* no longer focusable */ }
      }
    }
    function soundOn() {
      if (finished) return;
      film.defaultMuted = false;
      film.muted = false;
      film.volume = 1;
      try { film.currentTime = 0; } catch { /* media not buffered */ }
      message.textContent = 'Starting the original soundtrack…';
      let attempt;
      try { attempt = film.play(); } catch { message.textContent = 'Sound could not start. You can enter the product.'; return; }
      if (attempt && typeof attempt.catch === 'function') attempt.catch(() => {
        if (!finished) message.textContent = 'Your browser could not start sound. Check audio permissions or enter the product.';
      });
    }
    film.addEventListener('playing', () => {
      if (!finished) {
        root.classList.add('cd-intro-v2-playing');
        try { playingSkip.focus({ preventScroll: true }); } catch { /* no focus support */ }
      }
    });
    film.addEventListener('ended', finish);
    film.addEventListener('error', () => {
      if (!finished) {
        message.textContent = 'The film could not load. You can still enter the product.';
        play.disabled = true;
      }
    });
    play.addEventListener('click', soundOn);
    skip.addEventListener('click', finish);
    playingSkip.addEventListener('click', finish);
    root.addEventListener('keydown', event => {
      if (event.key === 'Escape') { event.preventDefault(); finish(); }
      if (event.key === 'Tab') {
        const options = root.classList.contains('cd-intro-v2-playing') ? [playingSkip] : [play, skip].filter(x => !x.disabled);
        const first = options[0], last = options[options.length - 1];
        if (first && ((event.shiftKey && document.activeElement === first) ||
          (!event.shiftKey && document.activeElement === last))) {
          event.preventDefault();
          (event.shiftKey ? last : first).focus();
        }
      }
    });
    document.body.appendChild(root);
    try { play.focus({ preventScroll: true }); } catch { /* no focus support */ }
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      message.textContent = 'Motion is reduced on this device. Play the film with sound, or enter the product.';
      return;
    }
    let attempt;
    try { attempt = film.play(); } catch { attempt = null; }
    if (attempt && typeof attempt.catch === 'function') attempt.catch(() => {
      if (!finished && !root.classList.contains('cd-intro-v2-playing')) {
        message.textContent = 'Your browser requires one tap to allow the original soundtrack.';
      }
    });
    else if (!attempt) message.textContent = 'Tap Play intro with sound to start the opening film.';
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', installIntro, { once: true });
  else installIntro();
})();
