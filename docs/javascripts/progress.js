document$.subscribe(function() {
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach(cb => {
    const key = 'task-' + cb.closest('article').querySelector('h1').innerText + '-' + cb.closest('li').innerText;
    const saved = localStorage.getItem(key);
    if (saved !== null) cb.checked = saved === 'true';
    cb.addEventListener('change', () => {
      localStorage.setItem(key, cb.checked);
    });
  });
});
