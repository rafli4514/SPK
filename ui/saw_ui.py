# ui/saw_ui.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from methods.saw import SAW
import pandas as pd
# from utils.tooltip import ToolTip  # Jika Anda menggunakan tooltip

class SAWFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        """
        Inisialisasi frame SAW.

        Args:
            parent (tk.Widget): Parent widget.
            **kwargs: Argument tambahan untuk Frame.
        """
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.saw = None  # Instance dari kelas SAW

        # Langkah pertama: Input Kriteria dan Alternatif
        self.setup_input_frame()

    def setup_input_frame(self):
        """
        Mengatur tampilan awal untuk memasukkan kriteria dan alternatif.
        """
        # Menghapus semua widget yang ada di frame saat ini
        for widget in self.winfo_children():
            widget.destroy()

        # Judul tampilan
        title = ttk.Label(self, text="Input Kriteria dan Alternatif (SAW)", font=("Helvetica", 16))
        title.pack(pady=10)

        # Frame untuk input kriteria dan alternatif
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10, fill=tk.X)

        # Label dan Entry untuk Kriteria
        criteria_label = ttk.Label(input_frame, text="Kriteria:")
        criteria_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.criteria_entry = ttk.Entry(input_frame, width=30)
        self.criteria_entry.grid(row=0, column=1, pady=5, padx=5)

        # Combobox untuk memilih tipe kriteria (Benefit/Cost)
        self.criteria_type = ttk.Combobox(input_frame, values=["Benefit", "Cost"], state="readonly", width=10)
        self.criteria_type.grid(row=0, column=2, pady=5, padx=5)
        self.criteria_type.current(0)

        # Tombol untuk menambahkan kriteria
        add_criteria_btn = ttk.Button(input_frame, text="Tambah Kriteria", command=self.add_criteria)
        add_criteria_btn.grid(row=0, column=3, padx=5, pady=5)

        # Listbox untuk menampilkan daftar kriteria
        self.criteria_listbox = tk.Listbox(input_frame, height=5, width=60)
        self.criteria_listbox.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.E, pady=5)

        # Binding tombol "Enter" pada Entry Kriteria untuk menambahkan kriteria
        self.criteria_entry.bind("<Return>", self.add_criteria_event)

        # Label dan Entry untuk Alternatif
        alternative_label = ttk.Label(input_frame, text="Alternatif:")
        alternative_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        self.alternative_entry = ttk.Entry(input_frame, width=30)
        self.alternative_entry.grid(row=2, column=1, pady=5, padx=5)

        # Tombol untuk menambahkan alternatif
        add_alternative_btn = ttk.Button(input_frame, text="Tambah Alternatif", command=self.add_alternative)
        add_alternative_btn.grid(row=2, column=2, padx=5, pady=5)

        # Listbox untuk menampilkan daftar alternatif
        self.alternative_listbox = tk.Listbox(input_frame, height=5, width=60)
        self.alternative_listbox.grid(row=3, column=0, columnspan=4, sticky=tk.W+tk.E, pady=5)

        # Binding tombol "Enter" pada Entry Alternatif untuk menambahkan alternatif
        self.alternative_entry.bind("<Return>", self.add_alternative_event)

        # Tombol untuk melanjutkan ke tahap input bobot kriteria
        proceed_btn = ttk.Button(self, text="Lanjut", command=self.saw_input_stage)
        proceed_btn.pack(pady=10)

    def add_criteria(self, event=None):
        """
        Menambahkan kriteria ke dalam listbox jika valid.

        Args:
            event: Event yang memicu fungsi ini (opsional).
        """
        criteria = self.criteria_entry.get().strip()  # Mengambil input kriteria
        type_ = self.criteria_type.get()  # Mengambil tipe kriteria
        if criteria and not self.is_duplicate_criteria(criteria):
            self.criteria_listbox.insert(tk.END, f"{criteria} ({type_})")  # Menambahkan kriteria ke listbox
            self.criteria_entry.delete(0, tk.END)  # Mengosongkan entry
        else:
            messagebox.showwarning("Peringatan", "Kriteria tidak boleh kosong atau sudah ada.")

    def is_duplicate_criteria(self, criteria):
        """
        Memeriksa apakah kriteria sudah ada dalam listbox.

        Args:
            criteria (str): Nama kriteria yang akan diperiksa.

        Returns:
            bool: True jika duplikat, False jika tidak.
        """
        existing = self.criteria_listbox.get(0, tk.END)
        for item in existing:
            name, _ = item.rsplit(" (", 1)
            if name.strip().lower() == criteria.lower():
                return True
        return False

    def add_criteria_event(self, event):
        """
        Event handler untuk tombol "Enter" pada Entry Kriteria.

        Args:
            event: Event yang memicu fungsi ini.
        """
        self.add_criteria()

    def add_alternative(self, event=None):
        """
        Menambahkan alternatif ke dalam listbox jika valid.

        Args:
            event: Event yang memicu fungsi ini (opsional).
        """
        alternative = self.alternative_entry.get().strip()  # Mengambil input alternatif
        if alternative and alternative not in self.alternative_listbox.get(0, tk.END):
            self.alternative_listbox.insert(tk.END, alternative)  # Menambahkan alternatif ke listbox
            self.alternative_entry.delete(0, tk.END)  # Mengosongkan entry
        else:
            messagebox.showwarning("Peringatan", "Alternatif tidak boleh kosong atau sudah ada.")

    def add_alternative_event(self, event):
        """
        Event handler untuk tombol "Enter" pada Entry Alternatif.

        Args:
            event: Event yang memicu fungsi ini.
        """
        self.add_alternative()

    def saw_input_stage(self):
        """
        Memeriksa validitas input dan menginisialisasi proses SAW.
        """
        criteria_raw = self.criteria_listbox.get(0, tk.END)
        alternatives = self.alternative_listbox.get(0, tk.END)

        # Validasi jumlah kriteria dan alternatif
        if len(criteria_raw) < 2:
            messagebox.showerror("Error", "Dibutuhkan minimal dua kriteria.")
            return
        if len(alternatives) < 2:
            messagebox.showerror("Error", "Dibutuhkan minimal dua alternatif.")
            return

        # Memisahkan kriteria berdasarkan tipe (Benefit/Cost)
        criteria_benefit = []
        criteria_cost = []
        for item in criteria_raw:
            name, type_ = item.rsplit(" (", 1)
            type_ = type_.rstrip(")")
            if type_ == "Benefit":
                criteria_benefit.append(name.strip())
            else:
                criteria_cost.append(name.strip())

        if not criteria_benefit and not criteria_cost:
            messagebox.showerror("Error", "Harus ada minimal satu kriteria Benefit atau Cost.")
            return

        # Inisialisasi instance SAW dengan kriteria dan alternatif yang dimasukkan
        self.saw = SAW()
        self.saw.set_criteria(criteria_benefit, criteria_cost)
        self.saw.set_alternatives(list(alternatives))

        # Lanjut ke tahap input bobot kriteria
        self.input_criteria_weights()

    def input_criteria_weights(self):
        """
        Mengatur tampilan untuk memasukkan bobot kriteria.
        """
        # Menghapus semua widget yang ada di frame saat ini
        for widget in self.winfo_children():
            widget.destroy()

        # Judul tampilan
        title = ttk.Label(self, text="Input Bobot Kriteria (SAW)", font=("Helvetica", 16))
        title.pack(pady=10)

        # Instruksi untuk pengguna
        instructions = ttk.Label(self, text="Masukkan bobot untuk setiap kriteria sebagai angka bulat (misal: 3)")
        instructions.pack(pady=5)

        # Frame untuk bobot kriteria
        weights_frame = ttk.Frame(self)
        weights_frame.pack(pady=10, padx=10)

        self.weight_entries = {}  # Dictionary untuk menyimpan entry bobot

        for idx, crit in enumerate(self.saw.criteria_benefit + self.saw.criteria_cost):
            label = ttk.Label(weights_frame, text=f"{crit}:")
            label.grid(row=idx, column=0, sticky=tk.W, pady=5, padx=5)

            entry = ttk.Entry(weights_frame, width=10)
            entry.grid(row=idx, column=1, pady=5, padx=5)
            self.weight_entries[crit] = entry

            # Menambahkan tooltip pada setiap entry bobot (opsional)
            # ToolTip(entry, "Masukkan bobot sebagai angka bulat, misal: 3")

        # Tombol untuk submit bobot kriteria
        submit_btn = ttk.Button(self, text="Submit", command=self.submit_criteria_weights)
        submit_btn.pack(pady=10)

    def submit_criteria_weights(self):
        """
        Mengumpulkan dan memproses bobot kriteria.
        """
        try:
            weights = {}
            for crit, entry in self.weight_entries.items():
                weight_str = entry.get().strip()
                if not weight_str:
                    raise ValueError(f"Bobot untuk kriteria '{crit}' tidak boleh kosong.")
                # Memeriksa apakah input adalah angka bulat
                if not weight_str.isdigit():
                    raise ValueError(f"Bobot untuk kriteria '{crit}' harus berupa angka bulat.")
                weight = int(weight_str)
                if weight <= 0:
                    raise ValueError(f"Bobot untuk kriteria '{crit}' harus positif.")
                weights[crit] = weight

            # Memisahkan bobot berdasarkan tipe kriteria
            weight_benefit = []
            weight_cost = []
            for crit in self.saw.criteria_benefit:
                weight_benefit.append(weights[crit])
            for crit in self.saw.criteria_cost:
                weight_cost.append(weights[crit])

            # Menetapkan bobot kriteria dalam SAW
            self.saw.set_weights(weight_benefit, weight_cost)

            # Lanjut ke tahap input nilai alternatif
            self.input_alternative_scores()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def input_alternative_scores(self):
        """
        Mengatur tampilan untuk memasukkan nilai alternatif untuk setiap kriteria.
        """
        # Menghapus semua widget yang ada di frame saat ini
        for widget in self.winfo_children():
            widget.destroy()

        # Judul tampilan
        title = ttk.Label(self, text="Input Nilai Alternatif (SAW)", font=("Helvetica", 16))
        title.pack(pady=10)

        # Instruksi untuk pengguna
        instructions = ttk.Label(self, text="Masukkan nilai untuk setiap alternatif berdasarkan setiap kriteria (misal: 80)")
        instructions.pack(pady=5)

        # Notebook untuk setiap kriteria agar input nilai alternatif dapat dilakukan per kriteria
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, fill=tk.BOTH, expand=True)

        self.alternative_score_entries = {}  # Dictionary untuk menyimpan entry nilai alternatif

        for crit in self.saw.criteria_benefit + self.saw.criteria_cost:
            # Membuat frame untuk setiap kriteria
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=crit)

            comparison_frame = ttk.Frame(frame)
            comparison_frame.pack(pady=10, padx=10)

            entries = {}

            for idx, alt in enumerate(self.saw.alternatives):
                label = ttk.Label(comparison_frame, text=f"{alt}:")
                label.grid(row=idx, column=0, sticky=tk.W, pady=5, padx=5)

                entry = ttk.Entry(comparison_frame, width=20)
                entry.grid(row=idx, column=1, pady=5, padx=5)
                entries[alt] = entry

                # Menambahkan tooltip pada setiap entry nilai alternatif (opsional)
                # ToolTip(entry, "Masukkan nilai sebagai angka bulat, misal: 80")

            self.alternative_score_entries[crit] = entries  # Menyimpan entry nilai alternatif untuk setiap kriteria

        # Tombol untuk submit nilai alternatif
        submit_btn = ttk.Button(self, text="Submit", command=self.submit_alternative_scores)
        submit_btn.pack(pady=10)

    def submit_alternative_scores(self):
        """
        Mengumpulkan dan memproses nilai alternatif untuk setiap kriteria.
        """
        try:
            # Mengumpulkan nilai alternatif untuk setiap kriteria
            for crit, entries in self.alternative_score_entries.items():
                scores = {}
                for alt, entry in entries.items():
                    score_str = entry.get().strip()
                    if not score_str:
                        raise ValueError(f"Nilai untuk alternatif '{alt}' pada kriteria '{crit}' tidak boleh kosong.")
                    if not self.is_valid_number(score_str):
                        raise ValueError(f"Nilai untuk alternatif '{alt}' pada kriteria '{crit}' harus berupa angka.")
                    score = float(score_str)
                    if score < 0:
                        raise ValueError(f"Nilai untuk alternatif '{alt}' pada kriteria '{crit}' harus non-negatif.")
                    scores[alt] = score
                self.saw.set_alternative_scores(crit, scores)  # Menetapkan nilai alternatif untuk kriteria

            # Melakukan perhitungan SAW
            self.saw.perform_saw()
            results = self.saw.get_results()
            self.display_results(results)  # Menampilkan hasil
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def is_valid_number(self, value):
        """
        Memeriksa apakah string merupakan angka valid.

        Args:
            value (str): String yang akan diperiksa.

        Returns:
            bool: True jika valid, False jika tidak.
        """
        try:
            float(value)
            return True
        except ValueError:
            return False

    def display_results(self, results):
        """
        Menampilkan hasil perhitungan SAW dalam bentuk tabel dan langkah-langkah pengerjaan.

        Args:
            results (dict): Dictionary yang berisi hasil perhitungan SAW.
        """
        # Menghapus semua widget yang ada di frame saat ini
        for widget in self.winfo_children():
            widget.destroy()

        # Judul tampilan
        title = ttk.Label(self, text="Hasil SAW", font=("Helvetica", 16))
        title.pack(pady=10)

        # Label dan Text untuk menampilkan langkah-langkah pengerjaan
        steps_label = ttk.Label(self, text="Langkah-langkah Pengerjaan:", font=("Helvetica", 12, 'bold'))
        steps_label.pack(pady=5)

        steps_text = tk.Text(self, height=15, width=80)
        steps_text.pack(pady=5)
        steps_text.insert(tk.END, "\n".join(results['steps']))  # Menambahkan langkah-langkah ke dalam Text widget
        steps_text.config(state=tk.DISABLED)  # Membuat Text widget tidak dapat diubah

        # Label untuk hasil perhitungan
        results_label = ttk.Label(self, text="Hasil Perhitungan:", font=("Helvetica", 12, 'bold'))
        results_label.pack(pady=5)

        # Notebook untuk menampilkan berbagai hasil dalam tab terpisah
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, fill=tk.BOTH, expand=True)

        # Tab untuk Matriks Kriteria
        frame_criteria = ttk.Frame(notebook)
        notebook.add(frame_criteria, text="Matriks Kriteria")

        # Menambahkan label penjelasan
        criteria_label = ttk.Label(
            frame_criteria, 
            text="Matriks Kriteria:\nBaris adalah Alternatif dan Kolom adalah Kriteria", 
            font=("Helvetica", 12, 'bold')
        )
        criteria_label.pack(pady=5)

        # Mengubah matriks kriteria menjadi DataFrame tanpa transpose
        df_criteria = pd.DataFrame(results['criteria_matrix'])
        df_criteria.index = self.saw.alternatives
        df_criteria.reset_index(inplace=True)
        df_criteria.rename(columns={'index': 'Alternatif'}, inplace=True)
        df_criteria.columns = ['Alternatif'] + self.saw.criteria_benefit + self.saw.criteria_cost

        # Debugging: Cetak jumlah kolom
        print(f"Jumlah kolom dalam DataFrame Matriks Kriteria: {len(df_criteria.columns)}")
        print(f"Jumlah kriteria: {len(self.saw.criteria_benefit) + len(self.saw.criteria_cost)}")

        # Pengecekan jumlah kolom
        expected_columns = ['Alternatif'] + self.saw.criteria_benefit + self.saw.criteria_cost
        actual_columns = df_criteria.columns.tolist()

        if len(actual_columns) != len(expected_columns):
            messagebox.showerror("Error", f"Jumlah kolom DataFrame Matriks Kriteria ({len(actual_columns)}) tidak sesuai dengan jumlah kriteria ({len(expected_columns)}).")
            return

        # Membuat Treeview untuk Matriks Kriteria
        tree_criteria = self.create_treeview(frame_criteria, df_criteria)
        tree_criteria.pack(fill=tk.BOTH, expand=True)

        # Tab untuk Bobot Kriteria
        frame_weights = ttk.Frame(notebook)
        notebook.add(frame_weights, text="Bobot Kriteria")

        df_weights = pd.DataFrame({
            'Kriteria': self.saw.criteria_benefit + self.saw.criteria_cost,
            'Bobot': results['criteria_weights']
        })
        tree_weights = self.create_treeview(frame_weights, df_weights)
        tree_weights.pack(fill=tk.BOTH, expand=True)

        # Tab untuk Normalisasi Matriks
        frame_normalization = ttk.Frame(notebook)
        notebook.add(frame_normalization, text="Normalisasi Matriks")

        # Menambahkan label penjelasan
        normalization_label = ttk.Label(
            frame_normalization, 
            text="Normalisasi Matriks dan Faktor Normalisasi untuk Setiap Kriteria", 
            font=("Helvetica", 12, 'bold')
        )
        normalization_label.pack(pady=5)

        # Notebook untuk sub-tab Normalisasi dan Faktor Normalisasi
        normalization_notebook = ttk.Notebook(frame_normalization)
        normalization_notebook.pack(pady=10, fill=tk.BOTH, expand=True)

        # Sub-Tab untuk Faktor Normalisasi
        frame_norm_factors = ttk.Frame(normalization_notebook)
        normalization_notebook.add(frame_norm_factors, text='Faktor Normalisasi')

        # Membuat DataFrame untuk faktor normalisasi
        df_norm_factors = pd.DataFrame(list(results['normalization_factors'].items()), columns=['Kriteria', 'Faktor Normalisasi'])

        # Membuat Treeview untuk Faktor Normalisasi
        tree_norm_factors = self.create_treeview_single_column(frame_norm_factors, df_norm_factors)
        tree_norm_factors.pack(fill=tk.BOTH, expand=True)

        # Sub-Tab untuk Normalisasi Alternatif
        frame_norm_alternatives = ttk.Frame(normalization_notebook)
        normalization_notebook.add(frame_norm_alternatives, text='Normalisasi Alternatif')

        # Membuat DataFrame untuk normalisasi alternatif
        df_norm_alternatives = pd.DataFrame(results['normalized_matrix'])
        df_norm_alternatives.index = self.saw.alternatives
        df_norm_alternatives.reset_index(inplace=True)
        df_norm_alternatives.rename(columns={'index': 'Alternatif'}, inplace=True)
        df_norm_alternatives.columns = ['Alternatif'] + self.saw.criteria_benefit + self.saw.criteria_cost

        # Membuat Treeview untuk Normalisasi Alternatif
        tree_norm_alternatives = self.create_treeview(frame_norm_alternatives, df_norm_alternatives)
        tree_norm_alternatives.pack(fill=tk.BOTH, expand=True)

        # Sub-Tab untuk Normalisasi per Kriteria dengan Label
        for crit in self.saw.criteria_benefit + self.saw.criteria_cost:
            frame_norm_matrix = ttk.Frame(normalization_notebook)
            normalization_notebook.add(frame_norm_matrix, text=f'Normalisasi {crit}')

            # Menambahkan label untuk Kriteria
            label_crit = ttk.Label(frame_norm_matrix, text=f'Normalisasi untuk Kriteria: {crit}', font=("Helvetica", 12, 'bold'))
            label_crit.pack(pady=5)

            # Mengambil matriks normalisasi untuk kriteria tersebut
            norm_values = results['normalized_matrix'].get(crit, {})
            if not norm_values:
                norm_values = {alt: 0 for alt in self.saw.alternatives}  # Jika tidak ada nilai, set 0

            df_norm_matrix = pd.DataFrame(list(norm_values.items()), columns=['Alternatif', 'Nilai Normalisasi'])

            # Membuat Treeview untuk Matriks Normalisasi
            tree_norm_matrix = self.create_treeview_single_column(frame_norm_matrix, df_norm_matrix)
            tree_norm_matrix.pack(fill=tk.BOTH, expand=True)

        # Tab untuk Final Ranking
        frame_final = ttk.Frame(notebook)
        notebook.add(frame_final, text='Final Ranking')

        df_final = pd.DataFrame({
            'Alternatif': list(results['final_ranking'].keys()),
            'Skor Akhir': list(results['final_ranking'].values())
        }).sort_values(by='Skor Akhir', ascending=False)

        tree_final = self.create_treeview(frame_final, df_final)
        tree_final.pack(fill=tk.BOTH, expand=True)

        # Tombol untuk mengekspor hasil ke file Excel
        export_btn = ttk.Button(self, text="Ekspor ke Excel", command=self.export_to_excel)
        export_btn.pack(pady=10)

    def create_treeview(self, parent, dataframe):
        """
        Membuat widget Treeview dari DataFrame pandas.

        Args:
            parent (tk.Widget): Parent widget untuk Treeview.
            dataframe (pd.DataFrame): DataFrame yang akan ditampilkan.

        Returns:
            ttk.Treeview: Treeview yang telah dibuat.
        """
        tree = ttk.Treeview(parent, columns=list(dataframe.columns), show='headings')

        # Mendefinisikan setiap kolom berdasarkan nama kolom DataFrame
        for col in dataframe.columns:
            tree.heading(col, text=col)
            # Atur lebar kolom agar cukup menampilkan semua data
            tree.column(col, anchor=tk.CENTER, width=150)

        # Menambahkan data ke dalam Treeview
        for index, row in dataframe.iterrows():
            tree.insert("", tk.END, values=list(row))

        # Menambahkan scrollbar vertikal
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return tree

    def create_treeview_single_column(self, parent, dataframe):
        """
        Membuat widget Treeview dari DataFrame pandas dengan dua kolom: Alternatif dan Nilai Normalisasi.

        Args:
            parent (tk.Widget): Parent widget untuk Treeview.
            dataframe (pd.DataFrame): DataFrame yang akan ditampilkan.

        Returns:
            ttk.Treeview: Treeview yang telah dibuat.
        """
        tree = ttk.Treeview(parent, columns=list(dataframe.columns), show='headings')

        # Mendefinisikan setiap kolom berdasarkan nama kolom DataFrame
        for col in dataframe.columns:
            tree.heading(col, text=col)
            # Atur lebar kolom agar cukup menampilkan nama Alternatif dan Nilai Normalisasi
            if col == 'Alternatif':
                tree.column(col, anchor=tk.CENTER, width=150)  # Diubah dari tk.W ke tk.CENTER
            else:
                tree.column(col, anchor=tk.CENTER, width=150)

        # Menambahkan data ke dalam Treeview
        for index, row in dataframe.iterrows():
            tree.insert("", tk.END, values=list(row))

        # Menambahkan scrollbar vertikal
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return tree

    def export_to_excel(self):
        """
        Mengekspor hasil SAW ke dalam file Excel dengan struktur sheet yang terorganisir.
        """
        # Membuka dialog untuk memilih lokasi penyimpanan file Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            try:
                # Membuat ExcelWriter dengan engine 'openpyxl'
                writer = pd.ExcelWriter(file_path, engine='openpyxl')

                # Mengambil hasil dari perhitungan SAW
                results = self.saw.get_results()

                # Menulis Matriks Kriteria ke sheet 'Matriks Kriteria'
                df_criteria = pd.DataFrame(results['criteria_matrix'])
                df_criteria.index = self.saw.alternatives
                df_criteria.reset_index(inplace=True)
                df_criteria.rename(columns={'index': 'Alternatif'}, inplace=True)
                df_criteria.columns = ['Alternatif'] + self.saw.criteria_benefit + self.saw.criteria_cost
                df_criteria.to_excel(writer, sheet_name='Matriks Kriteria', index=False)

                # Menulis Bobot Kriteria ke sheet 'Bobot Kriteria'
                df_weights = pd.DataFrame({
                    'Kriteria': self.saw.criteria_benefit + self.saw.criteria_cost,
                    'Bobot': results['criteria_weights']
                })
                df_weights.to_excel(writer, sheet_name='Bobot Kriteria', index=False)

                # Menulis Matriks Normalisasi Alternatif ke sheet 'Normalisasi Alternatif'
                df_norm_alternatives = pd.DataFrame(results['normalized_matrix'])
                df_norm_alternatives.index = self.saw.alternatives
                df_norm_alternatives.reset_index(inplace=True)
                df_norm_alternatives.rename(columns={'index': 'Alternatif'}, inplace=True)
                df_norm_alternatives.columns = ['Alternatif'] + self.saw.criteria_benefit + self.saw.criteria_cost
                df_norm_alternatives.to_excel(writer, sheet_name='Normalisasi Alternatif', index=False)

                # Menulis Matriks Normalisasi per Kriteria ke masing-masing sheet
                normalized_matrix = results['normalized_matrix']
                for crit in self.saw.criteria_benefit + self.saw.criteria_cost:
                    df_alt_matrix = pd.DataFrame(list(normalized_matrix[crit].items()), columns=['Alternatif', 'Nilai Normalisasi'])
                    df_alt_matrix.to_excel(writer, sheet_name=f'Normalisasi {crit}', index=False)

                # Menulis Faktor Normalisasi ke sheet 'Faktor Normalisasi'
                df_norm_factors = pd.DataFrame(list(results['normalization_factors'].items()), columns=['Kriteria', 'Faktor Normalisasi'])
                df_norm_factors.to_excel(writer, sheet_name='Faktor Normalisasi', index=False)

                # Menulis Final Ranking ke sheet 'Final Ranking'
                final_ranking = results['final_ranking']
                df_final = pd.DataFrame({
                    'Alternatif': list(final_ranking.keys()),
                    'Skor Akhir': list(final_ranking.values())
                }).sort_values(by='Skor Akhir', ascending=False)
                df_final.to_excel(writer, sheet_name='Final Ranking', index=False)

                # Menulis Langkah-langkah Pengerjaan ke sheet 'Langkah Pengerjaan'
                df_steps = pd.DataFrame({'Steps': self.saw.steps})
                df_steps.to_excel(writer, sheet_name='Langkah Pengerjaan', index=False)

                # Menyimpan file Excel
                writer.save()
                messagebox.showinfo("Success", f"Hasil berhasil diekspor ke {file_path}")
            except Exception as e:
                # Menampilkan pesan error jika terjadi kegagalan saat ekspor
                messagebox.showerror("Error", f"Gagal mengekspor ke Excel.\n{e}")
