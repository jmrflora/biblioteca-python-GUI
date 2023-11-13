import customtkinter as ctk
import tkinter as tk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('biblioteca GUI')
        
        self.width= 1280
        self.height= 720
        self.geometry(str(self.width) + 'x' + str(self.height) + '+0+0')
        
        self.current_frame = None
        
        #The container is a frame that contains the projects's frames
        self.container = tk.Frame(self, 
                                height=self.height, 
                                width=self.width)

        #Pack the container to the root
        self.container.pack(side="top", fill="both", expand=True)

        #Fixes pack location of the container using grid
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        # ir adicionado frames aqui:
        for frame in (FrameLoginContainer, teste):
            self.frames[frame] = frame(self.container)
            self.frames[frame].grid(row=0, column=0, sticky= "nsew")
        
        # teste de troca de frames    
        button = ctk.CTkButton( master= self,text="teste", command= lambda: self.selecionar_frame_container(teste))
        button.place(relx=0.1, rely=0.85)
        
        button2 = ctk.CTkButton( master= self,text="frame", command= lambda: self.selecionar_frame_container(FrameLoginContainer))
        button2.place(relx=0.3, rely=0.85)
        
    
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
        self.titulo_login = ctk.CTkLabel(self, text= "Login", font=fonte_titulo)
        # sub frame 1
        self.sub_frame_login = ctk.CTkFrame(self)
        
        # layout subframe 1
        self.sub_frame_login.rowconfigure(0, weight=4, uniform='b')
        self.sub_frame_login.rowconfigure(1, weight=1, uniform='b')
        self.sub_frame_login.columnconfigure(0, weight=1)

        EntryLoginFrame(self.sub_frame_login, self.user_text_var, self.passwd_text_var).grid(row=0, column=0, sticky="nsew")

        self.login_button = ctk.CTkButton(self.sub_frame_login,
                                          text="Login",
                                          width=150,
                                          height=40,
                                          font=("", 20),
                                          command= lambda: print(self.passwd_text_var.get())
                                          ).grid(row=1,column=0)

        self.titulo_login.grid(row=0, column=0)
        self.sub_frame_login.grid(row=1, column=0, sticky="nsew")


class EntryLoginFrame(ctk.CTkFrame):
    def __init__(self, parente, user_text, passwd_text):
        super().__init__(master=parente, fg_color="transparent")
        fonte_texto = ctk.CTkFont(size=30)

        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='c')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.user_label = ctk.CTkLabel(self, text='Usuário', font=fonte_texto).grid(row=0, column=1, stick= "s")
        self.user_entry = ctk.CTkEntry(self, width=200, textvariable=user_text).grid(row=1, column=1, sticky = 'n')

        self.passwd_label= ctk.CTkLabel(self, text='Senha', font=fonte_texto).grid(row=2, column=1, stick= "s")
        self.passwd_entry= ctk.CTkEntry(self, width=200, textvariable=passwd_text).grid(row=3, column=1, sticky = 'n')

class teste(ctk.CTkFrame):
    def __init__(self, parente):
        super().__init__(master=parente)
        

if __name__ == '__main__':
    app = App()
    # app.selecionar_frame_container(FrameLoginContainer)
    
    app.selecionar_frame_container(FrameLoginContainer)
    app.selecionar_frame_container(teste)
    app.selecionar_frame_container(FrameLoginContainer)
    app.mainloop()  # Keep mainloop at the end of your application's setup
    
    
    
