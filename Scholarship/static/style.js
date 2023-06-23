// JavaScript code goes here

// Function to enable auto scrolling of the carousel
function enableAutoScroll() {
  setInterval(function () {
    const carousel = document.querySelector("#carouselExampleIndicators");
    const currentIndex = Number(
      carousel
        .querySelector(".carousel-indicators .active")
        .getAttribute("data-bs-slide-to")
    );
    const totalSlides = carousel.querySelectorAll(
      ".carousel-indicators button"
    ).length;

    // Calculate the index of the next slide
    const nextIndex = (currentIndex + 1) % totalSlides;

    // Go to the next slide
    carousel
      .querySelector(
        `.carousel-indicators button[data-bs-slide-to="${nextIndex}"]`
      )
      .click();
  }, 5000); // Adjust the time interval (in milliseconds) as per your requirement
}

// Call the function to enable auto scrolling
enableAutoScroll();
