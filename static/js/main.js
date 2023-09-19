// Animated Scroll Reveal
AOS.init();



// Smooth scrolling for logo, CTA (hero) button and portfolio tabs on the home page
$(document).ready(function() {
    if (window.location.pathname === '/') {
        $("a.logo, a.cta-button, a.tab-link").on('click', function(event) {
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



// Smooth scrolling for navigation links on the home page
if (window.matchMedia('(max-width: 768px)').matches) {
  const toggleButton = document.getElementById('toggleButton');
}

$(document).ready(function() {
    if (window.location.pathname === '/') {
        $("a.nav-link.scrollto").on('click', function(event) {
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



// Portfolio tabs animation
$('#portfolio-tabs a').on('click', function (e) {
    e.preventDefault();
    $(this).tab('show');
});



// Smooth scrolling for Portfolio navlinks on the portfolio page
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



// Portfolio project images carousel animation
document.addEventListener('DOMContentLoaded', function () {
  var carousel = new bootstrap.Carousel(document.getElementById('portfolioCarousel'), {
    interval: 3000,
    wrap: true,
    keyboard: true
  });
});



// Skills bar animation
function initProgressBar(barId, progress) {
  var bar = document.getElementById(barId);

  var p_bar = new ProgressBar.Circle(bar, {
    color: '#3C486B',
    strokeWidth: 7,
    trailWidth: 2,
    easing: 'easeInOut',
    duration: 1400,
    text: {
      autoStyleContainer: false
    },
    from: { color: '#aaa', width: 2 },
    to: { color: '#F45050', width: 7 },
    step: function(state, circle) {
      circle.path.setAttribute('stroke', state.color);
      circle.path.setAttribute('stroke-width', state.width);

      var value = Math.round(circle.value() * 100);
      if (value === 0) {
        circle.setText('');
      } else {
        circle.setText(value+"%");
      }
    }
  });

  p_bar.text.style.fontFamily = "'Nunito', sans-serif";
  p_bar.text.style.fontSize = '1.7rem';

  function animateProgressBar(entries, observer, progressBar) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        progressBar.animate(progress);
      } else {
        progressBar.set(0); // Reset the progress bar if it's not intersecting
      }
    });
  }

  var observer = new IntersectionObserver(function(entries, observer) {
    animateProgressBar(entries, observer, p_bar);
  }, { threshold: 0.2 });

  var section = document.querySelector("#" + barId);
  observer.observe(section);
}

// Call the function for each progress bar
initProgressBar("pythonBar", 0.92);
initProgressBar("flaskBar", 0.87);
initProgressBar("htmlBar", 0.83);
initProgressBar("cssBar", 0.89);
initProgressBar("jsBar", 0.79);



// Testimonials carousel
const reviewWrap = document.getElementById("reviewWrap");
const leftArrow = document.getElementById("leftArrow");
const rightArrow = document.getElementById("rightArrow");
const testimonialId = document.getElementById("testimonialId");
const imgDiv = document.getElementById("imgDiv");
const personName = document.getElementById("personName");
const profession = document.getElementById("profession");
const description = document.getElementById("description");
const editTestimonial = document.getElementById('editTestimonial');
const deleteTestimonial = document.getElementById('deleteTestimonial');

console.log("testimonialsList");
let people = testimonialsList;

testimonialId.innerText = people[0].id;
imgDiv.style.backgroundImage = people[0].photo;
personName.innerText = people[0].name;
profession.innerText = people[0].profession;
profession.setAttribute("href", people[0].professionLink);
description.innerText = people[0].description;
let currentPerson = 0;

//Select the side where you want to slide
function slide(whichSide, personNumber) {
	let reviewWrapWidth = reviewWrap.offsetWidth + "px";
	let descriptionHeight = description.offsetHeight + "px";
	//(+ or -)
	let side1symbol = whichSide === "left" ? "" : "-";
	let side2symbol = whichSide === "left" ? "-" : "";

	let tl = gsap.timeline();

	tl.to(reviewWrap, {
		duration: 0.4,
		opacity: 0,
		translateX: `${side1symbol + reviewWrapWidth}`
	});

	tl.to(reviewWrap, {
		duration: 0,
		translateX: `${side2symbol + reviewWrapWidth}`
	});

	setTimeout(() => {
		testimonialId.innerText = people[personNumber].id;
	}, 400);
	setTimeout(() => {
		imgDiv.style.backgroundImage = people[personNumber].photo;
	}, 400);
	setTimeout(() => {
		description.style.height = descriptionHeight;
	}, 400);
	setTimeout(() => {
		personName.innerText = people[personNumber].name;
	}, 400);
	setTimeout(() => {
		profession.innerText = people[personNumber].profession;
	}, 400);
    setTimeout(() => {
      profession.setAttribute("href", people[personNumber].professionLink);
    }, 400);
  setTimeout(() => {
    description.innerText = people[personNumber].description;
    adjustSectionHeight();
  }, 400);

if (editTestimonial) {
  editTestimonial.addEventListener('click', () => {
    console.log(people[personNumber].id);
    window.location.href = '/edit-testimonial/' + people[personNumber].id;
  });
}

if (editTestimonial) {
  deleteTestimonial.addEventListener('click', () => {
      console.log(people[personNumber].id);
      window.location.href = '/delete-testimonial/' + people[personNumber].id;
  });
}


	tl.to(reviewWrap, {
		duration: 1,
		opacity: 1,
		translateX: 0
	});

}

function adjustSectionHeight() {
  description.style.height = "100%";
}

function setNextCardLeft() {
  currentPerson = (currentPerson - 1 + people.length) % people.length;
  slide("left", currentPerson);
  adjustSectionHeight();
}

function setNextCardRight() {
  currentPerson = (currentPerson + 1) % people.length;
  slide("right", currentPerson);
  adjustSectionHeight();
}

leftArrow.addEventListener("click", setNextCardLeft);
rightArrow.addEventListener("click", setNextCardRight);

window.addEventListener("resize", () => {
	description.style.height = "100%";
});

window.addEventListener("resize", adjustSectionHeight);
window.addEventListener("load", adjustSectionHeight);

function startTimer() {
  timer = setInterval(setNextCardLeft, 4000);
}

function stopTimer() {
  clearInterval(timer);
}

reviewWrap.addEventListener('mouseenter', stopTimer);
reviewWrap.addEventListener('mouseleave', startTimer);

startTimer();
setInterval(adjustSectionHeight, 100);


