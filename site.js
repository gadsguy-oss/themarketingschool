/* The Marketing School — shared mobile menu (homepage + inner pages). */
(function(){
  var btn=document.querySelector('.nav-toggle'), menu=document.getElementById('mobile-menu'), nav=document.querySelector('nav');
  if(!btn||!menu) return;
  var bd=document.querySelector('.menu-backdrop');
  if(!bd){ bd=document.createElement('div'); bd.className='menu-backdrop'; document.body.appendChild(bd); }
  function isOpen(){ return menu.classList.contains('open'); }
  function setOpen(o){
    var top=nav.getBoundingClientRect().bottom+'px';
    menu.style.top=top; bd.style.top=top;
    menu.classList.toggle('open',o); bd.classList.toggle('open',o);
    btn.setAttribute('aria-expanded',o?'true':'false');
    btn.setAttribute('aria-label',o?'Close menu':'Open menu');
    document.body.style.overflow=o?'hidden':'';
    document.dispatchEvent(new CustomEvent('tms:menu',{detail:{open:o}}));
  }
  btn.addEventListener('click',function(e){ e.stopPropagation(); setOpen(!isOpen()); });
  bd.addEventListener('click',function(){ setOpen(false); });
  menu.querySelectorAll('a').forEach(function(a){ a.addEventListener('click',function(){ setOpen(false); }); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&isOpen()){ setOpen(false); btn.focus(); } });
  document.addEventListener('click',function(e){ if(isOpen()&&!menu.contains(e.target)&&!btn.contains(e.target)) setOpen(false); });
  window.addEventListener('resize',function(){ if(innerWidth>820&&isOpen()) setOpen(false); });
})();
/* Learn email signup: posts to the TMS Leads form with Source "Learn signup". */
(function(){
  document.querySelectorAll('form.ls-form').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var name=f.querySelector('[name=name]'), email=f.querySelector('[name=email]'), hp=f.querySelector('[name=company]');
      if(hp&&hp.value) return;
      if(!email.value||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)){ email.focus(); return; }
      var btn=f.querySelector('button'); if(btn){btn.disabled=true;btn.textContent='Sending…';}
      var p=new URLSearchParams(location.search), utm=['utm_source','utm_medium','utm_campaign'].map(function(k){return p.get(k)?k+'='+p.get(k):'';}).filter(Boolean);
      if(document.referrer) utm.unshift('referrer='+document.referrer);
      var lead={source:'Learn signup',name:name?name.value:'',email:email.value,contact_pref:'Email',details:'Signed up on '+location.pathname,tracking:utm.join(' | ')};
      var done=function(){ f.outerHTML='<p class="ls-done">You\'re in. New guides will land in your inbox.</p>'; try{window.tmsConversion&&window.tmsConversion('learn',{path:location.pathname});}catch(x){} };
      try{ (window.tmsSubmitLead?window.tmsSubmitLead(lead):Promise.resolve()).then(done,done); }catch(x){ done(); }
    });
  });
})();
