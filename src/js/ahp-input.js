// ahp-input.js

const API_BASE_URL = 'http://localhost:5000/api/ahp';

// Seleksi elemen HTML
const kriteriaInput = document.getElementById('kriteria');
const addKriteriaButton = document.getElementById('add-kriteria');
const listKriteriaTableBody = document.querySelector('#list-kriteria tbody');

const alternatifInput = document.getElementById('alternatif');
const addAlternatifButton = document.getElementById('add-alternatif');
const listAlternatifTableBody = document.querySelector('#list-alternatif tbody');

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
function renderKriteria() {
    listKriteriaTableBody.innerHTML = '';

    criteriaArray.forEach((kriteria, index) => {
        const row = document.createElement('tr');

        // No
        const noCell = document.createElement('td');
        noCell.textContent = index + 1;
        row.appendChild(noCell);

        // Nama Kriteria
        const nameCell = document.createElement('td');
        nameCell.textContent = kriteria;
        row.appendChild(nameCell);

        // Aksi
        const actionCell = document.createElement('td');
        const removeButton = document.createElement('button');
        removeButton.textContent = 'Hapus';
        removeButton.className = 'remove-button';
        removeButton.setAttribute('data-index', index);
        actionCell.appendChild(removeButton);
        row.appendChild(actionCell);

        listKriteriaTableBody.appendChild(row);
    });
}

// Fungsi untuk Memperbarui Tampilan Daftar Alternatif
function renderAlternatif() {
    listAlternatifTableBody.innerHTML = '';

    alternativesArray.forEach((alternatif, index) => {
        const row = document.createElement('tr');

        // No
        const noCell = document.createElement('td');
        noCell.textContent = index + 1;
        row.appendChild(noCell);

        // Nama Alternatif
        const nameCell = document.createElement('td');
        nameCell.textContent = alternatif;
        row.appendChild(nameCell);

        // Aksi
        const actionCell = document.createElement('td');
        const removeButton = document.createElement('button');
        removeButton.textContent = 'Hapus';
        removeButton.className = 'remove-button';
        removeButton.setAttribute('data-index', index);
        actionCell.appendChild(removeButton);
        row.appendChild(actionCell);

        listAlternatifTableBody.appendChild(row);
    });
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
        renderKriteria();
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
        renderAlternatif();
        alternatifInput.value = '';
        showAlert('Alternatif berhasil ditambahkan.', 'success');
    } else {
        showAlert('Alternatif sudah ada dalam daftar.', 'error');
    }
}

// Fungsi untuk Menghapus Kriteria atau Alternatif
function hapusItem(event) {
    if (event.target.classList.contains('remove-button')) {
        const index = parseInt(event.target.getAttribute('data-index'), 10);
        const parentTable = event.target.closest('table').id;

        if (parentTable === 'list-kriteria') {
            criteriaArray.splice(index, 1);
            renderKriteria();
            showAlert('Kriteria berhasil dihapus.', 'success');
        } else if (parentTable === 'list-alternatif') {
            alternativesArray.splice(index, 1);
            renderAlternatif();
            showAlert('Alternatif berhasil dihapus.', 'success');
        }
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
            showAlert(data.message || 'Data berhasil disimpan.', 'success');
            setTimeout(() => {
                window.location.href = 'ahp-criteria-page.html'; // Ganti dengan halaman input skor
            }, 1500);
        } else {
            console.error('Error Response:', data);
            showAlert(`Error: ${data.error || 'Terjadi kesalahan.'}`, 'error');
        }
    } catch (error) {
        hideLoading();
        lanjutButton.disabled = false; // Aktifkan kembali tombol Lanjut
        console.error('Fetch Error:', error);
        showAlert('Terjadi kesalahan saat mengirim data ke server.', 'error');
    }
}

// Event Listener untuk Menambah Kriteria
if (addKriteriaButton) {
    addKriteriaButton.addEventListener('click', tambahKriteria);
}

// Event Listener untuk Menambah Alternatif
if (addAlternatifButton) {
    addAlternatifButton.addEventListener('click', tambahAlternatif);
}

// Event Listener untuk Menghapus Kriteria atau Alternatif
document.addEventListener('click', hapusItem);

// Event Listener untuk Menangani Enter Key pada Input Kriteria
if (kriteriaInput) {
    kriteriaInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            tambahKriteria();
        }
    });
}

// Event Listener untuk Menangani Enter Key pada Input Alternatif
if (alternatifInput) {
    alternatifInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            tambahAlternatif();
        }
    });
}

// Event Listener untuk Tombol Kembali
if (backButton) {
    backButton.addEventListener('click', () => {
        window.location.href = 'index.html';
    });
}

// Event Listener untuk Tombol Lanjut
if (lanjutButton) {
    lanjutButton.addEventListener('click', sendData);
}
