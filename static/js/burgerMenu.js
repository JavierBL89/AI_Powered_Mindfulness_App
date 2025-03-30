

document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.burguer');
    const menuContainer = document.querySelector('.burger-menu-container');
    const burguerDropdown = document.querySelector('.burger-nav');

    burger.addEventListener('click', () => {
        burger.classList.toggle('active');
        burguerDropdown.classList.toggle('show');

    });
});