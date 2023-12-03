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

class ConsultarLivrosFrame(ctk.CTkFrame):
    def __init__(self, parente, app_selecionar_frame):
        super().__init__(master=parente)
        self.parente = parente

        # values = [
        #     {
        #         "nome": "livro teste v4",
        #         "Autor": "jmrflora",
        #         "EP": False,
        #         "id": 2
        #     },
        #     {
        #         "nome": "moby dick",
        #         "Autor": "herman melville",
        #         "EP": False,
        #         "id": 4
        #     },
        #     {
        #         "nome": "os 3 mosqueteiros",
        #         "Autor": "pedro",
        #         "EP": False,
        #         "id": 5
        #     },
        #     {
        #         "nome": "1984",
        #         "Autor": "George Orwell",
        #         "EP": True,
        #         "id": 7
        #     },
        #     {
        #         "nome": "To Kill a Mockingbird",
        #         "Autor": "Harper Lee",
        #         "EP": False,
        #         "id": 9
        #     },
        #     {
        #         "nome": "The Great Gatsby",
        #         "Autor": "F. Scott Fitzgerald",
        #         "EP": True,
        #         "id": 11
        #     },
        #     {
        #         "nome": "Pride and Prejudice",
        #         "Autor": "Jane Austen",
        #         "EP": False,
        #         "id": 13
        #     },
        #     {
        #         "nome": "The Catcher in the Rye",
        #         "Autor": "J.D. Salinger",
        #         "EP": True,
        #         "id": 15
        #     },
        #     {
        #         "nome": "The Lord of the Rings",
        #         "Autor": "J.R.R. Tolkien",
        #         "EP": False,
        #         "id": 17
        #     },
        #         {
        #         "nome": "Harry Potter and the Sorcerer's Stone",
        #         "Autor": "J.K. Rowling",
        #         "EP": True,
        #         "id": 20
        #     },
        #     {
        #         "nome": "The Hobbit",
        #         "Autor": "J.R.R. Tolkien",
        #         "EP": False,
        #         "id": 22
        #     },
        #     {
        #         "nome": "The Da Vinci Code",
        #         "Autor": "Dan Brown",
        #         "EP": True,
        #         "id": 25
        #     },
        #     {
        #         "nome": "The Shining",
        #         "Autor": "Stephen King",
        #         "EP": False,
        #         "id": 28
        #     },
        #     {
        #         "nome": "The Alchemist",
        #         "Autor": "Paulo Coelho",
        #         "EP": True,
        #         "id": 30
        #     }
        # ]
        # list_of_lists = [[book["nome"], book["Autor"], str(book["EP"]), str(book["id"])] for book in values]

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
        self.butaologout = ctk.CTkButton(self, text="voltar", width=180, height=40,font=("", 18), command=lambda: self.selecionar_frame("WelcomeFrame"))
        self.butaologout.place(relx=0.5, rely=0.85, anchor="center")
        self.butao_disponibilidade = ctk.CTkButton(self, text="disponibilidade", width=180, height=40, font=("", 18),state="disabled", command=lambda: self.check_disponibilidade(self=self))
        self.butao_disponibilidade.place(relx=0.2, rely=0.85, anchor="center")

    def click(args, v, self):
        print(v)
        self.livro_id = self.table.get(row=v.get("row"), column=3)

        self.selecionarlivro(v.get("row"))
        
    def selecionarlivro(self, row):
        if self.clicked_row == None:
            self.table.select_row(row)
            self.clicked_row = row
            self.butao_disponibilidade.configure(state="normal")
        else:
            self.table.deselect_row(self.clicked_row)
            self.butao_disponibilidade.configure(state="disabled")
            if row == self.clicked_row:
                self.clicked_row = None
            else:
                self.table.select_row(row)
                self.clicked_row = row
                self.butao_disponibilidade.configure(state="normal")

    def check_disponibilidade(arg, self):
        resposta: dict = self.sessao.make_authenticated_request("GET", f"/livros/disponibilidade/{self.livro_id}")

        if resposta.get("disponivel"):
            CTkMessagebox(master=self, title="Disponível", message="Livro disponível para empréstimo",
                        icon="check", option_1="Ok")
        else:
            CTkMessagebox(master=self, title="Em falta", message="Livro não disponível para empréstimo",
                        icon="cancel", option_1="Ok")




                
            
