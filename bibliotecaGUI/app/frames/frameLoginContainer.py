import customtkinter as ctk
import tkinter as tk
import requests
from CTkMessagebox import CTkMessagebox

from app.requisicoes.request_handler import RequestHandler
from app.requisicoes.sessao import BackendTokenHandler
# from app.frames.welcomeFrame import WelcomeFrame

class FrameLoginContainer(ctk.CTkFrame):
    def __init__(self, parente, app_adicionarFrames):
        super().__init__(master=parente)
        
        self.adicionar_frames = app_adicionarFrames

        # variaveis
        fonte_titulo = ctk.CTkFont(size=55)

        # layout container
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=3, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        self.columnconfigure(0, weight=1)

        # tk variables
        self.user_text_var = ctk.StringVar()
        self.passwd_text_var = ctk.StringVar()
        
        # widgets
        self.titulo_login = ctk.CTkLabel(self, text="Login", font=fonte_titulo)
        # sub frame 1
        self.sub_frame_login = ctk.CTkFrame(self)

        # layout subframe 1
        self.sub_frame_login.rowconfigure(0, weight=4, uniform='b')
        self.sub_frame_login.rowconfigure(1, weight=1, uniform='b')
        self.sub_frame_login.columnconfigure(0, weight=1)

        EntryLoginFrame(self.sub_frame_login, self.user_text_var, self.passwd_text_var).grid(row=0, column=0,
                                                                                             sticky="nsew")

        self.login_button = ctk.CTkButton(self.sub_frame_login,
                                          text="Login",
                                          width=150,
                                          height=40,
                                          font=("", 20),
                                          command= lambda: self.requestTeste(self.user_text_var.get(), self.passwd_text_var.get(), self)
                                          )
        
        self.login_button.grid(row=1, column=0)

        self.titulo_login.grid(row=0, column=0)
        
        self.sub_frame_login.grid(row=1, column=0, sticky="nsew")

    def requestTeste(args, username, passwd, self):

        self.login_button.configure(state="disabled")
    
        try:
            sessao = BackendTokenHandler()
            sessao.initialize_with_credentials(username=username, passwd=passwd)
            self.user_text_var.set("")
            self.passwd_text_var.set("")
            self.adicionar_frames()
            
        except:
            self.passwd_text_var.set("")
            msg = CTkMessagebox(master=self, title="Erro", message="Credenciais inválidas",
                        icon="warning", option_1="Ok")

        self.login_button.configure(state="normal")    


class EntryLoginFrame(ctk.CTkFrame):
    def __init__(self, parente, user_text, passwd_text):
        super().__init__(master=parente, fg_color="transparent")
        fonte_texto = ctk.CTkFont(size=30)

        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='c')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.user_label = ctk.CTkLabel(self, text='Usuário', font=fonte_texto).grid(row=0, column=1, stick="s")
        self.user_entry = ctk.CTkEntry(self, width=200, textvariable=user_text).grid(row=1, column=1, sticky='n')

        self.passwd_label = ctk.CTkLabel(self, text='Senha', font=fonte_texto).grid(row=2, column=1, stick="s")
        self.passwd_entry = ctk.CTkEntry(self, width=200, textvariable=passwd_text).grid(row=3, column=1, sticky='n')

