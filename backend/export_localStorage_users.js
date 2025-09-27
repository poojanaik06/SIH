
// Browser Console Script to Export localStorage Users
// Run this in your browser's developer console while on your app

function exportLocalStorageUsers() {
    const users = localStorage.getItem('registeredUsers');
    if (users) {
        const userData = JSON.parse(users);
        console.log('Found users in localStorage:', userData);
        
        // Create downloadable JSON file
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(userData, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "exported_users.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
        
        return userData;
    } else {
        console.log('No users found in localStorage');
        return [];
    }
}

// Run the export
exportLocalStorageUsers();
