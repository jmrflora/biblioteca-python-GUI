import customtkinter as ctk
import tkinter as tk
from CTkTable import *
from CTkMessagebox import CTkMessagebox

from app.requisicoes.sessao import BackendTokenHandler
# from app.frames.frameLoginContainer import FrameLoginContainer

class MyCustomCTkTable(CTkTable):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
      
    def get(self, row=None, column=None):
        if row != None and column != None:
            return self.data[row,column]["value"]
        else:
            return self.values

class FormLivro(ctk.CTkToplevel):
    def __init__(self, parente, titulo_var, autor_var, ep_var, livro_id):
        super().__init__(master=parente)
        self.parente = parente
        self.geometry("500x400")

        # widgets
        nome_label = ctk.CTkLabel(self, text="Título")
        self.titulo_entry = ctk.CTkEntry(self, textvariable=titulo_var)
        autor_label = ctk.CTkLabel(self, text="Autor")
        self.autor_entry = ctk.CTkEntry(self, textvariable=autor_var)
        ep_label = ctk.CTkLabel(self, text="EP")
        # self.ep_entry = ctk.CTkEntry(self, textvariable=ep_var)
        self.ep_entry = ctk.CTkOptionMenu(self,values=["true", "false"], variable=ep_var)
        
        # draw
        nome_label.pack(pady=10)
        self.titulo_entry.pack()
        autor_label.pack(pady=10)
        self.autor_entry.pack()
        ep_label.pack(pady=10)
        self.ep_entry.pack()
    


class ConsultarLivrosFrameAdmin(ctk.CTkFrame):
    def __init__(self, parente, app_selecionar_frame):
        super().__init__(master=parente)
        self.parente = parente
        # variaveis
        self.clicked_row = None
        self.sessao = BackendTokenHandler()
        self.livro_id = None
        self.valueslivros = self.sessao.make_authenticated_request("GET", "/livros/")
        list_of_lists = [[book["nome"], book["Autor"], str(book["EP"]), str(book["id"])] for book in self.valueslivros]
        self.selecionar_frame = app_selecionar_frame
        # layout
        self.rowconfigure(0, weight=4, uniform="e")
        self.rowconfigure(1, weight=1, uniform="e")
        self.columnconfigure(0, weight=1)

        # widgets
        self.scrollframe = ctk.CTkScrollableFrame(master=self)
        self.scrollframe.grid(row=0, column=0, sticky="nsew")
        self.scrollframe.bind_all("<Button-4>", lambda e: self.scrollframe._parent_canvas.yview("scroll", -1, "units"))
        self.scrollframe.bind_all("<Button-5>", lambda e: self.scrollframe._parent_canvas.yview("scroll", 1, "units"))

        self.table = MyCustomCTkTable(master=self.scrollframe, values=list_of_lists, row=len(self.valueslivros),corner_radius=0, column=4, command= lambda v:self.click(self=self, v=v))
        
        self.table.pack(expand=True, fill="both")
        self.butaologout = ctk.CTkButton(self, text="voltar", width=180, height=40,font=("", 18), command=lambda: self.selecionar_frame("WelcomeFrameAdmin"))
        self.butaologout.place(relx=0.5, rely=0.85, anchor="center")
        self.butao_disponibilidade = ctk.CTkButton(self, text="disponibilidade", width=180, height=40, font=("", 18),state="disabled", command=lambda: self.check_disponibilidade(self=self))
        self.butao_disponibilidade.place(relx=0.2, rely=0.85, anchor="center")

        self.butao_editar = ctk.CTkButton(self, text="Editar", width=180, height=40, font=("", 18),state="disabled", command=lambda: self.editar_livro(self=self))
        self.butao_editar.place(relx=0.8, rely=0.85, anchor="center")


    def click(args, v, self):
        print(v)
        self.livro_id = self.table.get(row=v.get("row"), column=3)

        self.selecionarlivro(v.get("row"))
        
    def selecionarlivro(self, row):
        if self.clicked_row == None:
            self.table.select_row(row)
            self.clicked_row = row
            self.butao_disponibilidade.configure(state="normal")
            self.butao_editar.configure(state="normal")
        else:
            self.table.deselect_row(self.clicked_row)
            self.butao_disponibilidade.configure(state="disabled")
            self.butao_editar.configure(state="disabled")
            if row == self.clicked_row:
                self.clicked_row = None
            else:
                self.table.select_row(row)
                self.clicked_row = row
                self.butao_disponibilidade.configure(state="normal")
                self.butao_editar.configure(state="normal")

    def check_disponibilidade(arg, self):
        resposta: dict = self.sessao.make_authenticated_request("GET", f"/livros/disponibilidade/{self.livro_id}")

        if resposta.get("disponivel"):
            CTkMessagebox(master=self, title="Disponível", message="Livro disponível para empréstimo",
                        icon="check", option_1="Ok")
        else:
            CTkMessagebox(master=self, title="Em falta", message="Livro não disponível para empréstimo",
                        icon="cancel", option_1="Ok")

    def editar_livro(arg, self):
        row = self.clicked_row
        titulo_var = ctk.StringVar(value=self.table.get(row=row, column=0))
        autor_var = ctk.StringVar(value=self.table.get(row=row, column=1))
        ep_var = ctk.StringVar(value=self.table.get(row=row, column=2))

        self.novoForm = FormLivro(parente=self, titulo_var=titulo_var, autor_var=autor_var, ep_var=ep_var, livro_id=self.livro_id)
        self.novoForm.grab_set()

        self.confirmar_butao = ctk.CTkButton(self.novoForm, text="ok", command=lambda: self.metodo(titulo_var,autor_var,ep_var,self.livro_id))
        self.confirmar_butao.pack(pady=50)

    def metodo(self,titulo_var,autor_var,ep_var,livro_id):
        data = {"nome": titulo_var.get(),
                "Autor": autor_var.get(),
                "EP": ep_var.get()
                }
        print(data)
        sessao = BackendTokenHandler()
        resposta = sessao.make_authenticated_request("PATCH", f"/livros/{livro_id}/", data=data)
        print(resposta)
        self.atualizar_tabela()
        self.novoForm.destroy()

    def atualizar_tabela(self):
        self.valueslivros = self.sessao.make_authenticated_request("GET", "/livros/")
        list_of_lists = [[book["nome"], book["Autor"], str(book["EP"]), str(book["id"])] for book in self.valueslivros]
        self.table.destroy()
        self.table = MyCustomCTkTable(master=self.scrollframe, values=list_of_lists, row=len(self.valueslivros),corner_radius=0, column=4, command= lambda v:self.click(self=self, v=v))
        self.table.pack(expand=True, fill="both")

                
            
