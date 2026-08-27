/**
 * LE PINGOUIN BLEU — SCRIPTS & INTERACTIONS
 * Plage Privée & Grillades au Barbecue | Grimaud (Est. 1989)
 */

document.addEventListener('DOMContentLoaded', () => {

  /* --------------------------------------------------------------------------
     1. DATE DU JOUR DANS LE FORMULAIRE
     -------------------------------------------------------------------------- */
  const dateInput = document.getElementById('resDate');
  if (dateInput) {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    dateInput.min = `${yyyy}-${mm}-${dd}`;
    dateInput.value = `${yyyy}-${mm}-${dd}`;
  }

  /* --------------------------------------------------------------------------
     2. PARALLAX DU VOILE D'OMBRE DES TAMARIS
     -------------------------------------------------------------------------- */
  const shadowOverlay = document.getElementById('tamariskShadowOverlay');
  let mouseX = 0, mouseY = 0;
  let currentX = 0, currentY = 0;

  window.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 16;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 10;
  });

  function animateShadow() {
    currentX += (mouseX - currentX) * 0.05;
    currentY += (mouseY - currentY) * 0.05;
    const scrollOffset = window.scrollY * 0.08;

    if (shadowOverlay) {
      shadowOverlay.style.transform = `translate(${currentX}px, ${currentY + (scrollOffset % 30)}px)`;
    }
    requestAnimationFrame(animateShadow);
  }
  animateShadow();

  /* --------------------------------------------------------------------------
     3. NAVIGATION FLOTTANTE & SCROLL SPY
     -------------------------------------------------------------------------- */
  const navbar = document.getElementById('mainNavbar');
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    let currentSectionId = '';
    const scrollPos = window.scrollY + 220;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      if (scrollPos >= top && scrollPos < top + height) {
        currentSectionId = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentSectionId}`) {
        link.classList.add('active');
      }
    });
  });

  /* --------------------------------------------------------------------------
     4. MENU MOBILE DRAWER
     -------------------------------------------------------------------------- */
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const mobileLinks = document.querySelectorAll('.mobile-nav-link');

  if (mobileMenuBtn && mobileDrawer) {
    mobileMenuBtn.addEventListener('click', () => {
      const isOpen = mobileDrawer.classList.toggle('is-open');
      mobileMenuBtn.classList.toggle('is-active');
      mobileMenuBtn.setAttribute('aria-expanded', isOpen);
    });

    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileDrawer.classList.remove('is-open');
        mobileMenuBtn.classList.remove('is-active');
      });
    });
  }

  /* --------------------------------------------------------------------------
     5. ONGLETS REGROUPÉS DE LA CARTE DU RESTAURANT
     -------------------------------------------------------------------------- */
  const menuTabBtns = document.querySelectorAll('.menu-tab-btn');
  const menuCategories = document.querySelectorAll('.menu-category-group');

  menuTabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetCategory = btn.getAttribute('data-category');

      menuTabBtns.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      menuCategories.forEach(cat => {
        if (cat.getAttribute('data-cat') === targetCategory) {
          cat.classList.remove('is-hidden');
        } else {
          cat.classList.add('is-hidden');
        }
      });
    });
  });

  /* --------------------------------------------------------------------------
     6. GALERIE PHOTO : SLIDER MOBILE (1 IMAGE À LA FOIS) & ZOOM MODAL
     -------------------------------------------------------------------------- */
  const portfolioGrid = document.getElementById('portfolioGrid');
  const portPrevBtn = document.getElementById('portPrevBtn');
  const portNextBtn = document.getElementById('portNextBtn');
  const portCurrentIndex = document.getElementById('portCurrentIndex');
  const portTotalCount = document.getElementById('portTotalCount');
  const galleryItems = document.querySelectorAll('.port-masonry-item');
  const totalGalleryItems = galleryItems.length;

  if (portTotalCount) {
    portTotalCount.textContent = String(totalGalleryItems).padStart(2, '0');
  }

  function updateMobilePortfolioCounter() {
    if (!portfolioGrid || !portCurrentIndex) return;
    const scrollLeft = portfolioGrid.scrollLeft;
    const itemWidth = portfolioGrid.clientWidth || 1;
    const activeIndex = Math.min(
      Math.max(Math.round(scrollLeft / itemWidth) + 1, 1),
      totalGalleryItems
    );
    portCurrentIndex.textContent = String(activeIndex).padStart(2, '0');
  }

  if (portfolioGrid) {
    let scrollTimeout;
    portfolioGrid.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(updateMobilePortfolioCounter, 40);
    }, { passive: true });
  }

  if (portPrevBtn && portfolioGrid) {
    portPrevBtn.addEventListener('click', () => {
      portfolioGrid.scrollBy({ left: -portfolioGrid.clientWidth, behavior: 'smooth' });
    });
  }

  if (portNextBtn && portfolioGrid) {
    portNextBtn.addEventListener('click', () => {
      portfolioGrid.scrollBy({ left: portfolioGrid.clientWidth, behavior: 'smooth' });
    });
  }

  const galleryModal = document.getElementById('galleryModal');
  const galleryModalImg = document.getElementById('galleryModalImg');
  const galleryBackdrop = document.getElementById('galleryBackdrop');
  const galleryCloseBtn = document.getElementById('galleryCloseBtn');
  const galleryModalContent = document.getElementById('galleryModalContent');

  function openGalleryModal(src, alt) {
    if (!galleryModal || !galleryModalImg) return;
    galleryModalImg.src = src;
    galleryModalImg.alt = alt || 'Photo agrandie';
    galleryModal.classList.add('is-open');
    galleryModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeGalleryModal() {
    if (!galleryModal) return;
    galleryModal.classList.remove('is-open');
    galleryModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (galleryModalImg) {
      galleryModalImg.style.transform = '';
    }
  }

  let isSwipingGrid = false;
  let gridTouchStartX = 0;
  let gridTouchStartY = 0;

  if (portfolioGrid) {
    portfolioGrid.addEventListener('touchstart', (e) => {
      isSwipingGrid = false;
      gridTouchStartX = e.touches[0].clientX;
      gridTouchStartY = e.touches[0].clientY;
    }, { passive: true });

    portfolioGrid.addEventListener('touchmove', (e) => {
      const deltaX = Math.abs(e.touches[0].clientX - gridTouchStartX);
      const deltaY = Math.abs(e.touches[0].clientY - gridTouchStartY);
      if (deltaX > 8 || deltaY > 8) {
        isSwipingGrid = true;
      }
    }, { passive: true });
  }

  galleryItems.forEach(item => {
    item.addEventListener('click', () => {
      if (isSwipingGrid) return;
      const img = item.querySelector('img');
      if (img) {
        openGalleryModal(img.src, img.alt);
      }
    });
  });

  if (galleryCloseBtn) {
    galleryCloseBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      closeGalleryModal();
    });
  }

  if (galleryBackdrop) {
    galleryBackdrop.addEventListener('click', closeGalleryModal);
  }

  if (galleryModalContent) {
    galleryModalContent.addEventListener('click', (e) => {
      if (e.target === galleryModalContent || e.target === galleryModalImg) {
        closeGalleryModal();
      }
    });
  }

  // Keyboard Escape
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && galleryModal && galleryModal.classList.contains('is-open')) {
      closeGalleryModal();
    }
  });

  // Touch / Drag to dismiss gesture
  let startY = 0;
  let currentDragY = 0;
  let isDragging = false;

  if (galleryModalContent) {
    galleryModalContent.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        startY = e.touches[0].clientY;
        isDragging = true;
      }
    }, { passive: true });

    galleryModalContent.addEventListener('touchmove', (e) => {
      if (!isDragging) return;
      currentDragY = e.touches[0].clientY - startY;
      if (galleryModalImg) {
        galleryModalImg.style.transform = `translateY(${currentDragY}px) scale(${1 - Math.min(Math.abs(currentDragY) / 1000, 0.2)})`;
      }
    }, { passive: true });

    galleryModalContent.addEventListener('touchend', () => {
      if (!isDragging) return;
      isDragging = false;
      if (Math.abs(currentDragY) > 100) {
        closeGalleryModal();
      } else {
        if (galleryModalImg) {
          galleryModalImg.style.transform = '';
        }
      }
      currentDragY = 0;
    });
  }

  /* --------------------------------------------------------------------------
     7. SÉLECTION D'EXPÉRIENCE DE RÉSERVATION
     -------------------------------------------------------------------------- */
  const heroRestaurantBtns = document.querySelectorAll('[data-type="restaurant"]');
  const heroPlageBtns = document.querySelectorAll('[data-type="plage"]');

  function selectExperienceRadio(value) {
    const radio = document.querySelector(`input[name="expType"][value="${value}"]`);
    if (radio) {
      radio.checked = true;
      document.querySelectorAll('.exp-option').forEach(opt => opt.classList.remove('active'));
      const parentLabel = radio.closest('.exp-option');
      if (parentLabel) parentLabel.classList.add('active');
    }
  }

  heroRestaurantBtns.forEach(btn => {
    btn.addEventListener('click', () => selectExperienceRadio('terrasse'));
  });

  heroPlageBtns.forEach(btn => {
    btn.addEventListener('click', () => selectExperienceRadio('matelas'));
  });

  const expOptions = document.querySelectorAll('.exp-option input');
  expOptions.forEach(radio => {
    radio.addEventListener('change', () => {
      document.querySelectorAll('.exp-option').forEach(opt => opt.classList.remove('active'));
      radio.closest('.exp-option').classList.add('active');
    });
  });

  /* --------------------------------------------------------------------------
     8. FORMULAIRE DE RÉSERVATION ET MODAL DE CONFIRMATION
     -------------------------------------------------------------------------- */
  const reservationForm = document.getElementById('reservationForm');
  const bookingModal = document.getElementById('bookingModal');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const confirmModalBtn = document.getElementById('confirmModalBtn');

  if (reservationForm && bookingModal) {
    reservationForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('resName').value || 'Client';
      const date = document.getElementById('resDate').value;
      const timeSelect = document.getElementById('resTime');
      const timeText = timeSelect.options[timeSelect.selectedIndex].text;
      const guestsSelect = document.getElementById('resGuests');
      const guestsText = guestsSelect.options[guestsSelect.selectedIndex].text;

      const checkedExp = document.querySelector('input[name="expType"]:checked');
      let expName = "Table sous les Tamaris";
      if (checkedExp) {
        if (checkedExp.value === 'sable') expName = "Table Pieds dans le Sable";
        if (checkedExp.value === 'matelas') expName = "Matelas Plage Privée";
      }

      document.getElementById('modalCustomerName').textContent = name;
      document.getElementById('modalExp').textContent = expName;
      document.getElementById('modalDateTime').textContent = `${formatDateFrench(date)} — ${timeText}`;
      document.getElementById('modalGuests').textContent = guestsText;

      bookingModal.classList.add('is-open');
      bookingModal.setAttribute('aria-hidden', 'false');
    });

    const closeModal = () => {
      bookingModal.classList.remove('is-open');
      bookingModal.setAttribute('aria-hidden', 'true');
      reservationForm.reset();
      selectExperienceRadio('terrasse');
    };

    if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
    if (confirmModalBtn) confirmModalBtn.addEventListener('click', closeModal);
    bookingModal.addEventListener('click', (e) => {
      if (e.target === bookingModal) closeModal();
    });
  }

  function formatDateFrench(dateString) {
    if (!dateString) return 'Aujourd\'hui';
    const parts = dateString.split('-');
    if (parts.length === 3) {
      return `${parts[2]}/${parts[1]}/${parts[0]}`;
    }
    return dateString;
  }

});
