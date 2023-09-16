// Animated Scroll Reveal
AOS.init();


// Smooth scrolling for logo and CTA button
$(document).ready(function() {
    if (window.location.pathname === '/') {
        $("a.logo, a.cta-button").on('click', function(event) {
            if (this.hash !== "") {
                event.preventDefault();

                var hash = this.hash;

                $('html, body').animate({
                    scrollTop: $(hash).offset().top
                }, 800, function(){
                    window.location.hash = hash;
                });
            }
        });
    }
});


// Smooth scrolling for navigation links
  if (window.matchMedia('(max-width: 768px)').matches) {
    const toggleButton = document.getElementById('toggleButton');
  }

$(document).ready(function() {
    if (window.location.pathname === '/') {
        $("a.nav-link").on('click', function(event) {
            if (this.hash !== "") {
                event.preventDefault();

                var hash = this.hash;

                $('html, body').animate({
                    scrollTop: $(hash).offset().top
                }, 800, function(){
                    window.location.hash = hash;
                    if (window.matchMedia('(max-width: 768px)').matches) {
                         toggleButton.click();
                         toggleButton.classList.add('collapsed')
                         toggleButton.classList.remove('toggle-active')
                    }

                });
            }
        });
    }
});


// Navbar links active state on scroll
const navbarlinks = document.querySelectorAll('#navbar .scrollto')

const navbarlinksActive = () => {
  let position = window.scrollY + 200
  navbarlinks.forEach(navbarlink => {
    if (!navbarlink.hash) return
    let section = document.querySelector(navbarlink.hash)
    if (!section) return
    if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
      navbarlink.classList.add('active')
    } else {
      navbarlink.classList.remove('active')
    }
  })
}

window.addEventListener('load', navbarlinksActive)
window.addEventListener('scroll', navbarlinksActive)


/* When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar */
var prevScrollpos = window.pageYOffset;
var header = document.getElementById("header");

window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    header.classList.remove("slide-up");
    header.classList.add("slide-down");
  } else {
    header.classList.remove("slide-down");
    header.classList.add("slide-up");
  }
  prevScrollpos = currentScrollPos;
}


// Toggle button animation
const toggleButton = document.getElementById('toggleButton');

toggleButton.addEventListener('click', function() {
  toggleButton.classList.toggle('toggle-active');
});


// Hero typing effect
    document.addEventListener('DOMContentLoaded', function() {
      var typed = new Typed('.typed', {
        strings: ['Web Developer', 'Python Developer', 'UI/UX Designer', 'Medical Student'],
        loop: true,
        typeSpeed: 100,
        backSpeed: 50,
        backDelay: 2000
        });
    });


// Portfolio Section
$('#portfolio-tabs a').on('click', function (e) {
    e.preventDefault();
    $(this).tab('show');
});


// Smooth scrolling for Portfolio navlinks
$(document).ready(function() {
    if (window.location.pathname === '/Portfolio') {
        $("#portfolio-tabs a").on('click', function(event) {
            if (this.hash !== "") {
                event.preventDefault();

                var hash = this.hash;

                $('html, body').animate({
                    scrollTop: $(hash).offset().top
                }, 800, function(){
                    window.location.hash = hash;
                });
            }
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
  var carousel = new bootstrap.Carousel(document.getElementById('portfolioCarousel'), {
    interval: 3000,
    wrap: true,
    keyboard: true
  });
});
