# backend/ahp/ahp.py

import numpy as np

class AHP:
    def __init__(self):
        self.criteria = []
        self.alternatives = []
        self.criteria_matrix = None
        self.criteria_weights = None
        self.criteria_CR = None
        self.alternative_comparisons = {}
        self.alternative_weights = {}
        self.alternative_CR = {}
        self.final_ranking = None
        self.warnings = []

    def set_criteria(self, criteria):
        self.criteria = criteria
        n = len(criteria)
        self.criteria_matrix = np.ones((n, n))

    def set_alternatives(self, alternatives):
        self.alternatives = alternatives
        for crit in self.criteria:
            self.alternative_comparisons[crit] = np.ones((len(alternatives), len(alternatives)))

    def set_criteria_comparisons(self, comparisons):
        if self.criteria_matrix is None:
            raise ValueError("Matriks kriteria belum diinisialisasi.")
        for comp in comparisons:
            i, j, value = int(comp['i']), int(comp['j']), float(comp['value'])
            if i >= len(self.criteria) or j >= len(self.criteria):
                raise IndexError("Indeks kriteria di luar jangkauan.")
            self.criteria_matrix[i][j] = value
            self.criteria_matrix[j][i] = 1 / value
        weights, CR = self.calculate_weights_from_matrix(self.criteria_matrix)
        self.criteria_weights = weights
        self.criteria_CR = CR
        return CR

    def set_alternatives_comparisons(self, criteria_name, comparisons):
        if criteria_name not in self.criteria:
            raise ValueError(f"Criteria '{criteria_name}' tidak ada dalam kriteria yang telah diatur.")
        matrix = self.alternative_comparisons.get(criteria_name)
        if matrix is None:
            raise ValueError(f"Matriks alternatif untuk kriteria '{criteria_name}' belum diinisialisasi.")
        for comp in comparisons:
            i, j, value = int(comp['i']), int(comp['j']), float(comp['value'])
            if i >= len(self.alternatives) or j >= len(self.alternatives):
                raise IndexError("Indeks alternatif di luar jangkauan.")
            matrix[i][j] = value
            matrix[j][i] = 1 / value
        weights, CR = self.calculate_weights_from_matrix(matrix)
        self.alternative_weights[criteria_name] = weights
        self.alternative_CR[criteria_name] = CR
        return CR

    def calculate_weights_from_matrix(self, matrix):
        # Normalisasi kolom
        column_sums = np.sum(matrix, axis=0)
        if np.any(column_sums == 0):
            raise ValueError("Jumlah kolom pada matriks tidak boleh nol.")
        normalized_matrix = matrix / column_sums

        # Hitung bobot sebagai rata-rata baris matriks yang dinormalisasi
        weights = np.mean(normalized_matrix, axis=1)

        # Hitung lambda_max
        weighted_sum = matrix @ weights
        lambda_max = np.mean(weighted_sum / weights)

        # Hitung Consistency Index (CI)
        n = len(weights)
        CI = (lambda_max - n) / (n - 1)

        # Hitung Random Index (RI)
        RI_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
                   6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        RI = RI_dict.get(n, 1.49)  # Default RI untuk n > 10

        # Hitung Consistency Ratio (CR)
        CR = CI / RI if RI != 0 else 0

        return weights, CR

    def calculate_weights(self):
        if self.criteria_weights is None:
            raise ValueError("Perbandingan kriteria belum diinput.")
        for crit in self.criteria:
            if crit not in self.alternative_weights:
                raise ValueError(f"Perbandingan alternatif untuk kriteria '{crit}' belum diinput.")
        # Hitung skor akhir
        scores = np.zeros(len(self.alternatives))
        for crit, weight in zip(self.criteria, self.criteria_weights):
            scores += weight * self.alternative_weights[crit]
        self.final_ranking = scores
        return self.final_ranking

    def get_results(self):
        if self.final_ranking is None:
            return None
        results = {
            'criteria_matrix': {crit: {c: self.criteria_matrix[i][j] for j, c in enumerate(self.criteria)} for i, crit in enumerate(self.criteria)},
            'criteria_weights': {crit: {'Bobot': round(weight, 4)} for crit, weight in zip(self.criteria, self.criteria_weights)},
            'alternative_matrices': {},
            'alternative_weights': {},
            'final_ranking': {
                'Skor Akhir': {alt: round(score, 4) for alt, score in zip(self.alternatives, self.final_ranking)}
            },
            'CR': round(self.criteria_CR, 4),
            'warnings': self.warnings
        }
        for crit in self.criteria:
            matrix = self.alternative_comparisons[crit]
            results['alternative_matrices'][crit] = {alt: {a: matrix[i][j] for j, a in enumerate(self.alternatives)} for i, alt in enumerate(self.alternatives)}
            results['alternative_weights'][crit] = {alt: {'Bobot': round(weight, 4)} for alt, weight in zip(self.alternatives, self.alternative_weights[crit])}
        return results
