import tkinter as tk
from home import TelaHome

if __name__ == "__main__":
    janela = tk.Tk()
    TelaInicial = TelaHome(janela)
    janela.title('Tela Inicial')
    janela.geometry("800x600")
    janela.mainloop()
