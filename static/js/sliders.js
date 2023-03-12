const swiper = new Swiper(".swiper", {
	autoplay: {
		delay: 2000,
		disableOnInteraction: false,
		pauseOnMouseEnter: true,
	},
	speed: 800,
	breakpoints: {
		// when window width is >= 320px
		320: {
			slidesPerView: 1,
			spaceBetween: 20,
		},
		// when window width is >= 480px
		480: {
			slidesPerView: 2,
			spaceBetween: 30,
		},
		// when window width is >= 640px
		640: {
			slidesPerView: 3,
			spaceBetween: 40,
		},
		820: {
			slidesPerView: 4,
			spaceBetween: 40,
		},
		1000: {
			slidesPerView: 5,
			spaceBetween: 50,
		},
	},
});

const swiper2 = new Swiper(".swiper-2", {
	navigation: {
		nextEl: ".swiper-button-next",
		prevEl: ".swiper-button-prev",
	},
	autoplay: {
		delay: 3000,
		pauseOnMouseEnter: true,
	},
	speed: 800,
	breakpoints: {
		// when window width is >= 320px
		320: {
			slidesPerView: 1,
			spaceBetween: 20,
		},
		// when window width is >= 480px
		480: {
			slidesPerView: 2,
			spaceBetween: 30,
		},
		// when window width is >= 640px
		640: {
			slidesPerView: 3,
			spaceBetween: 40,
		},
		820: {
			slidesPerView: 4,
			spaceBetween: 40,
		},
		1000: {
			slidesPerView: 5,
			spaceBetween: 50,
		},
	},
});
