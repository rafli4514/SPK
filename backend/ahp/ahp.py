from backend.base_method import BaseMethod
import numpy as np

class AHP(BaseMethod):
    def __init__(self, criteria, alternatives):
        super().__init__(criteria, alternatives)
        self.criteria_matrix = None
        self.criteria_weights = None
        self.alternative_matrices = {}
        self.alternative_weights = {}
        self.final_ranking = None

    def set_criteria_comparisons(self, comparisons):
        n = len(self.criteria)
        self.criteria_matrix = np.ones((n, n))
        for (i, j, value) in comparisons:
            self.criteria_matrix[i, j] = value
            self.criteria_matrix[j, i] = 1 / value

    def set_alternative_comparisons(self, criteria, comparisons):
        n = len(self.alternatives)
        if criteria not in self.alternative_matrices:
            self.alternative_matrices[criteria] = np.ones((n, n))
        matrix = self.alternative_matrices[criteria]
        for (i, j, value) in comparisons:
            matrix[i, j] = value
            matrix[j, i] = 1 / value

    def perform_ahp(self):
        self.criteria_weights = self.calculate_weights_from_matrix(self.criteria_matrix)
        for crit in self.criteria:
            self.alternative_weights[crit] = self.calculate_weights_from_matrix(self.alternative_matrices[crit])
        self.final_ranking = self.calculate_final_ranking()

    def calculate_weights_from_matrix(self, matrix):
        eigvals, eigvecs = np.linalg.eig(matrix)
        max_index = np.argmax(eigvals.real)
        principal_eigvec = eigvecs[:, max_index].real
        normalized_weights = principal_eigvec / principal_eigvec.sum()
        return normalized_weights

    def calculate_final_ranking(self):
        final_ranking = np.zeros(len(self.alternatives))
        for i, crit in enumerate(self.criteria):
            final_ranking += self.criteria_weights[i] * self.alternative_weights[crit]
        return final_ranking.tolist()

    def get_results(self):
        return {
            "criteria_matrix": self.criteria_matrix.tolist(),
            "criteria_weights": self.criteria_weights.tolist(),
            "alternative_weights": {k: v.tolist() for k, v in self.alternative_weights.items()},
            "final_ranking": {self.alternatives[i]: score for i, score in enumerate(self.final_ranking)}
        }
