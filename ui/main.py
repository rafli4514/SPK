import tkinter as tk
from main_page import MainPage
from ahp_page import AHPPage
from criteria_ahp_page import CriteriaAHPPage
from alternative_ahp_page import AlternativeAHPPage
from result_ahp_page import ResultPage  

BG_MAIN = "#261A64"

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Pemilihan Metode")
        self.geometry("375x812")
        self.configure(bg=BG_MAIN)

        container = tk.Frame(self, bg=BG_MAIN)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (MainPage, AHPPage, CriteriaAHPPage, AlternativeAHPPage, ResultPage):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
