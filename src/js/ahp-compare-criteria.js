// ahp-compare-criteria.js

document.addEventListener('DOMContentLoaded', function () {
    const API_BASE_URL = 'http://localhost:5000/api';

    const alertContainer = document.getElementById('alert-container');
    const tabelKriteriaElem = document.getElementById('tabel-kriteria');
    const loadingSpinner = document.getElementById('loading-spinner');
    const submitButton = document.getElementById('submit-button');
    const backButton = document.getElementById('back-button');

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

    // Fungsi Navigasi ke Halaman Tertentu
    function navigateTo(page) {
        window.location.href = page;
    }

    // Mengambil kriteria dari backend
    fetch(`${API_BASE_URL}/get-criteria`)
        .then(response => response.json())
        .then(data => {
            const namaKriteria = data.criteria || [];
            if (namaKriteria.length === 0) {
                showAlert('Tidak ada kriteria ditemukan. Silakan kembali ke halaman sebelumnya!', 'error');
                setTimeout(() => {
                    navigateTo('ahp-page.html');
                }, 2000);
                return;
            }

            // Panggil fungsi untuk membuat matriks perbandingan
            buatTabelKriteria(namaKriteria);
        })
        .catch(error => {
            console.error('Error fetching criteria:', error);
            showAlert('Gagal memuat kriteria!', 'error');
        });

    // Fungsi untuk membuat tabel matriks NxN
    function buatTabelKriteria(namaKriteria) {
        let jumlahKriteria = namaKriteria.length;

        let html = '';

        // Header Tabel
        html += '<thead><tr class="bg-gray-200">';
        html += `<th class="border border-gray-300 p-2"></th>`;
        namaKriteria.forEach(kriteria => {
            html += `<th class="border border-gray-300 p-2">${kriteria}</th>`;
        });
        html += '</tr></thead>';

        // Body Tabel
        html += '<tbody>';
        for (let i = 0; i < jumlahKriteria; i++) {
            html += `<tr>`;
            html += `<td class="border border-gray-300 p-2 font-semibold">${namaKriteria[i]}</td>`;
            for (let j = 0; j < jumlahKriteria; j++) {
                if (i === j) {
                    // Diagonal selalu 1
                    html += `
                        <td class="border border-gray-300 p-2">
                            <input type="text" value="1" readonly
                                class="w-full text-center border rounded p-1 bg-gray-200 readonly-input">
                        </td>`;
                } else if (i < j) {
                    // Bagian atas diagonal (user input)
                    html += `
                        <td class="border border-gray-300 p-2">
                            <input type="text" placeholder="1/3 atau 3" maxlength="8"
                                class="w-full sm:w-24 md:w-32 text-center border rounded p-1 focus:outline-violet-500 perbandingan-input"
                                data-i="${i}" data-j="${j}">
                        </td>`;
                } else {
                    // Bagian bawah diagonal (otomatis terisi 1/value dari atas)
                    html += `
                        <td class="border border-gray-300 p-2">
                            <input type="text" readonly
                                class="w-full sm:w-24 md:w-32 text-center border rounded p-1 bg-gray-200 mirror-input readonly-input"
                                data-i="${i}" data-j="${j}" value="1">
                        </td>`;
                }
            }
            html += `</tr>`;
        }
        html += '</tbody>';

        tabelKriteriaElem.innerHTML = html;

        // Event listener untuk input di bagian atas diagonal
        const perbandinganInputs = tabelKriteriaElem.querySelectorAll('.perbandingan-input');
        perbandinganInputs.forEach(input => {
            input.addEventListener('input', function () {
                const inputVal = this.value.trim();
                const i = parseInt(this.getAttribute('data-i'), 10);
                const j = parseInt(this.getAttribute('data-j'), 10);

                let parsedValue = parseFraction(inputVal);

                if (parsedValue !== null && parsedValue > 0) {
                    // Cari sel mirror (j,i)
                    const mirrorCell = tabelKriteriaElem.querySelector(`.mirror-input[data-i='${j}'][data-j='${i}']`);
                    if (mirrorCell) {
                        const inverseVal = (1 / parsedValue).toFixed(4);
                        mirrorCell.value = inverseVal;
                    }
                } else {
                    // Jika input tidak valid, reset mirror dan berikan pesan
                    const mirrorCell = tabelKriteriaElem.querySelector(`.mirror-input[data-i='${j}'][data-j='${i}']`);
                    if (mirrorCell) {
                        mirrorCell.value = '1';
                    }
                    if (inputVal !== '') {
                        showAlert(`Nilai perbandingan antara kriteria ${i + 1} dan ${j + 1} tidak valid! Harus antara 1/9 dan 9.`, 'error');
                    }
                }
            });
        });
    }

    // Fungsi untuk parse input seperti "1/3" atau "3"
    function parseFraction(input) {
        if (input.includes('/')) {
            const parts = input.split('/');
            if (parts.length !== 2) return null;
            const numerator = parseFloat(parts[0]);
            const denominator = parseFloat(parts[1]);
            if (isNaN(numerator) || isNaN(denominator) || denominator === 0) return null;
            const value = numerator / denominator;
            if (value < (1 / 9) || value > 9) return null;
            return value;
        } else {
            const num = parseFloat(input);
            if (isNaN(num) || num <= 0 || num < (1 / 9) || num > 9) return null;
            return num;
        }
    }

    // Event Listener untuk Tombol Submit
    if (submitButton) {
        submitButton.addEventListener('click', function () {
            let comparisons = [];
            let isValid = true;

            const rows = tabelKriteriaElem.querySelectorAll('tbody tr');
            const n = rows.length;

            // Baca nilai input dari tabel (bagian atas diagonal)
            outerLoop:
                for (let i = 0; i < n; i++) {
                    const row = rows[i];
                    const inputs = row.querySelectorAll('input.perbandingan-input');
                    for (let input of inputs) {
                        const j = parseInt(input.getAttribute('data-j'), 10);
                        const value = input.value.trim();

                        // Validasi input
                        if (value === '') {
                            showAlert(`Nilai perbandingan antara kriteria ${i + 1} dan ${j + 1} tidak boleh kosong!`, 'error');
                            isValid = false;
                            break outerLoop;
                        }

                        const num = parseFraction(value);
                        if (num === null || num <= 0) {
                            showAlert(`Nilai perbandingan antara kriteria ${i + 1} dan ${j + 1} harus berupa angka positif atau fraksional antara 1/9 dan 9!`, 'error');
                            isValid = false;
                            break outerLoop;
                        }

                        comparisons.push({
                            i: i,
                            j: j,
                            value: num.toString()
                        });
                    }
                }

            if (!isValid) return;

            // Tampilkan spinner
            if (loadingSpinner) {
                loadingSpinner.classList.remove('hidden');
            }

            // Mengirim perbandingan ke backend
            fetch(`${API_BASE_URL}/compare_criteria`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ comparisons })
            })
                .then(response => response.json())
                .then(data => {
                    if (loadingSpinner) {
                        loadingSpinner.classList.add('hidden');
                    }
                    if (data.error) {
                        showAlert(`Error: ${data.error}`, 'error');
                    } else {
                        if (data.warning) {
                            const confirmProceed = confirm(`CR: ${data.CR}\n${data.warning}\nApakah Anda ingin melanjutkan?`);
                            if (!confirmProceed) {
                                return;
                            }
                        }
                        if (data.CR !== undefined) {
                            showAlert(`Perbandingan berhasil disimpan. CR: ${data.CR}`, 'success');
                        } else {
                            showAlert('Perbandingan berhasil disimpan.', 'success');
                        }
                        navigateTo('ahp-alternative-page.html');
                    }
                })
                .catch(error => {
                    if (loadingSpinner) {
                        loadingSpinner.classList.add('hidden');
                    }
                    console.error('Error mengirim perbandingan:', error);
                    showAlert('Terjadi kesalahan saat mengirim data ke server.', 'error');
                });
        });
    }

    // Event Listener untuk Tombol Kembali
    if (backButton) {
        backButton.addEventListener('click', function () {
            navigateTo('ahp-page.html');
        });
    }
});
