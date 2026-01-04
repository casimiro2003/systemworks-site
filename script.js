// ============================================
// PORTFOLIO SITE SCRIPTS
// ============================================

// ============ ANIMATED COUNTERS ============
function animateCounters() {
  const counters = document.querySelectorAll('.stat-number');

  counters.forEach(counter => {
    const target = counter.innerText;
    const isNumber = /^\d+/.test(target);

    if (!isNumber) return;

    const num = parseInt(target);
    const suffix = target.replace(/\d+/, '');
    let current = 0;
    const increment = num / 50;
    const duration = 1500;
    const stepTime = duration / 50;

    counter.innerText = '0' + suffix;

    const updateCounter = () => {
      current += increment;
      if (current < num) {
        counter.innerText = Math.floor(current) + suffix;
        setTimeout(updateCounter, stepTime);
      } else {
        counter.innerText = target;
      }
    };

    updateCounter();
  });
}

// Trigger counters when stats section is visible
const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateCounters();
      statsObserver.disconnect();
    }
  });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.hero-stats');
if (statsSection) statsObserver.observe(statsSection);

// Handle contact form submission
document.getElementById('contactForm').addEventListener('submit', function(e) {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  fetch('https://formspree.io/f/xvzgdgrj', {
    method: 'POST',
    body: formData,
    headers: { 'Accept': 'application/json' }
  })
  .then(response => {
    if (response.ok) {
      alert('Thanks! We\'ll get back to you within 24 hours.');
      form.reset();
    } else {
      alert('Oops! Something went wrong. Please try again.');
    }
  })
  .catch(error => {
    alert('Oops! Something went wrong. Please try again.');
  });
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Add shadow to nav on scroll
window.addEventListener('scroll', function() {
  const nav = document.querySelector('.nav');
  if (window.scrollY > 50) {
    nav.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
  } else {
    nav.style.boxShadow = 'none';
  }
});

// Animate elements on scroll (simple fade-in)
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, observerOptions);

// Apply to cards
document.querySelectorAll('.service-card, .work-card, .pricing-card, .process-step').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});
