const navbar = document.querySelector('nav');
const sideNavbar = document.getElementById('side-navbar');
const navbarToggleBtn = document.getElementById('mobile-toggle');
const navbarToggleBtnClose = document.getElementById('mobile-toggle-close');
const dropdownSidebar = document.querySelectorAll('.dropdown-side');
const overlay = document.getElementById('overlay');



navbarToggleBtn.onclick = () => {
    overlay.classList.add('active');
    sideNavbar.classList.add('active');
}

overlay.onclick = () => {
    overlay.classList.remove('active');
    sideNavbar.classList.remove('active');
}

navbarToggleBtnClose.onclick = () => {
    overlay.classList.remove('active');
    sideNavbar.classList.remove('active');
}

// editing after reloading the page
navbarBackground();

window.onscroll = () => {
    navbarBackground();
}

dropdownSidebar.forEach((dropdown) => {

    const textDropdown = dropdown.querySelector('.dropdown-text-side');

    textDropdown.onclick = () => {

        if (dropdown.classList.contains("active")) {
            
            dropdownSidebar.forEach((d) => {
                d.classList.remove("active");
                d.querySelector('.dropdown-text-side').classList.remove("active");
                d.querySelector('.dropdown-text-side i').style.transform = "scaleY(1)";
            })

        } else {

            dropdownSidebar.forEach((d) => {
                d.classList.remove("active");
                d.querySelector('.dropdown-text-side').classList.remove("active");
                d.querySelector('.dropdown-text-side').style.transform = "";
            })

            dropdown.classList.add("active");

            textDropdown.classList.add("active");

            textDropdown.querySelector("i").style.transform = "scaleY(-1)";

        }
        
    }

})




//? Helper Functions

function navbarBackground() {
    if (window.scrollY === 0 && location.pathname === "/") {
        navbar.style.setProperty('--nav-bg', 'transparent');
    } else {
        navbar.style.setProperty('--nav-bg', 'var(--overlay-clr)');
    }
}