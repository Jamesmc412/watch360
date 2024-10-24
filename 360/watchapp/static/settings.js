// Determine the current page
const settingsPanel = document.getElementById('SettingsPanel')

// Code specific to the first HTML file
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

const isOnline = document.getElementById('onlineOffline');
isOnline.checked = localStorage.getItem('isOnline') === true;

isOnline.addEventListener('change', () =>{
    localStorage.setItem('isOnline', isOnline.checked);

});
