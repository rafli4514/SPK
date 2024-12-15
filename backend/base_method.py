class BaseMethod:
    def __init__(self, criteria, alternatives):
        """
        Inisialisasi kelas dasar untuk semua metode pengambilan keputusan.
        
        Args:
            criteria (list): Daftar kriteria.
            alternatives (list): Daftar alternatif.
        """
        self.criteria = criteria
        self.alternatives = alternatives
        self.steps = []  # Langkah-langkah pengerjaan untuk dokumentasi

    def log_step(self, step):
        """
        Mencatat langkah-langkah pengerjaan.
        
        Args:
            step (str): Deskripsi langkah pengerjaan.
        """
        self.steps.append(step)

    def get_steps(self):
        """
        Mengembalikan semua langkah pengerjaan.
        
        Returns:
            list: Langkah-langkah yang dicatat.
        """
        return self.steps
