from AHP import AHP
from SAW import SAW

# Menampilkan menu utama
def display_main_menu():
    """
    Menampilkan menu utama untuk memilih metode AHP atau SAW.
    """
    print("\n=== Menu Utama ===")
    print("1. Pilih AHP (Analytic Hierarchy Process)")
    print("2. Pilih SAW (Simple Additive Weighting)")
    print("3. Keluar")

# Main Program untuk AHP
def run_ahp():
    """
    Fungsi untuk menjalankan proses AHP.
    """
    print("\n=== Menjalankan AHP ===")
    ahp = AHP()

    ahp.add_criteria()  # Menambah kriteria
    print("\n")
    ahp.add_alternatives()  # Menambah alternatif
    print("\n")
    ahp.input_comparisons_criteria()  # Input perbandingan untuk kriteria
    print("\n")
    ahp.input_comparisons_alternatives()  # Input perbandingan untuk alternatif
    print("\n")
    ahp.calculate_weights()  # Menghitung bobot dan ranking akhir
    print("\n")
    ahp.display_results()  # Menampilkan hasil

# Main Program untuk SAW
def run_saw():
    """
    Fungsi untuk menjalankan proses SAW.
    """
    print("\n=== Menjalankan SAW ===")
    saw = SAW()

    saw.add_criteria_benefit()  # Menambah kriteria benefit
    print("\n")
    saw.add_criteria_cost()  # Menambah kriteria cost
    print("\n")
    saw.add_weight_benefit()  # Menambah bobot kriteria benefit
    print("\n")
    saw.add_weight_cost()  # Menambah bobot kriteria cost
    print("\n")
    saw.add_alternatif()  # Menambahkan alternatif
    print("\n")
    saw.add_matrices()  # Memasukkan matriks benefit dan cost
    ranked_alternatives, scores = saw.rank_alternative()  # Menghitung skor dan ranking alternatif

    print("\n=== Ranking Alternatif ===")
    for i, alt in enumerate(ranked_alternatives):
        print(f"{alt}: {scores[i]:.4f}")

# Program utama
def main():
    while True:
        display_main_menu()  # Menampilkan menu utama
        choice = input("Pilih menu (1-3): ")

        if choice == '1':
            run_ahp()  # Menjalankan AHP
        elif choice == '2':
            run_saw()  # Menjalankan SAW
        elif choice == '3':
            print("Terima kasih! Program selesai.")
            break  # Keluar dari program
        else:
            print("Pilihan tidak valid. Silakan pilih antara 1 hingga 3.")

if __name__ == "__main__":
    main()
