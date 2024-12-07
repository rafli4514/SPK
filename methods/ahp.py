# methods/ahp.py

import numpy as np
import pandas as pd
from .base_method import BaseMethod

class AHP(BaseMethod):
    def __init__(self, criteria, alternatives):
        super().__init__(criteria, alternatives)
        self.criteria_matrix = None
        self.criteria_weights = None
        self.alternative_matrices = {}
        self.alternative_weights = {}
        self.final_ranking = None
        self.steps = []  # Menyimpan langkah-langkah pengerjaan

    def set_criteria_comparisons(self, comparisons):
        n = len(self.criteria)
        self.criteria_matrix = np.ones((n, n))
        for (i, j, value) in comparisons:
            self.criteria_matrix[i, j] = value
            self.criteria_matrix[j, i] = 1 / value
        self.steps.append("Perbandingan kriteria dimasukkan.")

    def set_alternative_comparisons(self, criteria, comparisons):
        n = len(self.alternatives)
        if criteria not in self.alternative_matrices:
            self.alternative_matrices[criteria] = np.ones((n, n))
        matrix = self.alternative_matrices[criteria]
        for (i, j, value) in comparisons:
            matrix[i, j] = value
            matrix[j, i] = 1 / value
        self.steps.append(f"Perbandingan alternatif untuk kriteria '{criteria}' dimasukkan.")

    def calculate_weights_from_matrix(self, matrix):
        eigvals, eigvecs = np.linalg.eig(matrix)
        max_index = np.argmax(eigvals.real)
        principal_eigvec = eigvecs[:, max_index].real
        normalized_weights = principal_eigvec / principal_eigvec.sum()
        return normalized_weights

    def calculate_consistency_ratio(self, matrix, weights):
        n = matrix.shape[0]
        lambda_max = np.dot(matrix, weights).sum() / weights.sum()
        CI = (lambda_max - n) / (n - 1)
        RI_dict = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12,
                   6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        RI = RI_dict.get(n, 1.49)  # Default ke 1.49 untuk n > 10
        if RI == 0:
            return 0.0  # Menghindari pembagian dengan nol
        CR = CI / RI
        return CR

    def perform_ahp(self):
        # Hitung bobot kriteria
        self.criteria_weights = self.calculate_weights_from_matrix(self.criteria_matrix)
        CR = self.calculate_consistency_ratio(self.criteria_matrix, self.criteria_weights)
        self.steps.append(f"Consistency Ratio untuk kriteria: {CR:.4f}")
        if CR > 0.1:
            self.steps.append("Warning: Consistency Ratio melebihi 0.1. Pertimbangkan untuk merevisi perbandingan Anda.")
        else:
            self.steps.append("Consistency Ratio dapat diterima.")

        # Hitung bobot alternatif untuk setiap kriteria
        for crit in self.criteria:
            weights = self.calculate_weights_from_matrix(self.alternative_matrices[crit])
            self.alternative_weights[crit] = weights
            CR_alt = self.calculate_consistency_ratio(self.alternative_matrices[crit], weights)
            self.steps.append(f"Consistency Ratio untuk alternatif di bawah '{crit}': {CR_alt:.4f}")
            if CR_alt > 0.1:
                self.steps.append(f"Warning: Consistency Ratio untuk '{crit}' melebihi 0.1. Pertimbangkan untuk merevisi perbandingan Anda.")
            else:
                self.steps.append(f"Consistency Ratio untuk '{crit}' dapat diterima.")

        # Hitung ranking akhir
        self.final_ranking = np.zeros(len(self.alternatives))
        for i, crit in enumerate(self.criteria):
            self.final_ranking += self.criteria_weights[i] * self.alternative_weights[crit]
        self.steps.append("Ranking akhir dihitung.")

    def get_results(self):
        # Konversi bobot kriteria dan bobot alternatif ke list
        criteria_weights = self.criteria_weights.tolist() if isinstance(self.criteria_weights, np.ndarray) else self.criteria_weights
        alternative_weights = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in self.alternative_weights.items()}
        
        # Konversi final_ranking ke dictionary dengan nama alternatif
        final_ranking_dict = {self.alternatives[i]: score for i, score in enumerate(self.final_ranking)}
        
        results = {
            'criteria_matrix': self.criteria_matrix,
            'criteria_weights': criteria_weights,
            'alternative_matrices': self.alternative_matrices,
            'alternative_weights': alternative_weights,
            'final_ranking': final_ranking_dict,
            'steps': self.steps
        }
        return results
