import customtkinter as ctk
import tkinter as tk
import requests
from CTkMenuBar import *
from app.frames.consultarEmprestimo import ConsultarEmprestimosFrame

from app.frames.frameLoginContainer import FrameLoginContainer
from app.requisicoes.sessao import BackendTokenHandler
from app.frames.welcomeFrame import WelcomeFrame
from app.frames.consultarLivors import ConsultarLivrosFrame

ctk.set_appearance_mode("light")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title('biblioteca GUI')
        self.width = 1280
        self.height = 720
        self.geometry(str(self.width) + 'x' + str(self.height) + '+0+0')
        
        self.current_frame = None
        self.sessao = BackendTokenHandler("http://127.0.0.1:8000", token_endpoint="auth/token", refresh_token_endpoint="auth/refresh")

        # todo: funcionalidade interessante
        self.menu = CTkMenuBar(self)
        button_1 = self.menu.add_cascade("File")
        button_2 = self.menu.add_cascade("Edit")
        button_3 = self.menu.add_cascade("Settings")
        button_4 = self.menu.add_cascade("About")

        # The container is a frame that contains the projects's frames
        self.container = tk.Frame(self,
                                  height=self.height,
                                  width=self.width)

        # Pack the container to the root
        self.container.pack(side="top", fill="both", expand=True)

        # Fixes pack location of the container using grid
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames[FrameLoginContainer.__name__] = FrameLoginContainer(self.container, self.add_frames)
        self.frames[FrameLoginContainer.__name__].grid(row=0, column=0, sticky="nsew")

        self.selecionar_frame_container(FrameLoginContainer.__name__)

        # ir adicionado frames aqui:
        # for frame in (FrameLoginContainer, teste, WelcomeFrame):
        #     self.frames[frame.__name__] = frame(self.container, self.selecionar_frame_container)
        #     self.frames[frame.__name__].grid(row=0, column=0, sticky="nsew")

        # teste de troca de frames    
        # button = ctk.CTkButton(master=self, text="teste", command=lambda: self.selecionar_frame_container("teste")) # type: ignore
        # button.place(relx=0.1, rely=0.85)

        # button2 = ctk.CTkButton(master=self, text="frame",
        #                         command=lambda: self.selecionar_frame_container("FrameLoginContainer")) # type: ignore
        # button2.place(relx=0.3, rely=0.85)
        
        # button3 = ctk.CTkButton(master=self, text="print", command=lambda: print(self.sessao.get_token()))
        # button3.place(relx=0.5, rely=0.85)

    def add_frames(self):

        tipo = self.sessao.get_tipo()
        if tipo == "cliente":
            for frame in (WelcomeFrame,ConsultarLivrosFrame, ConsultarEmprestimosFrame):
                print(frame.__name__)
                self.frames[frame.__name__] = frame(self.container, self.selecionar_frame_container)
                self.frames[frame.__name__].grid(row=0, column=0, sticky="nsew")

            self.selecionar_frame_container(WelcomeFrame.__name__)
        else:
            print("ola admin")

    def logout(self):
        # Get the existing FrameLoginContainer instance
        frame_var = self.frames.pop(FrameLoginContainer, None)

        # Check if an instance exists before destroying it
        if frame_var:
            frame_var.destroy()

        # Create and show a new instance of FrameLoginContainer
        self.frames[FrameLoginContainer] = FrameLoginContainer(self.container, self.selecionar_frame_container)
        self.frames[FrameLoginContainer].grid(row=0, column=0, sticky="nsew")

        # Additional cleanup steps (if needed)

        # Switch to the login frame
        self.selecionar_frame_container(FrameLoginContainer)

    def selecionar_frame_container(self, frame_name):
        # fazer com que sempre que selecionar login todos os outros frames sejam apagados
        if frame_name == FrameLoginContainer.__name__:
            novo_frames = {frame_name: self.frames[frame_name]}
            self.frames.clear()
            self.frames.update(novo_frames)
            self.frames[FrameLoginContainer.__name__].grid(row=0, column=0, sticky="nsew")

        framevar: ctk.CTkFrame = self.frames[frame_name]

        framevar.tkraise()



class teste(ctk.CTkFrame):
    def __init__(self, parente, app_selecionar_frame):
        super().__init__(master=parente)


if __name__ == '__main__':
    app = App()
    
    # app.selecionar_frame_container(FrameLoginContainer.__name__) # type: ignore
    app.mainloop()  # Keep mainloop at the end of your application's setup
