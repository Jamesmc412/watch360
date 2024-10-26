// const settingsData = [
//     {
//         title: 'Online/Offline Visibility',
//         uid: 'onlineOfflineVisibility',
//         description: 'Allow friends to be able to see whether or not you are online',
//         isChecked: false,
//         type: checkbox
//     },
//     {
//         title: 'Light/Dark Mode',
//         uid: 'lightDarkMode',
//         description: 'Set the app to a Light Theme or Dark Theme',
//         isChecked: true,
//         type: checkbox
//     },
//     {
//         title: 'Change Your Username',
//         uid: 'changeUsername',
//         description: 'Alter your current username to a new one',
//         isChecked: false,
//         type: text
//     },
//     {
//         title: 'Change Your Password',
//         uid: 'changePassword',
//         description: 'Alter your current password to a new one',
//         isChecked: false,
//         type: text
//     }
// ];

const settingsPanel = document.getElementById('SettingsPanel');
// settingsData.forEach(setting => {
//     createSetting(setting);
// });

// function createSetting(data){
//     const settings = document.getElementById('Settings');
//     settings.innerHTML += `
//     <div class="setting">
//         <label for="${data.uid}">
//             <span>${data.title}</span>
//             <span>${data.description}</span>
//         </label>
//         <input type="${data.type}" id="${data.uid}">
//     </div>
//     `
// }

if(document.getElementById('lightDarkMode')){
    document.getElementById('lightDarkMode').addEventListener('change', e => {
        const bodyBG = document.body.style;
        if (e.target.checked){
            settingsPanel.classList.add('dark');
            bodyBG.backgroundColor = 'black';
        } else {
            settingsPanel.classList.remove('dark');
            bodyBG.backgroundColor = 'white';
        }
    });
}