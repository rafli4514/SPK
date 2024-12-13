import tkinter as tk

TITLE_FONT = ("Poppins", 16, "bold")
INPUT_FONT = ("Poppins", 12)
BUTTON_FONT = ("Poppins", 18, "bold")
SECTION_FONT = ("Poppins", 16, "bold")

BG_MAIN = "#261A64"
FG_MAIN = "white"
BG_CARD = "white"
BG_INPUT = "white"
BG_BUTTON = "#261A64"
BG_ACTION = "#FA4553"

class AHPPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_MAIN)
        self.controller = controller

        # Header
        header_frame = tk.Frame(self, bg=BG_MAIN)
        header_frame.pack(fill="x", pady=(30,10))

        back_label = tk.Label(header_frame, text="←", font=("Poppins", 16), fg=FG_MAIN, bg=BG_MAIN)
        back_label.pack(side="left", padx=(20,0))
        back_label.bind("<Button-1>", lambda e: controller.show_frame("MainPage"))

        ahp_title_label = tk.Label(header_frame, text="Input  Kriteria Dan Alternatif (AHP)", font=TITLE_FONT, fg=FG_MAIN, bg=BG_MAIN)
        ahp_title_label.pack(side="left", padx=(10,0))

        # Frame kartu putih
        card_frame = tk.Frame(self, bg=BG_CARD)
        card_frame.pack(pady=(0,20), padx=10, fill="both", expand=False)

        # Kriteria
        kriteria_label = tk.Label(card_frame, text="Kriteria", font=SECTION_FONT, fg="black", bg=BG_CARD)
        kriteria_label.pack(anchor="w", padx=20, pady=(20,5))

        kriteria_frame = tk.Frame(card_frame, bg=BG_CARD)
        kriteria_frame.pack(fill="x", padx=20)

        kriteria_entry = tk.Entry(kriteria_frame, font=INPUT_FONT, fg="black", bg=BG_INPUT, bd=1, relief="solid")
        kriteria_entry.pack(side="left", fill="x", expand=True, ipady=4)

        tambah_kriteria_btn = tk.Button(kriteria_frame, text="Tambah\nKriteria", font=("Poppins", 10, "bold"), bg=BG_BUTTON, fg=FG_MAIN, bd=0, relief="flat")
        tambah_kriteria_btn.pack(side="right", padx=(10,0), ipady=4)

        kriteria_list_text = tk.Text(card_frame, font=INPUT_FONT, fg="black", bg="white", bd=1, relief="solid", height=5)
        kriteria_list_text.pack(fill="x", padx=20, pady=(10,20))

        # Alternatif
        alternatif_label = tk.Label(card_frame, text="Alternatif", font=SECTION_FONT, fg="black", bg=BG_CARD)
        alternatif_label.pack(anchor="w", padx=20, pady=(0,5))

        alternatif_frame = tk.Frame(card_frame, bg=BG_CARD)
        alternatif_frame.pack(fill="x", padx=20)

        alternatif_entry = tk.Entry(alternatif_frame, font=INPUT_FONT, fg="black", bg=BG_INPUT, bd=1, relief="solid")
        alternatif_entry.pack(side="left", fill="x", expand=True, ipady=4)

        tambah_alternatif_btn = tk.Button(alternatif_frame, text="Tambah\nAlternatif", font=("Poppins", 10, "bold"), bg=BG_BUTTON, fg=FG_MAIN, bd=0, relief="flat")
        tambah_alternatif_btn.pack(side="right", padx=(10,0), ipady=4)

        alternatif_list_text = tk.Text(card_frame, font=INPUT_FONT, fg="black", bg="white", bd=1, relief="solid", height=5)
        alternatif_list_text.pack(fill="x", padx=20, pady=(10,20))

        # Tombol Lanjut
        lanjut_button = tk.Button(card_frame, text="Lanjut", font=BUTTON_FONT, bg=BG_ACTION, fg=FG_MAIN, bd=0, relief="flat",
                                  command=lambda: controller.show_frame("CriteriaAHPPage"))
        lanjut_button.pack(pady=(10,20), ipadx=50, ipady=5)
