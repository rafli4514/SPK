// Memanggil API dari preload.js
document.getElementById('sendMessage').addEventListener('click', () => {
    window.api.sendMessage('Halo dari Frontend!');
  });
  
  window.api.onMessage((data) => {
    document.getElementById('message').innerText = `Pesan dari Backend: ${data}`;
  });
  