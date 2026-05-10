// Slideshow
const slides = document.querySelectorAll('.slide');
let current = 0;

function next() {
  slides[current].classList.remove('active');
  current = (current + 1) % slides.length;
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
