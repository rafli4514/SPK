const { contextBridge, ipcRenderer } = require('electron');

// Menyediakan API untuk komunikasi antara frontend dan backend
contextBridge.exposeInMainWorld('api', {
  sendMessage: (message) => ipcRenderer.send('message', message),
  onMessage: (callback) => ipcRenderer.on('reply', (_, data) => callback(data)),
});
