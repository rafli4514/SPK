// js/saw-alternative-weights.js

const API_BASE_URL = 'http://localhost:5000/api/saw'; 

// Seleksi elemen HTML
const skorContainer = document.getElementById('bobot-container');
const submitButton = document.getElementById('simpan-bobot');
const alertContainer = document.getElementById('alert-container');
const backButton = document.getElementById('back-button');
const loadingOverlay = document.getElementById('loading-overlay');

// Fungsi untuk menampilkan alert
function showAlert(message, type = 'error') {
    alertContainer.innerHTML = '';

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${type === 'error' ? 'alert-error' : 'alert-success'} p-4 mb-4 border rounded-lg`;
    alertDiv.textContent = message;
    alertContainer.appendChild(alertDiv);

    // Hapus alert setelah 5 detik
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Fungsi untuk menampilkan overlay loading
function showLoading() {
    if (loadingOverlay) {
        loadingOverlay.classList.remove('hidden');
    }
}

// Fungsi untuk menyembunyikan overlay loading
function hideLoading() {
    if (loadingOverlay) {
        loadingOverlay.classList.add('hidden');
    }
}

// Fungsi untuk mengambil data kriteria dan alternatif dari backend
async function fetchCriteriaAndAlternatives() {
    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/get-input`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        hideLoading();

        if (response.ok) {
            const { criteria_benefit, criteria_cost, alternatives } = data;

            // Validasi data yang diterima
            if ((!criteria_benefit || criteria_benefit.length === 0) &&
                (!criteria_cost || criteria_cost.length === 0)) {
                showAlert('Data kriteria benefit dan cost belum diatur. Silakan input terlebih dahulu.', 'error');
                return;
            }

            if (!alternatives || alternatives.length < 2) {
                showAlert('Data alternatif belum diatur atau kurang dari dua alternatif. Silakan input terlebih dahulu.', 'error');
                return;
            }

            renderSkorTable(criteria_benefit, criteria_cost, alternatives);
        } else {
            console.error('Error Response:', data);
            showAlert(`Error: ${data.error || 'Terjadi kesalahan.'}`, 'error');
        }
    } catch (error) {
        hideLoading();
        console.error('Fetch Error:', error);
        showAlert('Terjadi kesalahan saat mengambil data dari server.', 'error');
    }
}

// Fungsi untuk merender tabel skor secara dinamis
function renderSkorTable(criteria_benefit, criteria_cost, alternatives) {
    // Buat elemen tabel
    const table = document.createElement('table');
    table.className = 'min-w-full border-collapse block md:table';
    table.id = 'skor-table';

    // Buat header tabel
    const thead = table.createTHead();
    const headerRow = thead.insertRow();

    // Header untuk "Alternatif \ Kriteria"
    const thAlternatif = document.createElement('th');
    thAlternatif.textContent = 'Alternatif \ Kriteria';
    thAlternatif.className = 'p-2 border border-gray-300 bg-gray-200';
    headerRow.appendChild(thAlternatif);

    // Header untuk Kriteria Benefit
    if (criteria_benefit && criteria_benefit.length > 0) {
        criteria_benefit.forEach(k => {
            const th = document.createElement('th');
            th.textContent = `${k} (Benefit)`;
            th.className = 'p-2 border border-gray-300 bg-gray-200';
            headerRow.appendChild(th);
        });
    }

    // Header untuk Kriteria Cost
    if (criteria_cost && criteria_cost.length > 0) {
        criteria_cost.forEach(k => {
            const th = document.createElement('th');
            th.textContent = `${k} (Cost)`;
            th.className = 'p-2 border border-gray-300 bg-gray-200';
            headerRow.appendChild(th);
        });
    }

    const tbody = table.createTBody();

    // Buat baris untuk setiap alternatif
    alternatives.forEach(alt => {
        const row = tbody.insertRow();

        // Sel untuk Alternatif
        const tdAlternatif = row.insertCell();
        tdAlternatif.textContent = alt;
        tdAlternatif.className = 'p-2 border border-gray-300 font-semibold';
        row.appendChild(tdAlternatif);

        // Sel input untuk Kriteria Benefit
        if (criteria_benefit && criteria_benefit.length > 0) {
            criteria_benefit.forEach(k => {
                const tdSkor = row.insertCell();
                const inputSkor = document.createElement('input');
                inputSkor.type = 'number';
                inputSkor.min = '0';
                inputSkor.step = 'any';
                inputSkor.required = true;
                inputSkor.className = 'score-input border border-gray-300 rounded p-1 w-full';
                inputSkor.name = `${alt}-${k}`;
                inputSkor.placeholder = '0';
                tdSkor.appendChild(inputSkor);
                tdSkor.className = 'p-2 border border-gray-300';
            });
        }

        // Sel input untuk Kriteria Cost
        if (criteria_cost && criteria_cost.length > 0) {
            criteria_cost.forEach(k => {
                const tdSkor = row.insertCell();
                const inputSkor = document.createElement('input');
                inputSkor.type = 'number';
                inputSkor.min = '0';
                inputSkor.step = 'any';
                inputSkor.required = true;
                inputSkor.className = 'score-input border border-gray-300 rounded p-1 w-full';
                inputSkor.name = `${alt}-${k}`;
                inputSkor.placeholder = '0';
                tdSkor.appendChild(inputSkor);
                tdSkor.className = 'p-2 border border-gray-300';
            });
        }
    });

    // Masukkan tabel ke dalam container
    skorContainer.innerHTML = ''; // Kosongkan konten sebelumnya
    skorContainer.appendChild(table);
}

// Fungsi untuk mengumpulkan skor dan mengirimkan ke backend
async function submitScores() {
    // Ambil data kriteria dan alternatif lagi untuk memastikan konsistensi
    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/get-input`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        hideLoading();

        if (response.ok) {
            const { criteria_benefit, criteria_cost, alternatives } = data;

            // Kumpulkan semua input skor
            const skorInputs = document.querySelectorAll('.score-input');
            let matrix_benefit = [];
            let matrix_cost = [];

            // Inisialisasi matriks
            alternatives.forEach(() => {
                matrix_benefit.push([]);
                matrix_cost.push([]);
            });

            skorInputs.forEach(input => {
                const [alt, kr] = input.name.split('-');
                const value = parseFloat(input.value);
                const altIndex = alternatives.indexOf(alt);

                if (criteria_benefit.includes(kr)) {
                    matrix_benefit[altIndex].push(value);
                } else if (criteria_cost.includes(kr)) {
                    matrix_cost[altIndex].push(value);
                }
            });

            // Validasi: Pastikan semua input diisi dan valid
            let allValid = true;
            skorInputs.forEach(input => {
                if (input.value.trim() === '' || isNaN(parseFloat(input.value)) || parseFloat(input.value) < 0) {
                    allValid = false;
                }
            });

            if (!allValid) {
                showAlert('Semua skor harus diisi dan berupa angka non-negatif.', 'error');
                return;
            }

            // Siapkan payload
            const payload = {
                matrix_benefit: matrix_benefit,
                matrix_cost: matrix_cost
            };

            // Kirim payload ke backend
            showLoading();
            submitButton.disabled = true; // Nonaktifkan tombol Submit

            try {
                const calcResponse = await fetch(`${API_BASE_URL}/calculate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const calcData = await calcResponse.json();
                hideLoading();
                submitButton.disabled = false; // Aktifkan kembali tombol Submit

                if (calcResponse.ok) {
                    showAlert(calcData.message || 'Perhitungan SAW berhasil.', 'success');

                    // Simpan hasil ke sessionStorage
                    sessionStorage.setItem('sawResults', JSON.stringify(calcData.data));

                    // Alihkan ke halaman hasil
                    window.location.href = 'saw-results-page.html';
                } else {
                    console.error('Error Response:', calcData);
                    showAlert(`Error: ${calcData.error || 'Perhitungan SAW gagal.'}`, 'error');
                }
            } catch (error) {
                hideLoading();
                submitButton.disabled = false; 
                console.error('Fetch Error:', error);
                showAlert('Terjadi kesalahan saat mengirim data ke server.', 'error');
            }
        } else {
            console.error('Error Response:', data);
            showAlert(`Error: ${data.error || 'Terjadi kesalahan.'}`, 'error');
        }
    } catch (error) {
        hideLoading();
        console.error('Fetch Error:', error);
        showAlert('Terjadi kesalahan saat mengambil data dari server.', 'error');
    }
}

submitButton.addEventListener('click', submitScores);

if (backButton) {
    backButton.addEventListener('click', () => {
        window.history.back(); 
    });
}

window.onload = fetchCriteriaAndAlternatives;