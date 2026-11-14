(() => {
  const grid = document.querySelector('#templateGrid');
  const search = document.querySelector('#search');
  const filters = [...document.querySelectorAll('.filter')];
  const count = document.querySelector('#visibleCount');
  const empty = document.querySelector('#emptyResults');
  const modal = document.querySelector('#previewModal');
  const frame = document.querySelector('#previewFrame');
  const modalTitle = document.querySelector('#modalTitle');
  const openFull = document.querySelector('#openFull');
  const modalDownload = document.querySelector('#modalDownload');
  let activeFilter = 'All';
  let templates = [];
  const escapeHtml = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const palette = {
    'midnight-glass':['#131a36','#8b7cff','#1fd1c3','#0d1228','#fff','#ffffff55','12px','-4deg',.7],
    'neon-circuit':['#03131c','#00f5ff','#006b75','#091923','#d9ffff','#00f5ff','2px','2deg',1],
    'modern-editorial':['#e5d7c7','#bc7059','#d5b19b','#f8f5ef','#30231f','#cbbbaa','0px','-1deg',0],
    'aurora-float':['#243566','#ff9ad5','#6ce6d1','#ffffff20','#fff','#ffffff60','15px','3deg',0],
    'brutalist-blocks':['#f4e900','#121212','#fff','#fff','#111','#111','0px','-2deg',0],
    'obsidian-luxe':['#0d0d0b','#d9b77a','#76582d','#11110f','#f1e7d3','#8e774d','0px','1deg',0],
    'synthwave-sunset':['#1a1040','#ff79b8','#ffb76b','#25113f','#fff','#ff79b8','3px','-3deg',.8],
    'botanical-calm':['#dce8d6','#397b5c','#aec89b','#fbfcf7','#294533','#d3e0cf','15px','2deg',0],
    'blueprint-studio':['#0c3452','#7bd4ff','#276b8d','#08243c','#e7f8ff','#4d8eaf','0px','-1deg',1],
    'prism-play':['#9476ed','#f4a0cf','#73d9e2','#ffffffdc','#282246','#ffffff','13px','-4deg',0],
    'terminal-green':['#06140a','#a4ff71','#3c8739','#08160c','#d4ffd0','#488d40','0px','1deg',1],
    'swiss-minimal':['#f4f4f1','#e24d3d','#171717','#fff','#171717','#c8c8c2','0px','0deg',0],
    'deep-ocean':['#043047','#5de6ed','#146d85','#062a3c','#eaffff','#58dce4','14px','-2deg',.5],
    'chrome-future':['#dbe0e9','#60769c','#fff','#f2f5fa','#27334d','#fff','15px','3deg',0],
    'creative-canvas':['#fff1e8','#e85b42','#7ecdc1','#fffdf9','#30243a','#f1dfd6','11px','-3deg',0],
    'command-deck':['#182740','#7e9cff','#354c78','#0c1423','#e7eeff','#52688f','6px','-1deg',1],
    'paper-craft':['#f4eadc','#d58d70','#8ea58a','#fffaf1','#332a22','#d9c7b2','2px','2deg',0],
    'architectural-form':['#d2c7b9','#9b7054','#eee8df','#f9f6f1','#302b26','#d9cfc2','0px','-2deg',0],
    'velocity-sport':['#f36b43','#ffb23f','#152237','#0d1521','#f5f7fb','#34435a','3px','-4deg',.3],
    'dragon-ember':['#35151b','#ff744e','#f8b46c','#170f15','#fff0e6','#77413c','7px','-2deg',.5]
  };
  function card(t){
    const p=palette[t.slug]||['#172033',t.accent,'#fff','#fff','#222','#aaa','8px','0deg',0];
    return `<article class="template-card" data-category="${escapeHtml(t.category)}" data-search="${escapeHtml((t.name+' '+t.desc+' '+t.category).toLowerCase())}">
      <div class="thumb" style="--thumb-bg:${p[0]};--thumb-a:${p[1]};--thumb-b:${p[2]};--thumb-card:${p[3]};--thumb-ink:${p[4]};--thumb-line:${p[5]};--thumb-radius:${p[6]};--thumb-rotate:${p[7]};--grid-opacity:${p[8]}"><div class="thumb-grid"></div><span class="thumb-stamp">${escapeHtml(t.id)} / 20</span><div class="thumb-window"><div class="thumb-title"></div><div class="thumb-field"></div><div class="thumb-field"></div><div class="thumb-button"></div></div></div>
      <div class="template-info"><div class="template-topline"><span class="template-index">DESIGN ${escapeHtml(t.id)}</span><span class="template-category">${escapeHtml(t.category)}</span></div><h3>${escapeHtml(t.name)}</h3><p>${escapeHtml(t.desc)}</p><div class="template-actions"><button type="button" class="preview-button" data-preview="${escapeHtml(t.slug)}">Preview design ↗</button><a class="download-button" href="/downloads/${escapeHtml(t.slug)}.zip" download aria-label="Download ${escapeHtml(t.name)} template ZIP" title="Download template ZIP">↓</a></div></div></article>`;
  }
  function render(){
    const q=search.value.trim().toLowerCase();
    const items=templates.filter(t=>(activeFilter==='All'||t.category===activeFilter)&&(!q||(t.name+' '+t.desc+' '+t.category).toLowerCase().includes(q)));
    grid.innerHTML=items.map(card).join('');count.textContent=String(items.length).padStart(2,'0');empty.hidden=items.length!==0;
  }
  async function init(){
    try{const response=await fetch('/templates.json');if(!response.ok)throw new Error();templates=await response.json();render();}
    catch{grid.innerHTML='<p class="empty-results">The collection could not be loaded. Refresh this page to try again.</p>';}
  }
  filters.forEach(button=>button.addEventListener('click',()=>{activeFilter=button.dataset.filter;filters.forEach(x=>x.classList.toggle('active',x===button));render();}));
  search.addEventListener('input',render);
  grid.addEventListener('click',event=>{const button=event.target.closest('[data-preview]');if(!button)return;const t=templates.find(x=>x.slug===button.dataset.preview);if(!t)return;const url=`/templates/${t.slug}/index.html`;frame.loading='eager';modalTitle.textContent=`${t.id} / ${t.name}`;frame.src=url;openFull.href=url;modalDownload.href=`/downloads/${t.slug}.zip`;modal.classList.add('open');modal.setAttribute('aria-hidden','false');document.body.classList.add('modal-open');});
  function close(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true');frame.src='about:blank';document.body.classList.remove('modal-open');}
  modal.addEventListener('click',event=>{if(event.target.closest('[data-close]'))close();});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&modal.classList.contains('open'))close();});
  document.querySelector('#year').textContent=new Date().getFullYear();
  init();
})();
