const { app, BrowserWindow } = require('electron'); // Import modul utama Electron
const path = require('path'); // Modul path untuk mempermudah navigasi file

let mainWindow;

function createWindow() {
  // Membuat jendela aplikasi
  mainWindow = new BrowserWindow({
    width: 800, // Lebar jendela
    height: 600, // Tinggi jendela
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // Preload script untuk keamanan
      nodeIntegration: false, // Keamanan: nonaktifkan integrasi Node.js di renderer
      contextIsolation: true, // Keamanan: gunakan isolasi konteks
    },
  });

  // Memuat halaman `index.html` dari folder `UI/pages/`
  mainWindow.loadFile(path.join(__dirname, '../UI/pages/index.html'));

  // Opsional: Buka DevTools untuk debugging
  mainWindow.webContents.openDevTools();
}

// Event ketika aplikasi siap
app.whenReady().then(() => {
  createWindow();

  // Membuka kembali aplikasi jika ditutup di macOS
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Event untuk keluar dari aplikasi ketika semua jendela ditutup (kecuali di macOS)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
