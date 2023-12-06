import customtkinter as ctk
import tkinter as tk

from app.requisicoes.sessao import BackendTokenHandler
# from app.frames.frameLoginContainer import FrameLoginContainer

class ConsultarEmprestimosAdmin(ctk.CTkFrame):
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
        self.bem_vindo = ctk.CTkLabel(self, text="Epréstimos", font=fonte_titulo).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        self.butao_criar_emprestimos = ctk.CTkButton(self, text="criar empréstimo", width=180, height=40,font=("", 18), command= lambda: self.selecionar_frame("CriarEmprestimos"))
        self.butao_criar_emprestimos.grid(row=0, column=1)
        self.butao_ver_emprestimos = ctk.CTkButton(self, text="consultar emprestimos", width=180, height=40,font=("", 18), command= lambda: self.selecionar_frame("VerEmprestimos"))
        self.butao_ver_emprestimos.grid(row=0, column=2)
        # self.butaoemprestimos = ctk.CTkButton(self, text="consultar empréstimos", width=180, height=40,font=("", 18), command= lambda: self.selecionar_frame("ConsultarEmprestimosFrame")).grid(row=0, column=3)

        self.butaologout = ctk.CTkButton(self, text="voltar", width=180, height=40,font=("", 18), command=lambda: self.logout(self=self)).place(relx = 0.5, rely=0.8, anchor=ctk.CENTER)
    
    def logout(args, self):
        self.selecionar_frame("WelcomeFrameAdmin")