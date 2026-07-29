// EduManage Main Javascript Engine

document.addEventListener('DOMContentLoaded', function() {

  // 1. Hide Page Loader
  const loader = document.querySelector('.page-loader');
  if (loader) {
    setTimeout(() => {
      loader.style.opacity = '0';
      setTimeout(() => loader.remove(), 300);
    }, 200);
  }

  // 1b. Initialize Modern Flatpickr Date Picker
  if (typeof flatpickr !== 'undefined') {
    flatpickr('input[type="date"]', {
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "F j, Y",
      allowInput: true,
      animate: true
    });
  }

  // 2. Sidebar Mobile Toggle & Overlay
  const sidebar = document.querySelector('.sidebar');
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  const sidebarClose = document.querySelector('.sidebar-close-btn');
  const sidebarOverlay = document.querySelector('.sidebar-overlay');

  function openSidebar() {
    if (sidebar) sidebar.classList.add('open');
    if (sidebarOverlay) sidebarOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('open');
    if (sidebarOverlay) sidebarOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      if (sidebar && sidebar.classList.contains('open')) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
  }

  if (sidebarClose) {
    sidebarClose.addEventListener('click', closeSidebar);
  }

  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeSidebar);
  }

  window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
      closeSidebar();
    }
  });

  // 3. Highlight Active Navigation Item
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar .nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href !== '#' && (currentPath === href || (href !== '/' && currentPath.startsWith(href)))) {
      link.classList.add('active');
    }
  });

  // 4. Auto Dismiss Alerts
  setTimeout(() => {
    document.querySelectorAll('.alert-dismissible').forEach(alert => {
      alert.style.transition = 'opacity 0.4s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 400);
    });
  }, 4500);

  // 5. Select All Present for Attendance
  const selectAllBtn = document.querySelector('#selectAllPresent');
  if (selectAllBtn) {
    selectAllBtn.addEventListener('click', function() {
      document.querySelectorAll('input[type="radio"][value="present"]').forEach(radio => {
        radio.checked = true;
      });
    });
  }

  // 6. Realtime Grade Calculation in Exam Results Entry
  document.querySelectorAll('.marks-input').forEach(input => {
    const updateGrade = function() {
      const val = parseFloat(input.value);
      const totalMarks = parseFloat(input.dataset.max || 100);
      const gradeBadge = input.closest('tr').querySelector('.grade-cell');

      if (isNaN(val) || val < 0) {
        if (gradeBadge) {
          gradeBadge.textContent = '-';
          gradeBadge.className = 'grade-cell badge badge-secondary';
        }
        return;
      }

      const pct = (val / totalMarks) * 100;
      let grade = 'F';
      let badgeClass = 'badge-soft-danger';

      if (pct >= 90) { grade = 'A+'; badgeClass = 'badge-soft-primary'; }
      else if (pct >= 80) { grade = 'A'; badgeClass = 'badge-soft-primary'; }
      else if (pct >= 70) { grade = 'B+'; badgeClass = 'badge-soft-success'; }
      else if (pct >= 60) { grade = 'B'; badgeClass = 'badge-soft-success'; }
      else if (pct >= 50) { grade = 'C'; badgeClass = 'badge-soft-warning'; }
      else if (pct >= 40) { grade = 'D'; badgeClass = 'badge-soft-warning'; }
      else { grade = 'F'; badgeClass = 'badge-soft-danger'; }

      if (gradeBadge) {
        gradeBadge.textContent = grade;
        gradeBadge.className = `grade-cell ${badgeClass}`;
      }
    };

    input.addEventListener('input', updateGrade);
    input.addEventListener('keyup', updateGrade);
  });

  // 7. Profile Image Preview
  const imageInput = document.querySelector('#profileImageInput');
  const imagePreview = document.querySelector('#profilePreview');
  if (imageInput && imagePreview) {
    imageInput.addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          imagePreview.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  }

});

// Global Function for Confirm Delete Modal
function confirmDelete(deleteUrl, itemName) {
  const modalElem = document.getElementById('deleteConfirmModal');
  if (modalElem) {
    const itemNameSpan = modalElem.querySelector('.item-name');
    const confirmBtn = modalElem.querySelector('.confirm-delete-btn');
    if (itemNameSpan) itemNameSpan.textContent = itemName;
    if (confirmBtn) confirmBtn.href = deleteUrl;

    const modal = new bootstrap.Modal(modalElem);
    modal.show();
  } else {
    if (confirm(`Are you sure you want to delete "${itemName}"?`)) {
      window.location.href = deleteUrl;
    }
  }
}
