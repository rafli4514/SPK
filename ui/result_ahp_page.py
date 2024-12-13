import tkinter as tk

TITLE_FONT = ("Poppins", 16, "bold")
SECTION_FONT = ("Poppins", 16, "bold")
BUTTON_FONT = ("Poppins", 18, "bold")

BG_MAIN = "#261A64"
FG_MAIN = "white"
BG_CARD = "white"
FG_TEXT = "#1E1E1E"
ACTION_COLOR = "#FA4553"
BOX_BG = "#1F1360"  # Warna box ungu tua untuk hasil perhitungan

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_MAIN)
        self.controller = controller

        # Header
        header_label = tk.Label(self, text="Hasil  (AHP)", font=TITLE_FONT, fg=FG_MAIN, bg=BG_MAIN)
        header_label.pack(pady=(30,10))

        # Frame kartu putih di tengah
        card_frame = tk.Frame(self, bg=BG_CARD, bd=0, highlightthickness=0)
        card_frame.pack(pady=(0,20), padx=10, fill="both", expand=False)

        # Tombol kembali
        back_label = tk.Label(card_frame, text="←", font=("Poppins",16), fg=FG_TEXT, bg=BG_CARD)
        back_label.place(x=20, y=20)
        # Ganti "MainPage" dengan halaman yang diinginkan
        back_label.bind("<Button-1>", lambda e: controller.show_frame("MainPage"))

        # Label "Hasil Perhitungan:"
        hasil_label = tk.Label(card_frame, text="Hasil Perhitungan:", font=SECTION_FONT, fg="black", bg=BG_CARD)
        hasil_label.pack(pady=(70,10))

        # Kotak-kotak hasil perhitungan (misalnya daftar hasil)
        # Kita buat beberapa frame kotak sebagai placeholder
        box_frame = tk.Frame(card_frame, bg=BG_CARD)
        box_frame.pack(pady=(0,20))

        # Misalkan kita punya 7 kotak hasil
        # Atur dalam 2 baris (4 kotak di atas, 3 kotak di bawah)
        box_width = 10
        box_height = 1
        boxes = []
        # Baris atas
        for i in range(4):
            lbl = tk.Label(box_frame, text="", font=("Poppins",12,"bold"), fg=FG_MAIN, bg=BOX_BG, width=box_width, height=box_height)
            lbl.grid(row=0, column=i, padx=5, pady=5)
            boxes.append(lbl)

        # Baris bawah
        for i in range(3):
            lbl = tk.Label(box_frame, text="", font=("Poppins",12,"bold"), fg=FG_MAIN, bg=BOX_BG, width=box_width, height=box_height)
            lbl.grid(row=1, column=i, padx=5, pady=5)
            boxes.append(lbl)

        # Kotak text untuk menampilkan hasil detail
        hasil_text = tk.Text(card_frame, font=("Poppins",12), fg="black", bg="white", bd=1, relief="solid", height=5)
        hasil_text.pack(fill="x", padx=20, pady=(10,20))

        # Tombol Ekspor ke Excel
        export_button = tk.Button(card_frame, text="Ekspor ke excel", font=BUTTON_FONT, fg="white", bg=ACTION_COLOR, bd=0, relief="flat")
        export_button.pack(pady=(10,20), ipadx=50, ipady=5)

        # Jika Anda ingin menambahkan fungsi untuk tombol, 
        # misalnya export_button.config(command=lambda: self.export_to_excel())
        # Pastikan Anda telah menulis fungsi export_to_excel.

    def export_to_excel(self):
        # Implementasikan logika ekspor ke Excel di sini
        pass
