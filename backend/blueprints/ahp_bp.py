# backend/blueprints/ahp_bp.py

from flask import Blueprint, request, jsonify, send_file
import logging
import pandas as pd
import numpy as np
import io

from ahp.ahp import AHP

ahp_bp = Blueprint('ahp_bp', __name__)
logger = logging.getLogger(__name__)

# Inisialisasi objek AHP
ahp = AHP()

@ahp_bp.route('/save-input', methods=['POST'])
def save_input():
    data = request.json
    logger.debug(f"Data yang diterima untuk save_input: {data}")
    criteria = data.get('criteria', [])
    alternatives = data.get('alternatives', [])

    # Validate inputs
    if not isinstance(criteria, list) or not all(isinstance(c, str) for c in criteria):
        logger.error("Kriteria harus berupa daftar string.")
        return jsonify({"error": "Kriteria harus berupa daftar string."}), 400
    if not isinstance(alternatives, list) or not all(isinstance(a, str) for a in alternatives):
        logger.error("Alternatif harus berupa daftar string.")
        return jsonify({"error": "Alternatif harus berupa daftar string."}), 400
    if len(criteria) < 2 or len(alternatives) < 2:
        logger.error("Minimal dua kriteria dan dua alternatif diperlukan.")
        return jsonify({"error": "Minimal dua kriteria dan dua alternatif diperlukan."}), 400

    try:
        # Set criteria and alternatives in AHP object
        ahp.set_criteria(criteria)
        ahp.set_alternatives(alternatives)
        logger.info("Kriteria dan alternatif AHP berhasil diatur.")
    except Exception as e:
        logger.error(f"Error setting criteria and alternatives: {e}")
        return jsonify({"error": "Gagal menyimpan data kriteria dan alternatif."}), 500

    return jsonify({"message": "Data tersimpan."}), 200

@ahp_bp.route('/get-input', methods=['GET'])
def get_input():
    if not ahp.criteria or not ahp.alternatives:
        return jsonify({"error": "Data kriteria dan alternatif belum diset."}), 400
    return jsonify({
        "criteria": ahp.criteria,
        "alternatives": ahp.alternatives
    }), 200

@ahp_bp.route('/get-criteria', methods=['GET'])
def get_criteria():
    if not ahp.criteria:
        return jsonify({"error": "Belum ada kriteria yang diset."}), 400
    return jsonify({"criteria": ahp.criteria}), 200

@ahp_bp.route('/compare_criteria', methods=['POST'])
def compare_criteria():
    data = request.json
    comparisons = data.get('comparisons', [])
    if not comparisons:
        return jsonify({"error": "Tidak ada data perbandingan kriteria yang dikirim."}), 400

    # Validate comparisons
    if not isinstance(comparisons, list):
        return jsonify({"error": "Comparisons harus berupa daftar objek."}), 400
    for comp in comparisons:
        if not all(k in comp for k in ('i', 'j', 'value')):
            return jsonify({"error": "Setiap perbandingan harus memiliki 'i', 'j', dan 'value'."}), 400

    try:
        CR = ahp.set_criteria_comparisons(comparisons)
        logger.info(f"Perbandingan kriteria diatur dengan CR: {CR}")
    except Exception as e:
        logger.error(f"Error setting criteria comparisons: {e}")
        return jsonify({"error": "Gagal mengatur perbandingan kriteria."}), 500

    response = {"CR": CR}
    if CR > 0.1:
        response["warning"] = "Consistency Ratio melebihi 0.1, pertimbangkan revisi."

    return jsonify(response), 200

@ahp_bp.route('/compare_alternatives', methods=['POST'])
def compare_alternatives():
    data = request.json
    criteria_name = data.get('criteria_name')
    comparisons = data.get('comparisons', [])

    if not criteria_name:
        return jsonify({"error": "Nama kriteria diperlukan."}), 400
    if criteria_name not in ahp.criteria:
        return jsonify({"error": f"Criteria '{criteria_name}' tidak ditemukan."}), 400
    if not comparisons:
        return jsonify({"error": "Tidak ada data perbandingan alternatif yang dikirim."}), 400

    # Validate comparisons
    if not isinstance(comparisons, list):
        return jsonify({"error": "Comparisons harus berupa daftar objek."}), 400
    for comp in comparisons:
        if not all(k in comp for k in ('i', 'j', 'value')):
            return jsonify({"error": "Setiap perbandingan harus memiliki 'i', 'j', dan 'value'."}), 400

    try:
        CR = ahp.set_alternatives_comparisons(criteria_name, comparisons)
        logger.info(f"Perbandingan alternatif untuk '{criteria_name}' diatur dengan CR: {CR}")
    except Exception as e:
        logger.error(f"Error setting alternative comparisons for '{criteria_name}': {e}")
        return jsonify({"error": "Gagal mengatur perbandingan alternatif."}), 500

    response = {"CR": CR}
    if CR > 0.1:
        response["warning"] = f"Consistency Ratio untuk kriteria '{criteria_name}' melebihi 0.1, pertimbangkan revisi."

    return jsonify(response), 200

@ahp_bp.route('/compare_alternatives_bulk', methods=['POST'])
def compare_alternatives_bulk():
    data = request.get_json()
    comparisons = data.get('comparisons', [])

    # Validasi data
    if not comparisons:
        return jsonify({'error': 'Tidak ada data perbandingan yang dikirim.'}), 400

    if not isinstance(comparisons, list):
        return jsonify({'error': 'Comparisons harus berupa daftar objek.'}), 400

    warnings = []
    CRs = []

    for comp in comparisons:
        criteria_name = comp.get('criteria_name')
        crit_comparisons = comp.get('comparisons', [])

        if not criteria_name or not crit_comparisons:
            warnings.append(f'Kriteria atau perbandingan kosong dalam salah satu objek.')
            continue

        if criteria_name not in ahp.criteria:
            warnings.append(f'Kriteria "{criteria_name}" tidak ditemukan.')
            continue

        # Validate setiap perbandingan
        valid = True
        for c in crit_comparisons:
            if not all(k in c for k in ('i', 'j', 'value')):
                warnings.append(f'Perbandingan tidak lengkap untuk kriteria "{criteria_name}".')
                valid = False
                break
            try:
                # Coba konversi value ke float
                float(c['value'])
            except ValueError:
                warnings.append(f'Nilai perbandingan tidak valid untuk kriteria "{criteria_name}".')
                valid = False
                break

        if not valid:
            continue

        try:
            CR = ahp.set_alternatives_comparisons(criteria_name, crit_comparisons)
            CRs.append(CR)
            if CR > 0.1:
                warnings.append(f'Consistency Ratio untuk kriteria "{criteria_name}" melebihi 0.1.')
        except Exception as e:
            logger.error(f"Error setting alternative comparisons for '{criteria_name}': {e}")
            warnings.append(f'Gagal mengatur perbandingan alternatif untuk kriteria "{criteria_name}".')

    response = {
        'CRs': CRs,
        'warnings': warnings
    }

    return jsonify(response), 200

@ahp_bp.route('/calculate', methods=['GET'])
def calculate():
    try:
        if not ahp.criteria or not ahp.alternatives:
            logger.error("Kriteria atau alternatif belum diinput.")
            return jsonify({"error": "Kriteria atau alternatif belum diinput."}), 400
        if ahp.criteria_matrix is None:
            logger.error("Perbandingan kriteria belum diinput.")
            return jsonify({"error": "Perbandingan kriteria belum diinput."}), 400
        for crit in ahp.criteria:
            if crit not in ahp.alternative_comparisons or not ahp.alternative_comparisons[crit].any():
                logger.error(f'Perbandingan alternatif untuk kriteria "{crit}" belum diinput.')
                return jsonify({"error": f'Perbandingan alternatif untuk kriteria "{crit}" belum diinput.'}), 400

        # Identifikasi kriteria yang konsisten (CR <= 0.1)
        consistent_criteria = []
        inconsistent_criteria = []
        for crit in ahp.criteria:
            CR = ahp.criteria_CR if crit == ahp.criteria[0] else ahp.alternative_CR.get(crit, 1.0)
            if CR <= 0.1:
                consistent_criteria.append(crit)
            else:
                inconsistent_criteria.append(crit)

        logger.debug(f"Consistent criteria: {consistent_criteria}")
        logger.debug(f"Inconsistent criteria: {inconsistent_criteria}")

        if not consistent_criteria:
            logger.error("Tidak ada kriteria yang konsisten (CR <= 0.1).")
            return jsonify({"error": "Tidak ada kriteria yang konsisten (CR <= 0.1)."}), 400

        if inconsistent_criteria:
            warnings = [f'Kriteria "{crit}" diabaikan karena CR > 0.1.' for crit in inconsistent_criteria]
            logger.warning(f"Kriteria yang diabaikan: {inconsistent_criteria}")
        else:
            warnings = []

        # Normalisasi bobot kriteria yang konsisten
        weights = [ahp.criteria_weights[ahp.criteria.index(crit)] for crit in consistent_criteria]
        total_weight = sum(weights)
        if total_weight == 0:
            logger.error("Total bobot kriteria yang konsisten adalah nol.")
            return jsonify({"error": "Total bobot kriteria yang konsisten adalah nol."}), 400
        normalized_weights = [w / total_weight for w in weights]
        logger.debug(f"Normalized weights: {normalized_weights}")

        # Hitung skor akhir berdasarkan kriteria yang konsisten
        scores = np.zeros(len(ahp.alternatives))
        for crit, weight in zip(consistent_criteria, normalized_weights):
            scores += weight * ahp.alternative_weights[crit]

        final_ranking = scores
        logger.debug(f"Final ranking: {final_ranking}")

        # Update final_ranking in AHP object
        ahp.final_ranking = final_ranking
        ahp.warnings.extend(warnings)

        logger.info("AHP calculation completed successfully with some kriteria diabaikan.")
    except Exception as e:
        logger.error(f"Error during calculation: {e}")
        return jsonify({"error": f"Perhitungan gagal: {str(e)}"}), 500  # Menambahkan pesan kesalahan

    return jsonify({"message": "Calculation done", "final_ranking": final_ranking.tolist(), "warnings": warnings}), 200

@ahp_bp.route('/results', methods=['GET'])
def results():
    try:
        res = ahp.get_results()
        if not res:
            logger.error("Tidak ada hasil sama sekali. Pastikan sudah memasukkan data kriteria dan alternatif.")
            return jsonify({"error": "Tidak ada hasil sama sekali. Pastikan sudah memasukkan data kriteria dan alternatif."}), 400

        # Identifikasi kriteria yang konsisten
        consistent_criteria = []
        inconsistent_criteria = []
        for crit in ahp.criteria:
            CR = ahp.criteria_CR if crit == ahp.criteria[0] else ahp.alternative_CR.get(crit, 1.0)
            if CR <= 0.1:
                consistent_criteria.append(crit)
            else:
                inconsistent_criteria.append(crit)

        if inconsistent_criteria:
            for crit in inconsistent_criteria:
                if crit in res['criteria_matrix']:
                    del res['criteria_matrix'][crit]
                if crit in res['criteria_weights']:
                    del res['criteria_weights'][crit]
                if crit in res['alternative_matrices']:
                    del res['alternative_matrices'][crit]
                if crit in res['alternative_weights']:
                    del res['alternative_weights'][crit]

        # Update final_ranking and CR
        res['final_ranking'] = res.get('final_ranking', {})
        res['final_ranking']['Skor Akhir'] = {alt: round(score, 4) for alt, score in zip(ahp.alternatives, ahp.final_ranking)}
        res['CR'] = round(ahp.criteria_CR, 4)
        res['warnings'] = ahp.warnings

        logger.info("Results retrieved successfully, with inconsistent criteria dihapus.")
    except Exception as e:
        logger.error(f"Error retrieving results: {e}")
        return jsonify({"error": "Gagal mendapatkan hasil."}), 500

    return jsonify(res), 200

@ahp_bp.route('/export-excel', methods=['GET'])
def export_excel():
    try:
        res = ahp.get_results()
        if not res:
            return jsonify({"error": "Tidak ada hasil untuk diekspor."}), 400

        # Identifikasi kriteria yang konsisten
        consistent_criteria = []
        inconsistent_criteria = []
        for crit in ahp.criteria:
            CR = ahp.criteria_CR if crit == ahp.criteria[0] else ahp.alternative_CR.get(crit, 1.0)
            if CR <= 0.1:
                consistent_criteria.append(crit)
            else:
                inconsistent_criteria.append(crit)

        # Hapus kriteria yang tidak konsisten dari hasil
        if inconsistent_criteria:
            for crit in inconsistent_criteria:
                if crit in res['criteria_matrix']:
                    del res['criteria_matrix'][crit]
                if crit in res['criteria_weights']:
                    del res['criteria_weights'][crit]
                if crit in res['alternative_matrices']:
                    del res['alternative_matrices'][crit]
                if crit in res['alternative_weights']:
                    del res['alternative_weights'][crit]

        # Update final_ranking and CR
        res['final_ranking'] = res.get('final_ranking', {})
        res['final_ranking']['Skor Akhir'] = {alt: round(score, 4) for alt, score in zip(ahp.alternatives, ahp.final_ranking)}
        res['CR'] = round(ahp.criteria_CR, 4)
        res['warnings'] = ahp.warnings

        # Create Excel file using pandas
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Criteria Matrix
            if res.get('criteria_matrix'):
                df_criteria = pd.DataFrame(res['criteria_matrix'])
                df_criteria.to_excel(writer, sheet_name='Matriks Kriteria')

            # Alternative Matrices
            for crit, matrix in res.get('alternative_matrices', {}).items():
                df_alt_matrix = pd.DataFrame(matrix)
                sheet_name = f'Matriks Alternatif {crit}'
                sheet_name = sheet_name[:31]  # Excel sheet name limit
                df_alt_matrix.to_excel(writer, sheet_name=sheet_name)

            # Alternative Weights (Jika Ada)
            for crit, weights in res.get('alternative_weights', {}).items():
                df_alt_weights = pd.DataFrame(weights)
                sheet_name = f'Bobot Alternatif {crit}'
                sheet_name = sheet_name[:31]
                df_alt_weights.to_excel(writer, sheet_name=sheet_name)

            # Final Ranking
            if res.get('final_ranking'):
                df_final = pd.DataFrame(res['final_ranking']['Skor Akhir'], index=[0])
                df_final = df_final.T.rename(columns={0: 'Skor Akhir'})
                df_final.to_excel(writer, sheet_name='Ranking Akhir')

        output.seek(0)

        return send_file(
            output,
            download_name="Hasil_AHP.xlsx",
            as_attachment=True,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        logger.error(f"Error exporting Excel: {e}")
        return jsonify({"error": "Gagal mengekspor file Excel."}), 500
