import tkinter as tk
import psycopg2
from Programa import PrincipalBD  
from cadastro import CadastroFuncionario
class TelaLogin:
    def __init__(self, win):
        self.win = win
        self.win.title("Tela de Login")

        self.lbllogin = tk.Label(win, text='Login', font=('Arial', 26))
        self.lbllogin.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        win.eval('tk::PlaceWindow . center')

        self.lblNome = tk.Label(win, text='Nome:')
        self.lblSenha = tk.Label(win, text='Senha:')
        
        self.txtNome = tk.Entry(win)
        self.txtSenha = tk.Entry(win, show="*")

        self.btnLogin = tk.Button(win, text='Login', command=self.realizarLogin)
        self.btnCadastrar = tk.Button(win, text='Cadastre-se', command=self.abrirCadastro)

        self.lblNome.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        self.txtNome.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        self.lblSenha.place(relx=0.5, rely=0.40, anchor=tk.CENTER)
        self.txtSenha.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        self.btnLogin.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        self.btnCadastrar.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

    def realizarLogin(self):
        nome = self.txtNome.get()
        senha = self.txtSenha.get()

        if not nome or not senha:
            mensagem_erro = tk.Label(self.win, text='Campos vazios. Por favor, insira os devidos dados nos campos.', fg='red')
            mensagem_erro.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        else:
            try:
                connection = psycopg2.connect(user="postgres",
                                            password="trabalho",
                                            host="localhost",
                                            port="5432",
                                            database="Python")

                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM public.\"funcionario\" WHERE nome = '{nome}' AND senha = '{senha}'")
                record = cursor.fetchone()

                if record is not None:
                    self.abrirPrograma()
                else:
                    print("Credenciais inválidas. Tente novamente.")

            except (Exception, psycopg2.Error) as error:
                print("Erro ao conectar ao banco de dados:", error)

            finally:
                if connection:
                    cursor.close()
                    connection.close()

    def abrirPrograma(self):
        self.win.withdraw()
        janelaPrograma = tk.Tk()
        PrincipalBD(janelaPrograma)
        janelaPrograma.title('Tela do Programa')
        janelaPrograma.geometry("1000x900")
        janelaPrograma.deiconify()
        
    def abrirCadastro(self):
        self.janela_cadastro = tk.Tk()
        CadastroFuncionario(self.janela_cadastro, self)  
        self.janela_cadastro.protocol("WM_DELETE_WINDOW", self.fecharCadastro)
        self.janela_cadastro.title('Tela de Cadastro')
        self.janela_cadastro.geometry("800x600")
        self.win.iconify()


if __name__ == "__main__":
    janela = tk.Tk()
    TelaInicial = TelaLogin(janela)
    janela.title('Tela de Login')
    janela.geometry("800x600")
    janela.mainloop()
