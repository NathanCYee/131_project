function chooseIcon() {
    if (darkmode.inDarkMode) {
        document.getElementById('colorToggle').setAttribute('class', 'bi bi-sun-fill');
    } else if (!darkmode.inDarkMode) {
        document.getElementById('colorToggle').setAttribute('class', 'bi bi-moon-fill');
    }
}

function toggleColor() {
    darkmode.toggleDarkMode();
    chooseIcon();
}