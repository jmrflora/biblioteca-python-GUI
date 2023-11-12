import customtkinter as ctk
import tkinter as tk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('biblioteca GUI')
        self.geometry('1280x720')
        
       
    
    def login_screen(self):
        self.destroy()
        self.__init__()
        # variaveis
        fonte_titulo = ctk.CTkFont(size=55)
        
        # tk variables
        
        
        # layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=3, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        self.columnconfigure(0, weight=1)

        # widgets
        self.titulo_login = ctk.CTkLabel(self, text= "Login", font=fonte_titulo)
        self.frame_login = FrameLogin(self)

        
        # griding 
        self.titulo_login.grid(row=0, column=0)
        self.frame_login.grid(row=1, column=0, sticky="nsew")
        


class FrameLogin(ctk.CTkFrame):
    def __init__(self, parente):
        super().__init__(master=parente)
        # tk variables
        self.user_text_var = ctk.StringVar()
        self.passwd_text_var = ctk.StringVar()
        
        # layout
        self.rowconfigure(0, weight=4, uniform='b')
        self.rowconfigure(1, weight=1, uniform='b')
        self.columnconfigure(0, weight=1)

        EntryLoginFrame(self, self.user_text_var, self.passwd_text_var).grid(row=0, column=0, sticky="nsew")

        self.login_button = ctk.CTkButton(self,
                                          text="Login",
                                          width=150,
                                          height=40,
                                          font=("", 20),
                                          command= lambda: print(self.passwd_text_var.get())
                                          ).grid(row=1,column=0)


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


if __name__ == '__main__':
    app = App()
    app.login_screen()
    app.mainloop()
    
