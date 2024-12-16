// ahp-compare-alternative.js

document.addEventListener('DOMContentLoaded', function () {
    const API_BASE_URL = 'http://localhost:5000/api';

    const alertContainer = document.getElementById('alert-container');
    const comparisonFormsContainer = document.getElementById('comparison-forms');
    const submitButton = document.getElementById('submit-button');
    const backButton = document.getElementById('back-button');
    const loadingSpinner = document.getElementById('loading-spinner');

    // Fungsi Menampilkan Pesan Alert
    function showAlert(message, type = 'error') {
        // Hapus semua alert yang sudah ada
        alertContainer.innerHTML = '';

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert ${type === 'error' ? 'alert-error' : 'alert-success'} p-4 mb-4 border rounded-lg`;
        alertDiv.textContent = message;
        alertContainer.appendChild(alertDiv);

        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Fungsi Navigasi ke Halaman Tertentu
    function navigateTo(page) {
        window.location.href = page;
    }

    // Fungsi untuk menampilkan indikator loading
    function showLoading() {
        if (loadingSpinner) loadingSpinner.classList.remove('hidden');
    }

    // Fungsi untuk menyembunyikan indikator loading
    function hideLoading() {
        if (loadingSpinner) loadingSpinner.classList.add('hidden');
    }

    // Mengambil data kriteria dan alternatif dari backend
    fetch(`${API_BASE_URL}/get-input`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok (${response.status})`);
            }
            return response.json();
        })
        .then(data => {
            const criteria = data.criteria || [];
            const alternatives = data.alternatives || [];

            if (criteria.length === 0 || alternatives.length === 0) {
                showAlert('Tidak ada kriteria atau alternatif ditemukan. Silakan kembali ke halaman sebelumnya!', 'error');
                setTimeout(() => {
                    navigateTo('ahp-page.html'); 
                }, 2000);
                return;
            }

            // Membuat form perbandingan alternatif untuk setiap kriteria
            createComparisonForms(criteria, alternatives);
        })
        .catch(error => {
            console.error('Error fetching input data:', error);
            showAlert('Gagal memuat data kriteria dan alternatif!', 'error');
        });

    // Fungsi untuk membuat form perbandingan alternatif untuk setiap kriteria
    function createComparisonForms(criteria, alternatives) {
        for (let critIndex = 0; critIndex < criteria.length; critIndex++) {
            const crit = criteria[critIndex];

            let html = `
                <div class="bg-gray-100 p-4 rounded-lg mb-4">
                    <h2 class="text-xl font-semibold mb-4">Perbandingan Alternatif untuk Kriteria: ${crit}</h2>
                    <div class="overflow-x-auto">
                        <table class="w-full min-w-max border border-gray-300 text-center">
                            <thead>
                                <tr class="bg-gray-200">
                                    <th class="border border-gray-300 p-2"></th>
                                    ${alternatives.map(alt => `<th class="border border-gray-300 p-2">${alt}</th>`).join('')}
                                </tr>
                            </thead>
                            <tbody>
                                ${alternatives.map((altRow, i) => `
                                    <tr>
                                        <td class="border border-gray-300 p-2 font-semibold">${altRow}</td>
                                        ${alternatives.map((altCol, j) => {
                                            if (i === j) {
                                                return `
                                                    <td class="border border-gray-300 p-2">
                                                        <input type="text" value="1" readonly
                                                            class="w-full sm:w-24 md:w-32 text-center border rounded p-1 bg-gray-200 readonly-input">
                                                    </td>`;
                                            } else if (i < j) {
                                                return `
                                                    <td class="border border-gray-300 p-2">
                                                        <input type="text" placeholder="1/3 atau 3" maxlength="8"
                                                            class="w-full sm:w-24 md:w-32 text-center border rounded p-1 focus:outline-violet-500 comparison-input"
                                                            data-crit="${critIndex}" data-i="${i}" data-j="${j}">
                                                    </td>`;
                                            } else {
                                                return `
                                                    <td class="border border-gray-300 p-2">
                                                        <input type="text" readonly
                                                            class="w-full sm:w-24 md:w-32 text-center border rounded p-1 bg-gray-200 mirror-input readonly-input"
                                                            data-crit="${critIndex}" data-i="${i}" data-j="${j}" value="1">
                                                    </td>`;
                                            }
                                        }).join('')}
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            comparisonFormsContainer.insertAdjacentHTML('beforeend', html);
        }

        // Pasang event listener untuk input di bagian atas diagonal
        const comparisonInputs = comparisonFormsContainer.querySelectorAll('.comparison-input');
        comparisonInputs.forEach(input => {
            input.addEventListener('input', function () {
                const inputVal = this.value.trim();
                const critIndex = parseInt(this.getAttribute('data-crit'), 10);
                const i = parseInt(this.getAttribute('data-i'), 10);
                const j = parseInt(this.getAttribute('data-j'), 10);

                let parsedValue = parseFraction(inputVal);

                if (parsedValue !== null && parsedValue > 0) {
                    // Cari sel mirror (j,i)
                    const mirrorCell = comparisonFormsContainer.querySelector(`.mirror-input[data-crit='${critIndex}'][data-i='${j}'][data-j='${i}']`);
                    if (mirrorCell) {
                        const inverseVal = (1 / parsedValue).toFixed(4); 
                        mirrorCell.value = inverseVal;
                    }
                } else {
                    // Jika input tidak valid, reset mirror dan berikan pesan
                    const mirrorCell = comparisonFormsContainer.querySelector(`.mirror-input[data-crit='${critIndex}'][data-i='${j}'][data-j='${i}']`);
                    if (mirrorCell) mirrorCell.value = '1';
                    const critNameElem = this.closest('div');
                    let critName = 'Kriteria';
                    if (critNameElem) {
                        const h2 = critNameElem.querySelector('h2');
                        if (h2) {
                            const parts = h2.textContent.split(': ');
                            if (parts.length > 1) {
                                critName = parts[1];
                            }
                        }
                    }
                    showAlert(`Nilai perbandingan antara alternatif ke-${i + 1} dan ke-${j + 1} untuk kriteria "${critName}" tidak valid! Harus antara 1/9 dan 9.`, 'error');
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
            const forms = comparisonFormsContainer.querySelectorAll('div.bg-gray-100');
            let hasError = false;

            showLoading();
            submitButton.disabled = true; // Nonaktifkan tombol Submit

            let allComparisons = [];

            // Loop setiap form (setiap kriteria)
            for (let form of forms) {
                const inputs = form.querySelectorAll('.comparison-input');
                const critNameElem = form.querySelector('h2');
                let critName = 'Kriteria';
                if (critNameElem) {
                    const parts = critNameElem.textContent.split(': ');
                    if (parts.length > 1) {
                        critName = parts[1];
                    }
                }

                const comparisons = [];
                let isValid = true;

                for (let input of inputs) {
                    const i = parseInt(input.getAttribute('data-i'), 10);
                    const j = parseInt(input.getAttribute('data-j'), 10);
                    const valueStr = input.value.trim();
                    const value = parseFraction(valueStr);

                    if (value === null || value <= 0) {
                        showAlert(`Semua nilai perbandingan harus berupa angka positif antara 1/9 dan 9 untuk kriteria "${critName}".`, 'error');
                        isValid = false;
                        hasError = true;
                        break;
                    }

                    comparisons.push({ i, j, value: value.toString() });
                }

                if (!isValid) {
                    break;
                }

                allComparisons.push({
                    criteria_name: critName,
                    comparisons: comparisons
                });
            }

            if (hasError) {
                hideLoading();
                submitButton.disabled = false; 
                return;
            }

            fetch(`${API_BASE_URL}/compare_alternatives_bulk`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ comparisons: allComparisons })
            })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(errData => {
                            throw new Error(errData.error || `Network response was not ok (${response.status})`);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    hideLoading();
                    submitButton.disabled = false; 

                    if (data.error) {
                        showAlert(`Error: ${data.error}`, 'error');
                    } else {
                        if (data.warnings && data.warnings.length > 0) {
                            data.warnings.forEach(warning => {
                                alert(warning); 
                            });
                        }
                        if (data.CR !== undefined) {
                            showAlert(`Perbandingan berhasil disimpan. CR: ${data.CR.toFixed(4)}`, 'success');
                        } else {
                            showAlert('Perbandingan berhasil disimpan.', 'success');
                        }
                        setTimeout(() => {
                            navigateTo('ahp-results-page.html'); 
                        }, 1500);
                    }
                })
                .catch(error => {
                    hideLoading();
                    submitButton.disabled = false; 
                    console.error('Error mengirim perbandingan:', error);
                    showAlert('Terjadi kesalahan saat mengirim data!', 'error');
                });
        });
    }

    if (backButton) {
        backButton.addEventListener('click', function () {
            navigateTo('ahp-criteria-page.html');
        });
    }
});
