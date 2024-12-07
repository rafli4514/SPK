# methods/ahp.py

import numpy as np
import pandas as pd
from .base_method import BaseMethod

class AHP(BaseMethod):
    def __init__(self, criteria, alternatives):
        """
        Inisialisasi kelas AHP dengan kriteria dan alternatif yang diberikan.
        
        Args:
            criteria (list): Daftar nama kriteria.
            alternatives (list): Daftar nama alternatif.
        """
        super().__init__(criteria, alternatives)
        self.criteria_matrix = None        # Matriks perbandingan berpasangan antar kriteria
        self.criteria_weights = None       # Bobot kriteria setelah perhitungan
        self.alternative_matrices = {}     # Matriks perbandingan berpasangan antar alternatif untuk setiap kriteria
        self.alternative_weights = {}      # Bobot alternatif untuk setiap kriteria setelah perhitungan
        self.final_ranking = None          # Ranking akhir alternatif berdasarkan bobot kriteria dan bobot alternatif
        self.steps = []                    # Menyimpan langkah-langkah pengerjaan untuk dokumentasi
    
    def set_criteria_comparisons(self, comparisons):
        """
        Mengatur matriks perbandingan berpasangan antar kriteria berdasarkan input pengguna.
        
        Args:
            comparisons (list of tuples): Daftar tuple dalam format (i, j, value) 
                dimana 'i' dan 'j' adalah indeks kriteria dan 'value' adalah nilai perbandingan kriteria_i terhadap kriteria_j.
        """
        n = len(self.criteria)
        self.criteria_matrix = np.ones((n, n))  # Inisialisasi matriks dengan 1 di diagonal utama
        for (i, j, value) in comparisons:
            self.criteria_matrix[i, j] = value              # Menetapkan nilai perbandingan
            self.criteria_matrix[j, i] = 1 / value          # Menetapkan invers dari nilai perbandingan
        self.steps.append("Perbandingan kriteria dimasukkan.")  # Menyimpan langkah pengerjaan
    
    def set_alternative_comparisons(self, criteria, comparisons):
        """
        Mengatur matriks perbandingan berpasangan antar alternatif untuk sebuah kriteria.
        
        Args:
            criteria (str): Nama kriteria yang sedang diproses.
            comparisons (list of tuples): Daftar tuple dalam format (i, j, value) 
                dimana 'i' dan 'j' adalah indeks alternatif dan 'value' adalah nilai perbandingan alternatif_i terhadap alternatif_j.
        """
        n = len(self.alternatives)
        if criteria not in self.alternative_matrices:
            self.alternative_matrices[criteria] = np.ones((n, n))  # Inisialisasi matriks dengan 1 di diagonal utama jika belum ada
        matrix = self.alternative_matrices[criteria]
        for (i, j, value) in comparisons:
            matrix[i, j] = value              # Menetapkan nilai perbandingan
            matrix[j, i] = 1 / value          # Menetapkan invers dari nilai perbandingan
        self.steps.append(f"Perbandingan alternatif untuk kriteria '{criteria}' dimasukkan.")  # Menyimpan langkah pengerjaan
    
    def calculate_weights_from_matrix(self, matrix):
        """
        Menghitung bobot (prioritas) dari matriks perbandingan berpasangan menggunakan eigenvector utama.
        
        Args:
            matrix (np.ndarray): Matriks perbandingan berpasangan.
        
        Returns:
            np.ndarray: Bobot yang telah dinormalisasi.
        """
        eigvals, eigvecs = np.linalg.eig(matrix)             # Menghitung nilai eigen dan vektor eigen
        max_index = np.argmax(eigvals.real)                  # Menemukan indeks nilai eigen terbesar (principal eigenvalue)
        principal_eigvec = eigvecs[:, max_index].real        # Mengambil vektor eigen utama
        normalized_weights = principal_eigvec / principal_eigvec.sum()  # Normalisasi bobot
        return normalized_weights
    
    def calculate_consistency_ratio(self, matrix, weights):
        """
        Menghitung Consistency Ratio (CR) untuk memeriksa konsistensi matriks perbandingan berpasangan.
        
        Args:
            matrix (np.ndarray): Matriks perbandingan berpasangan.
            weights (np.ndarray): Bobot yang telah dihitung dari matriks.
        
        Returns:
            float: Consistency Ratio.
        """
        n = matrix.shape[0]
        lambda_max = np.dot(matrix, weights).sum() / weights.sum()  # Menghitung lambda_max
        CI = (lambda_max - n) / (n - 1)                              # Menghitung Consistency Index (CI)
        RI_dict = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12,
                   6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        RI = RI_dict.get(n, 1.49)  # Mengambil Random Index (RI) berdasarkan ukuran matriks
        if RI == 0:
            return 0.0  # Menghindari pembagian dengan nol jika RI=0
        CR = CI / RI       # Menghitung Consistency Ratio (CR)
        return CR
    
    def perform_ahp(self):
        """
        Melakukan seluruh proses perhitungan AHP, termasuk menghitung bobot kriteria,
        bobot alternatif, serta ranking akhir alternatif.
        """
        # Hitung bobot kriteria menggunakan matriks perbandingan kriteria
        self.criteria_weights = self.calculate_weights_from_matrix(self.criteria_matrix)
        CR = self.calculate_consistency_ratio(self.criteria_matrix, self.criteria_weights)  # Menghitung CR untuk kriteria
        self.steps.append(f"Consistency Ratio untuk kriteria: {CR:.4f}")  # Menyimpan CR kriteria
        
        if CR > 0.1:
            # Memberikan peringatan jika CR > 0.1
            self.steps.append("Warning: Consistency Ratio melebihi 0.1. Pertimbangkan untuk merevisi perbandingan Anda.")
        else:
            self.steps.append("Consistency Ratio dapat diterima.")  # Menyimpan bahwa CR dapat diterima
        
        # Hitung bobot alternatif untuk setiap kriteria
        for crit in self.criteria:
            weights = self.calculate_weights_from_matrix(self.alternative_matrices[crit])  # Menghitung bobot alternatif
            self.alternative_weights[crit] = weights
            CR_alt = self.calculate_consistency_ratio(self.alternative_matrices[crit], weights)  # Menghitung CR untuk alternatif
            self.steps.append(f"Consistency Ratio untuk alternatif di bawah '{crit}': {CR_alt:.4f}")  # Menyimpan CR alternatif
            
            if CR_alt > 0.1:
                # Memberikan peringatan jika CR alternatif > 0.1
                self.steps.append(f"Warning: Consistency Ratio untuk '{crit}' melebihi 0.1. Pertimbangkan untuk merevisi perbandingan Anda.")
            else:
                self.steps.append(f"Consistency Ratio untuk '{crit}' dapat diterima.")  # Menyimpan bahwa CR alternatif dapat diterima
        
        # Hitung ranking akhir dengan menjumlahkan bobot alternatif dikalikan bobot kriteria
        self.final_ranking = np.zeros(len(self.alternatives))
        for i, crit in enumerate(self.criteria):
            self.final_ranking += self.criteria_weights[i] * self.alternative_weights[crit]
        self.steps.append("Ranking akhir dihitung.")  # Menyimpan langkah menghitung ranking akhir
    
    def get_results(self):
        """
        Mengembalikan semua hasil perhitungan AHP, termasuk matriks, bobot, ranking, dan langkah-langkah pengerjaan.
        
        Returns:
            dict: Dictionary yang berisi berbagai hasil perhitungan AHP.
        """
        # Konversi bobot kriteria dan bobot alternatif ke dalam list untuk kemudahan penggunaan
        criteria_weights = self.criteria_weights.tolist() if isinstance(self.criteria_weights, np.ndarray) else self.criteria_weights
        alternative_weights = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in self.alternative_weights.items()}
        
        # Konversi final_ranking ke dictionary dengan nama alternatif sebagai key dan skor akhir sebagai value
        final_ranking_dict = {self.alternatives[i]: score for i, score in enumerate(self.final_ranking)}
        
        # Menyusun semua hasil ke dalam sebuah dictionary
        results = {
            'criteria_matrix': self.criteria_matrix,                     # Matriks perbandingan kriteria
            'criteria_weights': criteria_weights,                        # Bobot kriteria
            'alternative_matrices': self.alternative_matrices,           # Matriks perbandingan alternatif per kriteria
            'alternative_weights': alternative_weights,                   # Bobot alternatif per kriteria
            'final_ranking': final_ranking_dict,                         # Ranking akhir alternatif
            'steps': self.steps                                          # Langkah-langkah pengerjaan
        }
        return results
