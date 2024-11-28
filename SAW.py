import numpy as np

class SAW:
    def __init__(self):
        """
        Inisialisasi objek SAW tanpa kriteria dan alternatif awal.
        """
        self.criteria_benefit = []  # Daftar kriteria benefit
        self.criteria_cost = []  # Daftar kriteria cost
        self.weight_benefit = []  # Daftar bobot benefit
        self.weight_cost = []  # Daftar bobot cost
        self.alternatives = []  # Daftar alternatif yang dievaluasi
        self.matrix_benefit = None  # Matriks perbandingan untuk benefit
        self.matrix_cost = None  # Matriks perbandingan untuk cost
        
    def add_criteria_benefit(self):
        """
        Meminta pengguna untuk memasukkan kriteria benefit ke dalam SAW.
        """
        print("=== Tambahkan Kriteria Benefit ===")
        while(True):
            criteria_name = input("Masukkan nama kriteria (atau ketik 'selesai' untuk mengakhiri): ")
            if criteria_name.lower() == 'selesai':
                break
            self.criteria_benefit.append(criteria_name)
    
    def add_criteria_cost(self):
        """
        Meminta pengguna untuk memasukkan kriteria cost ke dalam SAW.
        """
        print("=== Tambahkan Kriteria Cost ===")
        while(True):
            criteria_name = input("Masukkan nama kriteria (atau ketik 'selesai' untuk mengakhiri): ")
            if criteria_name.lower() == 'selesai':
                 break
            self.criteria_cost.append(criteria_name)
        
    def add_weight_benefit(self):
        """
        Meminta pengguna untuk memasukkan bobot benefit ke dalam SAW.
        """
        print("=== Tambahkan Bobot Benefit ===")
        for i, criteria in enumerate(self.criteria_benefit):
            try:
                weight = float(input(f"Masukkan bobot untuk kriteria {criteria}: "))
                self.weight_benefit.append(weight)
            except ValueError:
                print("Bobot harus berupa angka")

    def add_weight_cost(self):
        """
        Meminta pengguna untuk memasukkan bobot cost ke dalam SAW.
        """
        print("=== Tambahkan Bobot Cost ===")
        for i, criteria in enumerate(self.criteria_cost):
            try:
                weight = float(input(f"Masukkan bobot untuk kriteria {criteria}: "))
                self.weight_cost.append(weight)
            except ValueError:
                print("Bobot harus berupa angka")
                
    def add_alternatif(self):
        """
        Meminta pengguna untuk memasukkan alternatif ke dalam SAW.
        """
        print("=== Tambahkan Alternatif ===")
        while(True):
            alternative_name = input("Masukkan nama alternatif (atau ketik 'selesai' untuk mengakhiri): ")
            if alternative_name.lower() == 'selesai':
                 break
            self.alternatives.append(alternative_name)
    
    def add_matrices(self):
        """
        Membuat matriks untuk kriteria benefit dan cost.
        """
        lenght_alternative = len(self.alternatives)
        self.matrix_benefit = np.zeros((lenght_alternative, len(self.criteria_benefit)))
        self.matrix_cost = np.zeros((lenght_alternative, len(self.criteria_cost)))
        
        print("\n=== Masukkan nilai untuk Matriks Benefit ===")
        for i, alternative in enumerate(self.alternatives):
            for j, criteria in enumerate(self.criteria_benefit):
                while(True):
                    try:
                        value = float(input(f"Masukkan nilai untuk alternatif '{alternative}' pada kriteria '{criteria}': "))
                        self.matrix_benefit[i][j] = value
                        break
                    except ValueError:
                        print("Nilai harus berupa angka")
        
        print("\n=== Masukkan nilai untuk Matriks Cost ===")
        for i, alternative in enumerate(self.alternatives):
            for j, criteria in enumerate(self.criteria_cost):
                while(True):
                    try:
                        value = float(input(f"Masukkan nilai untuk alternatif '{alternative}' pada kriteria '{criteria}': "))
                        self.matrix_cost[i][j] = value
                        break
                    except ValueError:
                        print("Nilai harus berupa angka")
        
    def normalization(self):
        """
        Normalisasi matriks kriteria benefit dan cost.
        """
        # Normalisasi Benefit (max normalization)
        normal_benefit = self.matrix_benefit / self.matrix_benefit.max(axis=0)
        
        # Normalisasi Cost (min normalization)
        normal_cost =  self.matrix_cost.min(axis=0) / self.matrix_cost
        
        return normal_benefit, normal_cost
    
    def calculate_score(self):
        """
        Hitung skor total untuk setiap alternatif dengan bobot.
        """
        # Normalisasi matriks
        normal_benefit, normal_cost = self.normalization()
        scores = np.zeros(len(self.alternatives))
        
        for i in range(len(self.alternatives)):
            # Menghitung skor dari alternatif dengan bobot benefit dan cost yang sudah dinormalisasi
            score_benefit = np.dot(normal_benefit[i], self.weight_benefit)
            score_cost = np.dot(normal_cost[i], self.weight_cost)
            scores[i] = score_benefit + score_cost
        
        return scores
        
    def rank_alternative(self):
        """
        Menentukan peringkat alternatif berdasarkan skor tertinggi.
        """
        scores = self.calculate_score()
        ranked_indices = np.argsort(scores)[::-1]  # Urutkan skor dari yang tertinggi
        ranked_alternatives = [self.alternatives[i] for i in ranked_indices]
        return ranked_alternatives, scores
    
    def display(self):
        """
        Fungsi untuk menampilkan hasil SAW.
        Menampilkan Matriks Benefit, Matriks Cost, dan Ranking Alternatif berdasarkan skor.
        """
        print("\n=== Hasil SAW ===")
        
        # Matriks Benefit
        print("\nMatriks Benefit: ")
        print(self.matrix_benefit)

        # Matriks Cost
        print("\nMatriks Cost: ")
        print(self.matrix_cost)

        # Ranking Alternatif berdasarkan skor
        print("\nRanking Alternatif Berdasarkan Skor: ")
        ranked_alternatives, scores = self.rank_alternative()
        
        for i, alt in enumerate(ranked_alternatives):
            print(f"Ranking {i + 1}: {alt} (Skor: {scores[i]:.4f})")
