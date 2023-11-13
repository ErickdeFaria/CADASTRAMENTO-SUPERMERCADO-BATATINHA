import tkinter as tk
from cadastro import CadastroFuncionario

class TelaHome:
    def __init__(self, win):
        self.win = win

        self.lblBemVindo = tk.Label(win, text='Seja bem-vindo', font=('Arial', 24))
        self.lblBemVindo.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.lblBemVindo2 = tk.Label(win, text='ao sistema de cadastramento do SuperMercado', font=('Arial', 18))
        self.lblBemVindo2.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.lblBemVindo3 = tk.Label(win, text='BATATINHA', font=('Arial', 24))
        self.lblBemVindo3.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.btnIniciar = tk.Button(win, text="Iniciar", command=self.abrirCadastro)
        self.btnIniciar.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        self.janela_cadastro = None  
    def abrirCadastro(self):
        self.janela_cadastro = tk.Toplevel(self.win)
        CadastroFuncionario(self.janela_cadastro, self)  
        self.janela_cadastro.protocol("WM_DELETE_WINDOW", self.fecharCadastro)
        self.janela_cadastro.title('Tela de Cadastro')
        self.janela_cadastro.geometry("800x600")
        self.win.iconify()



janela = tk.Tk()
TelaInicial = TelaHome(janela)
janela.title('Tela Inicial')
janela.geometry("800x600")
janela.mainloop()