(function(){
  const root = document.documentElement;
  const btn = document.querySelector('[data-theme-toggle]');
  const stored = localStorage.getItem('theme');
  if(stored === 'dark'){ root.classList.add('theme-dark'); }

  btn && btn.addEventListener('click', ()=> {
    root.classList.toggle('theme-dark');
    const isDark = root.classList.contains('theme-dark');
    localStorage.setItem('theme', isDark ? 'dark':'light');
  });

  // activar link actual
  const links = document.querySelectorAll('.nav-links a');
  links.forEach(a=>{
    if(location.pathname.startsWith(a.getAttribute('href'))){
      a.classList.add('active');
    }
  });
})();
