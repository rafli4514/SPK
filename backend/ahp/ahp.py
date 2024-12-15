# backend/ahp/ahp.py
import numpy as np


class AHP:
    def __init__(self, criteria, alternatives):
        """
        Inisialisasi objek AHP dengan kriteria dan alternatif yang diberikan.
        
        Parameters:
            criteria (list): Daftar nama kriteria
            alternatives (list): Daftar nama alternatif
        """
        self.criteria = criteria
        self.alternatives = alternatives
        self.criteria_matrix = np.ones((len(criteria), len(criteria)))
        self.criteria_weights = None
        self.alternative_matrices = {crit: np.ones((len(alternatives), len(alternatives))) for crit in criteria}
        self.alternative_weights = {}
        self.final_ranking = None

    def set_criteria_comparisons(self, comparisons):
        """
        Mengatur matriks perbandingan kriteria berdasarkan input perbandingan.

        Parameters:
            comparisons (list of tuples): Setiap tuple berisi perbandingan antar kriteria dalam format (i, j, value).
                i dan j adalah indeks kriteria, dan value adalah nilai perbandingan kriteria[i] terhadap kriteria[j].
        """
        for (i, j, value) in comparisons:
            if not (0 <= i < len(self.criteria)) or not (0 <= j < len(self.criteria)):
                raise ValueError(f"Indeks {i}, {j} di criteria_comparisons berada di luar rentang yang valid.")
            if not isinstance(value, (int, float)) or value <= 0:
                raise ValueError(f"Nilai perbandingan harus berupa angka positif, got {value}.")
            self.criteria_matrix[i, j] = value
            self.criteria_matrix[j, i] = 1 / value

    def set_alternative_comparisons(self, criteria, comparisons):
        """
        Mengatur matriks perbandingan alternatif berdasarkan kriteria tertentu.

        Parameters:
            criteria (str): Nama kriteria yang sedang diproses.
            comparisons (list of tuples): Setiap tuple berisi perbandingan antar alternatif untuk kriteria tertentu
                dalam format (i, j, value), di mana value adalah nilai perbandingan alternatif[i] terhadap alternatif[j].
        """
        if criteria not in self.criteria:
            raise ValueError(f"Kriteria '{criteria}' tidak ditemukan dalam daftar kriteria.")
        
        matrix = self.alternative_matrices[criteria]
        for (i, j, value) in comparisons:
            if not (0 <= i < len(self.alternatives)) or not (0 <= j < len(self.alternatives)):
                raise ValueError(f"Indeks {i}, {j} di alternative_comparisons untuk kriteria '{criteria}' berada di luar rentang yang valid.")
            if not isinstance(value, (int, float)) or value <= 0:
                raise ValueError(f"Nilai perbandingan harus berupa angka positif, got {value}.")
            matrix[i, j] = value
            matrix[j, i] = 1 / value

    def calculate_weights_from_matrix(self, matrix):
        """
        Menghitung bobot (prioritas) menggunakan eigenvector utama dari matriks perbandingan berpasangan.

        Parameters:
            matrix (np.ndarray): Matriks perbandingan berpasangan (n x n).
        
        Returns:
            np.ndarray: Vektor bobot yang telah dinormalisasi.
        """
        eigvals, eigvecs = np.linalg.eig(matrix)
        max_index = np.argmax(eigvals.real)  # Menemukan indeks nilai eigen terbesar
        principal_eigvec = eigvecs[:, max_index].real  # Mengambil vektor eigen utama
        normalized_weights = principal_eigvec / principal_eigvec.sum()  # Normalisasi bobot
        return normalized_weights

    def calculate_consistency_ratio(self, matrix, weights):
        """
        Menghitung **Consistency Ratio (CR)** untuk memeriksa konsistensi matriks perbandingan.

        Parameters:
            matrix (np.ndarray): Matriks perbandingan berpasangan (n x n).
            weights (np.ndarray): Vektor bobot dari matriks perbandingan.
        
        Returns:
            float: Consistency Ratio (CR).
        """
        n = matrix.shape[0]
        lambda_max = np.dot(matrix, weights).sum() / weights.sum()  # Menghitung lambda_max
        CI = (lambda_max - n) / (n - 1)  # Menghitung Consistency Index (CI)
        # Random Index (RI) berdasarkan ukuran matriks
        RI_dict = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        RI = RI_dict.get(n, 1.49)  # Default ke 1.49 untuk n > 10
        return CI / RI if RI != 0 else 0  # Menghitung CR

    def perform_ahp(self):
        """
        Melakukan perhitungan AHP, termasuk menghitung bobot kriteria dan alternatif,
        serta menghasilkan ranking akhir alternatif.

        Perhitungan dilakukan dengan metode Eigenvector.
        """

        # Hitung bobot kriteria (tanpa pengecekan CR)
        self.criteria_weights = self.calculate_weights_from_matrix(self.criteria_matrix)

        # Hitung bobot alternatif untuk setiap kriteria (tanpa pengecekan CR)
        for crit, matrix in self.alternative_matrices.items():
            weights = self.calculate_weights_from_matrix(matrix)
            self.alternative_weights[crit] = weights

        # Hitung ranking akhir dengan bobot kriteria dan alternatif
        self.final_ranking = np.zeros(len(self.alternatives))
        for i, crit in enumerate(self.criteria):
            self.final_ranking += self.criteria_weights[i] * self.alternative_weights[crit]


    def get_results(self):
        """
        Mengembalikan hasil perhitungan AHP, termasuk bobot kriteria, bobot alternatif, dan ranking akhir alternatif.

        Returns:
            dict: Hasil perhitungan AHP dalam format dictionary.
        """
        return {
            "criteria_weights": self.criteria_weights.tolist(),
            "alternative_weights": {k: v.tolist() for k, v in self.alternative_weights.items()},
            "final_ranking": {self.alternatives[i]: score for i, score in enumerate(self.final_ranking)}
        }
