/* ---------------------------------- Utility Functions ---------------------------------- */
function showAlert(message, type = 'info') {
    alert(message);
}

function navigateTo(page) {
    window.location.href = `./${page}.html`;
}

/* ---------------------------------- Fetch Helpers ---------------------------------- */
async function fetchJSON(url, options = {}) {
    try {
        const response = await fetch(url, options);
        const contentType = response.headers.get('Content-Type');

        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Terjadi kesalahan');
            }
            return data;
        } else {
            // Handle non-JSON responses if necessary
            throw new Error('Respons tidak valid dari server.');
        }
    } catch (error) {
        console.error(`Error fetching ${url}:`, error);
        throw error;
    }
}

/* ---------------------------------- API Functions ---------------------------------- */
async function saveInput(criteria, alternatives) {
    try {
        const data = await fetchJSON(`${API_BASE_URL}/save-input`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ criteria, alternatives })
        });
        showAlert(data.message, 'success');
        navigateTo('ahp-criteria-page');
    } catch (error) {
        showAlert(error.message, 'error');
    }
}

async function compareCriteria(comparisonsMatrix) {
    try {
        const data = await fetchJSON(`${API_BASE_URL}/compare_criteria`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ comparisons: comparisonsMatrix })
        });

        if (data.warning) {
            showAlert(`${data.warning}\nConsistency Ratio (CR): ${data.CR.toFixed(4)}`, 'warning');
        } else {
            showAlert(`Consistency Ratio (CR): ${data.CR.toFixed(4)}`, 'success');
        }

        navigateTo('ahp-alternative-page');
    } catch (error) {
        showAlert(error.message, 'error');
    }
}

async function compareAlternatives(criteriaName, comparisonsMatrix) {
    try {
        const data = await fetchJSON(`${API_BASE_URL}/compare_alternatives`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ criteria_name: criteriaName, comparisons: comparisonsMatrix })
        });

        if (data.warning) {
            showAlert(`${data.warning}\nConsistency Ratio (CR): ${data.CR.toFixed(4)}`, 'warning');
        } else {
            showAlert(`Consistency Ratio (CR): ${data.CR.toFixed(4)}`, 'success');
        }

        // Optionally, navigate or allow multiple comparisons
    } catch (error) {
        showAlert(error.message, 'error');
    }
}

async function calculateWeights() {
    try {
        const data = await fetchJSON(`${API_BASE_URL}/calculate`, { method: 'GET' });
        showAlert('Perhitungan selesai.', 'success');
        navigateTo('ahp-results-page');
    } catch (error) {
        showAlert(error.message, 'error');
    }
}

async function getResults() {
    return await fetchJSON(`${API_BASE_URL}/results`, { method: 'GET' });
}

async function exportToExcel() {
    try {
        const response = await fetch(`${API_BASE_URL}/export-excel`, { method: 'GET' });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Gagal mengekspor Excel');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'Hasil_AHP.xlsx';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        showAlert('File Excel berhasil diekspor.', 'success');
    } catch (error) {
        console.error('Error exporting Excel:', error);
        showAlert(error.message, 'error');
    }
}

/* ---------------------------------- Data Retrieval Helpers ---------------------------------- */
async function getStoredCriteria() {
    try {
        const data = await fetchJSON(`${API_BASE_URL}/get-criteria`, { method: 'GET' });
        return data.criteria;
    } catch (error) {
        showAlert(error.message, 'error');
        return [];
    }
}

async function getStoredInput() {
    try {
        const data = await fetchJSON(`${API_BASE_URL}/get-input`, { method: 'GET' });
        return { criteria: data.criteria, alternatives: data.alternatives };
    } catch (error) {
        showAlert(error.message, 'error');
        return { criteria: [], alternatives: [] };
    }
}

async function getStoredAlternatives() {
    const inputData = await getStoredInput();
    return inputData.alternatives;
}

/* ---------------------------------- UI Generation Functions ---------------------------------- */
async function generateCriteriaComparisonInputs() {
    try {
        const criteria = await getStoredCriteria();
        const container = document.getElementById('criteria-comparisons-container');
        if (!container) return;

        container.innerHTML = '';

        for (let i = 0; i < criteria.length; i++) {
            for (let j = i + 1; j < criteria.length; j++) {
                const div = document.createElement('div');
                div.className = 'comparison-row';
                div.innerHTML = `
                    <label>${criteria[i]} vs ${criteria[j]}:</label>
                    <input type="number" step="0.1" id="comp-criteria-${i}-${j}" placeholder="Value" required>
                `;
                container.appendChild(div);
            }
        }
    } catch (error) {
        console.error('Error generating criteria comparisons:', error);
        showAlert('Gagal menghasilkan input perbandingan kriteria.', 'error');
    }
}

async function generateAlternativesComparisonInputs() {
    try {
        const alternatives = await getStoredAlternatives();
        const criteria = await getStoredCriteria();
        const container = document.getElementById('alternatives-comparisons-container');
        if (!container) return;

        container.innerHTML = '';

        // Create a section for each criterion
        criteria.forEach(crit => {
            const critDiv = document.createElement('div');
            critDiv.className = 'alternative-comparison-container';
            critDiv.setAttribute('data-criteria', crit);

            const header = document.createElement('h3');
            header.innerText = `Comparisons for ${crit}`;
            critDiv.appendChild(header);

            // Create comparison inputs for each pair of alternatives
            for (let i = 0; i < alternatives.length; i++) {
                for (let j = i + 1; j < alternatives.length; j++) {
                    const rowDiv = document.createElement('div');
                    rowDiv.className = 'comparison-row';
                    rowDiv.innerHTML = `
                        <label>${alternatives[i]} vs ${alternatives[j]}:</label>
                        <input type="number" step="0.1" id="comp-${crit}-${i}-${j}" placeholder="Value" required>
                    `;
                    critDiv.appendChild(rowDiv);
                }
            }

            container.appendChild(critDiv);
        });
    } catch (error) {
        console.error('Error generating alternatives comparisons:', error);
        showAlert('Gagal menghasilkan input perbandingan alternatif.', 'error');
    }
}

/* ---------------------------------- Data Processing Functions ---------------------------------- */
function buildComparisonMatrix(count, inputPrefix) {
    const matrix = Array.from({ length: count }, () => Array(count).fill(1));

    for (let i = 0; i < count; i++) {
        for (let j = i + 1; j < count; j++) {
            const inputId = `${inputPrefix}-${i}-${j}`;
            const inputEl = document.getElementById(inputId);
            if (!inputEl) {
                console.error(`Element with ID ${inputId} not found`);
                continue;
            }

            const val = parseFloat(inputEl.value);
            if (isNaN(val) || val <= 0) {
                showAlert('Nilai perbandingan harus berupa angka positif.');
                throw new Error('Invalid comparison value');
            }

            matrix[i][j] = val;
            matrix[j][i] = 1 / val;
        }
    }
    return matrix;
}

function displayResultsData(data) {
    const resultsSection = document.getElementById('results-section');
    if (!resultsSection) return;

    resultsSection.innerHTML = ''; // Clear previous results

    // Display Criteria Matrix
    if (data.criteria_matrix) {
        const matrixDiv = document.createElement('div');
        matrixDiv.id = 'criteria-matrix';
        matrixDiv.innerHTML = '<h2>Matriks Kriteria</h2>';
        const table = document.createElement('table');
        table.border = '1';
        const headers = [''].concat(Object.keys(data.criteria_matrix));
        let headerRow = '<tr><th></th>';
        headers.slice(1).forEach(header => { headerRow += `<th>${header}</th>`; });
        headerRow += '</tr>';
        table.innerHTML += headerRow;

        Object.keys(data.criteria_matrix).forEach(row => {
            let rowHTML = `<tr><th>${row}</th>`;
            Object.keys(data.criteria_matrix[row]).forEach(col => {
                rowHTML += `<td>${parseFloat(data.criteria_matrix[row][col]).toFixed(4)}</td>`;
            });
            rowHTML += '</tr>';
            table.innerHTML += rowHTML;
        });

        matrixDiv.appendChild(table);
        resultsSection.appendChild(matrixDiv);
    }

    // Display Criteria Weights
    if (data.criteria_weights) {
        const weightsDiv = document.createElement('div');
        weightsDiv.id = 'criteria-weights';
        weightsDiv.innerHTML = '<h2>Bobot Kriteria</h2>';
        const table = document.createElement('table');
        table.border = '1';
        table.innerHTML = '<tr><th>Kriteria</th><th>Bobot</th></tr>';

        Object.keys(data.criteria_weights).forEach(crit => {
            const row = `<tr><td>${crit}</td><td>${parseFloat(data.criteria_weights[crit].Bobot).toFixed(4)}</td></tr>`;
            table.innerHTML += row;
        });

        weightsDiv.appendChild(table);
        resultsSection.appendChild(weightsDiv);
    }

    // Display Final Ranking
    if (data.final_ranking) {
        const rankingDiv = document.createElement('div');
        rankingDiv.id = 'final-ranking';
        rankingDiv.innerHTML = '<h2>Ranking Akhir</h2>';
        const table = document.createElement('table');
        table.border = '1';
        table.innerHTML = '<tr><th>Alternatif</th><th>Skor Akhir</th></tr>';

        Object.keys(data.final_ranking).forEach(alt => {
            const row = `<tr><td>${alt}</td><td>${parseFloat(data.final_ranking[alt].Skor_Akhir).toFixed(4)}</td></tr>`;
            table.innerHTML += row;
        });

        rankingDiv.appendChild(table);
        resultsSection.appendChild(rankingDiv);
    }

    // Similarly, display alternative matrices and weights as needed
    // Example for alternative matrices
    if (data.alternative_matrices) {
        const altMatricesDiv = document.createElement('div');
        altMatricesDiv.id = 'alternative-matrices';
        altMatricesDiv.innerHTML = '<h2>Matriks Alternatif</h2>';

        Object.keys(data.alternative_matrices).forEach(crit => {
            const critDiv = document.createElement('div');
            critDiv.innerHTML = `<h3>Matriks Alternatif untuk ${crit}</h3>`;
            const table = document.createElement('table');
            table.border = '1';
            const headers = [''].concat(Object.keys(data.alternative_matrices[crit]));
            let headerRow = '<tr><th></th>';
            headers.slice(1).forEach(header => { headerRow += `<th>${header}</th>`; });
            headerRow += '</tr>';
            table.innerHTML += headerRow;

            Object.keys(data.alternative_matrices[crit]).forEach(row => {
                let rowHTML = `<tr><th>${row}</th>`;
                Object.keys(data.alternative_matrices[crit][row]).forEach(col => {
                    rowHTML += `<td>${parseFloat(data.alternative_matrices[crit][row][col]).toFixed(4)}</td>`;
                });
                rowHTML += '</tr>';
                table.innerHTML += rowHTML;
            });

            critDiv.appendChild(table);
            altMatricesDiv.appendChild(critDiv);
        });

        resultsSection.appendChild(altMatricesDiv);
    }

    // Example for alternative weights
    if (data.alternative_weights) {
        const altWeightsDiv = document.createElement('div');
        altWeightsDiv.id = 'alternative-weights';
        altWeightsDiv.innerHTML = '<h2>Bobot Alternatif</h2>';

        Object.keys(data.alternative_weights).forEach(crit => {
            const critDiv = document.createElement('div');
            critDiv.innerHTML = `<h3>Bobot Alternatif untuk ${crit}</h3>`;
            const table = document.createElement('table');
            table.border = '1';
            table.innerHTML = '<tr><th>Alternatif</th><th>Bobot</th></tr>';

            Object.keys(data.alternative_weights[crit]).forEach(alt => {
                const row = `<tr><td>${alt}</td><td>${parseFloat(data.alternative_weights[crit][alt].Bobot).toFixed(4)}</td></tr>`;
                table.innerHTML += row;
            });

            critDiv.appendChild(table);
            altWeightsDiv.appendChild(critDiv);
        });

        resultsSection.appendChild(altWeightsDiv);
    }
}
