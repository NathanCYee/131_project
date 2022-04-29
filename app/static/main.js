function getColor() {
    let cookie = document.cookie.split(';');
    let [k, v] = cookie[0].split('=');
    if (v == null) {
        return 'bootstrap';
    }
    return v;
}

function chooseIcon() {
    console.log('here');
    if (getColor() == 'bootstrap') {
        document.getElementById('colorToggle').setAttribute('class', 'bi bi-moon-fill');
    }
    if (getColor() == 'bootstrap-dark') {
        document.getElementById('colorToggle').setAttribute('class', 'bi bi-sun-fill');
    }
}

function toggleColor() {
    if (document.getElementsByTagName('body')[0].getAttribute('class') == 'bootstrap') {
        document.cookie = 'color=bootstrap-dark;'
    } else {
        document.cookie = 'color=bootstrap;'
    }
    document.getElementsByTagName('body')[0].setAttribute('class', getColor());
    chooseIcon();
}

document.getElementsByTagName('body')[0].setAttribute('class', getColor());
chooseIcon();