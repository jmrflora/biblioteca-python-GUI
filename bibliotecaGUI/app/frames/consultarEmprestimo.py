import customtkinter as ctk
import tkinter as tk
from CTkTable import *
from CTkMessagebox import CTkMessagebox
from datetime import datetime

from app.requisicoes.sessao import BackendTokenHandler


class MyCustomCTkTable(CTkTable):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
      
    def get(self, row=None, column=None):
        if row != None and column != None:
            return self.data[row,column]["value"]
        else:
            return self.values

class ConsultarEmprestimosFrame(ctk.CTkFrame):
    def __init__(self, parente, app_selecionar_frame):
        super().__init__(master=parente)
        self.parente = parente

        # variaveis
        self.clicked_row = None
        self.sessao = BackendTokenHandler()
        self.livro_id = None
        self.valuesemprestimos :list[dict] = self.sessao.make_authenticated_request("GET", "/emprestimos/me")
        self.lista_de_listas = []
        for emprestimo in self.valuesemprestimos:
            exemplar_id = emprestimo.get("exemplar_id")
            usuario_id = emprestimo.get("usuario_id")
            emprestimo_id = emprestimo.get("id")
            timestamp = emprestimo.get("created_at")
            dt_object = datetime.fromisoformat(timestamp)
            created_at = dt_object.strftime("%B %d")
            self.lista_de_listas.append([emprestimo_id, usuario_id, exemplar_id, created_at])
            
        self.selecionar_frame = app_selecionar_frame
        # layout
        self.rowconfigure(0, weight=4, uniform="f")
        self.rowconfigure(1, weight=1, uniform="f")
        self.columnconfigure(0, weight=1)

        # widgets
        # scrollframe
        self.scrollframe = ctk.CTkScrollableFrame(master=self)
        self.scrollframe.grid(row=0, column=0, sticky="nsew")
        self.scrollframe.bind_all("<Button-4>", lambda e: self.scrollframe._parent_canvas.yview("scroll", -1, "units"))
        self.scrollframe.bind_all("<Button-5>", lambda e: self.scrollframe._parent_canvas.yview("scroll", 1, "units"))
        # tabela
        self.table = MyCustomCTkTable(master=self.scrollframe, values=self.lista_de_listas, row=len(self.valuesemprestimos),corner_radius=0, column=4, command= lambda v:self.click(self=self, v=v))
        self.table.pack(expand=True, fill="both")
        # butoes
        self.butaologout = ctk.CTkButton(self, text="voltar", width=180, height=40,font=("", 18), command=lambda: self.selecionar_frame("WelcomeFrame"))
        self.butaologout.place(relx=0.5, rely=0.85, anchor="center")
        