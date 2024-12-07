# main.py

import tkinter as tk
from ui.main_app import DecisionMakingApp

def main():
    root = tk.Tk()
    app = DecisionMakingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
