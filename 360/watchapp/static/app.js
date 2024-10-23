const settingsPanel = document.getElementById('SettingsPanel');

// Determine the current page
const currentPage = window.location.pathname;

if (currentPage.includes('settings.html')) {
    // Code specific to the first HTML file
    if (document.getElementById('lightDarkMode')) {
        document.getElementById('lightDarkMode').addEventListener('change', e => {
            const bodyBG = document.body.style;
            if (e.target.checked) {
                settingsPanel.classList.add('dark');
                bodyBG.backgroundColor = 'black';
            } else {
                settingsPanel.classList.remove('dark');
                bodyBG.backgroundColor = 'white';
            }
        });
    }
} else if (currentPage.includes('homepage.html')) {
    // Code specific to the second HTML file
    if (document.getElementById('onlineOffline')) {
        document.getElementById('onlineOffline').addEventListener('change', f => {
            dot.is_Online = f.target.checked;
        });
    }
}
