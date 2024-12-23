// frontend/js/input.js

const API_BASE_URL = 'http://localhost:5000/api/saw';

// Seleksi elemen HTML
const kriteriaInput = document.getElementById('kriteria');
const tipeKriteriaSelect = document.getElementById('tipe-kriteria');
const weightKriteriaInput = document.getElementById('weight-kriteria');
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
        nameCell.textContent = kriteria.name;
        row.appendChild(nameCell);

        // Tipe Kriteria
        const typeCell = document.createElement('td');
        typeCell.textContent = kriteria.type;
        row.appendChild(typeCell);

        // Bobot Kriteria
        const weightCell = document.createElement('td');
        weightCell.textContent = kriteria.weight;
        row.appendChild(weightCell);

        // Aksi
        const actionCell = document.createElement('td');
        const removeButton = document.createElement('button');
        removeButton.textContent = 'Hapus';
        removeButton.className = 'remove-button bg-red-500 text-white px-2 py-1 rounded hover:bg-red-700';
        removeButton.setAttribute('data-index', index);
        actionCell.appendChild(removeButton);
        row.appendChild(actionCell);

        listKriteriaTableBody.appendChild(row);
    });
}

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
        removeButton.className = 'remove-button bg-red-500 text-white px-2 py-1 rounded hover:bg-red-700';
        removeButton.setAttribute('data-index', index);
        actionCell.appendChild(removeButton);
        row.appendChild(actionCell);

        listAlternatifTableBody.appendChild(row);
    });
}

// Fungsi Menambah Kriteria
function tambahKriteria() {
    const kriteriaValue = kriteriaInput.value.trim();
    const tipeKriteria = tipeKriteriaSelect.value;
    const weightValue = weightKriteriaInput.value.trim();

    // Validasi Kriteria
    if (!kriteriaValue) {
        showAlert('Kriteria tidak boleh kosong.', 'error');
        return;
    }

    if (!isValidInput(kriteriaValue)) {
        showAlert('Kriteria mengandung karakter yang tidak diizinkan.', 'error');
        return;
    }

    // Validasi Tipe Kriteria
    if (!tipeKriteria) {
        showAlert('Tipe kriteria harus dipilih.', 'error');
        return;
    }

    // Validasi Bobot Kriteria
    if (!weightValue) {
        showAlert('Bobot kriteria tidak boleh kosong.', 'error');
        return;
    }

    const weightNumber = parseFloat(weightValue);
    if (isNaN(weightNumber) || weightNumber <= 0) {
        showAlert('Bobot kriteria harus berupa angka positif.', 'error');
        return;
    }

    // Cek duplikasi kriteria berdasarkan nama
    const isDuplicate = criteriaArray.some(k => k.name.toLowerCase() === kriteriaValue.toLowerCase());
    if (isDuplicate) {
        showAlert('Kriteria sudah ada dalam daftar.', 'error');
        return;
    }

    // Tambahkan kriteria ke array
    criteriaArray.push({ name: kriteriaValue, type: tipeKriteria, weight: weightNumber });
    renderKriteria();

    // Reset input
    kriteriaInput.value = '';
    tipeKriteriaSelect.value = '';
    weightKriteriaInput.value = '';
    showAlert('Kriteria berhasil ditambahkan.', 'success');
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

    // Cek duplikasi alternatif berdasarkan nama
    const isDuplicate = alternativesArray.some(a => a.toLowerCase() === alternatifValue.toLowerCase());
    if (isDuplicate) {
        showAlert('Alternatif sudah ada dalam daftar.', 'error');
        return;
    }

    // Tambahkan alternatif ke array
    alternativesArray.push(alternatifValue);
    renderAlternatif();

    // Reset input
    alternatifInput.value = '';
    showAlert('Alternatif berhasil ditambahkan.', 'success');
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

// Fungsi untuk Memisahkan Kriteria Berdasarkan Tipe
function separateCriteria() {
    const criteria_benefit = [];
    const weight_benefit = [];
    const criteria_cost = [];
    const weight_cost = [];

    criteriaArray.forEach(kriteria => {
        if (kriteria.type.toLowerCase() === 'benefit') {
            criteria_benefit.push(kriteria.name);
            weight_benefit.push(kriteria.weight);
        } else if (kriteria.type.toLowerCase() === 'cost') {
            criteria_cost.push(kriteria.name);
            weight_cost.push(kriteria.weight);
        }
    });

    return { criteria_benefit, weight_benefit, criteria_cost, weight_cost };
}

// Fungsi untuk Mengirim Data ke Backend
async function sendData() {
    if (criteriaArray.length < 2 || alternativesArray.length < 2) {
        showAlert('Kriteria dan Alternatif minimal harus berjumlah 2!', 'error');
        return;
    }

    // Validasi Total Bobot (opsional, tergantung kebutuhan)
    const totalWeightBenefit = criteriaArray
        .filter(k => k.type.toLowerCase() === 'benefit')
        .reduce((sum, k) => sum + k.weight, 0);
    const totalWeightCost = criteriaArray
        .filter(k => k.type.toLowerCase() === 'cost')
        .reduce((sum, k) => sum + k.weight, 0);

    if (totalWeightBenefit <= 0 && totalWeightCost <= 0) {
        showAlert('Total bobot kriteria harus lebih besar dari nol.', 'error');
        return;
    }

    const separated = separateCriteria();

    // Cek apakah ada setidaknya satu kriteria benefit atau cost
    if (separated.criteria_benefit.length === 0 && separated.criteria_cost.length === 0) {
        showAlert('Minimal harus ada satu kriteria Benefit atau Cost.', 'error');
        return;
    }

    const payload = {
        criteria_benefit: separated.criteria_benefit,
        weight_benefit: separated.weight_benefit,
        criteria_cost: separated.criteria_cost,
        weight_cost: separated.weight_cost,
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
                window.location.href = 'saw-alternative-page.html'; // Ganti dengan halaman input skor
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

// Event Listener untuk Menangani Enter Key pada Semua Input Kriteria
const kriteriaFields = [kriteriaInput, tipeKriteriaSelect, weightKriteriaInput];
kriteriaFields.forEach(field => {
    if (field) {
        field.addEventListener('keydown', (event) => { // Menggunakan 'keydown' alih-alih 'keypress'
            if (event.key === 'Enter') {
                event.preventDefault();
                tambahKriteria();
            }
        });
    }
});

// Event Listener untuk Menangani Enter Key pada Input Alternatif
if (alternatifInput) {
    alternatifInput.addEventListener('keydown', (event) => { // Menggunakan 'keydown' alih-alih 'keypress'
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
