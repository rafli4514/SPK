// saw-result-page.js

document.addEventListener('DOMContentLoaded', () => {
    const baseUrl = 'http://localhost:5000/api/saw'; // Sesuaikan dengan URL backend Anda
    
    const alertContainer = document.getElementById('alert-container');
    const loadingIndicator = document.getElementById('loading-indicator');
    const content = document.getElementById('content');
    const exportButton = document.getElementById('export-button');
    const backButton = document.getElementById('back-button'); 
    
    function showAlert(message, type = 'error') {
        alertContainer.innerHTML = '';
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert ${type === 'error' ? 'alert-error' : 'alert-success'} p-4 mb-4 border rounded-lg`;
        alertDiv.textContent = message;
        alertContainer.appendChild(alertDiv);
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
    
    function navigateTo(page) {
        window.location.href = page;
    }
    
    function showLoading() {
        if (loadingIndicator) loadingIndicator.classList.remove('hidden');
        if (content) content.classList.add('hidden');
    }
    
    function hideLoading() {
        if (loadingIndicator) loadingIndicator.classList.add('hidden');
        if (content) content.classList.remove('hidden');
    }
    
    // Fungsi untuk menampilkan tabel matriks
    function displayMatrix(matrixData, containerId, headerType) {
        let container = document.getElementById(containerId);
        if (!container) return;
    
        if (!matrixData || Object.keys(matrixData).length === 0) {
            container.innerHTML = '<p class="text-gray-500">Data kosong</p>';
            return;
        }
    
        let table = '<table class="w-full border border-gray-300 text-center text-sm">';
        table += '<thead><tr class="bg-gray-200">';
        table += `<th class="border border-gray-300 p-2">${headerType}</th>`;
        const headers = Object.keys(matrixData[Object.keys(matrixData)[0]]);
        headers.forEach(k => {
            table += `<th class="border border-gray-300 p-2">${k}</th>`;
        });
        table += '</tr></thead><tbody>';
        for (const rowKey in matrixData) {
            table += `<tr><td class="border border-gray-300 p-2 font-semibold">${rowKey}</td>`;
            headers.forEach(colKey => {
                table += `<td class="border border-gray-300 p-2">${matrixData[rowKey][colKey]}</td>`;
            });
            table += '</tr>';
        }
        table += '</tbody></table>';
    
        container.innerHTML = table;
    }
    
    // Fungsi untuk menampilkan tabel bobot
    function displayWeights(weightsData, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
    
        if (!weightsData || Object.keys(weightsData).length === 0) {
            container.innerHTML = '<p class="text-gray-500">Data kosong</p>';
            return;
        }
    
        let table = '<table class="w-full border border-gray-300 text-center text-sm">';
        table += '<thead><tr class="bg-gray-200">';
        table += '<th class="border border-gray-300 p-2">Kriteria</th>';
        table += '<th class="border border-gray-300 p-2">Bobot</th>';
        table += '</tr></thead><tbody>';
        for (const crit in weightsData) {
            table += `<tr><td class="border border-gray-300 p-2">${crit}</td>`;
            table += `<td class="border border-gray-300 p-2">${weightsData[crit].toFixed(4)}</td></tr>`;
        }
        table += '</tbody></table>';
    
        container.innerHTML = table;
    }
    
    // Fungsi untuk menampilkan skor dan ranking
    function displayRanking(rankedAlternatives, rankedScores, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
    
        if (!rankedAlternatives || rankedAlternatives.length === 0) {
            container.innerHTML = '<p class="text-gray-500">Data kosong</p>';
            return;
        }
    
        let table = '<table class="w-full border border-gray-300 text-center text-sm">';
        table += '<thead><tr class="bg-gray-200">';
        table += '<th class="border border-gray-300 p-2">No</th>';
        table += '<th class="border border-gray-300 p-2">Alternatif</th>';
        table += '<th class="border border-gray-300 p-2">Skor</th>';
        table += '</tr></thead><tbody>';
        rankedAlternatives.forEach((alt, index) => {
            table += `<tr><td class="border border-gray-300 p-2">${index + 1}</td>`;
            table += `<td class="border border-gray-300 p-2">${alt}</td>`;
            table += `<td class="border border-gray-300 p-2">${rankedScores[index].toFixed(4)}</td></tr>`;
        });
        table += '</tbody></table>';
    
        container.innerHTML = table;
    }
    
    // Fungsi untuk inisialisasi halaman hasil SAW
    function initializeResultsPage(data) {
        hideLoading();
        if (data.error) {
            showAlert(`Error: ${data.error}`, 'error');
            return;
        }
    
        // Menampilkan Matriks Benefit
        createSectionTitle('Matriks Benefit', 'benefit-matrix-title', 'benefit-matrix');
        displayMatrix(data.matriks_benefit, 'benefit-matrix', 'Alternatif');
    
        // Menampilkan Matriks Cost
        createSectionTitle('Matriks Cost', 'cost-matrix-title', 'cost-matrix');
        displayMatrix(data.matriks_cost, 'cost-matrix', 'Alternatif');
    
        // Menampilkan Normalisasi Benefit
        createSectionTitle('Normalisasi Matriks Benefit', 'normal-benefit-title', 'normal-benefit');
        displayMatrix(data.matriks_normal_benefit, 'normal-benefit', 'Alternatif');
    
        // Menampilkan Normalisasi Cost
        createSectionTitle('Normalisasi Matriks Cost', 'normal-cost-title', 'normal-cost');
        displayMatrix(data.matriks_normal_cost, 'normal-cost', 'Alternatif');
    
        // Menampilkan Skor dan Ranking
        displayRanking(data.ranked_alternatives, data.ranked_scores, 'final-ranking');
    
        content.classList.remove('hidden');
    }
    
    // Fungsi untuk membuat judul seksi
    function createSectionTitle(text, id, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
    
        const title = document.createElement('h3');
        title.id = id;
        title.className = 'text-lg font-semibold mb-2 mt-4';
        title.innerText = text;
        container.appendChild(title);
    }
    
    // Fungsi untuk ekspor hasil ke Excel
    function exportToExcel() {
        // Ambil data dari sessionStorage
        const hasilJSON = sessionStorage.getItem('sawResults');
        if (!hasilJSON) {
            showAlert('Tidak ada data untuk diekspor.', 'error');
            return;
        }
    
        const hasil = JSON.parse(hasilJSON);
    
        const wb = XLSX.utils.book_new();
    
        // Tambahkan Matriks Benefit
        if (hasil.matriks_benefit) {
            const ws_benefit = XLSX.utils.json_to_sheet(convertMatrixToArray(hasil.matriks_benefit));
            XLSX.utils.book_append_sheet(wb, ws_benefit, 'Matriks Benefit');
        }
    
        // Tambahkan Matriks Cost
        if (hasil.matriks_cost) {
            const ws_cost = XLSX.utils.json_to_sheet(convertMatrixToArray(hasil.matriks_cost));
            XLSX.utils.book_append_sheet(wb, ws_cost, 'Matriks Cost');
        }
    
        // Tambahkan Normalisasi Matriks Benefit
        if (hasil.matriks_normal_benefit) {
            const ws_normal_benefit = XLSX.utils.json_to_sheet(convertMatrixToArray(hasil.matriks_normal_benefit));
            XLSX.utils.book_append_sheet(wb, ws_normal_benefit, 'Normalisasi Benefit');
        }
    
        // Tambahkan Normalisasi Matriks Cost
        if (hasil.matriks_normal_cost) {
            const ws_normal_cost = XLSX.utils.json_to_sheet(convertMatrixToArray(hasil.matriks_normal_cost));
            XLSX.utils.book_append_sheet(wb, ws_normal_cost, 'Normalisasi Cost');
        }
    
        // Tambahkan Ranking
        if (hasil.ranked_alternatives && hasil.ranked_scores) {
            const rankingData = hasil.ranked_alternatives.map((alt, index) => ({
                'No': index + 1,
                'Alternatif': alt,
                'Skor': hasil.ranked_scores[index].toFixed(4)
            }));
            const ws_ranking = XLSX.utils.json_to_sheet(rankingData);
            XLSX.utils.book_append_sheet(wb, ws_ranking, 'Ranking');
        }
    
        // Simpan file
        XLSX.writeFile(wb, 'Hasil_SAW.xlsx');
    }
    
    // Fungsi untuk mengonversi matriks ke array objek untuk Excel
    function convertMatrixToArray(matrix) {
        const keys = Object.keys(matrix);
        const headers = Object.keys(matrix[keys[0]]);
        const dataArray = [];
    
        keys.forEach(rowKey => {
            const row = { 'Alternatif': rowKey };
            headers.forEach(colKey => {
                row[colKey] = matrix[rowKey][colKey];
            });
            dataArray.push(row);
        });
    
        return dataArray;
    }
    
    // Fungsi untuk mengambil hasil dari backend atau sessionStorage
    function fetchAndDisplayResults() {
        showLoading();
    
        // Ambil hasil dari sessionStorage
        const hasilJSON = sessionStorage.getItem('sawResults');
    
        if (!hasilJSON) {
            hideLoading();
            showAlert('Hasil perhitungan SAW tidak ditemukan. Silakan lakukan perhitungan terlebih dahulu.', 'error');
            return;
        }
    
        const hasil = JSON.parse(hasilJSON);
        initializeResultsPage(hasil);
    }
    
    // Event Listener untuk tombol Ekspor ke Excel
    if (exportButton) {
        exportButton.addEventListener('click', () => {
            exportToExcel();
        });
    }
    
    // Event Listener untuk tombol Kembali
    if (backButton) {
        backButton.addEventListener('click', () => {
            navigateTo('saw-alternative-weights.html'); // Sesuaikan dengan halaman sebelumnya
        });
    }
    
    // Inisialisasi halaman dengan menampilkan hasil
    fetchAndDisplayResults();
});
