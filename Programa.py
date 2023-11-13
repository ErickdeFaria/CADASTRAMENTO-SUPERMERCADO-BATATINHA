import tkinter as tk
import psycopg2
from tkinter import ttk

class AppBD:
    def __init__(self):
        print('Método Construtor')

    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(user="postgres", password="trabalho",
            host="localhost", port="5432", database="Python")
        except (Exception, psycopg2.Error) as error:
            if(self.connection):
                print("Falha ao se conectar ao Banco de Dados", error)

    def inserirDados(self, codigo, nome, preco, juros):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            postgres_insert_query = """ INSERT INTO public."produto"
            ("codigo", "nome", "preco", "juros", "preco_com_juros") VALUES (%s, %s, %s, %s, %s)"""
            preco_com_juros = preco + (preco * (juros / 100))
            record_to_insert = (codigo, nome, preco, juros, preco_com_juros)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro inserido com sucesso na tabela PRODUTO")
        except (Exception, psycopg2.Error) as error:
            if(self.connection):
                print("Falha ao inserir registro na tabela PRODUTO", error)
        finally:
            if(self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada")

    def atualizarDados(self, codigo, nome, preco, juros):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            sql_update_query = """Update public."produto" set "nome" = %s, "preco" = %s, "juros" = %s, "preco_com_juros" = %s where "codigo" = %s"""
            preco_com_juros = preco + (preco * (juros / 100))
            cursor.execute(sql_update_query, (nome, preco, juros, preco_com_juros, codigo))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro atualizado com sucesso!")
            print("Registro Depois da Atualização ")
            sql_select_query = """select * from public."produto" where "codigo" = %s"""
            cursor.execute(sql_select_query, (codigo,))
            record = cursor.fetchone()
            print(record)
        except (Exception, psycopg2.Error) as error:
            print("Erro na Atualização", error)
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada")

    def excluirDados(self, codigo):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            sql_delete_query = """Delete from public."produto" where "codigo" = %s"""
            cursor.execute(sql_delete_query, (codigo, ))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro excluído com sucesso!")
        except (Exception, psycopg2.Error) as error:
            print("Erro na Exclusão", error)
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada")


class PrincipalBD:
    def __init__(self, win):
        self.objBD = AppBD()
        
        win.title('Bem Vindo à Tela de Cadastro')
        win.geometry("1000x900")
        win.eval('tk::PlaceWindow . center')
        win.maxsize(width=1200, height=800)
        win.minsize(width=300, height=200)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)
         
        titulo_label = tk.Label(win, text='Cadastro de produtos', font=('Arial', 24, 'bold'))
        titulo_label.grid(row=0, column=0, columnspan=4, pady=(20, 10))

        linha_em_branco = tk.Label(win, text='', font=('Arial', 12))
        linha_em_branco.grid(row=1, column=0, columnspan=4, pady=10)

        frame_codigo = tk.Frame(win)
        frame_nome = tk.Frame(win)
        frame_preco = tk.Frame(win)
        frame_calculo_juros = tk.Frame(win)
        frame_preco_com_juros = tk.Frame(win)

        frame_codigo.grid(row=2, column=0, padx=2, pady=10)
        frame_nome.grid(row=3, column=0, padx=5, pady=5)
        frame_preco.grid(row=4, column=0, padx=2, pady=10)
        frame_calculo_juros.grid(row=5, column=0, padx=2, pady=10)
        frame_preco_com_juros.grid(row=6, column=0, padx=2, pady=10)

        lbCodigo = tk.Label(frame_codigo, text='Código do Produto:', font=('Arial', 12))
        lblNome = tk.Label(frame_nome, text='Nome do Produto', font=('Arial', 12))
        lblPreco = tk.Label(frame_preco, text='Preço', font=('Arial', 12))
        lblCalculoJuros = tk.Label(frame_calculo_juros, text='Cálculo de Juros (%)', font=('Arial', 12))
        lblPrecoComJuros = tk.Label(frame_preco_com_juros, text='Preço com Juros', font=('Arial', 12))

        lbCodigo.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        lblNome.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        lblPreco.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        lblCalculoJuros.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        lblPrecoComJuros.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        self.txtCodigo = tk.Entry(frame_codigo, font=('Arial', 12))
        self.txtNome = tk.Entry(frame_nome, font=('Arial', 12))
        self.txtPreco = tk.Entry(frame_preco, font=('Arial', 12))
        self.txtCalculoJuros = tk.Entry(frame_calculo_juros, font=('Arial', 12))
        self.txtPrecoComJuros = tk.Entry(frame_preco_com_juros, font=('Arial', 12))

        self.txtCodigo.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.txtNome.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.txtPreco.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.txtCalculoJuros.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.txtPrecoComJuros.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.frame_botoes = tk.Frame(win)
        self.frame_botoes.grid(row=7, column=0, columnspan=5, pady=10)

        self.btnCadastrar = tk.Button(self.frame_botoes, text='Cadastrar', command=self.fCadastrarProduto)
        self.btnAtualizar = tk.Button(self.frame_botoes, text='Atualizar', command=self.fAtualizarProduto)
        self.btnExcluir = tk.Button(self.frame_botoes, text='Excluir', command=self.fExcluirProduto)
        self.btnLimpar = tk.Button(self.frame_botoes, text='Limpar', command=self.fLimparTela)
        self.btnCalcularJuros = tk.Button(self.frame_botoes, text='Calcular Juros', command=self.fCalcularJuros)

        self.btnCadastrar.grid(row=0, column=0, padx=10, pady=10)
        self.btnAtualizar.grid(row=0, column=1, padx=10, pady=10)
        self.btnExcluir.grid(row=0, column=2, padx=10, pady=10)
        self.btnLimpar.grid(row=0, column=3, padx=10, pady=10)
        self.btnCalcularJuros.grid(row=0, column=4, padx=10, pady=10)

        self.msgLabel = tk.Label(win, text='', fg='red')
        self.msgLabel.grid(row=8, columnspan=4, padx=10, pady=10, sticky='w')

        self.abas = ttk.Notebook(win)
        self.aba_listagem = ttk.Frame(self.abas)
        self.abas.add(self.aba_listagem, text='Lista de Produtos')
        self.abas.grid(row=9, columnspan=4, padx=10, pady=10)

        self.txtProdutos = tk.Text(self.aba_listagem, height=10, width=60)
        self.txtProdutos.config(state=tk.DISABLED)
        self.txtProdutos.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.btnListarProdutos = tk.Button(self.aba_listagem, text='Listar Produtos', command=self.fListarProdutos)
        self.btnListarProdutos.grid(row=1, column=0, columnspan=2, pady=10)


    def fLerCampos(self):
        try:
            codigo = self.txtCodigo.get()
            if not codigo.isdigit():
                self.msgLabel.config(text='Código deve conter apenas números', fg='red')
                return None
            codigo = int(codigo)
            nome = self.txtNome.get()
            if not nome.isalnum():
                self.msgLabel.config(text='Nome deve conter apenas letras e números', fg='red')
                return None
            preco = self.txtPreco.get()
            try:
                preco = float(preco)
            except ValueError:
                self.msgLabel.config(text='Preço deve conter apenas números', fg='red')
                return None
            calculo_juros = self.txtCalculoJuros.get()
            try:
                calculo_juros = float(calculo_juros)
            except ValueError:
                self.msgLabel.config(text='Cálculo de Juros deve conter apenas números', fg='red')
                return None
            print('Leitura dos Dados com Sucesso!')
            self.msgLabel.config(text='', fg='black')
        except ValueError:
            self.msgLabel.config(text='Campos Código e Preço devem conter apenas números', fg='red')
            return None
        return codigo, nome, preco, calculo_juros

    def fCadastrarProduto(self):
        try:
            codigo, nome, preco, juros = self.fLerCampos()
            self.objBD.inserirDados(codigo, nome, preco, juros)
            self.fLimparTela()
            print('Produto Cadastrado com Sucesso!')
        except Exception as e:
            print('Não foi possível fazer o cadastro. Erro:', e)

    def fLimparTela(self):
        try:
            self.txtCodigo.delete(0, tk.END)
            self.txtNome.delete(0, tk.END)
            self.txtPreco.delete(0, tk.END)
            self.txtCalculoJuros.delete(0, tk.END)
            self.txtPrecoComJuros.delete(0, tk.END)
            print('Campos Limpos!')
        except:
            print('Não foi possível limpar os campos.')

    def fAtualizarProduto(self):
        try:
            codigo, nome, preco, juros = self.fLerCampos()

            preco_com_juros = preco + (preco * (juros / 100))

            self.txtPrecoComJuros.delete(0, tk.END)
            self.txtPrecoComJuros.insert(0, str(preco_com_juros))

            self.objBD.atualizarDados(codigo, nome, preco, juros)
            self.fLimparTela()
            print('Produto Atualizado com Sucesso!')
        except Exception as e:
            print('Não foi possível fazer a atualização. Erro:', e)

    def fExcluirProduto(self):
        try:
            codigo, nome, preco, _ = self.fLerCampos()
            self.objBD.excluirDados(codigo)
            self.fLimparTela()
            print('Produto Excluído com Sucesso!')
        except Exception as e:
            print('Não foi possível fazer a exclusão do produto. Erro:', e)

    def fCalcularJuros(self):
        try:
            result = self.fLerCampos()
            if result is not None:
                _, _, preco, calculo_juros = result

                preco_com_juros = preco + (preco * (calculo_juros / 100))
                
                self.txtPrecoComJuros.delete(0, tk.END)
                self.txtPrecoComJuros.insert(0, str(preco_com_juros))
        except Exception as e:
            print('Não foi possível calcular o juro. Erro:', e)

    def fListarProdutos(self):
        try:
            self.objBD.abrirConexao()
            cursor = self.objBD.connection.cursor()

            sql_select_query = """SELECT * FROM public."produto" """
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
          
            self.txtProdutos.config(state=tk.NORMAL)
            self.txtProdutos.delete('1.0', tk.END)

            for record in records:
                codigo, nome, preco, juros, preco_com_juros = record
                texto = f'Código: {codigo}, Nome: {nome}, Preço: {preco}, Juros: {juros},
                Preço com Juros: {preco_com_juros}\n'
                self.txtProdutos.insert(tk.END, texto)

            self.txtProdutos.config(state=tk.DISABLED)

        except Exception as e:
            print('Erro ao listar produtos:', e)
        finally:
            if self.objBD.connection:
                cursor.close()
                self.objBD.connection.close()
                print("A conexão com o PostgreSQL foi fechada")

if __name__ == "__main__":
    janelaPrograma = tk.Tk()
    Principal = PrincipalBD(janelaPrograma)
    janelaPrograma.title('Bem Vindo à Tela de Cadastro')
    janelaPrograma.geometry("1000x900")  
    
    janelaPrograma.eval('tk::PlaceWindow . center')

    janelaPrograma.mainloop()