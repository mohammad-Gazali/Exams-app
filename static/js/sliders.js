const swiper = new Swiper(".swiper", {
	pagination: {
		el: ".swiper-pagination",
		type: "bullets",
		clickable: true,
	},
	autoplay: {
		delay: 2000,
		disableOnInteraction: false,
		pauseOnMouseEnter: true,
	},
	speed: 800,
	breakpoints: {
		320: {
			slidesPerView: 1,
			spaceBetween: 20,
		},
		480: {
			slidesPerView: 2,
			spaceBetween: 30,
		},
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
	pagination: {
		el: ".swiper-pagination",
		type: "bullets",
		clickable: true,
	},
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
		0: {
			slidesPerView: 1,
			spaceBetween: 20,
		},
		480: {
			slidesPerView: 2,
			spaceBetween: 30,
		},
		640: {
			slidesPerView: 3,
			spaceBetween: 40,
		},
		900: {
			slidesPerView: 4,
			spaceBetween: 40,
		},
		1200: {
			slidesPerView: 5,
			spaceBetween: 50,
		},
	},
});

const swiper3 = new Swiper(".swiper-3", {
	pagination: {
		el: ".swiper-pagination",
		type: "bullets",
		clickable: true,
	},
	navigation: {
		nextEl: ".swiper-button-next",
		prevEl: ".swiper-button-prev",
	},
	speed: 800,
	breakpoints: {
		0: {
			slidesPerView: 1,
			spaceBetween: 20,
		},
		520: {
			slidesPerView: 2,
			spaceBetween: 30,
		},
		940: {
			slidesPerView: 3,
			spaceBetween: 40,
		},
		1200: {
			slidesPerView: 4,
			spaceBetween: 40,
		},
	},
});