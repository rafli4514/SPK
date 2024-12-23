# backend/blueprints/saw_bp.py

from flask import Blueprint, request, jsonify, send_file
import logging
import pandas as pd
import io

from saw.saw import SAW

saw_bp = Blueprint('saw_bp', __name__)
logger = logging.getLogger(__name__)

# Initialize SAW object
saw = SAW()

@saw_bp.route('/save-input', methods=['POST'])
def saw_save_input():
    data = request.json
    criteria_benefit = data.get('criteria_benefit', [])
    criteria_cost = data.get('criteria_cost', [])
    weight_benefit = data.get('weight_benefit', [])
    weight_cost = data.get('weight_cost', [])
    alternatives = data.get('alternatives', [])

    # Input Validation
    if not isinstance(criteria_benefit, list) or not all(isinstance(c, str) for c in criteria_benefit):
        return jsonify({"error": "Kriteria benefit harus berupa daftar string."}), 400
    if not isinstance(criteria_cost, list) or not all(isinstance(c, str) for c in criteria_cost):
        return jsonify({"error": "Kriteria cost harus berupa daftar string."}), 400
    if not isinstance(weight_benefit, list) or not all(isinstance(w, (int, float)) for w in weight_benefit):
        return jsonify({"error": "Bobot benefit harus berupa daftar angka."}), 400
    if not isinstance(weight_cost, list) or not all(isinstance(w, (int, float)) for w in weight_cost):
        return jsonify({"error": "Bobot cost harus berupa daftar angka."}), 400
    if not isinstance(alternatives, list) or not all(isinstance(a, str) for a in alternatives):
        return jsonify({"error": "Alternatif harus berupa daftar string."}), 400
    if len(alternatives) < 2:
        return jsonify({"error": "Minimal dua alternatif diperlukan."}), 400

    # Validate weights match criteria
    if (len(weight_benefit) != len(criteria_benefit)) or (len(weight_cost) != len(criteria_cost)):
        return jsonify({"error": "Jumlah bobot harus sesuai dengan jumlah kriteria."}), 400

    try:
        # Set criteria, weights, and alternatives in SAW object
        saw.set_criteria(criteria_benefit, criteria_cost)
        saw.set_weights(weight_benefit, weight_cost)
        saw.set_alternatives(alternatives)
        logger.info("Kriteria, bobot, dan alternatif SAW berhasil diatur.")
    except Exception as e:
        logger.error(f"Error setting SAW input: {e}")
        return jsonify({"error": "Gagal menyimpan data kriteria, bobot, dan alternatif SAW."}), 500

    return jsonify({"message": "Data SAW tersimpan."}), 200

@saw_bp.route('/get-input', methods=['GET'])
def get_input():
    if not saw.criteria_benefit or not saw.criteria_cost or not saw.alternatives:
        return jsonify({"error": "Data kriteria dan alternatif belum diset"}), 400
    return jsonify({
        "criteria_benefit": saw.criteria_benefit,
        "criteria_cost": saw.criteria_cost,
        "alternatives": saw.alternatives
    }), 200

@saw_bp.route('/get-criteria', methods=['GET'])
def get_criteria():
    if not saw.criteria_benefit or not saw.criteria_cost:
        return jsonify({"error": "Data kriteria belum di set"}), 400
    return jsonify({
        "criteria_benefit": saw.criteria_benefit,
        "criteria_cost": saw.criteria_cost
    }), 200

@saw_bp.route('/calculate', methods=['POST'])
def saw_calculate():
    data = request.json

    # Validate inputs
    if not saw.criteria_benefit and not saw.criteria_cost:
        return jsonify({"error": "Kriteria SAW belum diinput."}), 400
    if not saw.alternatives:
        return jsonify({"error": "Alternatif SAW belum diinput."}), 400
    if (saw.criteria_benefit and (len(saw.weight_benefit) != len(saw.criteria_benefit))) or \
       (saw.criteria_cost and (len(saw.weight_cost) != len(saw.criteria_cost))):
        return jsonify({"error": "Bobot SAW belum diinput atau tidak sesuai dengan jumlah kriteria."}), 400

    # Set benefit and cost matrices
    matrix_benefit = data.get('matrix_benefit', [])
    matrix_cost = data.get('matrix_cost', [])

    # Logging matriks
    logger.info(f"Received matrix_benefit: {matrix_benefit}")
    logger.info(f"Received matrix_cost: {matrix_cost}")

    # Validate matriks
    if saw.criteria_benefit:
        expected_shape_benefit = (len(saw.alternatives), len(saw.criteria_benefit))
        logger.info(f"Expected Benefit Matrix Shape: {expected_shape_benefit}")
        if len(matrix_benefit) != expected_shape_benefit[0]:
            return jsonify({"error": f"Matriks benefit harus memiliki {expected_shape_benefit[0]} baris."}), 400
        for row in matrix_benefit:
            if len(row) != expected_shape_benefit[1]:
                return jsonify({"error": "Setiap baris di matriks benefit harus memiliki panjang yang sesuai dengan jumlah kriteria benefit."}), 400

    if saw.criteria_cost:
        expected_shape_cost = (len(saw.alternatives), len(saw.criteria_cost))
        logger.info(f"Expected Cost Matrix Shape: {expected_shape_cost}")
        if len(matrix_cost) != expected_shape_cost[0]:
            return jsonify({"error": f"Matriks cost harus memiliki {expected_shape_cost[0]} baris."}), 400
        for row in matrix_cost:
            if len(row) != expected_shape_cost[1]:
                return jsonify({"error": "Setiap baris di matriks cost harus memiliki panjang yang sesuai dengan jumlah kriteria cost."}), 400

    try:
        # Set matrices in SAW object
        saw.set_matrices(matrix_benefit, matrix_cost)

        # Perform SAW calculation
        saw.perform_saw_calculation()
        results = saw.get_results()
        logger.info("Perhitungan SAW berhasil dilakukan.")
    except Exception as e:
        logger.error(f"Error during SAW calculation: {e}")
        return jsonify({"error": f"Perhitungan SAW gagal: {str(e)}"}), 500

    return jsonify({"message": "Perhitungan SAW berhasil.", "data": results}), 200

@saw_bp.route('/export-excel', methods=['GET'])
def saw_export_excel():
    try:
        # Ensure SAW calculation is done
        if not saw.ranked_alternatives or not saw.ranked_scores:
            return jsonify({"error": "Perhitungan SAW belum dilakukan."}), 400

        results = saw.get_results()

        # Create Excel file using pandas
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Benefit Matrix
            if results.get('matriks_benefit'):
                df_benefit = pd.DataFrame(results['matriks_benefit'], index=saw.alternatives, columns=saw.criteria_benefit)
                df_benefit.to_excel(writer, sheet_name='Matriks Benefit')

            # Cost Matrix
            if results.get('matriks_cost'):
                df_cost = pd.DataFrame(results['matriks_cost'], index=saw.alternatives, columns=saw.criteria_cost)
                df_cost.to_excel(writer, sheet_name='Matriks Cost')

            # Normalized Benefit Matrix
            if results.get('matriks_normal_benefit'):
                df_normal_benefit = pd.DataFrame(results['matriks_normal_benefit'], index=saw.alternatives, columns=saw.criteria_benefit)
                df_normal_benefit.to_excel(writer, sheet_name='Normalisasi Benefit')

            # Normalized Cost Matrix
            if results.get('matriks_normal_cost'):
                df_normal_cost = pd.DataFrame(results['matriks_normal_cost'], index=saw.alternatives, columns=saw.criteria_cost)
                df_normal_cost.to_excel(writer, sheet_name='Normalisasi Cost')

            # Scores and Ranking
            if results.get('ranked_alternatives') and results.get('ranked_scores'):
                df_scores = pd.DataFrame({
                    'Alternatif': results['ranked_alternatives'],
                    'Skor': results['ranked_scores']
                })
                df_scores.to_excel(writer, sheet_name='Ranking')

        output.seek(0)

        return send_file(
            output,
            download_name="Hasil_SAW.xlsx",
            as_attachment=True,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        logger.error(f"Error exporting SAW to Excel: {e}")
        return jsonify({"error": "Gagal mengekspor file Excel SAW."}), 500
