import customtkinter as ctk
import tkinter as tk
import requests

from app.requisicoes.request_handler import RequestHandler

class FrameLoginContainer(ctk.CTkFrame):
    def __init__(self, parente):
        super().__init__(master=parente)

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
                                          command=self.requestTeste
                                          ).grid(row=1, column=0)

        self.titulo_login.grid(row=0, column=0)
        self.sub_frame_login.grid(row=1, column=0, sticky="nsew")

    def requestTeste(*args):

        
        resposta = RequestHandler.make_post_request("auth/token", data={"username":"admin", "password":"1234"})
        
        for key, value in resposta.items():
            print(f"Key: {key}, Value: {value}")
        
        resposta = RequestHandler.make_get_request("/livros/")

        for book in resposta:
            for key, value in book.items():
                print(f"Key: {key}, Value: {value}")
        
        # print("request")

        # # Replace with your actual FastAPI server URL
        # base_url = "http://127.0.0.1:8000"

        # response = requests.get(f"{base_url}/")

        # if response.status_code == 200:
        #     resposta_json = response.json()
        #     for key, value in resposta_json.items():
        #         print(f"Key: {key}, Value: {value}")
        # else:
        #     print('Failed to get token:', response.status_code)
        #     return 0

        # # Define the login credentials
        # login_data = {
        #     'username': 'user@example.com',
        #     'password': 'user_password'
        # }

        # Make a POST request to get the access token
        # response = requests.post(f"{base_url}/token", data=login_data)

        # if response.status_code == 200:
        #     token = response.json()
        #     access_token = token['access_token']
        #     print('Access Token:', access_token)
        # else:
        #     print('Failed to get token:', response.status_code)
        #     return 0

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

