# methods/base_method.py

class BaseMethod:
    def __init__(self, criteria, alternatives):
        self.criteria = criteria
        self.alternatives = alternatives

    def input_data(self):
        """
        Mengatur tampilan untuk memasukkan data spesifik metode.
        """
        raise NotImplementedError

    def process(self):
        """
        Melakukan perhitungan spesifik metode.
        """
        raise NotImplementedError

    def get_results(self):
        """
        Mengembalikan hasil perhitungan.
        """
        raise NotImplementedError
