import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

function initProgressTracking(): void {
  const article = document.querySelector('article');
  if (!article) {
    return;
  }

  const checkboxes = article.querySelectorAll<HTMLInputElement>(
    'input[type="checkbox"]',
  );
  if (checkboxes.length === 0) {
    return;
  }

  const pageKey = window.location.pathname;

  checkboxes.forEach((checkbox, index) => {
    // Enable the checkbox (Docusaurus renders them disabled by default)
    checkbox.disabled = false;
    checkbox.style.cursor = 'pointer';

    // Build a storage key from page path + index + label text
    const label =
      checkbox.closest('li')?.textContent?.trim().slice(0, 60) ?? String(index);
    const storageKey = `progress:${pageKey}:${index}:${label}`;

    // Restore saved state
    const saved = localStorage.getItem(storageKey);
    if (saved === 'true') {
      checkbox.checked = true;
    }

    // Save on change
    checkbox.addEventListener('change', () => {
      localStorage.setItem(storageKey, String(checkbox.checked));
    });
  });
}

if (ExecutionEnvironment.canUseDOM) {
  // Run on initial load
  if (document.readyState === 'complete') {
    initProgressTracking();
  } else {
    window.addEventListener('load', initProgressTracking);
  }

  // Re-run on client-side navigation
  const observer = new MutationObserver(() => {
    initProgressTracking();
  });

  const startObserver = (): void => {
    const target = document.getElementById('__docusaurus');
    if (target) {
      observer.observe(target, {childList: true, subtree: true});
    }
  };

  if (document.readyState === 'complete') {
    startObserver();
  } else {
    window.addEventListener('load', startObserver);
  }
}
