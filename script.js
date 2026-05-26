// Slideshow
const slides = document.querySelectorAll('.slide');
let current = 0;

function loadSlideBg(slide) {
  if (slide.dataset.bg) {
    slide.style.backgroundImage = "url('" + slide.dataset.bg + "')";
    delete slide.dataset.bg;
  }
}

function next() {
  slides[current].classList.remove('active');
  current = (current + 1) % slides.length;
  loadSlideBg(slides[current]);
  slides[current].classList.add('active');
}

setInterval(next, 5000);

// Burger
const burger = document.getElementById('burger');
const navItems = document.getElementById('navItems');

burger.addEventListener('click', () => {
  burger.classList.toggle('open');
  navItems.classList.toggle('open');
});
