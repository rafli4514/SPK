import numpy as np
from ..base_method import BaseMethod

class MAUT:
    def __init__(self):
        """
        Inisialisasi objek MAUT tanpa kriteria dan alternatif awal.
        """
        self.criteria_benefit = []
        self.criteria_cost = []
        self.weight_benefit = []
        self.weight_cost = []
        self.alternatives = []
        self.matrix_benefit = None
        self.matrix_cost = None
        self.S_scores = None
        self.V_scores = None
        self.ranked_alternatives = None
        self.ranked_V = None

    def add_criteria(self, criteria_type='benefit'):
        """
        Meminta pengguna untuk memasukkan kriteria ke dalam MAUT.
        
        Parameters:
            criteria_type (str): Tipe kriteria ('benefit' atau 'cost').
        """
        if criteria_type == 'benefit':
            criteria_list = self.criteria_benefit
            title = "=== Tambahkan Kriteria Benefit ==="
        elif criteria_type == 'cost':
            criteria_list = self.criteria_cost
            title = "=== Tambahkan Kriteria Cost ==="
        else:
            raise ValueError("Tipe kriteria harus 'benefit' atau 'cost'.")

        print(f"\n{title}")
        while True:
            criteria_name = input("Masukkan nama kriteria (atau ketik 'selesai' untuk mengakhiri): ").strip()
            if criteria_name.lower() == 'selesai':
                break
            elif criteria_name == '':
                print("Nama kriteria tidak boleh kosong.")
                continue
            elif criteria_name in self.criteria_benefit + self.criteria_cost:
                print("Kriteria sudah ada.")
                continue
            criteria_list.append(criteria_name)
        print(f"Jumlah kriteria {criteria_type}: {len(criteria_list)}")

    def add_weights(self, criteria_type='benefit'):
        """
        Meminta pengguna untuk memasukkan bobot kriteria ke dalam MAUT tanpa normalisasi awal.
        
        Parameters:
            criteria_type (str): Tipe kriteria ('benefit' atau 'cost').
        """
        if criteria_type == 'benefit':
            criteria = self.criteria_benefit
            weights = self.weight_benefit
            title = "=== Tambahkan Bobot Benefit ==="
        elif criteria_type == 'cost':
            criteria = self.criteria_cost
            weights = self.weight_cost
            title = "=== Tambahkan Bobot Cost ==="
        else:
            raise ValueError("Tipe kriteria harus 'benefit' atau 'cost'.")

        if not criteria:
            print(f"Belum ada kriteria {criteria_type}. Silakan tambahkan terlebih dahulu.")
            return

        print(f"\n{title}")
        weights.clear()  # Menghapus bobot sebelumnya jika ada
        for crit in criteria:
            while True:
                try:
                    weight_input = input(f"Masukkan bobot untuk kriteria '{crit}': ").strip()
                    weight = float(weight_input)
                    if weight <= 0:
                        print("Bobot harus > 0. Silakan masukkan kembali.")
                        continue
                    weights.append(weight)
                    break
                except ValueError:
                    print("Bobot harus berupa angka. Silakan masukkan kembali.")

        # Pastikan total bobot tidak nol
        if sum(weights) == 0:
            print(f"Total bobot untuk {criteria_type} adalah nol. Silakan masukkan bobot kembali.")
            weights.clear()
            self.add_weights(criteria_type)
        else:
            print(f"Bobot {criteria_type} berhasil ditambahkan.")

    def add_alternatives(self):
        """
        Meminta pengguna untuk memasukkan alternatif.
        """
        print("\n=== Tambahkan Alternatif ===")
        while True:
            alternative_name = input("Masukkan nama alternatif (atau ketik 'selesai' untuk mengakhiri): ").strip()
            if alternative_name.lower() == 'selesai':
                break
            elif alternative_name == '':
                print("Nama alternatif tidak boleh kosong.")
                continue
            elif alternative_name in self.alternatives:
                print("Alternatif sudah ada.")
                continue
            self.alternatives.append(alternative_name)
        print(f"Jumlah alternatif: {len(self.alternatives)}")

    def add_matrices(self):
        """
        Membuat matriks untuk kriteria benefit dan cost.
        """
        if not self.alternatives:
            print("Belum ada alternatif. Silakan tambahkan terlebih dahulu.")
            return

        length_alternative = len(self.alternatives)

        if self.criteria_benefit:
            self.matrix_benefit = np.zeros((length_alternative, len(self.criteria_benefit)))
            print("\n=== Masukkan nilai untuk Matriks Benefit ===")
            for i, alternative in enumerate(self.alternatives):
                for j, criteria in enumerate(self.criteria_benefit):
                    while True:
                        try:
                            value_input = input(f"Masukkan nilai untuk alternatif '{alternative}' pada kriteria '{criteria}': ").strip()
                            value = float(value_input)
                            if value < 0:
                                print("Nilai benefit tidak boleh negatif. Silakan masukkan kembali.")
                                continue
                            self.matrix_benefit[i][j] = value
                            break
                        except ValueError:
                            print("Nilai harus berupa angka. Silakan masukkan kembali.")
        else:
            self.matrix_benefit = None

        if self.criteria_cost:
            self.matrix_cost = np.zeros((length_alternative, len(self.criteria_cost)))
            print("\n=== Masukkan nilai untuk Matriks Cost ===")
            for i, alternative in enumerate(self.alternatives):
                for j, criteria in enumerate(self.criteria_cost):
                    while True:
                        try:
                            value_input = input(f"Masukkan nilai untuk alternatif '{alternative}' pada kriteria '{criteria}': ").strip()
                            value = float(value_input)
                            if value < 0:
                                print("Nilai cost tidak boleh negatif. Silakan masukkan kembali.")
                                continue
                            self.matrix_cost[i][j] = value
                            break
                        except ValueError:
                            print("Nilai harus berupa angka. Silakan masukkan kembali.")
        else:
            self.matrix_cost = None

        print("Matriks telah dibuat.")

    def normalize_weights(self):
        """
        Normalisasi bobot kriteria agar total bobot sama dengan 1.
        """
        total_benefit = sum(self.weight_benefit)
        total_cost = sum(self.weight_cost)
        total = total_benefit + total_cost
        if total == 0:
            raise ValueError("Total bobot tidak boleh nol.")
        # Normalisasi
        self.weight_benefit = [w / total for w in self.weight_benefit]
        self.weight_cost = [w / total for w in self.weight_cost]
        print("\nBobot telah dinormalisasi.")

    def calculate_scores(self):
        """
        Hitung skor MAUT untuk setiap alternatif.
        
        Langkah:
        1. Normalisasi nilai kriteria (benefit dan cost).
        2. Hitung utilitas total S_i = sum (U_j(x_ij) * w_j) untuk semua j.
        3. Hitung skor V_i = S_i / sum(S_i).
        """
        if not self.weight_benefit and not self.weight_cost:
            print("Belum ada bobot yang diinput.")
            return

        # Normalisasi matriks kriteria benefit
        if self.matrix_benefit is not None:
            norm_matrix_benefit = np.zeros_like(self.matrix_benefit)
            for j in range(self.matrix_benefit.shape[1]):
                column = self.matrix_benefit[:, j]
                max_val = column.max()
                if max_val == 0:
                    norm_matrix_benefit[:, j] = 0
                else:
                    norm_matrix_benefit[:, j] = column / max_val
        else:
            norm_matrix_benefit = None

        # Normalisasi matriks kriteria cost
        if self.matrix_cost is not None:
            norm_matrix_cost = np.zeros_like(self.matrix_cost)
            for j in range(self.matrix_cost.shape[1]):
                column = self.matrix_cost[:, j]
                min_val = column.min()
                if min_val == 0:
                    norm_matrix_cost[:, j] = 0
                else:
                    norm_matrix_cost[:, j] = min_val / column
        else:
            norm_matrix_cost = None

        # Hitung utilitas total S_i
        S = np.zeros(len(self.alternatives))

        # Tambahkan kontribusi dari kriteria benefit
        if norm_matrix_benefit is not None:
            weighted_benefit = norm_matrix_benefit * self.weight_benefit
            S += weighted_benefit.sum(axis=1)

        # Tambahkan kontribusi dari kriteria cost
        if norm_matrix_cost is not None:
            weighted_cost = norm_matrix_cost * self.weight_cost
            S += weighted_cost.sum(axis=1)

        self.S_scores = S

        # Hitung sum S_i
        sum_S = S.sum()
        if sum_S == 0:
            print("Jumlah total skor S adalah nol. Tidak dapat menghitung skor V.")
            self.V_scores = None
            return

        # Hitung skor V_i
        V = S / sum_S
        self.V_scores = V
        print("Skor S dan V telah dihitung.")

    def rank_alternatives(self):
        """
        Mengurutkan alternatif berdasarkan nilai V (tertinggi ke terendah).
        """
        if self.V_scores is None:
            self.calculate_scores()
        if self.V_scores is None:
            print("Tidak dapat melakukan ranking karena skor V belum tersedia.")
            return
        ranked_indices = np.argsort(self.V_scores)[::-1]
        self.ranked_alternatives = [self.alternatives[i] for i in ranked_indices]
        self.ranked_V = self.V_scores[ranked_indices]
        print("Alternatif telah diurutkan berdasarkan skor V.")

    def display(self):
        """
        Menampilkan hasil perhitungan MAUT.
        """
        print("\n=== Hasil MAUT ===")

        # Matriks Benefit
        if self.matrix_benefit is not None:
            print("\nMatriks Benefit:")
            header = "Alternatif\t" + "\t".join(self.criteria_benefit)
            print(header)
            for i, alternative in enumerate(self.alternatives):
                values = "\t".join(f"{val:.4f}" for val in self.matrix_benefit[i])
                print(f"{alternative}\t{values}")
        else:
            print("\nTidak ada Matriks Benefit.")

        # Matriks Cost
        if self.matrix_cost is not None:
            print("\nMatriks Cost:")
            header = "Alternatif\t" + "\t".join(self.criteria_cost)
            print(header)
            for i, alternative in enumerate(self.alternatives):
                values = "\t".join(f"{val:.4f}" for val in self.matrix_cost[i])
                print(f"{alternative}\t{values}")
        else:
            print("\nTidak ada Matriks Cost.")

        # Bobot yang sudah dinormalisasi
        print("\nBobot Kriteria (Ternormalisasi):")
        for crit, w in zip(self.criteria_benefit, self.weight_benefit):
            print(f"{crit} (Benefit): {w:.4f}")
        for crit, w in zip(self.criteria_cost, self.weight_cost):
            print(f"{crit} (Cost): {w:.4f}")

        # Nilai S
        if self.S_scores is not None:
            print("\nNilai S untuk setiap alternatif:")
            for alt, s in zip(self.alternatives, self.S_scores):
                print(f"{alt}: {s:.6f}")
        else:
            print("\nBelum menghitung nilai S.")

        # Nilai V
        if self.V_scores is not None:
            print("\nNilai V untuk setiap alternatif:")
            for alt, v in zip(self.alternatives, self.V_scores):
                print(f"{alt}: {v:.6f}")
        else:
            print("\nBelum menghitung nilai V.")

        # Ranking
        if self.ranked_alternatives is not None and self.ranked_V is not None:
            print("\nRanking Alternatif Berdasarkan V:")
            for i, (alt, score) in enumerate(zip(self.ranked_alternatives, self.ranked_V)):
                print(f"Ranking {i+1}: {alt} (V: {score:.6f})")
        else:
            print("\nBelum ada ranking yang dihitung.")

    def run_maut(self):
        """
        Menjalankan keseluruhan proses MAUT.
        """
        print("\n=== Proses MAUT Dimulai ===")

        # Menambahkan Kriteria Benefit
        self.add_criteria('benefit')

        # Menambahkan Kriteria Cost
        self.add_criteria('cost')

        # Memastikan setidaknya ada satu kriteria
        if not self.criteria_benefit and not self.criteria_cost:
            print("Tidak ada kriteria yang ditambahkan. Proses MAUT dihentikan.")
            return

        # Menambahkan Bobot Benefit
        if self.criteria_benefit:
            self.add_weights('benefit')

        # Menambahkan Bobot Cost
        if self.criteria_cost:
            self.add_weights('cost')

        # Memastikan setidaknya ada bobot
        if not self.weight_benefit and not self.weight_cost:
            print("Tidak ada bobot yang ditambahkan. Proses MAUT dihentikan.")
            return

        # Normalisasi bobot
        self.normalize_weights()

        # Menambahkan Alternatif
        self.add_alternatives()

        # Memastikan setidaknya ada satu alternatif
        if not self.alternatives:
            print("Tidak ada alternatif yang ditambahkan. Proses MAUT dihentikan.")
            return

        # Menambahkan Matriks
        self.add_matrices()

        # Memastikan setidaknya ada satu matriks
        if self.matrix_benefit is None and self.matrix_cost is None:
            print("Tidak ada matriks kriteria yang dimasukkan. Proses MAUT dihentikan.")
            return

        # Hitung Skor
        self.calculate_scores()

        # Memastikan skor telah dihitung
        if self.S_scores is None or self.V_scores is None:
            print("Skor tidak dapat dihitung. Proses MAUT dihentikan.")
            return

        # Ranking Alternatif
        self.rank_alternatives()

        # Tampilkan Hasil
        self.display()

        print("\n=== Proses MAUT Selesai ===")


def main():
    maut = MAUT()
    maut.run_maut()

if __name__ == "__main__":
    main()