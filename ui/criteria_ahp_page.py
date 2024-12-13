import tkinter as tk

TITLE_FONT = ("Poppins", 16, "bold")
INSTR_FONT = ("Poppins", 16, "bold")
LABEL_FONT = ("Poppins", 16)
BUTTON_FONT = ("Poppins", 18, "bold")
ENTRY_FONT = ("Poppins", 14)

BG_MAIN = "#261A64"
BG_CARD = "white"
FG_MAIN = "white"
FG_TEXT = "#1E1E1E"
ACTION_COLOR = "#FA4553"

class CriteriaAHPPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_MAIN)
        self.controller = controller

        # Header Label
        header_label = tk.Label(self, text="Input  Perbandingan Berpasangan Kriteria\n(AHP)", 
                                font=TITLE_FONT, fg=FG_MAIN, bg=BG_MAIN, justify="center")
        header_label.pack(pady=(30,10))

        # Frame kartu putih
        card_frame = tk.Frame(self, bg=BG_CARD, bd=0, highlightthickness=0)
        card_frame.pack(pady=(0,10), padx=10, fill="both", expand=False)

        # Tombol kembali ke MainPage
        back_label = tk.Label(card_frame, text="←", font=("Poppins",16), fg=FG_TEXT, bg=BG_CARD)
        back_label.place(x=20, y=20)
        back_label.bind("<Button-1>", lambda e: controller.show_frame("MainPage"))

        # Instruksi
        instr_label = tk.Label(card_frame, text="Masukkan Nilai Perbandingan Antar Kriteria\n(misal: 1/3 atau 3)",
                               font=INSTR_FONT, fg=FG_TEXT, bg=BG_CARD, justify="center")
        instr_label.pack(pady=(50,10))

        # Tabel perbandingan kriteria
        table_frame = tk.Frame(card_frame, bg=BG_CARD)
        table_frame.pack(pady=(10,20))

        col1_label = tk.Label(table_frame, text="Kriteria 1", font=LABEL_FONT, fg=FG_TEXT, bg=BG_CARD)
        col1_label.grid(row=0, column=1, padx=20, pady=5)

        col2_label = tk.Label(table_frame, text="Kriteria 2", font=LABEL_FONT, fg=FG_TEXT, bg=BG_CARD)
        col2_label.grid(row=0, column=2, padx=20, pady=5)

        # Baris 1
        row1_label = tk.Label(table_frame, text="Kriteria 1", font=LABEL_FONT, fg=FG_TEXT, bg=BG_CARD)
        row1_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        val_11 = tk.Label(table_frame, text="1", font=LABEL_FONT, fg=FG_TEXT, bg="white", width=5, relief="solid")
        val_11.grid(row=1, column=1, padx=5, pady=5)

        val_12 = tk.Entry(table_frame, font=ENTRY_FONT, fg="black", bg="white", width=5, bd=1, relief="solid", justify="center")
        val_12.insert(0, "1")
        val_12.grid(row=1, column=2, padx=5, pady=5)

        # Baris 2
        row2_label = tk.Label(table_frame, text="Kriteria 2", font=LABEL_FONT, fg=FG_TEXT, bg=BG_CARD)
        row2_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        val_21 = tk.Entry(table_frame, font=ENTRY_FONT, fg="black", bg="white", width=5, bd=1, relief="solid", justify="center")
        val_21.insert(0, "1000")
        val_21.grid(row=2, column=1, padx=5, pady=5)

        val_22 = tk.Label(table_frame, text="1", font=LABEL_FONT, fg=FG_TEXT, bg="white", width=5, relief="solid")
        val_22.grid(row=2, column=2, padx=5, pady=5)

        # Tombol Submit
        submit_button = tk.Button(card_frame, text="Submit", font=BUTTON_FONT, fg="white", bg=ACTION_COLOR, bd=0, relief="flat",
                                  command=lambda: self.go_to_alternative(controller))
        submit_button.pack(pady=(10,20), ipadx=50, ipady=5)

    def go_to_alternative(self, controller):
        # Metode ini dipanggil saat tombol Submit ditekan
        # Di sini Anda bisa menambahkan logika untuk menyimpan input
        # dan kemudian pindah ke AlternativeAHPPage
        controller.show_frame("AlternativeAHPPage")
