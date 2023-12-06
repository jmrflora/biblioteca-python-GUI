import customtkinter as ctk
import tkinter as tk
from app.CTkScrollableDropdown import *
from CTkMessagebox import CTkMessagebox

from app.requisicoes.sessao import BackendTokenHandler

class CriarEmprestimos(ctk.CTkFrame):
    def __init__(self, parente, app_selecionar_frame):
        super().__init__(master=parente)
        fonte_texto = ctk.CTkFont(size=20)
        self.app_selecionar_frame = app_selecionar_frame
        values = ["python","tkinter","customtkinter","widgets",
          "options","menu","combobox","dropdown","search"]

        sessao = BackendTokenHandler()

        self.livros_resposta = sessao.make_authenticated_request("GET", "/livros")
        self.lista_nomes_livros = []
        for livro in self.livros_resposta:
            self.lista_nomes_livros.append(livro.get("nome"))
        
        self.usuarios_resposta = sessao.make_authenticated_request("GET", "/usuarios/cliente/all")
        self.lista_usuarios = []
        for usuario in self.usuarios_resposta:
            self.lista_usuarios.append(usuario.get("nome"))

        self.rowconfigure(0, weight=1, uniform='c')
        self.rowconfigure((1, 2, 3, 4), weight=1, uniform='c')
        self.rowconfigure(5, weight=2, uniform='c')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.livro_str_var = ctk.StringVar()
        self.usuario_str_var = ctk.StringVar()

        # self.user_entry = ctk.CTkEntry(self, width=200, textvariable=user_text).grid(row=1, column=1, sticky='n')

        self.nome_livro_label = ctk.CTkLabel(self, text='Nome do livro', font=fonte_texto)
        self.nome_livro_label.grid(row=1, column=1, stick="s")
        self.combobox_livro = ctk.CTkComboBox(self, width=200, variable=self.livro_str_var)
        self.combobox_livro.grid(row=2, column=1, sticky='n')

        CTkScrollableDropdown(self.combobox_livro, values=self.lista_nomes_livros, justify="left", button_color="transparent", autocomplete=True)
        
        self.nome_usuario_label = ctk.CTkLabel(self, text='Nome do usuario', font=fonte_texto)
        self.nome_usuario_label.grid(row=3, column=1, stick="s")
        self.combobox_usuario = ctk.CTkComboBox(self, width=200, variable=self.usuario_str_var)
        self.combobox_usuario.grid(row=4, column=1, sticky='n')

        CTkScrollableDropdown(self.combobox_usuario, values=self.lista_usuarios, justify="left", button_color="transparent", autocomplete=True)

        self.butao_confirmar = ctk.CTkButton(self, text="confirma", width=180, height=40,font=("", 18), command=lambda:self.metodo(self=self))
        self.butao_confirmar.grid(row=5, column=1)
        

        self.butao_voltar = ctk.CTkButton(self, text="voltar", width=180, height=40,font=("", 18), command=lambda:self.voltar(self=self))
        self.butao_voltar.grid(row=5, column=2)
    
    def voltar(arg, self):
        self.app_selecionar_frame("ConsultarEmprestimosAdmin")
    
    def metodo(arg,self):
        try:
            sessao = BackendTokenHandler()
            livro_id:int = None
            for livro in self.livros_resposta:
                print(f"nome do livro:{livro.get('nome')}, livro var: {self.combobox_livro.get()}")
                if livro.get("nome") == self.combobox_livro.get():
                    print("ola")
                    livro_id = livro.get("id")
                    break
            
            resposta_disponibilidade = sessao.make_authenticated_request("GET", f"/livros/disponibilidade/{livro_id}")
            print(resposta_disponibilidade)
            exemplar_id = resposta_disponibilidade.get("exemplar")
            
            for usuario in self.usuarios_resposta:
                if usuario.get("nome") == self.combobox_usuario.get():
                    usuario_id:int = usuario.get("id")
                    break
            
            data = {"exemplar_id": exemplar_id, "usuario_id": usuario_id}
            print(data)
            resposta = sessao.make_authenticated_request("POST", "/emprestimos/", data=data)
            print(resposta)

            msg = CTkMessagebox(master=self, title="ok", message="tudo ok",
                        icon="check", option_1="ok")
    
            if msg.get()=="ok":
                self.combobox_livro.set("")
                self.combobox_usuario.set("")
        except Exception as e:
            msg = CTkMessagebox(master=self, title="Erro", message=str(e),
                        icon="cancel", option_1="ok")
            if msg.get()=="ok":
                self.combobox_livro.set("")
                self.combobox_usuario.set("")
            