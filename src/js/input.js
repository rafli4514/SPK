// input.js

const API_BASE_URL = 'http://localhost:5000/api';

// Seleksi elemen HTML
const kriteriaInput = document.getElementById('kriteria');
const addKriteriaButton = document.getElementById('add-kriteria');
const listKriteria = document.getElementById('list-kriteria');

const alternatifInput = document.getElementById('alternatif');
const addAlternatifButton = document.getElementById('add-alternatif');
const listAlternatif = document.getElementById('list-alternatif');

const lanjutButton = document.getElementById('lanjut');
const backButton = document.getElementById('back-button');

const alertContainer = document.getElementById('alert-container');

// Array penyimpanan data sementara
let criteriaArray = [];
let alternativesArray = [];

// Fungsi Validasi Input
function isValidInput(input) {
    const regex = /^[a-zA-Z0-9\s\-]+$/;
    return regex.test(input);
}

// Fungsi Menampilkan Pesan Alert
function showAlert(message, type = 'error') {
    // Hapus semua alert yang sudah ada
    alertContainer.innerHTML = '';

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${type === 'error' ? 'alert-error' : 'alert-success'} p-4 mb-4 border rounded-lg`;
    alertDiv.textContent = message;
    alertContainer.appendChild(alertDiv);

    // Hapus pesan setelah 5 detik
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Fungsi Menampilkan Loading Overlay
function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.remove('hidden');
    }
}

// Fungsi Menghilangkan Loading Overlay
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.add('hidden');
    }
}

// Fungsi untuk Memperbarui Tampilan Daftar Kriteria
function updateKriteriaList() {
    const formattedCriteria = criteriaArray.map(crit => `• ${crit}`).join('\n');
    listKriteria.value = formattedCriteria;
}

// Fungsi untuk Memperbarui Tampilan Daftar Alternatif
function updateAlternatifList() {
    const formattedAlternatif = alternativesArray.map(alt => `• ${alt}`).join('\n');
    listAlternatif.value = formattedAlternatif;
}

// Fungsi Menambah Kriteria
function tambahKriteria() {
    const kriteriaValue = kriteriaInput.value.trim();
    if (!kriteriaValue) {
        showAlert('Kriteria tidak boleh kosong.', 'error');
        return;
    }
    if (!isValidInput(kriteriaValue)) {
        showAlert('Kriteria mengandung karakter yang tidak diizinkan.', 'error');
        return;
    }
    if (!criteriaArray.includes(kriteriaValue)) {
        criteriaArray.push(kriteriaValue);
        updateKriteriaList();
        kriteriaInput.value = '';
        showAlert('Kriteria berhasil ditambahkan.', 'success');
    } else {
        showAlert('Kriteria sudah ada dalam daftar.', 'error');
    }
}

// Fungsi Menambah Alternatif
function tambahAlternatif() {
    const alternatifValue = alternatifInput.value.trim();
    if (!alternatifValue) {
        showAlert('Alternatif tidak boleh kosong.', 'error');
        return;
    }
    if (!isValidInput(alternatifValue)) {
        showAlert('Alternatif mengandung karakter yang tidak diizinkan.', 'error');
        return;
    }
    if (!alternativesArray.includes(alternatifValue)) {
        alternativesArray.push(alternatifValue);
        updateAlternatifList();
        alternatifInput.value = '';
        showAlert('Alternatif berhasil ditambahkan.', 'success');
    } else {
        showAlert('Alternatif sudah ada dalam daftar.', 'error');
    }
}

// Fungsi untuk Mengirim Data ke Backend
async function sendData() {
    if (criteriaArray.length < 2 || alternativesArray.length < 2) {
        showAlert('Kriteria dan Alternatif minimal harus berjumlah 2!', 'error');
        return;
    }

    const payload = {
        criteria: criteriaArray,
        alternatives: alternativesArray
    };

    showLoading();
    lanjutButton.disabled = true; // Nonaktifkan tombol Lanjut

    try {
        const response = await fetch(`${API_BASE_URL}/save-input`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        hideLoading();
        lanjutButton.disabled = false; // Aktifkan kembali tombol Lanjut

        if (response.ok) {
            showAlert(data.message, 'success');
            setTimeout(() => {
                window.location.href = 'ahp-criteria-page.html';
            }, 1500);
        } else {
            console.error('Error Response:', data);
            showAlert(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        hideLoading();
        lanjutButton.disabled = false; // Aktifkan kembali tombol Lanjut
        console.error('Fetch Error:', error);
        showAlert('Terjadi kesalahan saat mengirim data ke server.', 'error');
    }
}

// Event Listener
if (addKriteriaButton) {
    addKriteriaButton.addEventListener('click', tambahKriteria);
}
if (addAlternatifButton) {
    addAlternatifButton.addEventListener('click', tambahAlternatif);
}

if (kriteriaInput) {
    kriteriaInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            tambahKriteria();
        }
    });
}

if (alternatifInput) {
    alternatifInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            tambahAlternatif();
        }
    });
}

if (backButton) {
    backButton.addEventListener('click', () => {
        window.location.href = 'index.html';
    });
}

if (lanjutButton) {
    lanjutButton.addEventListener('click', sendData);
}
