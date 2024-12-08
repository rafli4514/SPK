# ui/main_app.py

import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from .ahp_ui import AHPFrame
from .saw_ui import SAWFrame
# from .topsis_ui import TOPSISFrame  # Metode lain yang belum diimplementasikan
# from .wp_ui import WPFrame
# from .promethee_ui import PrometheeFrame
# from .maut_ui import MAUTFrame
import sys

class DecisionMakingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pengambilan Keputusan")
        self.style = Style(theme='cosmo')  # Tema biru
        self.style.theme_use('cosmo')

        # Membuat Frame Utama
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Membuat Halaman Utama
        self.create_home_page()

    def create_home_page(self):
        """
        Membuat halaman utama dengan pilihan metode.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ttk.Label(self.main_frame, text="Pilih Metode Pengambilan Keputusan", font=("Helvetica", 16))
        title.pack(pady=20)

        # Daftar Metode
        methods = ["Analytic Hierarchy Process (AHP)", "Simple Additive Weighting (SAW)", "TOPSIS", "WP", "Promethee", "MAUT"]  # Tambahkan metode lain di sini

        for method in methods:
            btn = ttk.Button(self.main_frame, text=method, width=30,
                             command=lambda m=method: self.select_method(m))
            btn.pack(pady=10)

        # Tombol Import Excel (Fitur akan ditambahkan nanti)
        # import_btn = ttk.Button(self.main_frame, text="Import dari Excel", command=self.import_data)
        # import_btn.pack(pady=20)

    def select_method(self, method_name):
        """
        Mengarahkan pengguna ke halaman input berdasarkan metode yang dipilih.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Tombol Kembali
        back_btn = ttk.Button(self.main_frame, text="Kembali", command=self.create_home_page)
        back_btn.pack(anchor='w', pady=5)

        # Display Frame Metode yang Dipilih
        if method_name == "Analytic Hierarchy Process (AHP)":
            ahp_frame = AHPFrame(self.main_frame)
            ahp_frame.pack(fill=tk.BOTH, expand=True)
        elif method_name == "Simple Additive Weighting (SAW)":
            saw_frame = SAWFrame(self.main_frame)
            saw_frame.pack(fill=tk.BOTH, expand=True)
        elif method_name == "TOPSIS":
            # topsis_frame = TOPSISFrame(self.main_frame)
            # topsis_frame.pack(fill=tk.BOTH, expand=True)
            messagebox.showinfo("Info", "Metode TOPSIS belum diimplementasikan.")
        elif method_name == "WP":
            # wp_frame = WPFrame(self.main_frame)
            # wp_frame.pack(fill=tk.BOTH, expand=True)
            messagebox.showinfo("Info", "Metode WP belum diimplementasikan.")
        elif method_name == "Promethee":
            # promethee_frame = PrometheeFrame(self.main_frame)
            # promethee_frame.pack(fill=tk.BOTH, expand=True)
            messagebox.showinfo("Info", "Metode Promethee belum diimplementasikan.")
        elif method_name == "MAUT":
            # maut_frame = MAUTFrame(self.main_frame)
            # maut_frame.pack(fill=tk.BOTH, expand=True)
            messagebox.showinfo("Info", "Metode MAUT belum diimplementasikan.")
        else:
            messagebox.showinfo("Info", f"Metode {method_name} belum diimplementasikan.")

    # Implementasikan metode lainnya seperti TOPSIS, SAW, WP, Promethee, MAUT di sini

def main():
    root = tk.Tk()
    app = DecisionMakingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
