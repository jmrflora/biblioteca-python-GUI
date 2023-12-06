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

# class FormLivro(ctk.CTkToplevel):
#     def __init__(self, parente, titulo_var, autor_var, ep_var, livro_id):
#         super().__init__(master=parente)
#         self.parente = parente
#         self.geometry("500x400")

#         # widgets
#         nome_label = ctk.CTkLabel(self, text="Título")
#         self.titulo_entry = ctk.CTkEntry(self, textvariable=titulo_var)
#         autor_label = ctk.CTkLabel(self, text="Autor")
#         self.autor_entry = ctk.CTkEntry(self, textvariable=autor_var)
#         ep_label = ctk.CTkLabel(self, text="EP")
#         # self.ep_entry = ctk.CTkEntry(self, textvariable=ep_var)
#         self.ep_entry = ctk.CTkOptionMenu(self,values=["true", "false"], variable=ep_var)
        
#         # draw
#         nome_label.pack(pady=10)
#         self.titulo_entry.pack()
#         autor_label.pack(pady=10)
#         self.autor_entry.pack()
#         ep_label.pack(pady=10)
#         self.ep_entry.pack()
    


class VerEmprestimos(ctk.CTkFrame):
    def __init__(self, parente, app_selecionar_frame):
        super().__init__(master=parente)
        self.parente = parente
        # variaveis

        # self.clicked_row = None
        self.sessao = BackendTokenHandler()
        # self.livro_id = None
        # self.valueslivros = self.sessao.make_authenticated_request("GET", "/livros/")
        # list_of_lists = [[book["nome"], book["Autor"], str(book["EP"]), str(book["id"])] for book in self.valueslivros]
        
        self.resposta_emprestimos = self.sessao.make_authenticated_request("GET", "/emprestimos/")
        self.lista_emprestimos = []
        for emprestimo in self.resposta_emprestimos:
            
            self.lista_emprestimos.append([str(emprestimo.get("id")), str(emprestimo.get("usuario_id")), str(emprestimo.get("exemplar_id"))])

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
      
        self.table = MyCustomCTkTable(master=self.scrollframe, values=self.lista_emprestimos, row=len(self.lista_emprestimos),corner_radius=0, column=3)
        self.table.pack(expand=True, fill="both")

        self.botao_voltar = ctk.CTkButton(self, text="voltar", width=180, height=40,font=("", 18), command=lambda: self.selecionar_frame("ConsultarEmprestimosAdmin"))
        self.botao_voltar.place(relx=0.5, rely=0.85, anchor="center")
        
    # def atualizar_tabela(self):
    #     self.valueslivros = self.sessao.make_authenticated_request("GET", "/livros/")
    #     list_of_lists = [[book["nome"], book["Autor"], str(book["EP"]), str(book["id"])] for book in self.valueslivros]
    #     self.table.destroy()
    #     self.table = MyCustomCTkTable(master=self.scrollframe, values=list_of_lists, row=len(self.valueslivros),corner_radius=0, column=4, command= lambda v:self.click(self=self, v=v))
    #     self.table.pack(expand=True, fill="both")

                
            
