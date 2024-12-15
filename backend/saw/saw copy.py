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
        self.matrix_benefit = None
        self.matrix_cost = None
        self.normal_benefit = None  # Matriks benefit yang dinormalisasi
        self.normal_cost = None     # Matriks cost yang dinormalisasi
        self.scores = None          # Skor untuk setiap alternatif
        self.ranked_alternatives = None  # Alternatif yang telah diurutkan
        self.ranked_scores = None        # Skor yang telah diurutkan

    def add_criteria(self, criteria_type='benefit'):
        """
        Meminta pengguna untuk memasukkan kriteria ke dalam SAW.
        
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
            elif criteria_name in criteria_list:
                print("Kriteria sudah ada dalam kategori ini.")
                continue
            elif criteria_name in self.criteria_benefit + self.criteria_cost:
                print("Kriteria sudah ada di kategori lain.")
                continue
            criteria_list.append(criteria_name)

    def add_weights(self, criteria_type='benefit'):
        """
        Meminta pengguna untuk memasukkan bobot kriteria ke dalam SAW tanpa normalisasi.
        
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
        weights.clear()  # Mengosongkan list bobot sebelumnya
        for crit in criteria:
            while True:
                try:
                    weight_input = input(f"Masukkan bobot untuk kriteria '{crit}': ").strip()
                    weight = float(weight_input)
                    if weight < 0:
                        print("Bobot tidak boleh negatif. Silakan masukkan kembali.")
                        continue
                    weights.append(weight)
                    break
                except ValueError:
                    print("Bobot harus berupa angka. Silakan masukkan kembali.")

        # Pastikan bobot tidak semua nol
        if sum(weights) == 0:
            print(f"Total bobot untuk {criteria_type} adalah nol. Silakan masukkan bobot kembali.")
            weights.clear()
            self.add_weights(criteria_type)
        # Tidak melakukan normalisasi bobot

    def add_alternatives(self):
        """
        Meminta pengguna untuk memasukkan alternatif ke dalam SAW.
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

    def add_matrices(self):
        """
        Membuat matriks untuk kriteria benefit dan cost.
        """
        if not self.alternatives:
            print("Belum ada alternatif. Silakan tambahkan terlebih dahulu.")
            return
        if not self.criteria_benefit and not self.criteria_cost:
            print("Belum ada kriteria benefit atau cost. Silakan tambahkan terlebih dahulu.")
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

    def normalization(self):
        """
        Normalisasi matriks kriteria benefit dan cost.
        
        Returns:
            normal_benefit (np.ndarray): Matriks benefit yang sudah dinormalisasi.
            normal_cost (np.ndarray): Matriks cost yang sudah dinormalisasi.
        """
        normal_benefit = None
        normal_cost = None

        if self.matrix_benefit is not None:
            # Normalisasi Benefit (max normalization)
            max_benefit = self.matrix_benefit.max(axis=0)
            # Hindari pembagian dengan nol
            max_benefit[max_benefit == 0] = 1
            normal_benefit = self.matrix_benefit / max_benefit

        if self.matrix_cost is not None:
            # Normalisasi Cost (min normalization)
            min_cost = self.matrix_cost.min(axis=0)
            # Hindari pembagian dengan nol pada min_cost
            min_cost[min_cost == 0] = 1
            with np.errstate(divide='ignore', invalid='ignore'):
                normal_cost = min_cost / self.matrix_cost
                normal_cost[~np.isfinite(normal_cost)] = 1  # Gantikan inf atau NaN dengan 1

        self.normal_benefit = normal_benefit
        self.normal_cost = normal_cost

        return self.normal_benefit, self.normal_cost

    def calculate_score(self):
        """
        Hitung skor total untuk setiap alternatif dengan bobot.
        
        Returns:
            scores (np.ndarray): Array skor total untuk setiap alternatif.
        """
        if self.normal_benefit is None or self.normal_cost is None:
            self.normal_benefit, self.normal_cost = self.normalization()
        scores = np.zeros(len(self.alternatives))

        for i in range(len(self.alternatives)):
            score = 0
            if self.normal_benefit is not None:
                score += np.dot(self.normal_benefit[i], self.weight_benefit)
            if self.normal_cost is not None:
                score += np.dot(self.normal_cost[i], self.weight_cost)
            scores[i] = score

        self.scores = scores
        return scores

    def rank_alternative(self):
        """
        Menentukan peringkat alternatif berdasarkan skor tertinggi.
        
        Returns:
            ranked_alternatives (list): Daftar alternatif yang diurutkan dari skor tertinggi ke terendah.
            ranked_scores (np.ndarray): Array skor total yang diurutkan.
        """
        if self.scores is None:
            self.calculate_score()
        ranked_indices = np.argsort(self.scores)[::-1]  # Urutkan skor dari yang tertinggi
        self.ranked_alternatives = [self.alternatives[i] for i in ranked_indices]
        self.ranked_scores = self.scores[ranked_indices]
        return self.ranked_alternatives, self.ranked_scores

    def display(self):
        """
        Fungsi untuk menampilkan hasil SAW.
        Menampilkan Matriks Benefit, Matriks Cost, Matriks Normalisasi, dan Ranking Alternatif berdasarkan skor.
        """
        print("\n=== Hasil SAW ===")

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

        # Matriks Normalisasi Benefit
        if self.normal_benefit is not None:
            print("\nMatriks Normalisasi Benefit:")
            header = "Alternatif\t" + "\t".join(self.criteria_benefit)
            print(header)
            for i, alternative in enumerate(self.alternatives):
                values = "\t".join(f"{val:.4f}" for val in self.normal_benefit[i])
                print(f"{alternative}\t{values}")
        else:
            print("\nTidak ada Matriks Normalisasi Benefit.")

        # Matriks Normalisasi Cost
        if self.normal_cost is not None:
            print("\nMatriks Normalisasi Cost:")
            header = "Alternatif\t" + "\t".join(self.criteria_cost)
            print(header)
            for i, alternative in enumerate(self.alternatives):
                values = "\t".join(f"{val:.4f}" for val in self.normal_cost[i])
                print(f"{alternative}\t{values}")
        else:
            print("\nTidak ada Matriks Normalisasi Cost.")

        # Ranking Alternatif berdasarkan skor
        if self.ranked_alternatives is not None and self.ranked_scores is not None:
            print("\nRanking Alternatif Berdasarkan Skor:")
            for i, (alt, score) in enumerate(zip(self.ranked_alternatives, self.ranked_scores)):
                print(f"Ranking {i + 1}: {alt} (Skor: {score:.4f})")
        else:
            print("\nBelum ada ranking yang dihitung. Silakan lakukan perhitungan terlebih dahulu.")

    def run_saw(self):
        """
        Menjalankan keseluruhan proses SAW: menambahkan kriteria, bobot, alternatif, matriks, dan menampilkan hasil.
        """
        print("\n=== Proses SAW Dimulai ===")

        # Menambahkan Kriteria Benefit
        self.add_criteria('benefit')

        # Menambahkan Kriteria Cost
        self.add_criteria('cost')

        # Menambahkan Bobot Benefit
        self.add_weights('benefit')

        # Menambahkan Bobot Cost
        self.add_weights('cost')

        # Menambahkan Alternatif
        self.add_alternatives()

        # Menambahkan Matriks
        self.add_matrices()

        # Melakukan Normalisasi dan Perhitungan Skor
        self.calculate_score()

        # Mengurutkan Alternatif berdasarkan Skor
        self.rank_alternative()

        # Menampilkan Hasil
        self.display()

        print("\n=== Proses SAW Selesai ===")

def main():
    saw = SAW()
    saw.run_saw()

if __name__ == "__main__":
    main()
