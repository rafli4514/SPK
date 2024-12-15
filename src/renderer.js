const { spawn } = require('child_process');

// Fungsi untuk menjalankan AHP Python
function runAHP(criteria, alternatives) {
    return new Promise((resolve, reject) => {
        // Menjalankan script Python
        const pythonProcess = spawn('python', ['methods/ahp.py']);

        let output = '';
        pythonProcess.stdin.write(JSON.stringify({
            criteria: criteria,
            alternatives: alternatives
        }));
        pythonProcess.stdin.end();

        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`Error: ${data}`);
            reject(data.toString());
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve(JSON.parse(output));
            } else {
                reject(`Process exited with code ${code}`);
            }
        });
    });
}

// Handle Button Click
document.getElementById('calculate').addEventListener('click', async () => {
    const criteriaInput = document.getElementById('criteria').value.split(',');
    const alternativesInput = document.getElementById('alternatives').value.split(',');

    try {
        const results = await runAHP(criteriaInput, alternativesInput);
        document.getElementById('output').textContent = JSON.stringify(results, null, 2);
        document.getElementById('results').classList.remove('hidden');
    } catch (error) {
        alert('Error: ' + error);
    }
});
