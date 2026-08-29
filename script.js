// SPReAD Project Academic Homepage Scripts
document.addEventListener('DOMContentLoaded', () => {
  // 1. Theme Toggle
  const themeToggleBtn = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const savedTheme = localStorage.getItem('spread_theme');

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('spread_theme', theme);
    if (themeIcon) {
      themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
  }

  if (savedTheme) {
    setTheme(savedTheme);
  } else if (prefersDark) {
    setTheme('dark');
  } else {
    setTheme('light');
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
      setTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });
  }

  // 2. Lightbox Modal for Figures
  const modalOverlay = document.getElementById('modal-overlay');
  const modalImg = document.getElementById('modal-img');
  const modalCaption = document.getElementById('modal-caption');
  const modalCloseBtn = document.getElementById('modal-close-btn');

  function openModal(src, caption) {
    if (modalOverlay && modalImg) {
      modalImg.src = src;
      if (modalCaption) modalCaption.textContent = caption || '';
      modalOverlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeModal() {
    if (modalOverlay) {
      modalOverlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  document.querySelectorAll('.zoomable-fig').forEach(fig => {
    fig.addEventListener('click', () => {
      const img = fig.querySelector('img');
      const caption = fig.getAttribute('data-caption') || (img ? img.alt : '');
      if (img) openModal(img.src, caption);
    });
  });

  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });

  // 3. Toast Notifications & Clipboard Copy
  const toast = document.getElementById('toast');
  const toastMsg = document.getElementById('toast-msg');

  function showToast(message) {
    if (toast && toastMsg) {
      toastMsg.textContent = message;
      toast.classList.add('show');
      setTimeout(() => {
        toast.classList.remove('show');
      }, 3000);
    }
  }

  window.copyTextToClipboard = function(text, successMsg = 'Copied to clipboard!') {
    navigator.clipboard.writeText(text).then(() => {
      showToast(successMsg);
    }).catch(err => {
      console.error('Failed to copy:', err);
    });
  };

  // 4. Abstract toggle in publications
  document.querySelectorAll('.toggle-abstract-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        const isHidden = targetEl.style.display === 'none' || targetEl.style.display === '';
        targetEl.style.display = isHidden ? 'block' : 'none';
        btn.textContent = isHidden ? 'Hide Abstract' : 'Show Abstract';
      }
    });
  });

  // 5. Copy BibTeX Citation
  window.copyBibtexCitation = function() {
    const el = document.getElementById('bibtex-citation-code');
    if (el) {
      window.copyTextToClipboard(el.textContent.trim(), 'BibTeX citation copied to clipboard!');
    }
  };
});
