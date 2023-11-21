import customtkinter as ctk
import tkinter as tk
import requests
from CTkMenuBar import *

from app.frames.frameLoginContainer import FrameLoginContainer
from app.requisicoes.sessao import BackendTokenHandler
from app.frames.welcomeFrame import WelcomeFrame

ctk.set_appearance_mode("light")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title('biblioteca GUI')
        self.width = 1280
        self.height = 720
        self.geometry(str(self.width) + 'x' + str(self.height) + '+0+0')
        
        self.current_frame = None

        self.sessao = BackendTokenHandler()

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

        # ir adicionado frames aqui:
        for frame in (FrameLoginContainer, teste, WelcomeFrame):
            self.frames[frame] = frame(self.container, self.selecionar_frame_container)
            self.frames[frame].grid(row=0, column=0, sticky="nsew")

        # teste de troca de frames    
        button = ctk.CTkButton(master=self, text="teste", command=lambda: self.selecionar_frame_container(teste)) # type: ignore
        button.place(relx=0.1, rely=0.85)

        button2 = ctk.CTkButton(master=self, text="frame",
                                command=lambda: self.selecionar_frame_container(FrameLoginContainer)) # type: ignore
        button2.place(relx=0.3, rely=0.85)
        
        button3 = ctk.CTkButton(master=self, text="print", command=lambda: print(self.sessao.get_token()))
        button3.place(relx=0.5, rely=0.85)

    def selecionar_frame_container(self, frame: ctk.CTkFrame):
        # if self.current_frame:
        #     self.current_frame.grid_forget()  # Forget the current frame

        # self.current_frame = self.frames[frame]

        # self.current_frame.grid(row=0, column=0, sticky="nsew")  # Display the new frame

        # # Additional configuration to ensure the frame displays properly
        # self.current_frame.tkraise()
        # self.current_frame.update_idletasks()

        framevar: ctk.CTkFrame = self.frames[frame]

        framevar.tkraise()



class teste(ctk.CTkFrame):
    def __init__(self, parente, app_selecionar_frame):
        super().__init__(master=parente)


if __name__ == '__main__':
    app = App()
    # app.selecionar_frame_container(FrameLoginContainer)
    
    app.selecionar_frame_container(FrameLoginContainer) # type: ignore
    

    # app.selecionar_frame_container(teste)
    # app.selecionar_frame_container(FrameLoginContainer)
    app.mainloop()  # Keep mainloop at the end of your application's setup
