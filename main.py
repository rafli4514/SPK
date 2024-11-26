from AHP import AHP

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
    ahp.add_criteria()  # Meminta input kriteriaa
    ahp.add_alternatives()  # Meminta input alternatif
    ahp.input_comparisons_criteria()  # Input perbandingan untuk kriteria
    ahp.input_comparisons_alternatives()  # Input perbandingan untuk alternatif
    ahp.calculate_weights()  # Menghitung bobot
    ahp.display_results()  # Menampilkan hasil

if __name__ == "__main__":
    main()