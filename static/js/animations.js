document.addEventListener('DOMContentLoaded', () => {

    const navLinks = document.querySelectorAll('#navigation-bar-container .navigation-items .navigation-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            // Remove "active" class from all links
            navLinks.forEach(nav => nav.classList.remove('active'));

            // Add "active" class to the clicked link
            event.target.classList.add('active');
        });
    });
});