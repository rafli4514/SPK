// ahp-result-page.js

document.addEventListener('DOMContentLoaded', () => {
    const baseUrl = 'http://localhost:5000/api'; 

    const alertContainer = document.getElementById('alert-container');
    const loadingIndicator = document.getElementById('loading-indicator');
    const content = document.getElementById('content');
    const exportButton = document.getElementById('export-button');
    const backButton = document.querySelector('.bg-indigo-600 button'); 

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

    function displayMatrix(matrixData, containerId, headerType) {
        let container = document.getElementById(containerId);
        if (!container) return;

        const keys = Object.keys(matrixData);
        if (keys.length === 0) {
            container.innerHTML = '<p class="text-gray-500">Data kosong</p>';
            return;
        }

        let table = '<table class="w-full border border-gray-300 text-center text-sm">';
        table += '<thead><tr class="bg-gray-200">';
        table += `<th class="border border-gray-300 p-2">${headerType}</th>`;
        keys.forEach(k => {
            table += `<th class="border border-gray-300 p-2">${k}</th>`;
        });
        table += '</tr></thead><tbody>';
        keys.forEach(rowKey => {
            table += `<tr><td class="border border-gray-300 p-2 font-semibold">${rowKey}</td>`;
            keys.forEach(colKey => {
                table += `<td class="border border-gray-300 p-2">${matrixData[rowKey][colKey]}</td>`;
            });
            table += '</tr>';
        });
        table += '</tbody></table>';

        container.innerHTML += table;
    }

    function displayWeights(weightsData, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const keys = Object.keys(weightsData);
        if (keys.length === 0) {
            container.innerHTML = '<p class="text-gray-500">Data kosong</p>';
            return;
        }

        let table = '<table class="w-full border border-gray-300 text-center text-sm">';
        table += '<thead><tr class="bg-gray-200">';
        table += '<th class="border border-gray-300 p-2">Kriteria</th>';
        table += '<th class="border border-gray-300 p-2">Bobot</th>';
        table += '</tr></thead><tbody>';
        keys.forEach(k => {
            table += `<tr><td class="border border-gray-300 p-2">${k}</td>`;
            table += `<td class="border border-gray-300 p-2">${weightsData[k]['Bobot'].toFixed(4)}</td></tr>`;
        });
        table += '</tbody></table>';

        container.innerHTML = table;
    }

    function displayAltWeights(weightsData, containerElement) {
        const keys = Object.keys(weightsData);
        if (keys.length === 0) {
            containerElement.innerHTML += '<p class="text-gray-500">Data kosong</p>';
            return;
        }

        let table = '<table class="w-full border border-gray-300 text-center text-sm">';
        table += '<thead><tr class="bg-gray-200">';
        table += '<th class="border border-gray-300 p-2">Alternatif</th>';
        table += '<th class="border border-gray-300 p-2">Bobot</th>';
        table += '</tr></thead><tbody>';
        keys.forEach(alt => {
            table += `<tr><td class="border border-gray-300 p-2">${alt}</td>`;
            table += `<td class="border border-gray-300 p-2">${weightsData[alt]['Bobot'].toFixed(4)}</td></tr>`;
        });
        table += '</tbody></table>';

        containerElement.innerHTML += table;
    }

    function displayRanking(rankingData, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const finalRank = rankingData['Skor Akhir'];
        const keys = Object.keys(finalRank);

        if (keys.length === 0) {
            container.innerHTML = '<p class="text-gray-500">Data kosong</p>';
            return;
        }

        // Sort berdasarkan nilai skor akhir secara menurun
        const sorted = keys.sort((a, b) => finalRank[b] - finalRank[a]);

        let table = '<table class="w-full border border-gray-300 text-center text-sm">';
        table += '<thead><tr class="bg-gray-200">';
        table += '<th class="border border-gray-300 p-2">Alternatif</th>';
        table += '<th class="border border-gray-300 p-2">Skor Akhir</th>';
        table += '<th class="border border-gray-300 p-2">Ranking</th>';
        table += '</tr></thead><tbody>';
        sorted.forEach((alt, index) => {
            table += `<tr><td class="border border-gray-300 p-2">${alt}</td>`;
            table += `<td class="border border-gray-300 p-2">${finalRank[alt].toFixed(4)}</td>`;
            table += `<td class="border border-gray-300 p-2">${index + 1}</td></tr>`;
        });
        table += '</tbody></table>';

        container.innerHTML = table;
    }

    function createTitle(text, container) {
        const h3 = document.createElement('h3');
        h3.className = 'text-lg font-semibold mb-2 mt-4';
        h3.innerText = text;
        container.appendChild(h3);
    }

    function displayAlternativeMatrices(alternativeMatrices, alternativeWeights) {
        const altMatricesSection = document.getElementById('alternative-matrices-section');
        const altWeightsSection = document.getElementById('alternative-weights-section');

        if (!altMatricesSection || !altWeightsSection) return;

        Object.keys(alternativeMatrices).forEach(crit => {
            createTitle(`Matriks Alternatif untuk Kriteria: ${crit}`, altMatricesSection);
            displayMatrix(alternativeMatrices[crit], 'alternative-matrices-section', 'Alternatif');

            createTitle(`Bobot Alternatif untuk Kriteria: ${crit}`, altWeightsSection);
            displayAltWeights(alternativeWeights[crit], altWeightsSection);
        });
    }

    function initializeResultsPage(data) {
        hideLoading();
        if (data.error) {
            showAlert(`Error: ${data.error}\nCek kembali input data Anda.`, 'error');
            return;
        }

        displayMatrix(data.criteria_matrix, 'criteria-matrix', 'Kriteria');
        displayWeights(data.criteria_weights, 'criteria-weights');
        displayAlternativeMatrices(data.alternative_matrices, data.alternative_weights);
        displayRanking(data.final_ranking, 'final-ranking');
        content.classList.remove('hidden');

        if (data.warnings && data.warnings.length > 0) {
            data.warnings.forEach(warning => {
                showAlert(warning, 'error');
            });
        }
    }

    function exportToExcel() {
        fetch(`${baseUrl}/results`)
            .then(res => {
                if (!res.ok) {
                    throw new Error("Gagal memuat hasil untuk ekspor.");
                }
                return res.json();
            })
            .then(data => {
                if (data.error) {
                    showAlert(`Error: ${data.error}`, 'error');
                    return;
                }

                const wb = XLSX.utils.book_new();

                const criteriaMatrixTable = document.querySelector('#criteria-matrix table');
                if (criteriaMatrixTable) {
                    const criteriaMatrix = XLSX.utils.table_to_sheet(criteriaMatrixTable);
                    XLSX.utils.book_append_sheet(wb, criteriaMatrix, 'Matriks Kriteria');
                }

                const criteriaWeightsTable = document.querySelector('#criteria-weights table');
                if (criteriaWeightsTable) {
                    const criteriaWeights = XLSX.utils.table_to_sheet(criteriaWeightsTable);
                    XLSX.utils.book_append_sheet(wb, criteriaWeights, 'Bobot Kriteria');
                }

                const alternativeMatricesTables = document.querySelectorAll('#alternative-matrices-section table');
                alternativeMatricesTables.forEach((table, index) => {
                    const sheet = XLSX.utils.table_to_sheet(table);
                    const sheetName = `Matriks Alternatif ${index + 1}`;
                    XLSX.utils.book_append_sheet(wb, sheet, sheetName);
                });

                const alternativeWeightsTables = document.querySelectorAll('#alternative-weights-section table');
                alternativeWeightsTables.forEach((table, index) => {
                    const sheet = XLSX.utils.table_to_sheet(table);
                    const sheetName = `Bobot Alternatif ${index + 1}`;
                    XLSX.utils.book_append_sheet(wb, sheet, sheetName);
                });

                const finalRankingTable = document.querySelector('#final-ranking table');
                if (finalRankingTable) {
                    const finalRanking = XLSX.utils.table_to_sheet(finalRankingTable);
                    XLSX.utils.book_append_sheet(wb, finalRanking, 'Ranking Akhir');
                }

                XLSX.writeFile(wb, 'Hasil_AHP.xlsx');
            })
            .catch(err => {
                console.error('Error mengexport ke Excel:', err);
                showAlert('Terjadi kesalahan saat mengexport data ke Excel!', 'error');
            });
    }

    function fetchAndDisplayResults() {
        showLoading();
        fetch(`${baseUrl}/calculate`, { method: 'GET' })
            .then(res => {
                if (!res.ok) {
                    throw new Error("Gagal menghitung. Pastikan Anda telah:\n1. Menginput kriteria & alternatif (/api/save-input)\n2. Menginput perbandingan kriteria (/api/compare_criteria)\n3. Menginput perbandingan alternatif (/api/compare_alternatives) untuk setiap kriteria.");
                }
                return res.json();
            })
            .then(() => {
                return fetch(`${baseUrl}/results`);
            })
            .then(res => {
                if (!res.ok) {
                    throw new Error("Gagal memuat hasil. Pastikan semua langkah sudah selesai dan tidak ada error pada input data.");
                }
                return res.json();
            })
            .then(data => {
                initializeResultsPage(data);
            })
            .catch(err => {
                hideLoading();
                console.error(err);
                showAlert(err.message, 'error');
            });
    }

    fetchAndDisplayResults();

    if (exportButton) {
        exportButton.addEventListener('click', () => {
            exportToExcel();
        });
    }

    if (backButton) {
        backButton.addEventListener('click', () => {
            navigateTo('ahp-alternative-page.html'); 
        });
    }
});
