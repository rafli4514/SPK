# methods/saw.py

import numpy as np

class SAW:
    def __init__(self):
        """
        Inisialisasi objek SAW tanpa kriteria dan alternatif awal.
        """
        self.criteria_benefit = []
        self.criteria_cost = []
        self.weight_benefit = []
        self.weight_cost = []
        self.alternatives = []
        self.alternative_scores = {}  # Dictionary untuk menyimpan nilai alternatif per kriteria
        self.matrix_benefit = None
        self.matrix_cost = None
        self.normal_benefit = None  # Matriks benefit yang dinormalisasi
        self.normal_cost = None     # Matriks cost yang dinormalisasi
        self.scores = None          # Skor untuk setiap alternatif
        self.ranked_alternatives = None  # Alternatif yang telah diurutkan
        self.ranked_scores = None        # Skor yang telah diurutkan
        self.steps = []                # Langkah-langkah pengerjaan SAW

    def set_criteria(self, criteria_benefit, criteria_cost):
        """
        Mengatur kriteria benefit dan cost.

        Args:
            criteria_benefit (list): Daftar kriteria benefit.
            criteria_cost (list): Daftar kriteria cost.
        """
        self.criteria_benefit = criteria_benefit
        self.criteria_cost = criteria_cost
        self.steps.append("Kriteria Benefit dan Cost telah diatur.")

    def set_alternatives(self, alternatives):
        """
        Mengatur alternatif yang akan dievaluasi.

        Args:
            alternatives (list): Daftar alternatif.
        """
        self.alternatives = alternatives
        self.steps.append("Alternatif telah diatur.")

    def set_weights(self, weight_benefit, weight_cost):
        """
        Mengatur bobot untuk kriteria benefit dan cost.

        Args:
            weight_benefit (list): Daftar bobot untuk kriteria benefit.
            weight_cost (list): Daftar bobot untuk kriteria cost.
        """
        self.weight_benefit = weight_benefit
        self.weight_cost = weight_cost
        self.steps.append("Bobot kriteria Benefit dan Cost telah diatur.")

    def set_alternative_scores(self, criteria, scores):
        """
        Mengatur nilai alternatif untuk setiap kriteria.

        Args:
            criteria (str): Nama kriteria.
            scores (dict): Dictionary dengan key sebagai alternatif dan value sebagai nilai.
        """
        self.alternative_scores[criteria] = scores
        self.steps.append(f"Nilai alternatif untuk kriteria '{criteria}' telah diatur.")

    def perform_saw(self):
        """
        Melakukan seluruh proses SAW: membuat matriks, normalisasi, perhitungan skor, dan ranking.
        """
        self.steps.append("Proses SAW dimulai.")
        self.create_matrices()
        self.normalization()
        self.calculate_score()
        self.rank_alternative()
        self.steps.append("Proses SAW selesai.")

    def create_matrices(self):
        """
        Membuat matriks benefit dan cost berdasarkan nilai alternatif yang telah diatur.
        """
        self.steps.append("Membuat matriks Benefit dan Cost.")
        length_alternative = len(self.alternatives)

        if self.criteria_benefit:
            self.matrix_benefit = np.zeros((length_alternative, len(self.criteria_benefit)))
            for i, alternative in enumerate(self.alternatives):
                for j, criteria in enumerate(self.criteria_benefit):
                    self.matrix_benefit[i][j] = self.alternative_scores.get(criteria, {}).get(alternative, 0)

        if self.criteria_cost:
            self.matrix_cost = np.zeros((length_alternative, len(self.criteria_cost)))
            for i, alternative in enumerate(self.alternatives):
                for j, criteria in enumerate(self.criteria_cost):
                    self.matrix_cost[i][j] = self.alternative_scores.get(criteria, {}).get(alternative, 0)

    def normalization(self):
        """
        Normalisasi matriks kriteria benefit dan cost.
        """
        self.steps.append("Melakukan normalisasi matriks Benefit dan Cost.")
        self.normal_benefit = None
        self.normal_cost = None

        if self.matrix_benefit is not None:
            # Normalisasi Benefit (max normalization)
            max_benefit = self.matrix_benefit.max(axis=0)
            max_benefit[max_benefit == 0] = 1  # Hindari pembagian dengan nol
            self.normal_benefit = self.matrix_benefit / max_benefit
            self.steps.append("Matriks Benefit telah dinormalisasi.")

        if self.matrix_cost is not None:
            # Normalisasi Cost (min normalization)
            min_cost = self.matrix_cost.min(axis=0)
            min_cost[min_cost == 0] = 1  # Hindari pembagian dengan nol
            self.normal_cost = min_cost / self.matrix_cost
            self.normal_cost[~np.isfinite(self.normal_cost)] = 1  # Gantikan inf atau NaN dengan 1
            self.steps.append("Matriks Cost telah dinormalisasi.")

    def calculate_score(self):
        """
        Menghitung skor total untuk setiap alternatif dengan bobot.
        """
        self.steps.append("Menghitung skor total untuk setiap alternatif.")
        if self.normal_benefit is None and self.normal_cost is None:
            raise ValueError("Matriks normalisasi belum dibuat.")

        benefit_scores = self.normal_benefit @ self.weight_benefit if self.normal_benefit is not None else 0
        cost_scores = self.normal_cost @ self.weight_cost if self.normal_cost is not None else 0
        self.scores = benefit_scores + cost_scores
        self.steps.append("Skor total telah dihitung.")

    def rank_alternative(self):
        """
        Mengurutkan alternatif berdasarkan skor tertinggi.
        """
        self.steps.append("Mengurutkan alternatif berdasarkan skor.")
        if self.scores is None:
            raise ValueError("Skor belum dihitung.")

        ranked_indices = np.argsort(self.scores)[::-1]  # Urutkan skor dari yang tertinggi
        self.ranked_alternatives = [self.alternatives[i] for i in ranked_indices]
        self.ranked_scores = self.scores[ranked_indices]
        self.steps.append("Alternatif telah diurutkan.")

    def get_results(self):
        """
        Mengembalikan hasil perhitungan SAW dalam format dictionary.

        Returns:
            dict: Dictionary berisi hasil perhitungan SAW.
        """
        results = {
            'steps': self.steps,
            'criteria_matrix': self.combine_matrices(),
            'criteria_weights': self.weight_benefit + self.weight_cost,
            'normalization_factors': self.get_normalization_factors(),
            'normalized_matrix': self.get_normalized_matrix(),
            'final_ranking': dict(zip(self.ranked_alternatives, self.ranked_scores))
        }
        return results

    def combine_matrices(self):
        """
        Menggabungkan matriks benefit dan cost menjadi satu matriks kriteria.

        Returns:
            dict: Dictionary dengan key sebagai kriteria dan value sebagai dictionary alternatif dan nilainya.
        """
        combined = {}
        # Tambahkan matriks benefit
        for idx, criteria in enumerate(self.criteria_benefit):
            combined[criteria] = {alt: self.matrix_benefit[i][idx] for i, alt in enumerate(self.alternatives)}
        # Tambahkan matriks cost
        for idx, criteria in enumerate(self.criteria_cost):
            combined[criteria] = {alt: self.matrix_cost[i][idx] for i, alt in enumerate(self.alternatives)}
        return combined

    def get_normalization_factors(self):
        """
        Mengambil faktor normalisasi untuk setiap kriteria.

        Returns:
            dict: Dictionary dengan key sebagai kriteria dan value sebagai faktor normalisasi.
        """
        factors = {}
        for idx, criteria in enumerate(self.criteria_benefit):
            factors[criteria] = self.matrix_benefit[:, idx].max()
        for idx, criteria in enumerate(self.criteria_cost):
            factors[criteria] = self.matrix_cost[:, idx].min()
        return factors

    def get_normalized_matrix(self):
        """
        Menggabungkan matriks normalisasi benefit dan cost menjadi satu.

        Returns:
            dict: Dictionary dengan key sebagai kriteria dan value sebagai dictionary alternatif dan nilainya.
        """
        normalized = {}
        # Tambahkan matriks benefit yang dinormalisasi
        if self.normal_benefit is not None:
            for idx, criteria in enumerate(self.criteria_benefit):
                normalized[criteria] = {alt: self.normal_benefit[i][idx] for i, alt in enumerate(self.alternatives)}
        # Tambahkan matriks cost yang dinormalisasi
        if self.normal_cost is not None:
            for idx, criteria in enumerate(self.criteria_cost):
                normalized[criteria] = {alt: self.normal_cost[i][idx] for i, alt in enumerate(self.alternatives)}
        return normalized