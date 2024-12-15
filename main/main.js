// main.js
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const axios = require('axios');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  });

  mainWindow.loadFile(path.join(__dirname, '../src/pages/index.html'));
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

ipcMain.on('run-ahp', async (event, data) => {
  try {
    const response = await axios.post('http://localhost:5000/api/ahp', data);
    event.reply('ahp-result', response.data);  // Kirim hasil ke renderer
  } catch (error) {
    event.reply('ahp-result', { status: 'error', message: error.message });
  }
});