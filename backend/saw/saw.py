# saw/saw.py

import numpy as np
import logging

logger = logging.getLogger(__name__)

class SAW:
    def __init__(self):
        self.criteria_benefit = []
        self.criteria_cost = []
        self.alternatives = []
        self.weight_benefit = []
        self.weight_cost = []
        self.matrix_benefit = []
        self.matrix_cost = []
        self.normal_benefit = []
        self.normal_cost = []
        self.scores = []
        self.ranked_alternatives = []
        self.ranked_scores = []

    def set_criteria(self, criteria_benefit, criteria_cost):
        self.criteria_benefit = criteria_benefit
        self.criteria_cost = criteria_cost
        logger.info(f"Set criteria_benefit: {criteria_benefit}")
        logger.info(f"Set criteria_cost: {criteria_cost}")

    def set_weights(self, weight_benefit, weight_cost):
        self.weight_benefit = weight_benefit
        self.weight_cost = weight_cost
        logger.info(f"Set weight_benefit: {weight_benefit}")
        logger.info(f"Set weight_cost: {weight_cost}")

    def set_alternatives(self, alternatives):
        self.alternatives = alternatives
        logger.info(f"Set alternatives: {alternatives}")

    def set_matrices(self, matrix_benefit, matrix_cost):
        self.matrix_benefit = matrix_benefit
        self.matrix_cost = matrix_cost
        logger.info(f"Set matrix_benefit: {matrix_benefit}")
        logger.info(f"Set matrix_cost: {matrix_cost}")

    def perform_saw_calculation(self):
        try:
            num_alternatives = len(self.alternatives)
            num_benefit_criteria = len(self.criteria_benefit)
            num_cost_criteria = len(self.criteria_cost)

            logger.info(f"Number of Alternatives: {num_alternatives}")
            logger.info(f"Number of Benefit Criteria: {num_benefit_criteria}")
            logger.info(f"Number of Cost Criteria: {num_cost_criteria}")

            # Validasi ukuran matriks
            if len(self.matrix_benefit) != num_alternatives:
                raise ValueError(f"Matriks benefit harus memiliki {num_alternatives} baris.")
            if len(self.matrix_cost) != num_alternatives:
                raise ValueError(f"Matriks cost harus memiliki {num_alternatives} baris.")

            for row in self.matrix_benefit:
                if len(row) != num_benefit_criteria:
                    raise ValueError("Setiap baris di matriks benefit harus memiliki panjang yang sesuai dengan jumlah kriteria benefit.")

            for row in self.matrix_cost:
                if len(row) != num_cost_criteria:
                    raise ValueError("Setiap baris di matriks cost harus memiliki panjang yang sesuai dengan jumlah kriteria cost.")

            # Normalisasi matriks benefit
            self.normal_benefit = self.normalize_matrix(self.matrix_benefit, benefit=True)
            # Normalisasi matriks cost
            self.normal_cost = self.normalize_matrix(self.matrix_cost, benefit=False)

            self.scores = []
            for i in range(num_alternatives):
                score = 0
                for j in range(num_benefit_criteria):
                    score += self.normal_benefit[i][j] * self.weight_benefit[j]
                for j in range(num_cost_criteria):
                    score += self.normal_cost[i][j] * self.weight_cost[j]
                self.scores.append(score)
                logger.info(f"Alternative {self.alternatives[i]} scored {score}")

            # Ranking
            combined = list(zip(self.alternatives, self.scores))
            combined.sort(key=lambda x: x[1], reverse=True)
            if combined:
                self.ranked_alternatives, self.ranked_scores = zip(*combined)
            else:
                self.ranked_alternatives, self.ranked_scores = [], []

            logger.info("SAW calculation completed successfully.")
        except Exception as e:
            logger.error(f"Error in perform_saw_calculation: {e}")
            raise

    def normalize_matrix(self, matrix, benefit=True):
        matrix_np = np.array(matrix, dtype=float)
        if benefit:
            max_values = matrix_np.max(axis=0)
            if np.any(max_values == 0):
                raise ValueError("Nilai maksimum pada kriteria benefit tidak boleh nol.")
            normalized = matrix_np / max_values
        else:
            min_values = matrix_np.min(axis=0)
            if np.any(min_values == 0):
                raise ValueError("Nilai minimum pada kriteria cost tidak boleh nol.")
            normalized = min_values / matrix_np
        logger.info(f"Normalized {'benefit' if benefit else 'cost'} matrix: {normalized}")
        return normalized.tolist()

    def get_results(self):
        """
        Mengembalikan hasil SAW dalam format dictionary.
        """
        if not self.ranked_alternatives or not self.ranked_scores:
            self.perform_saw_calculation()

        results = {
            "matriks_benefit": self.matrix_benefit if self.matrix_benefit is not None else None,
            "matriks_cost": self.matrix_cost if self.matrix_cost is not None else None,
            "matriks_normal_benefit": self.normal_benefit if self.normal_benefit is not None else None,
            "matriks_normal_cost": self.normal_cost if self.normal_cost is not None else None,
            "skor": self.scores if self.scores is not None else None,
            "ranked_alternatives": self.ranked_alternatives,
            "ranked_scores": list(self.ranked_scores) if self.ranked_scores is not None else None
        }

        return results
