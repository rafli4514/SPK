import numpy as np
import pandas as pd

class AHP:
    def __init__(self):
        """
        Inisialisasi objek AHP tanpa kriteria dan alternatif awal.
        """
        self.criteria = []
        self.alternatives = []
        self.criteria_matrix = None
        self.criteria_weights = None
        self.alternative_matrices = {}
        self.alternative_weights = {}
        self.final_ranking = None

    @staticmethod
    def parse_input(prompt):
        """
        Memproses input pengguna. Mendukung angka biasa atau pecahan (misal: 1/3).

        Parameters:
            prompt (str): Pesan prompt untuk input pengguna.

        Returns:
            float: Nilai numerik yang diinputkan.
        """
        user_input = input(prompt).strip()
        try:
            if '/' in user_input:
                numerator, denominator = map(float, user_input.split('/'))
                if denominator == 0:
                    raise ValueError
                return numerator / denominator
            else:
                value = float(user_input)
                if value <= 0:
                    raise ValueError
                return value
        except Exception:
            raise ValueError("Input tidak valid. Harap masukkan angka positif atau pecahan seperti 1/3.")

    def add_criteria(self):
        """
        Meminta pengguna untuk memasukkan kriteria ke dalam AHP.
        """
        print("\n=== Tambahkan Kriteria ===")
        while True:
            criteria_name = input("Masukkan nama kriteria (atau ketik 'selesai' untuk mengakhiri): ").strip()
            if criteria_name.lower() == 'selesai':
                break
            if not criteria_name:
                print("Nama kriteria tidak boleh kosong.")
                continue
            if criteria_name in self.criteria:
                print("Kriteria sudah ada. Harap masukkan nama yang unik.")
                continue
            self.criteria.append(criteria_name)

        n = len(self.criteria)
        if n < 2:
            print("Dibutuhkan minimal dua kriteria untuk AHP.")
            self.criteria = []  # Reset kriteria
            return
        self.criteria_matrix = np.ones((n, n))

    def add_alternatives(self):
        """
        Meminta pengguna untuk memasukkan alternatif ke dalam AHP.
        """
        print("\n=== Tambahkan Alternatif ===")
        while True:
            alternative_name = input("Masukkan nama alternatif (atau ketik 'selesai' untuk mengakhiri): ").strip()
            if alternative_name.lower() == 'selesai':
                break
            if not alternative_name:
                print("Nama alternatif tidak boleh kosong.")
                continue
            if alternative_name in self.alternatives:
                print("Alternatif sudah ada. Harap masukkan nama yang unik.")
                continue
            self.alternatives.append(alternative_name)

        n = len(self.alternatives)
        if n < 2:
            print("Dibutuhkan minimal dua alternatif untuk AHP.")
            self.alternatives = []  # Reset alternatif
            return
        for crit in self.criteria:
            self.alternative_matrices[crit] = np.ones((n, n))

    def input_comparisons_criteria(self):
        """
        Meminta pengguna untuk memasukkan nilai perbandingan antar kriteria dan memeriksa konsistensi.
        """
        if not self.criteria:
            print("Belum ada kriteria. Silakan tambahkan kriteria terlebih dahulu.")
            return

        print("\n=== Input Perbandingan Berpasangan untuk Kriteria ===")
        n = len(self.criteria)
        for i in range(n):
            for j in range(i + 1, n):
                while True:
                    try:
                        prompt = f"Masukkan nilai perbandingan '{self.criteria[i]}' terhadap '{self.criteria[j]}' (contoh: 1/3 atau 3): "
                        value = self.parse_input(prompt)
                        self.criteria_matrix[i, j] = value
                        self.criteria_matrix[j, i] = 1 / value
                        break
                    except ValueError as ve:
                        print(ve)

        # Hitung bobot dan konsistensi
        self.criteria_weights = self.calculate_weights_from_matrix(self.criteria_matrix)
        CR = self.calculate_consistency_ratio(self.criteria_matrix, self.criteria_weights)
        print(f"\nConsistency Ratio untuk kriteria: {CR:.4f}")
        if CR > 0.1:
            print("Peringatan: Consistency Ratio melebihi 0.1. Pertimbangkan untuk merevisi perbandingan Anda.")
            self.retry_comparisons("criteria")
        else:
            print("Consistency Ratio dapat diterima.")

    def input_comparisons_alternatives(self):
        """
        Meminta pengguna untuk memasukkan nilai perbandingan antar alternatif berdasarkan masing-masing kriteria dan memeriksa konsistensi.
        """
        if not self.alternatives:
            print("Belum ada alternatif. Silakan tambahkan alternatif terlebih dahulu.")
            return

        print("\n=== Input Perbandingan Berpasangan untuk Alternatif ===")
        for crit in self.criteria:
            print(f"\n-- Kriteria: {crit} --")
            matrix = self.alternative_matrices[crit]
            n = len(self.alternatives)
            for i in range(n):
                for j in range(i + 1, n):
                    while True:
                        try:
                            prompt = f"Masukkan nilai perbandingan '{self.alternatives[i]}' terhadap '{self.alternatives[j]}' (contoh: 1/3 atau 3): "
                            value = self.parse_input(prompt)
                            matrix[i, j] = value
                            matrix[j, i] = 1 / value
                            break
                        except ValueError as ve:
                            print(ve)
            # Hitung bobot dan konsistensi untuk alternatif di bawah kriteria ini
            weights = self.calculate_weights_from_matrix(matrix)
            self.alternative_weights[crit] = weights
            CR = self.calculate_consistency_ratio(matrix, weights)
            print(f"Consistency Ratio untuk alternatif di bawah '{crit}': {CR:.4f}")
            if CR > 0.1:
                print("Peringatan: Consistency Ratio melebihi 0.1. Pertimbangkan untuk merevisi perbandingan Anda.")
                self.retry_comparisons("alternative", crit)
            else:
                print("Consistency Ratio dapat diterima.")

    def retry_comparisons(self, comparison_type, criteria=None):
        """
        Menyediakan opsi untuk mengulang perbandingan jika CR terlalu tinggi.

        Parameters:
            comparison_type (str): 'criteria' atau 'alternative'.
            criteria (str, optional): Nama kriteria jika comparison_type adalah 'alternative'.
        """
        while True:
            choice = input("Apakah Anda ingin mengulang perbandingan ini? (ya/tidak): ").strip().lower()
            if choice == 'ya':
                if comparison_type == 'criteria':
                    self.input_comparisons_criteria()
                elif comparison_type == 'alternative' and criteria:
                    self.input_comparisons_alternatives_specific(criteria)
                break
            elif choice == 'tidak':
                print("Melanjutkan tanpa mengubah perbandingan.")
                break
            else:
                print("Pilihan tidak valid. Silakan masukkan 'ya' atau 'tidak'.")

    def input_comparisons_alternatives_specific(self, criteria):
        """
        Meminta pengguna untuk memasukkan ulang perbandingan berpasangan untuk alternatif di bawah kriteria tertentu.

        Parameters:
            criteria (str): Nama kriteria.
        """
        print(f"\n=== Ulangi Input Perbandingan Berpasangan untuk Alternatif di Bawah Kriteria: {criteria} ===")
        matrix = self.alternative_matrices[criteria]
        n = len(self.alternatives)
        for i in range(n):
            for j in range(i + 1, n):
                while True:
                    try:
                        prompt = f"Masukkan nilai perbandingan '{self.alternatives[i]}' terhadap '{self.alternatives[j]}' (contoh: 1/3 atau 3): "
                        value = self.parse_input(prompt)
                        matrix[i, j] = value
                        matrix[j, i] = 1 / value
                        break
                    except ValueError as ve:
                        print(ve)
        # Hitung bobot dan konsistensi
        weights = self.calculate_weights_from_matrix(matrix)
        self.alternative_weights[criteria] = weights
        CR = self.calculate_consistency_ratio(matrix, weights)
        print(f"Consistency Ratio untuk alternatif di bawah '{criteria}': {CR:.4f}")
        if CR > 0.1:
            print("Peringatan: Consistency Ratio melebihi 0.1. Pertimbangkan untuk merevisi perbandingan Anda.")
            self.retry_comparisons("alternative", criteria)
        else:
            print("Consistency Ratio dapat diterima.")

    def calculate_weights_from_matrix(self, matrix):
        """
        Menghitung bobot menggunakan eigenvektor utama dari matriks perbandingan.

        Parameters:
            matrix (np.ndarray): Matriks perbandingan berpasangan.

        Returns:
            np.ndarray: Vektor bobot yang telah dinormalisasi.
        """
        eigvals, eigvecs = np.linalg.eig(matrix)
        max_index = np.argmax(eigvals.real)
        principal_eigvec = eigvecs[:, max_index].real
        normalized_weights = principal_eigvec / principal_eigvec.sum()
        return normalized_weights

    def calculate_consistency_ratio(self, matrix, weights):
        """
        Menghitung Consistency Ratio (CR) dari matriks perbandingan berpasangan.

        Parameters:
            matrix (np.ndarray): Matriks perbandingan berpasangan.
            weights (np.ndarray): Vektor bobot.

        Returns:
            float: Consistency Ratio.
        """
        n = matrix.shape[0]
        lamda_max = np.max(np.linalg.eigvals(matrix).real)
        CI = (lamda_max - n) / (n - 1)
        RI_dict = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12,
                   6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        RI = RI_dict.get(n, 1.49)  # Default ke 1.49 untuk n > 10
        if RI == 0:
            return 0.0  # Menghindari pembagian dengan nol
        CR = CI / RI
        return CR

    def calculate_weights(self):
        """
        Menghitung bobot untuk kriteria dan alternatif, serta menghasilkan ranking akhir.
        """
        if self.criteria_weights is None or not self.alternatives:
            print("Bobot kriteria belum dihitung atau tidak ada alternatif.")
            return

        self.final_ranking = np.zeros(len(self.alternatives))
        for i, crit in enumerate(self.criteria):
            self.final_ranking += self.criteria_weights[i] * self.alternative_weights[crit]

    def display_results(self):
        """
        Menampilkan hasil AHP dalam format yang terstruktur.
        """
        if self.final_ranking is None:
            print("Belum ada perhitungan ranking akhir.")
            return

        print("\n=== Matriks Perbandingan Kriteria ===")
        df_criteria = pd.DataFrame(self.criteria_matrix, index=self.criteria, columns=self.criteria)
        print(df_criteria)

        print("\n=== Bobot Kriteria ===")
        df_criteria_weights = pd.DataFrame(self.criteria_weights, index=self.criteria, columns=['Bobot'])
        print(df_criteria_weights)

        print("\n=== Matriks Perbandingan Alternatif per Kriteria ===")
        for crit in self.criteria:
            print(f"\n-- Kriteria: {crit} --")
            df_alt_matrix = pd.DataFrame(self.alternative_matrices[crit], index=self.alternatives, columns=self.alternatives)
            print(df_alt_matrix)

        print("\n=== Bobot Alternatif per Kriteria ===")
        for crit, weights in self.alternative_weights.items():
            print(f"\nKriteria: {crit}")
            df_alt_weights = pd.DataFrame(weights, index=self.alternatives, columns=['Bobot'])
            print(df_alt_weights)

        print("\n=== Ranking Akhir Alternatif ===")
        df_final = pd.DataFrame(self.final_ranking, index=self.alternatives, columns=['Skor Akhir'])
        df_final_sorted = df_final.sort_values(by='Skor Akhir', ascending=False)
        print(df_final_sorted)

    def run_ahp(self):
        """
        Menjalankan seluruh proses AHP secara terstruktur.
        """
        print("=== Selamat Datang di Program AHP ===")

        # Langkah 1: Tambahkan Kriteria
        self.add_criteria()
        if not self.criteria:
            print("Proses AHP dibatalkan karena kurangnya kriteria.")
            return

        # Langkah 2: Tambahkan Alternatif
        self.add_alternatives()
        if not self.alternatives:
            print("Proses AHP dibatalkan karena kurangnya alternatif.")
            return

        # Langkah 3: Input Perbandingan Berpasangan untuk Kriteria
        self.input_comparisons_criteria()
        if self.criteria_weights is None:
            print("Proses AHP dibatalkan karena perbandingan kriteria gagal.")
            return

        # Langkah 4: Input Perbandingan Berpasangan untuk Alternatif
        self.input_comparisons_alternatives()
        if not self.alternative_weights:
            print("Proses AHP dibatalkan karena perbandingan alternatif gagal.")
            return

        # Langkah 5: Hitung Bobot dan Ranking Akhir
        self.calculate_weights()
        if self.final_ranking is None:
            print("Proses AHP dibatalkan karena perhitungan bobot gagal.")
            return

        # Langkah 6: Tampilkan Hasil
        self.display_results()

# Contoh penggunaan
if __name__ == "__main__":
    ahp = AHP()
    ahp.run_ahp()