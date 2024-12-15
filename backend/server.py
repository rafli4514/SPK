import sys
import os
from flask import Flask, request, jsonify

# Menambahkan root direktori proyek ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.ahp.ahp import AHP

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Server Flask berjalan untuk AHP."})

@app.route('/api/ahp', methods=['POST'])
def process_ahp():
    """
    Endpoint untuk memproses metode AHP.
    """
    try:
        # Ambil data dari request JSON
        data = request.json
        criteria = data.get('criteria')
        alternatives = data.get('alternatives')
        criteria_comparisons = data.get('criteria_comparisons')
        alternative_comparisons = data.get('alternative_comparisons')

        # Validasi input
        if not criteria or not alternatives:
            raise ValueError("Kriteria dan alternatif harus disediakan.")

        # Inisialisasi AHP dan input data
        ahp = AHP(criteria, alternatives)
        ahp.set_criteria_comparisons(criteria_comparisons)

        for crit, comp in alternative_comparisons.items():
            ahp.set_alternative_comparisons(crit, comp)

        # Proses perhitungan AHP
        ahp.perform_ahp()
        results = ahp.get_results()

        return jsonify({"status": "success", "results": results}), 200

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
