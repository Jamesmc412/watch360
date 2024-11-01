const settingsPanel = document.getElementById('SettingsPanel');
const bodyBG = document.body.style;
const lightDarkMode = document.getElementById('lightDarkMode');
const isOnline = document.getElementById('onlineOffline');

// Code specific to the first HTML file
lightDarkMode.addEventListener('change', (e) => {
    if (e.target.checked) {
        settingsPanel.classList.add('dark');
        bodyBG.backgroundColor = 'black';
    } else {
        settingsPanel.classList.remove('dark');
        bodyBG.backgroundColor = 'white';
    }
});

// Set the initial state of isOnline checkbox on page load
document.addEventListener('DOMContentLoaded', () => {
    const isChecked = localStorage.getItem('checkboxState') === 'true';
    isOnline.checked = isChecked;
});

// Save the checkbox state when it changes
isOnline.addEventListener('change', () => {
    localStorage.setItem('checkboxState', isOnline.checked.toString());
    localStorage.setItem('isOnline', isOnline.checked.toString());
});