const { app, BrowserWindow } = require('electron'); 
const path = require('path'); 

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800, 
    height: 600, 
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), 
      nodeIntegration: false, 
      contextIsolation: true, 
    },
  });

  mainWindow.loadFile(path.join(__dirname, '../src/pages/index.html'));

}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
