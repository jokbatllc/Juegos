document.addEventListener('DOMContentLoaded', () => {
  const html = document.documentElement;
  const stored = localStorage.getItem('theme');
  if (stored === 'dark') {
    html.classList.add('dark');
  }
  const btn = document.getElementById('theme-toggle');
  if (btn) {
    btn.addEventListener('click', () => {
      html.classList.toggle('dark');
      localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
    });
  }
});
