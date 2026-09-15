document.querySelectorAll('.sage-menu a').forEach(link => {
  link.addEventListener('click', () => {
    link.closest('details').open = false;
  });
});
document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  const menu = document.querySelector('.sage-menu[open]');
  if (menu) {
    menu.open = false;
    menu.querySelector('summary').focus();
  }
});
