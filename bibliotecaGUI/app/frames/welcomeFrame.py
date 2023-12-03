import customtkinter as ctk
import tkinter as tk

from app.requisicoes.sessao import BackendTokenHandler
# from app.frames.frameLoginContainer import FrameLoginContainer

class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, parente, app_selecionar_frame):
        super().__init__(master=parente)

        # variaveis
        fonte_titulo = ctk.CTkFont(size=55)
        self.selecionar_frame = app_selecionar_frame

        # layout
        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1, uniform="d")
        self.columnconfigure((1,2,3), weight=2, uniform="d")
        self.columnconfigure(4, weight=1, uniform="d")

        # widgets
        self.bem_vindo = ctk.CTkLabel(self, text="Seja bem vindo", font=fonte_titulo).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        self.butaoLivros = ctk.CTkButton(self, text="consultar livros", width=180, height=40,font=("", 18), command= lambda: self.selecionar_frame("ConsultarLivrosFrame")).grid(row=0, column=1)
        self.butaoreservas = ctk.CTkButton(self, text="consultar reservas", width=180, height=40,font=("", 18)).grid(row=0, column=2)
        self.butaoemprestimos = ctk.CTkButton(self, text="consultar empréstimos", width=180, height=40,font=("", 18), command= lambda: self.selecionar_frame("ConsultarEmprestimosFrame")).grid(row=0, column=3)

        self.butaologout = ctk.CTkButton(self, text="sair", width=180, height=40,font=("", 18), command=lambda: self.logout(self=self)).place(relx = 0.5, rely=0.8, anchor=ctk.CENTER)
    
    def logout(args, self):
        sessao = BackendTokenHandler()
        sessao.close()
        
        self.selecionar_frame("FrameLoginContainer")