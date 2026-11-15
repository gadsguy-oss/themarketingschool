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
