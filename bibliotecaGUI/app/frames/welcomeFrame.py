import customtkinter as ctk
import tkinter as tk

from app.requisicoes.sessao import BackendTokenHandler

class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, parente, app_selecionar_frame):
        super().__init__(master=parente)

        # variaveis
        fonte_titulo = ctk.CTkFont(size=55)

        # layout
        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1, uniform="d")
        self.columnconfigure((1,2,3), weight=2, uniform="d")
        self.columnconfigure(4, weight=1, uniform="d")

        # widgets
        butaoLivros = ctk.CTkButton(self, text="consultar livros").grid(row=0, column=1)