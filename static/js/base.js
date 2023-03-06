const sideNavbar = document.getElementById('side-navbar');
const navbarToggleBtn = document.getElementById('mobile-toggle');
const navbarToggleBtnClose = document.getElementById('mobile-toggle-close');
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