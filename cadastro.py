import tkinter as tk
import psycopg2


class AppBD:
    def __init__(self):
        self.abrirConexao()

    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(user="postgres", password="trabalho",
            host="localhost", port="5432", database="Python")
        except (Exception, psycopg2.Error) as error:
            if(self.connection):
                print("Falha ao se conectar ao Banco de Dados", error)
                
    def inserirDados(self, nome, cpf, senha):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            postgres_insert_query = """ INSERT INTO public."funcionario"
            ("nome", "cpf", "senha") VALUES (%s,%s,%s)"""
            record_to_insert = (nome, cpf, senha)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro inserido com sucesso na tabela FUNCIONARIO")
        except (Exception, psycopg2.Error) as error:
            if(self.connection):
                print("Falha ao inserir registro na tabela FUNCIONARIO", error)
        finally:
            if(self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada")

class CadastroFuncionario:
    def __init__(self, win, tela_login):
        self.win = win
        self.tela_login = tela_login
        self.objBD = AppBD()
        
        win.geometry("800x600")
        win.title('Cadastramento de funcionário')
        
        self.lblcadastro = tk.Label(win, text='Cadastramento de funcionário', font=('Arial', 28))
        self.lblcadastro.pack(pady=(30, 10))  
        
        self.lblNome = tk.Label(win, text='Nome:')
        self.lblCPF = tk.Label(win, text='CPF:')
        self.lblSenha = tk.Label(win, text='Senha:')
        
        self.txtNome = tk.Entry(win)
        self.txtCPF = tk.Entry(win)
        self.txtSenha = tk.Entry(win, show="*")  
        
        self.btnCadastrar = tk.Button(win, text='Cadastrar', command=self.fCadastrarFuncionario)
        
        self.lblNome.pack()
        self.txtNome.pack()
        self.lblCPF.pack()
        self.txtCPF.pack()
        self.lblSenha.pack()
        self.txtSenha.pack()
        self.btnCadastrar.pack(pady=10)
        
        self.lblJaTemConta = tk.Label(win, text="Já tem uma conta? Logue-se")
        self.lblJaTemConta.pack()
        
        self.btnLogin = tk.Button(win, text="Login", command=self.abrirTelaLogin)
        self.btnLogin.pack()
        
        self.msgLabel = tk.Label(win, text='', fg='red')
        self.msgLabel.pack(pady=(10, 20))

    def fCadastrarFuncionario(self):
        try:
            nome = self.txtNome.get()
            cpf = self.txtCPF.get()
            senha = self.txtSenha.get()

            if not nome or any(char.isdigit() or not char.isalpha() and char not in (" ", "'") for char in nome):
                raise ValueError("Nome inválido. Por favor, insira um nome válido.")

            if not cpf or not cpf.isdigit() or len(cpf) != 11:
                raise ValueError("CPF inválido. Por favor, insira um CPF válido com 11 dígitos numéricos.")

            if not senha or len(senha) < 3:
                raise ValueError("Senha inválida. A senha deve ter no mínimo 3 caracteres.")

            self.objBD.inserirDados(nome, cpf, senha)
            print('Funcionário Cadastrado com Sucesso!')
            self.abrirTelaLogin()

        except ValueError as ve:
            self.msgLabel.config(text=str(ve))
        except Exception as e:
            print('Não foi possível fazer o cadastro. Erro:', e)

    def abrirTelaLogin(self):
        from login import TelaLogin
        janela_login = tk.Tk()
        TelaLogin(janela_login)
        self.win.withdraw()
        janela_login.title('Tela de Login')
        janela_login.geometry("800x600")

        janela_login.eval('tk::PlaceWindow . center')

        janela_login.mainloop()

if __name__ == "__main__":
    from login import TelaLogin
    janela_cadastro = tk.Tk()
    tela_login = TelaLogin(janela_cadastro)
    CadastroFuncionario(janela_cadastro, tela_login)
    janela_cadastro.mainloop()
