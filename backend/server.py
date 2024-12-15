# app/main.py
import os
import sys
from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from datetime import datetime
import logging

# Menambahkan path backend agar modul AHP dapat diimpor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.ahp.ahp import AHP

app = Flask(__name__)

# Konfigurasi CORS
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
CORS(app, resources={r"/api/*": {"origins": cors_origins}})

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Setup Caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Setup Flask-RESTX (Swagger)
api = Api(app, version='1.0', title='AHP API',
          description='API untuk melakukan perhitungan Analytic Hierarchy Process')

ns = api.namespace('api', description='Operasi AHP')

# Definisikan Model untuk Validasi dan Dokumentasi Swagger
ahp_model = api.model('AHPModel', {
    'criteria': fields.List(fields.String, required=True, description='Daftar kriteria'),
    'alternatives': fields.List(fields.String, required=True, description='Daftar alternatif'),
    'criteria_comparisons': fields.List(fields.List(fields.Float, min_length=3, max_length=3),
                                        required=True,
                                        description='Perbandingan kriteria dalam format [i, j, value]'),
    'alternative_comparisons': fields.Raw(required=True, description='Perbandingan alternatif per kriteria dalam format dict')
})

def success_response(data, message="Success"):
    """
    Mengembalikan response sukses dalam bentuk dictionary.
    Flask-RESTX akan otomatis mengonversi dict ini menjadi JSON.
    """
    return {
        "status": "success",
        "timestamp": datetime.utcnow().isoformat(),
        "message": message,
        "data": data
    }, 200

def error_response(message, status_code=400):
    """
    Mengembalikan response error dalam bentuk dictionary.
    Flask-RESTX akan otomatis mengonversi dict ini menjadi JSON.
    """
    return {
        "status": "error",
        "timestamp": datetime.utcnow().isoformat(),
        "message": message
    }, status_code

@ns.route('/ahp')
class AHPResource(Resource):
    @ns.expect(ahp_model)
    @limiter.limit("10 per minute")  # Rate limit per endpoint
    def post(self):
        """
        Melakukan perhitungan AHP berdasarkan data yang diberikan.
        """
        try:
            data = request.get_json(force=True)

            # Ambil data dari request JSON
            criteria = data.get('criteria')
            alternatives = data.get('alternatives')
            criteria_comparisons = data.get('criteria_comparisons')
            alternative_comparisons = data.get('alternative_comparisons')

            # Validasi input dasar
            if not isinstance(criteria, list) or not all(isinstance(c, str) for c in criteria):
                raise ValueError("Kriteria harus disediakan dalam bentuk list of strings.")
            if not isinstance(alternatives, list) or not all(isinstance(a, str) for a in alternatives):
                raise ValueError("Alternatif harus disediakan dalam bentuk list of strings.")
            if len(criteria) < 2 or len(alternatives) < 2:
                raise ValueError("Minimal diperlukan dua kriteria dan dua alternatif.")

            if not isinstance(criteria_comparisons, list):
                raise ValueError("Perbandingan kriteria (criteria_comparisons) harus berupa list.")
            for comp in criteria_comparisons:
                if not isinstance(comp, (list, tuple)) or len(comp) != 3:
                    raise ValueError("Setiap elemen di criteria_comparisons harus berupa [i, j, value].")

            if not isinstance(alternative_comparisons, dict):
                raise ValueError("Perbandingan alternatif (alternative_comparisons) harus berupa dict.")
            for crit, comps in alternative_comparisons.items():
                if crit not in criteria:
                    raise ValueError(f"Kriteria '{crit}' dalam alternative_comparisons tidak ada di daftar criteria.")
                if not isinstance(comps, list):
                    raise ValueError("Setiap nilai dalam alternative_comparisons harus berupa list.")
                for c in comps:
                    if not isinstance(c, (list, tuple)) or len(c) != 3:
                        raise ValueError("Setiap elemen di alternative_comparisons[kriteria] harus berupa [i, j, value].")

            # Inisialisasi AHP
            ahp = AHP(criteria, alternatives)

            # Atur perbandingan kriteria
            ahp.set_criteria_comparisons(criteria_comparisons)

            # Atur perbandingan alternatif
            for crit, comps in alternative_comparisons.items():
                ahp.set_alternative_comparisons(crit, comps)

            # Jalankan perhitungan AHP
            ahp.perform_ahp()
            results = ahp.get_results()

            return success_response(results, "Perhitungan AHP berhasil dilakukan.")

        except ValueError as e:
            logger.warning(f"Input error: {e}")
            return error_response(str(e), 400)
        except Exception as e:
            logger.error(f"Error during AHP calculation: {str(e)}", exc_info=True)
            return error_response("Internal Server Error.", 500)

@ns.route('/')
class HomeResource(Resource):
    def get(self):
        """
        Endpoint utama untuk memverifikasi bahwa server berjalan.
        """
        return success_response({"message": "Server Flask berjalan untuk AHP."}, "Server aktif.")

if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
