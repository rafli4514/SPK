import tkinter as tk

TITLE_FONT = ("Poppins", 16, "bold")
METHOD_TITLE_FONT = ("Poppins", 16, "bold")
METHOD_SUB_FONT = ("Poppins", 10, "normal")

BG_MAIN = "#261A64"
FG_MAIN = "white"
BG_CARD = "white"
BG_METHOD = "#E7E7E7"
BG_SELECTED = "#FA4553"
FG_NORMAL = "black"
ICON_BG_NORMAL = "#261A64"
ICON_BG_SELECTED = "#ffffff"

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_MAIN)
        self.controller = controller
        
        title_label = tk.Label(self, text="Pilih Metode Pengambilan Keputusan", font=TITLE_FONT, fg=FG_MAIN, bg=BG_MAIN)
        title_label.pack(pady=(30,10))

        card_frame = tk.Frame(self, bg=BG_CARD, bd=0, highlightthickness=0)
        card_frame.pack(pady=10, padx=10, fill="both", expand=False)

        methods_container = tk.Frame(card_frame, bg=BG_CARD)
        methods_container.pack(pady=20, padx=20)

        # Metode AHP yang ketika diklik pindah ke AHPPage
        ahp_frame = self.create_method_frame(methods_container, "AHP", "Analytic Hierarchy Process", 
                                             command=lambda: controller.show_frame("AHPPage"))
        saw_frame = self.create_method_frame(methods_container, "SAW", "Simple Additive Weighting")
        topsis_frame = self.create_method_frame(methods_container, "TOPSIS")
        wp_frame = self.create_method_frame(methods_container, "WP", "Weighted Product")
        promethee_frame = self.create_method_frame(methods_container, "Promethee")
        maut_frame = self.create_method_frame(methods_container, "MAUT")

        ahp_frame.grid(row=0, column=0, padx=10, pady=10)
        saw_frame.grid(row=0, column=1, padx=10, pady=10)
        topsis_frame.grid(row=1, column=0, padx=10, pady=10)
        wp_frame.grid(row=1, column=1, padx=10, pady=10)
        promethee_frame.grid(row=2, column=0, padx=10, pady=10)
        maut_frame.grid(row=2, column=1, padx=10, pady=10)

    def create_method_frame(self, parent, title, subtitle=None, command=None):
        f = tk.Frame(parent, width=150, height=149, bg=BG_METHOD)
        f.pack_propagate(False)

        ikon_frame = tk.Frame(f, width=60, height=60, bg=ICON_BG_NORMAL)
        ikon_frame.place(relx=0.5, y=40, anchor="center")

        title_label = tk.Label(f, text=title, font=METHOD_TITLE_FONT, fg=FG_NORMAL, bg=BG_METHOD)
        title_label.place(relx=0.5, rely=0.5, anchor="center", y=15)

        subtitle_label = None
        if subtitle:
            subtitle_label = tk.Label(f, text=subtitle, font=METHOD_SUB_FONT, fg=FG_NORMAL, bg=BG_METHOD)
            subtitle_label.place(relx=0.5, rely=0.5, anchor="center", y=35)
        
        def on_enter(e):
            f.config(bg=BG_SELECTED)
            title_label.config(bg=BG_SELECTED, fg=FG_MAIN)
            ikon_frame.config(bg=ICON_BG_SELECTED)
            if subtitle:
                subtitle_label.config(bg=BG_SELECTED, fg=FG_MAIN)

        def on_leave(e):
            f.config(bg=BG_METHOD)
            title_label.config(bg=BG_METHOD, fg=FG_NORMAL)
            ikon_frame.config(bg=ICON_BG_NORMAL)
            if subtitle:
                subtitle_label.config(bg=BG_METHOD, fg=FG_NORMAL)

        f.bind("<Enter>", on_enter)
        f.bind("<Leave>", on_leave)

        if command:
            f.bind("<Button-1>", lambda e: command())

        return f
