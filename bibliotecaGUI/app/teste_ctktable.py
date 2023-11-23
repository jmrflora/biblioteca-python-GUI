import customtkinter
from CTkTable import *

root = customtkinter.CTk()
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

class MyCustomCTkTable(CTkTable):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.column_visibility = [True] * self.columns

    def set_column_visibility(self, column_index, visible=True):
        """ Set the visibility of a specific column """
        if 0 <= column_index < self.columns:
            self.column_visibility[column_index] = visible
            self.redraw_table()

    def redraw_table(self):
        """ Redraw the table with updated visibility """
        for i in range(self.rows):
            for j in range(self.columns):
                widget = self.frame[i, j]
                if self.column_visibility[j]:
                    widget.grid(row=i, column=j, padx=self.padx, pady=self.pady, sticky="nsew")
                else:
                    widget.grid_forget()

false = False
# value = [[1,2,3,4,5],
#          [1,2,3,4,5],
#          [1,2,3,4,5],
#          [1,2,3,4,5],
#          [1,2,3,4,5]]

# table = CTkTable(master=root, row=5, column=5, values=value)
# table.pack(expand=True, fill="both", padx=20, pady=20)
values = [
    {
        "nome": "livro teste v4",
        "Autor": "jmrflora",
        "EP": False,
        "id": 2
    },
    {
        "nome": "moby dick",
        "Autor": "herman melville",
        "EP": False,
        "id": 4
    },
    {
        "nome": "os 3 mosqueteiros",
        "Autor": "pedro",
        "EP": False,
        "id": 5
    },
    {
        "nome": "1984",
        "Autor": "George Orwell",
        "EP": True,
        "id": 7
    },
    {
        "nome": "To Kill a Mockingbird",
        "Autor": "Harper Lee",
        "EP": False,
        "id": 9
    },
    {
        "nome": "The Great Gatsby",
        "Autor": "F. Scott Fitzgerald",
        "EP": True,
        "id": 11
    },
    {
        "nome": "Pride and Prejudice",
        "Autor": "Jane Austen",
        "EP": False,
        "id": 13
    },
    {
        "nome": "The Catcher in the Rye",
        "Autor": "J.D. Salinger",
        "EP": True,
        "id": 15
    },
    {
        "nome": "The Lord of the Rings",
        "Autor": "J.R.R. Tolkien",
        "EP": False,
        "id": 17
    },
        {
        "nome": "Harry Potter and the Sorcerer's Stone",
        "Autor": "J.K. Rowling",
        "EP": True,
        "id": 20
    },
    {
        "nome": "The Hobbit",
        "Autor": "J.R.R. Tolkien",
        "EP": False,
        "id": 22
    },
    {
        "nome": "The Da Vinci Code",
        "Autor": "Dan Brown",
        "EP": True,
        "id": 25
    },
    {
        "nome": "The Shining",
        "Autor": "Stephen King",
        "EP": False,
        "id": 28
    },
    {
        "nome": "The Alchemist",
        "Autor": "Paulo Coelho",
        "EP": True,
        "id": 30
    }
]

def comando(row, column, value):
    print(f"row{row}, column{column}, value{value}")

list_of_lists = [[book["nome"], book["Autor"], str(book["EP"]), str(book["id"])] for book in values]

teste_frame = customtkinter.CTkScrollableFrame(master=root)
teste_frame.grid(row=0, column=0, sticky="nsew")

teste_frame.bind_all("<Button-4>", lambda e: teste_frame._parent_canvas.yview("scroll", -1, "units"))
teste_frame.bind_all("<Button-5>", lambda e: teste_frame._parent_canvas.yview("scroll", 1, "units"))

table = MyCustomCTkTable(master=teste_frame, values=list_of_lists, row=len(values), column=4, command= lambda v:print(v))

table.set_column_visibility(3, visible=False)
print(table.get_row(0))


table.pack(expand=True, fill="both")

root.mainloop()