
import requests

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter.filedialog import askopenfilename

import fitz
from PIL import ImageTk, Image

# from jinja2 import Environment, select_autoescape
# from jinja2.loaders import FileSystemLoader

import os
import webbrowser
import random
from os import startfile



class do_buys():
    def __init__(self) -> None:
    #def do_buys(self):
        self.do_buys = tk.Tk()
        self.do_buys.title('Shopping Cart')
        self.do_buys.geometry('370x470+650+150')

        self.txt_shop_qtt = tk.Label(self.do_buys, text = f"Quantity Items: ")
        self.txt_shop_qtt.place(x = 60, y=15)
        self.txt_shop_tt = tk.Label(self.do_buys, text = f"Total Price:")
        self.txt_shop_tt.place(x = 200, y=15)

        self.style = ttk.Style()
        self.style.theme_use("default")

        self.style.configure("Treeview", 
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
            )

        self.style.map('Treeview', background=[('selected', 'blue')])


        self.tree_frame2 = Frame(self.do_buys)
        self.tree_frame2.pack(pady=50)
        self.tree_scroll2 = Scrollbar(self.tree_frame2)
        self.tree_scroll2.pack(side=RIGHT, fill=Y)
        self.my_tree2 = ttk.Treeview(self.tree_frame2, yscrollcommand=self.tree_scroll2.set, selectmode="extended")
        self.my_tree2.pack()

        self.tree_scroll2.config(command=self.my_tree2.yview)

        self.my_tree2['columns'] = ("Id", "Name", "Category", "Price")

        self.my_tree2.column("#0", width=0, stretch=NO)
        self.my_tree2.column("Id", anchor=CENTER, width=50)
        self.my_tree2.column("Name", anchor=CENTER, width=100)
        self.my_tree2.column("Category", anchor=CENTER, width=100)
        self.my_tree2.column("Price", anchor=CENTER, width=50)

        self.my_tree2.heading("#0", text="", anchor=CENTER)
        self.my_tree2.heading("Id", text="Id", anchor=CENTER)
        self.my_tree2.heading("Name", text="Name",  anchor=CENTER)
        self.my_tree2.heading("Category", text="Category", anchor=CENTER)
        self.my_tree2.heading("Price", text="Price", anchor=CENTER)

        self.my_tree2.tag_configure('oddrow', background="white")
        self.my_tree2.tag_configure('evenrow', background="lightblue")

        # global count
        # count=0

        # x = requests.get(f'{base_url}/items')
        # datas = x.json()
        
        # for categoria in datas:
        #     for articulo in categoria:
        #         if count % 2 == 0:
        #             self.my_tree2.insert(parent='', index='end', iid=count, text="", values=(articulo['id'], articulo['nombre'], articulo['categoria'], articulo['precio']), tags=('evenrow',))
        #         else:
        #             self.my_tree2.insert(parent='', index='end', iid=count, text="", values=(articulo['id'], articulo['nombre'], articulo['categoria'], articulo['precio']), tags=('oddrow',))
        #         count += 1


        self.add_frame2 = Frame(self.do_buys)
        self.add_frame2.pack(pady=30)

        self.nl2 = Label(self.add_frame2, text="Id")
        self.nl2.grid(row=0, column=0)

        self.il2 = Label(self.add_frame2, text="Name")
        self.il2.grid(row=0, column=1)

        self.tl2 = Label(self.add_frame2, text="Category")
        self.tl2.grid(row=0, column=2)

        self.cl2 = Label(self.add_frame2, text="Price")
        self.cl2.grid(row=0, column=3)

        self.id_box2 = Entry(self.add_frame2)
        self.id_box2.grid(row=1, column=0)
        self.id_box2.config(width=12, state= "disabled")

        self.name_box2 = Entry(self.add_frame2)
        self.name_box2.grid(row=1, column=1)
        self.name_box2.config(width=12, state= "disabled")

        self.catgry_box2 = Entry(self.add_frame2)
        self.catgry_box2.grid(row=1, column=2)
        self.catgry_box2.config(width=12, state= "disabled")

        self.price_box2 = Entry(self.add_frame2)
        self.price_box2.grid(row=1, column=3)
        self.price_box2.config(width=12, state= "disabled")

        def select_record():
            try:
                    
                self.id_box2.config(state= "normal")
                self.name_box2.config(state= "normal")
                self.catgry_box2.config(state= "normal")
                self.price_box2.config(state= "normal")

                self.id_box2.delete(0, END)
                self.name_box2.delete(0, END)
                self.catgry_box2.delete(0, END)
                self.price_box2.delete(0, END)

                self.selected = self.my_tree2.focus()
                self.values = self.my_tree2.item(self.selected, 'values')

                self.id_box2.insert(0, self.values[0])
                self.name_box2.insert(0, self.values[1])
                self.catgry_box2.insert(0, self.values[2])
                self.price_box2.insert(0, self.values[3])

                self.id_box2.config(state= "disabled")
                self.name_box2.config(state= "disabled")
                self.catgry_box2.config(state= "disabled")
                self.price_box2.config(state= "disabled")

            except:
                pass

        # Create Binding Click function
        def clicker(e):
            select_record()

        # Bindings
        self.my_tree2.bind("<ButtonRelease-1>", clicker)

        self.btn_buy2 = Button(self.do_buys, width = 14, text="Delete")
        self.btn_buy2.place(x=60, y=330)

        self.btn_show2 = Button(self.do_buys, width = 14, text="Buy")
        self.btn_show2.place(x= 200, y=330)

        self.btn_buy2 = Button(self.do_buys, width = 14, text="Cancel")
        self.btn_buy2.place(x=60, y=365)

        self.btn_show2 = Button(self.do_buys, width = 14, text="Graphviz")
        self.btn_show2.place(x= 200, y=365)

        self.do_buys.resizable(0,0)
        self.do_buys.mainloop()


if __name__ == '__main__':
    do_buys()

