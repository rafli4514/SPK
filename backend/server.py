from flask import Flask, request, jsonify
from backend.ahp.ahp import AHP  # Import kelas AHP

app = Flask(__name__)

@app.route('/api/ahp', methods=['POST'])
def process_ahp():
    try:
        data = request.json
        criteria = data.get('criteria')
        alternatives = data.get('alternatives')
        criteria_comparisons = data.get('criteria_comparisons')
        alternative_comparisons = data.get('alternative_comparisons')

        # Inisialisasi AHP
        ahp = AHP(criteria, alternatives)

        # Set perbandingan kriteria
        ahp.set_criteria_comparisons(criteria_comparisons)

        # Set perbandingan alternatif
        for crit, comp in alternative_comparisons.items():
            ahp.set_alternative_comparisons(crit, comp)

        # Hitung AHP
        ahp.perform_ahp()
        results = ahp.get_results()

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)