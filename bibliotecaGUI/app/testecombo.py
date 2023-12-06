import customtkinter

app = customtkinter.CTk()

combobox_var = customtkinter.StringVar(value="option 2")  # set initial value

def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

combobox = customtkinter.CTkComboBox(master=app,
                                     values=["option 1", "option 2"],
                                     command=combobox_callback,
                                     variable=combobox_var)
combobox.pack(padx=20, pady=10)

app.mainloop()