import numpy as np

class AHP:
    def __init__(self):
        """
        Inisialisasi objek AHP tanpa kriteria dan alternatif awal.
        """
        self.criteria = []  # Daftar kriteria
        self.alternatives = []  # Daftar alternatif
        self.criteria_matrix = None  # Matriks perbandingan berpasangan untuk kriteria
        self.criteria_weights = None  # Bobot kriteria
        self.alternative_matrices = {}  # Matriks perbandingan berpasangan untuk alternatif per kriteria
        self.alternative_weights = {}  # Bobot alternatif berdasarkan masing-masing kriteria
        self.final_ranking = None  # Ranking akhir alternatif

    def add_criteria(self):
        """
        Meminta pengguna untuk memasukkan kriteria ke dalam AHP.
        """
        print("=== Tambahkan Kriteria ===")
        while True:
            criteria_name = input("Masukkan nama kriteria (atau ketik 'selesai' untuk mengakhiri): ")
            if criteria_name.lower() == 'selesai':
                break
            self.criteria.append(criteria_name)

        self.criteria_matrix = np.ones((len(self.criteria), len(self.criteria)))  # Inisialisasi matriks kriteria

    def add_alternatives(self):
        """
        Meminta pengguna untuk memasukkan alternatif ke dalam AHP.
        """
        print("=== Tambahkan Alternatif ===")
        while True:
            alternative_name = input("Masukkan nama alternatif (atau ketik 'selesai' untuk mengakhiri): ")
            if alternative_name.lower() == 'selesai':
                break
            self.alternatives.append(alternative_name)

        # Inisialisasi matriks perbandingan untuk alternatif per kriteria
        for crit in self.criteria:
            self.alternative_matrices[crit] = np.ones((len(self.alternatives), len(self.alternatives)))

    def input_comparisons_criteria(self):
        """
        Meminta pengguna untuk memasukkan nilai perbandingan antar kriteria.
        Matriks perbandingan berpasangan diisi untuk kriteria.
        """
        print("=== Input Perbandingan Berpasangan untuk Kriteria ===")
        for i in range(len(self.criteria)):
            for j in range(i + 1, len(self.criteria)):
                while True:
                    try:
                        # Masukkan nilai perbandingan antar kriteria
                        value = float(parse_input(f"Masukkan nilai perbandingan {self.criteria[i]} terhadap {self.criteria[j]} (contoh: 1/3 atau 3): "))
                        self.criteria_matrix[i, j] = value
                        self.criteria_matrix[j, i] = 1 / value  # Hubungan timbal balik
                        break
                    except ValueError:
                        print("Masukkan nilai yang valid.")

    def input_comparisons_alternatives(self):
        """
        Meminta pengguna untuk memasukkan nilai perbandingan antar alternatif berdasarkan masing-masing kriteria.
        Matriks perbandingan berpasangan diisi untuk setiap kriteria.
        """
        print("=== Input Perbandingan Berpasangan untuk Alternatif ===")
        for crit in self.criteria:
            print(f"\nKriteria: {crit}")
            for i in range(len(self.alternatives)):
                for j in range(i + 1, len(self.alternatives)):
                    while True:
                        try:
                            # Masukkan nilai perbandingan antar alternatif untuk kriteria tertentu
                            value = float(parse_input(f"Masukkan nilai perbandingan {self.alternatives[i]} terhadap {self.alternatives[j]} (contoh: 1/3 atau 3): "))
                            self.alternative_matrices[crit][i, j] = value
                            self.alternative_matrices[crit][j, i] = 1 / value  # Hubungan timbal balik
                            break
                        except ValueError:
                            print("Masukkan nilai yang valid.")

    def calculate_weights(self):
        """
        Menghitung bobot untuk kriteria dan alternatif.
        1. Menghitung eigenvector utama (bobot) dari matriks kriteria.
        2. Menghitung eigenvector utama (bobot) untuk setiap matriks alternatif per kriteria.
        3. Menggabungkan bobot kriteria dan alternatif untuk menghasilkan ranking akhir.
        """
        # Hitung eigenvector utama untuk kriteria
        self.criteria_weights = self.calculate_eigenvector(self.criteria_matrix)

        # Hitung eigenvector utama untuk setiap matriks alternatif berdasarkan kriteria
        for crit, matrix in self.alternative_matrices.items():
            self.alternative_weights[crit] = self.calculate_eigenvector(matrix)

        # Gabungkan bobot alternatif berdasarkan bobot kriteria
        self.final_ranking = np.zeros(len(self.alternatives))
        for i, crit in enumerate(self.criteria):
            self.final_ranking += self.criteria_weights[i] * self.alternative_weights[crit]

    def calculate_eigenvector(self, matrix, max_iter=100, tol=1e-4):
        """
        Menghitung eigenvector utama dari sebuah matriks menggunakan metode iterasi.
        Args:
            matrix (np.ndarray): Matriks perbandingan berpasangan.
            max_iter (int): Maksimum iterasi untuk konvergensi.
            tol (float): Toleransi perbedaan antar iterasi.
        Returns:
            np.ndarray: Eigenvector utama (bobot relatif).
        """
        n = matrix.shape[0]  # Ukuran matriks
        w = np.ones(n)  # Inisialisasi vektor awal
        for _ in range(max_iter):
            w_new = np.dot(matrix, w)  # Kalikan matriks dengan vektor
            w_new = w_new / np.sum(w_new)  # Normalisasi vektor
            if np.linalg.norm(w_new - w, ord=1) < tol:  # Periksa konvergensi
                break
            w = w_new
        return w_new

    def display_results(self):
        """
        Menampilkan hasil:
        1. Matriks perbandingan kriteria.
        2. Bobot kriteria.
        3. Bobot alternatif per kriteria.
        4. Ranking akhir alternatif.
        """
        print("\n=== Matriks Perbandingan Kriteria ===")
        print(self.criteria_matrix)

        print("\n=== Bobot Kriteria ===")
        for i, crit in enumerate(self.criteria):
            print(f"{crit}: {self.criteria_weights[i]:.4f}")

        print("\n=== Bobot Alternatif per Kriteria ===")
        for crit, weights in self.alternative_weights.items():
            print(f"\nKriteria: {crit}")
            for i, alt in enumerate(self.alternatives):
                print(f"{alt}: {weights[i]:.4f}")

        print("\n=== Ranking Akhir Alternatif ===")
        for i, alt in enumerate(self.alternatives):
            print(f"{alt}: {self.final_ranking[i]:.4f}")


def parse_input(prompt):
    """
    Memproses input pengguna. Mendukung input angka biasa atau pecahan (contoh: 1/3).
    Args:
        prompt (str): Teks untuk meminta input pengguna.
    Returns:
        float: Nilai yang diinput pengguna dalam bentuk desimal.
    """
    user_input = input(prompt)
    try:
        if '/' in user_input:
            numerator, denominator = map(float, user_input.split('/'))
            return numerator / denominator
        else:
            return float(user_input)
    except Exception:
        raise ValueError("Input tidak valid. Harap masukkan angka atau pecahan seperti 1/3.")


# Main Program
def main():
    """
    Program utama untuk menjalankan AHP.
    1. Meminta input kriteria dan alternatif.
    2. Meminta input perbandingan kriteria dan alternatif.
    3. Menghitung bobot dan ranking akhir.
    4. Menampilkan hasil.
    """
    ahp = AHP()
    ahp.add_criteria()  # Meminta input kriteria
    ahp.add_alternatives()  # Meminta input alternatif
    ahp.input_comparisons_criteria()  # Input perbandingan untuk kriteria
    ahp.input_comparisons_alternatives()  # Input perbandingan untuk alternatif
    ahp.calculate_weights()  # Menghitung bobot
    ahp.display_results()  # Menampilkan hasil

if __name__ == "__main__":
    main()