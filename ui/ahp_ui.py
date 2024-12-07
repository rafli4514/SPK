# ui/ahp_ui.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from methods.ahp import AHP
import pandas as pd

class AHPFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        """
        Inisialisasi frame AHP.
        
        Args:
            parent (tk.Widget): Parent widget.
            **kwargs: Argument tambahan untuk Frame.
        """
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.ahp = None  # Instance dari kelas AHP
        
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
        title = ttk.Label(self, text="Input Kriteria dan Alternatif (AHP)", font=("Helvetica", 16))
        title.pack(pady=10)
        
        # Frame untuk input kriteria dan alternatif
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10, fill=tk.X)
        
        # Label dan Entry untuk Kriteria
        criteria_label = ttk.Label(input_frame, text="Kriteria:")
        criteria_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.criteria_entry = ttk.Entry(input_frame, width=50)
        self.criteria_entry.grid(row=0, column=1, pady=5)
        
        # Tombol untuk menambahkan kriteria
        add_criteria_btn = ttk.Button(input_frame, text="Tambah Kriteria", command=self.add_criteria)
        add_criteria_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Listbox untuk menampilkan daftar kriteria
        self.criteria_listbox = tk.Listbox(input_frame, height=5)
        self.criteria_listbox.grid(row=1, column=0, columnspan=3, sticky=tk.W+tk.E, pady=5)
        
        # Binding tombol "Enter" pada Entry Kriteria untuk menambahkan kriteria
        self.criteria_entry.bind("<Return>", self.add_criteria_event)
        
        # Label dan Entry untuk Alternatif
        alternative_label = ttk.Label(input_frame, text="Alternatif:")
        alternative_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.alternative_entry = ttk.Entry(input_frame, width=50)
        self.alternative_entry.grid(row=2, column=1, pady=5)
        
        # Tombol untuk menambahkan alternatif
        add_alternative_btn = ttk.Button(input_frame, text="Tambah Alternatif", command=self.add_alternative)
        add_alternative_btn.grid(row=2, column=2, padx=5, pady=5)
        
        # Listbox untuk menampilkan daftar alternatif
        self.alternative_listbox = tk.Listbox(input_frame, height=5)
        self.alternative_listbox.grid(row=3, column=0, columnspan=3, sticky=tk.W+tk.E, pady=5)
        
        # Binding tombol "Enter" pada Entry Alternatif untuk menambahkan alternatif
        self.alternative_entry.bind("<Return>", self.add_alternative_event)
        
        # Tombol untuk melanjutkan ke tahap perbandingan berpasangan
        proceed_btn = ttk.Button(self, text="Lanjut", command=self.ahp_input_stage)
        proceed_btn.pack(pady=10)
    
    def add_criteria(self, event=None):
        """
        Menambahkan kriteria ke dalam listbox jika valid.
        
        Args:
            event: Event yang memicu fungsi ini (opsional).
        """
        criteria = self.criteria_entry.get().strip()  # Mengambil input kriteria
        if criteria and criteria not in self.criteria_listbox.get(0, tk.END):
            self.criteria_listbox.insert(tk.END, criteria)  # Menambahkan kriteria ke listbox
            self.criteria_entry.delete(0, tk.END)  # Mengosongkan entry
        else:
            messagebox.showwarning("Peringatan", "Kriteria tidak boleh kosong atau sudah ada.")
    
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
    
    def ahp_input_stage(self):
        """
        Memeriksa validitas input dan menginisialisasi proses AHP.
        """
        criteria = self.criteria_listbox.get(0, tk.END)
        alternatives = self.alternative_listbox.get(0, tk.END)
        
        # Validasi jumlah kriteria dan alternatif
        if len(criteria) < 2:
            messagebox.showerror("Error", "Dibutuhkan minimal dua kriteria.")
            return
        if len(alternatives) < 2:
            messagebox.showerror("Error", "Dibutuhkan minimal dua alternatif.")
            return
        
        # Inisialisasi instance AHP dengan kriteria dan alternatif yang dimasukkan
        self.ahp = AHP(list(criteria), list(alternatives))
        
        # Lanjut ke tahap input perbandingan kriteria
        self.input_criteria_comparisons()
    
    def input_criteria_comparisons(self):
        """
        Mengatur tampilan untuk memasukkan perbandingan berpasangan antar kriteria.
        """
        # Menghapus semua widget yang ada di frame saat ini
        for widget in self.winfo_children():
            widget.destroy()
        
        # Judul tampilan
        title = ttk.Label(self, text="Input Perbandingan Berpasangan Kriteria (AHP)", font=("Helvetica", 16))
        title.pack(pady=10)
        
        # Tombol untuk kembali ke tahap sebelumnya
        back_btn = ttk.Button(self, text="Kembali", command=self.setup_input_frame)
        back_btn.pack(anchor='w')
        
        # Instruksi untuk pengguna
        instructions = ttk.Label(self, text="Masukkan nilai perbandingan antar kriteria (misal: 1/3 atau 3)")
        instructions.pack(pady=5)
        
        # Frame untuk perbandingan kriteria
        comparison_frame = ttk.Frame(self)
        comparison_frame.pack(pady=10)
        
        n = len(self.ahp.criteria)  # Jumlah kriteria
        self.criteria_comparison_entries = {}  # Dictionary untuk menyimpan entry perbandingan
        
        # Membuat header kolom dengan nama kriteria
        for idx, crit in enumerate(self.ahp.criteria):
            label = ttk.Label(comparison_frame, text=crit, font=('Helvetica', 10, 'bold'))
            label.grid(row=0, column=idx+1, padx=5, pady=5)
        
        # Membuat label baris dan entry untuk input perbandingan
        for i in range(n):
            # Label baris dengan nama kriteria
            row_label = ttk.Label(comparison_frame, text=self.ahp.criteria[i], font=('Helvetica', 10, 'bold'))
            row_label.grid(row=i+1, column=0, padx=5, pady=5)
            
            for j in range(n):
                if i == j:
                    # Diagonal utama selalu 1
                    label = ttk.Label(comparison_frame, text="1", width=10, anchor='center')
                    label.grid(row=i+1, column=j+1, padx=5, pady=5)
                elif j < i:
                    # Sel di bawah diagonal adalah invers dari sel di atas
                    key = (j, i)
                    if key in self.criteria_comparison_entries:
                        try:
                            value = 1 / float(self.criteria_comparison_entries[key].get())
                        except:
                            value = 1
                        label = ttk.Label(comparison_frame, text=f"{value:.3f}", width=10, anchor='center')
                    else:
                        label = ttk.Label(comparison_frame, text="1", width=10, anchor='center')
                    label.grid(row=i+1, column=j+1, padx=5, pady=5)
                else:
                    # Sel di atas diagonal utama memerlukan input dari pengguna
                    entry = ttk.Entry(comparison_frame, width=10)
                    entry.grid(row=i+1, column=j+1, padx=5, pady=5)
                    self.criteria_comparison_entries[(i, j)] = entry
        
        # Tombol untuk submit perbandingan kriteria
        submit_btn = ttk.Button(self, text="Submit", command=self.submit_criteria_comparisons)
        submit_btn.pack(pady=10)
    
    def submit_criteria_comparisons(self):
        """
        Mengumpulkan dan memproses perbandingan berpasangan antar kriteria.
        """
        comparisons = []
        try:
            for (i, j), entry in self.criteria_comparison_entries.items():
                value_str = entry.get().strip()  # Mengambil nilai dari entry
                if '/' in value_str:
                    # Jika input dalam bentuk pecahan, konversi ke float
                    numerator, denominator = map(float, value_str.split('/'))
                    if denominator == 0:
                        raise ValueError("Denominator cannot be zero.")
                    value = numerator / denominator
                else:
                    value = float(value_str)  # Konversi langsung ke float
                if value <= 0:
                    raise ValueError("Values must be positive.")  # Validasi nilai positif
                comparisons.append((i, j, value))  # Menambahkan tuple perbandingan
            self.ahp.set_criteria_comparisons(comparisons)  # Menetapkan perbandingan kriteria
            self.input_alternative_comparisons()  # Lanjut ke tahap perbandingan alternatif
        except Exception as e:
            # Menampilkan pesan error jika terjadi kesalahan input
            messagebox.showerror("Error", f"Invalid input for criteria comparisons.\n{e}")
    
    def input_alternative_comparisons(self):
        """
        Mengatur tampilan untuk memasukkan perbandingan berpasangan antar alternatif untuk setiap kriteria.
        """
        # Menghapus semua widget yang ada di frame saat ini
        for widget in self.winfo_children():
            widget.destroy()
        
        # Judul tampilan
        title = ttk.Label(self, text="Input Perbandingan Berpasangan Alternatif (AHP)", font=("Helvetica", 16))
        title.pack(pady=10)
        
        # Tombol untuk kembali ke tahap perbandingan kriteria
        back_btn = ttk.Button(self, text="Kembali", command=self.input_criteria_comparisons)
        back_btn.pack(anchor='w')
        
        # Instruksi untuk pengguna
        instructions = ttk.Label(self, text="Masukkan nilai perbandingan antar alternatif untuk setiap kriteria (misal: 1/3 atau 3)")
        instructions.pack(pady=5)
        
        # Notebook untuk setiap kriteria agar input perbandingan alternatif dapat dilakukan per kriteria
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.alternative_comparison_entries = {}  # Dictionary untuk menyimpan entry perbandingan alternatif
        
        for crit in self.ahp.criteria:
            # Membuat frame untuk setiap kriteria
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=crit)
            
            comparison_frame = ttk.Frame(frame)
            comparison_frame.pack(pady=10, padx=10)
            
            n = len(self.ahp.alternatives)  # Jumlah alternatif
            entries = {}
            
            # Membuat header kolom dengan nama alternatif
            for idx, alt in enumerate(self.ahp.alternatives):
                label = ttk.Label(comparison_frame, text=alt, font=('Helvetica', 10, 'bold'))
                label.grid(row=0, column=idx+1, padx=5, pady=5)
            
            # Membuat label baris dan entry untuk input perbandingan
            for i in range(n):
                # Label baris dengan nama alternatif
                row_label = ttk.Label(comparison_frame, text=self.ahp.alternatives[i], font=('Helvetica', 10, 'bold'))
                row_label.grid(row=i+1, column=0, padx=5, pady=5)
                
                for j in range(n):
                    if i == j:
                        # Diagonal utama selalu 1
                        label = ttk.Label(comparison_frame, text="1", width=10, anchor='center')
                        label.grid(row=i+1, column=j+1, padx=5, pady=5)
                    elif j < i:
                        # Sel di bawah diagonal adalah invers dari sel di atas
                        key = (j, i)
                        if key in entries:
                            try:
                                value = 1 / float(entries[key].get())
                            except:
                                value = 1
                            label = ttk.Label(comparison_frame, text=f"{value:.3f}", width=10, anchor='center')
                        else:
                            label = ttk.Label(comparison_frame, text="1", width=10, anchor='center')
                        label.grid(row=i+1, column=j+1, padx=5, pady=5)
                    else:
                        # Sel di atas diagonal utama memerlukan input dari pengguna
                        entry = ttk.Entry(comparison_frame, width=10)
                        entry.grid(row=i+1, column=j+1, padx=5, pady=5)
                        entries[(i, j)] = entry
            self.alternative_comparison_entries[crit] = entries  # Menyimpan entry perbandingan alternatif untuk setiap kriteria
        
        # Tombol untuk submit perbandingan alternatif
        submit_btn = ttk.Button(self, text="Submit", command=self.submit_alternative_comparisons)
        submit_btn.pack(pady=10)
    
    def submit_alternative_comparisons(self):
        """
        Mengumpulkan dan memproses perbandingan berpasangan antar alternatif untuk setiap kriteria.
        """
        try:
            for crit in self.ahp.criteria:
                entries = self.alternative_comparison_entries[crit]
                comparisons = []
                for (i, j), entry in entries.items():
                    value_str = entry.get().strip()  # Mengambil nilai dari entry
                    if '/' in value_str:
                        # Jika input dalam bentuk pecahan, konversi ke float
                        numerator, denominator = map(float, value_str.split('/'))
                        if denominator == 0:
                            raise ValueError("Denominator cannot be zero.")
                        value = numerator / denominator
                    else:
                        value = float(value_str)  # Konversi langsung ke float
                    if value <= 0:
                        raise ValueError("Values must be positive.")  # Validasi nilai positif
                    comparisons.append((i, j, value))  # Menambahkan tuple perbandingan
                self.ahp.set_alternative_comparisons(crit, comparisons)  # Menetapkan perbandingan alternatif untuk kriteria
            # Melakukan perhitungan AHP
            self.ahp.perform_ahp()
            self.display_results()  # Menampilkan hasil
        except Exception as e:
            # Menampilkan pesan error jika terjadi kesalahan input
            messagebox.showerror("Error", f"Invalid input for alternative comparisons.\n{e}")
    
    def display_results(self):
        """
        Menampilkan hasil perhitungan AHP dalam bentuk tabel dan langkah-langkah pengerjaan.
        """
        # Menghapus semua widget yang ada di frame saat ini
        for widget in self.winfo_children():
            widget.destroy()
        
        # Judul tampilan
        title = ttk.Label(self, text="Hasil AHP", font=("Helvetica", 16))
        title.pack(pady=10)
        
        # Tombol untuk kembali ke tahap perbandingan alternatif
        back_btn = ttk.Button(self, text="Kembali", command=self.input_alternative_comparisons)
        back_btn.pack(anchor='w')
        
        # Mengambil hasil dari perhitungan AHP
        results = self.ahp.get_results()
        
        # Label dan Text untuk menampilkan langkah-langkah pengerjaan
        steps_label = ttk.Label(self, text="Langkah-langkah Pengerjaan:", font=("Helvetica", 12, 'bold'))
        steps_label.pack(pady=5)
        
        steps_text = tk.Text(self, height=15, width=80)
        steps_text.pack(pady=5)
        steps_text.insert(tk.END, "\n\n".join(results['steps']))  # Menambahkan langkah-langkah ke dalam Text widget
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
        
        df_criteria = pd.DataFrame(results['criteria_matrix'], index=self.ahp.criteria, columns=self.ahp.criteria)
        tree_criteria = self.create_treeview(frame_criteria, df_criteria)
        tree_criteria.pack(fill=tk.BOTH, expand=True)
        
        # Tab untuk Bobot Kriteria
        frame_weights = ttk.Frame(notebook)
        notebook.add(frame_weights, text="Bobot Kriteria")
        
        df_weights = pd.DataFrame({
            'Kriteria': self.ahp.criteria,
            'Bobot': results['criteria_weights']
        })
        tree_weights = self.create_treeview(frame_weights, df_weights)
        tree_weights.pack(fill=tk.BOTH, expand=True)
        
        # Tab untuk Matriks Alternatif per Kriteria
        for crit in self.ahp.criteria:
            frame_alt_matrix = ttk.Frame(notebook)
            notebook.add(frame_alt_matrix, text=f'Matriks Alternatif {crit}')
            
            df_alt_matrix = pd.DataFrame(results['alternative_matrices'][crit], index=self.ahp.alternatives, columns=self.ahp.alternatives)
            tree_alt_matrix = self.create_treeview(frame_alt_matrix, df_alt_matrix)
            tree_alt_matrix.pack(fill=tk.BOTH, expand=True)
        
        # Tab untuk Bobot Alternatif per Kriteria
        for crit in self.ahp.criteria:
            frame_alt_weights = ttk.Frame(notebook)
            notebook.add(frame_alt_weights, text=f'Bobot Alternatif {crit}')
            
            df_alt_weights = pd.DataFrame({
                'Alternatif': self.ahp.alternatives,
                'Bobot': results['alternative_weights'][crit]
            })
            tree_alt_weights = self.create_treeview(frame_alt_weights, df_alt_weights)
            tree_alt_weights.pack(fill=tk.BOTH, expand=True)
        
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
        Mengekspor hasil AHP ke dalam file Excel dengan struktur sheet yang terorganisir.
        """
        # Membuka dialog untuk memilih lokasi penyimpanan file Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            try:
                # Membuat ExcelWriter dengan engine 'openpyxl'
                writer = pd.ExcelWriter(file_path, engine='openpyxl')
                
                # Menulis Matriks Kriteria ke sheet 'Matriks Kriteria'
                df_criteria = pd.DataFrame(self.ahp.criteria_matrix, index=self.ahp.criteria, columns=self.ahp.criteria)
                df_criteria.to_excel(writer, sheet_name='Matriks Kriteria')
                
                # Menulis Bobot Kriteria ke sheet 'Bobot Kriteria'
                df_weights = pd.DataFrame({
                    'Kriteria': self.ahp.criteria,
                    'Bobot': self.ahp.criteria_weights
                })
                df_weights.to_excel(writer, sheet_name='Bobot Kriteria', index=False)
                
                # Menulis Matriks Alternatif per Kriteria ke masing-masing sheet
                for crit in self.ahp.criteria:
                    df_alt_matrix = pd.DataFrame(self.ahp.alternative_matrices[crit], index=self.ahp.alternatives, columns=self.ahp.alternatives)
                    df_alt_matrix.to_excel(writer, sheet_name=f'Matriks Alternatif {crit}')
                    
                    # Menulis Bobot Alternatif per Kriteria ke masing-masing sheet
                    df_alt_weights = pd.DataFrame({
                        'Alternatif': self.ahp.alternatives,
                        'Bobot': self.ahp.alternative_weights[crit]
                    })
                    df_alt_weights.to_excel(writer, sheet_name=f'Bobot Alternatif {crit}', index=False)
                
                # Menulis Final Ranking ke sheet 'Final Ranking'
                df_final = pd.DataFrame({
                    'Alternatif': list(self.ahp.final_ranking.keys()),
                    'Skor Akhir': list(self.ahp.final_ranking.values())
                }).sort_values(by='Skor Akhir', ascending=False)
                df_final.to_excel(writer, sheet_name='Final Ranking', index=False)
                
                # Menulis Langkah-langkah Pengerjaan ke sheet 'Langkah Pengerjaan'
                df_steps = pd.DataFrame({'Steps': self.ahp.steps})
                df_steps.to_excel(writer, sheet_name='Langkah Pengerjaan', index=False)
                
                # Menyimpan file Excel
                writer.save()
                messagebox.showinfo("Success", f"Hasil berhasil diekspor ke {file_path}")
            except Exception as e:
                # Menampilkan pesan error jika terjadi kegagalan saat ekspor
                messagebox.showerror("Error", f"Gagal mengekspor ke Excel.\n{e}")
