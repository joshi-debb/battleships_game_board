
from blockchain import Blockchain
from tabla_hash import Tabla_Hash, L_Simple
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

base_url = "http://localhost:5000"

active_user = ""
active_pass = ""
active_id = 10
user_life = 3
user_tokens = 0
game_over = False
game_over2 = False
src_objects = ""

invited_life = 3
invited_name = ""
invited_tokens = 0

prefijo = ""

#matrix Size
matrix_size = 10

#Colores
Shot = 'purple:pink'
Maroon = '#800000'
Navy = '#4B68B8'
Gray = '#808080'
Teal = '#008080'
withe = '#FFFFFF'
Fill = 'red:violet'

Row_c = '#1CD6CE'
Col_c = '#FEDB39'
Org_c = '#D61C4E'

#Cant Barcos      
portaviones  = 0
submarinos = 0
destructores = 0
buques = 0

#Cant Barcos Generados
rec_pa = 0
rec_sb = 0
rec_dt = 0
rec_bq = 0

#Cant Barcos Destruidos
rec_pa_d1 = 0
rec_sb_d1 = 0
rec_dt_d1 = 0
rec_bq_d1 = 0

rec_pa_d2 = 0
rec_sb_d2 = 0
rec_dt_d2 = 0
rec_bq_d2 = 0


count=0

total_price = 0
cant_cart = 0

#---------------------------NODO ENCABEZADO PARA MATRIZ DISPERSA
class Nodo_Encabezado():
    def __init__(self, id):
        self.id: int = int(id)
        self.siguiente = None
        self.anterior = None

        self.acceso = None

#---------------------------LISTA ENCABEZADO PARA MATRIZ DISPERSA
class Lista_Encabezado():
    def __init__(self, tipo):
        self.primero: Nodo_Encabezado = None
        self.ultimo: Nodo_Encabezado = None
        self.tipo = tipo
        self.size = 0

    def insertar_nodoEncabezado(self, nuevo):
        self.size += 1
        if self.primero == None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            if nuevo.id < self.primero.id:
                nuevo.siguiente = self.primero
                self.primero.anterior = nuevo
                self.primero = nuevo
            elif nuevo.id > self.ultimo.id:
                self.ultimo.siguiente = nuevo
                nuevo.anterior = self.ultimo
                self.ultimo = nuevo
            else:
                tmp: Nodo_Encabezado = self.primero
                while tmp != None:
                    if nuevo.id < tmp.id:
                        nuevo.siguiente = tmp
                        nuevo.anterior = tmp.anterior
                        tmp.anterior.siguiente = nuevo
                        tmp.anterior = nuevo
                        break
                    elif nuevo.id > tmp.id:
                        tmp = tmp.siguiente
                    else:
                        break

    def getEncabezado(self, id) -> Nodo_Encabezado:
        tmp = self.primero
        while tmp != None:
            if id == tmp.id:
                return tmp
            tmp = tmp.siguiente
        return None

#---------------------------NODO INTERNO PARA MATRIZ DISPERSA
class Nodo_Interno():
    def __init__(self, x, y, caracter, color):
        self.caracter = caracter
        self.coordenadaX = int(x)
        self.coordenadaY = int(y)
        self.color = color

        self.arriba = None
        self.abajo = None
        self.derecha = None
        self.izquierda = None
        

#--------------------------- MATRIZ DISPERSA
class MatrizDispersa():
    def __init__(self, capa):
        self.capa = capa
        self.filas = Lista_Encabezado('fila')
        self.columnas = Lista_Encabezado('columna')

        global matrix_size

        for i in range(1,matrix_size+1):
            nodo_X = self.filas.getEncabezado(i)
            nodo_Y = self.columnas.getEncabezado(i)

            if nodo_X == None:
                nodo_X = Nodo_Encabezado(i)
                self.filas.insertar_nodoEncabezado(nodo_X)

            if nodo_Y == None:
                nodo_Y = Nodo_Encabezado(i)
                self.columnas.insertar_nodoEncabezado(nodo_Y)


    def insert(self, pos_x, pos_y, caracter, color):
        nuevo = Nodo_Interno(pos_x, pos_y, caracter, color)
        nodo_X = self.filas.getEncabezado(pos_x)
        nodo_Y = self.columnas.getEncabezado(pos_y)

        if nodo_X == None:
            nodo_X = Nodo_Encabezado(pos_x)
            self.filas.insertar_nodoEncabezado(nodo_X)

        if nodo_Y == None:
            nodo_Y = Nodo_Encabezado(pos_y)
            self.columnas.insertar_nodoEncabezado(nodo_Y)

        

        if nodo_X.acceso == None:
            nodo_X.acceso = nuevo
        else:
            if nuevo.coordenadaY < nodo_X.acceso.coordenadaY:
                nuevo.derecha = nodo_X.acceso              
                nodo_X.acceso.izquierda = nuevo
                nodo_X.acceso = nuevo
            else:
                tmp : Nodo_Interno = nodo_X.acceso 
                while tmp != None:
                    if nuevo.coordenadaY < tmp.coordenadaY:
                        nuevo.derecha = tmp
                        nuevo.izquierda = tmp.izquierda
                        tmp.izquierda.derecha = nuevo
                        tmp.izquierda = nuevo
                        break;
                    elif nuevo.coordenadaX == tmp.coordenadaX and nuevo.coordenadaY == tmp.coordenadaY:
                        break;
                    else:
                        if tmp.derecha == None:
                            tmp.derecha = nuevo
                            nuevo.izquierda = tmp
                            break;
                        else:
                            tmp = tmp.derecha 

        if nodo_Y.acceso == None:
            nodo_Y.acceso = nuevo
        else:
            if nuevo.coordenadaX < nodo_Y.acceso.coordenadaX:
                nuevo.abajo = nodo_Y.acceso
                nodo_Y.acceso.arriba = nuevo
                nodo_Y.acceso = nuevo
            else:
                tmp2 : Nodo_Interno = nodo_Y.acceso
                while tmp2 != None:
                    if nuevo.coordenadaX < tmp2.coordenadaX:
                        nuevo.abajo = tmp2
                        nuevo.arriba = tmp2.arriba
                        tmp2.arriba.abajo = nuevo
                        tmp2.arriba = nuevo
                        break;
                    elif nuevo.coordenadaX == tmp2.coordenadaX and nuevo.coordenadaY == tmp2.coordenadaY:
                        break;
                    else:
                        if tmp2.abajo == None:
                            tmp2.abajo = nuevo
                            nuevo.arriba = tmp2
                            break
                        else:
                            tmp2 = tmp2.abajo


    def do_Graphics(self,type_player):
        global Org_c,Row_c,Col_c
        contenido = '''digraph G{node[shape=box, width=0.7, height=0.7, fontname="Arial", fillcolor="white", style=filled] edge[style = "bold"] node[label = "''' + str(self.capa) +'''" fillcolor="{}" pos = "-1,1!"]raiz;'''.format(Org_c)
        
        pivote = self.filas.primero
        posx = 0
        while pivote != None:
            contenido += '\n\tnode[label = "X:{}" fillcolor="{}" pos="-1,-{}!" shape=box]x{};'.format(pivote.id, Row_c, posx, pivote.id)
            pivote = pivote.siguiente
            posx += 1
        pivote = self.filas.primero

        while pivote.siguiente != None:
        
                contenido += '\n\tx{}->x{};'.format(pivote.id, pivote.siguiente.id)
                contenido += '\n\tx{}->x{}[dir=back];'.format(pivote.id, pivote.siguiente.id)
                pivote = pivote.siguiente

        contenido += '\n\traiz->x{};'.format(self.filas.primero.id)

        pivotey = self.columnas.primero
        posy = 0
        while pivotey != None:
            contenido += '\n\tnode[label = "Y:{}" fillcolor="{}" pos = "{},1!" shape=box]y{};'.format(pivotey.id, Col_c, posy, pivotey.id)
            pivotey = pivotey.siguiente
            posy += 1
        pivotey = self.columnas.primero
        while pivotey.siguiente != None:
            contenido += '\n\ty{}->y{};'.format(pivotey.id, pivotey.siguiente.id)
            contenido += '\n\ty{}->y{}[dir=back];'.format(pivotey.id, pivotey.siguiente.id)
            pivotey = pivotey.siguiente
        contenido += '\n\traiz->y{};'.format(self.columnas.primero.id)

        pivote = self.filas.primero
        posx = 0
        while pivote != None:
            pivote_celda : Nodo_Interno = pivote.acceso
            while pivote_celda != None:
                # --- buscamos posy
                pivotey = self.columnas.primero
                posy_celda = 0
                while pivotey != None:
                    if pivotey.id == pivote_celda.coordenadaY: break
                    posy_celda += 1
                    pivotey = pivotey.siguiente
                   
                if pivote_celda.caracter == 'p':
                    contenido += '\n\tnode[label="P" fillcolor="{}" pos="{},-{}!" shape=box]i{}_{};'.format(
                        pivote_celda.color,posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                        )
                elif pivote_celda.caracter == 's':
                    contenido += '\n\tnode[label="S" fillcolor="{}" pos="{},-{}!" shape=box]i{}_{};'.format(
                        pivote_celda.color,posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.caracter == 'd':
                    contenido += '\n\tnode[label="D" fillcolor="{}" pos="{},-{}!" shape=box]i{}_{};'.format(
                        pivote_celda.color,posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.caracter == 'b':
                    contenido += '\n\tnode[label="B" fillcolor="{}" pos="{},-{}!" shape=box]i{}_{};'.format(
                        pivote_celda.color,posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.caracter == 'x':
                    contenido += '\n\tnode[label="X" fillcolor="{}" pos="{},-{}!" shape=box]i{}_{};'.format(
                        pivote_celda.color,posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.caracter == '*':
                    contenido += '\n\tnode[label="[{},{}]" fillcolor="{}" pos="{},-{}!" shape=box]i{}_{};'.format(
                        pivote_celda.coordenadaX, pivote_celda.coordenadaY, pivote_celda.color,posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                pivote_celda = pivote_celda.derecha

            pivote_celda = pivote.acceso
            while pivote_celda != None:
                if pivote_celda.derecha != None:
                    contenido += '\n\ti{}_{}->i{}_{};'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.derecha.coordenadaX, pivote_celda.derecha.coordenadaY)
                    contenido += '\n\ti{}_{}->i{}_{}[dir=back];'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.derecha.coordenadaX, pivote_celda.derecha.coordenadaY)
                pivote_celda = pivote_celda.derecha

            try:
                contenido += '\n\tx{}->i{}_{};'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
                contenido += '\n\tx{}->i{}_{}[dir=back];'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
            except:
                pass
            pivote = pivote.siguiente
            posx += 1
        
        pivote = self.columnas.primero
        while pivote != None:
            pivote_celda : Nodo_Interno = pivote.acceso
            while pivote_celda != None:
                if pivote_celda.abajo != None:
                    contenido += '\n\ti{}_{}->i{}_{};'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.abajo.coordenadaX, pivote_celda.abajo.coordenadaY)
                    contenido += '\n\ti{}_{}->i{}_{}[dir=back];'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.abajo.coordenadaX, pivote_celda.abajo.coordenadaY) 
                pivote_celda = pivote_celda.abajo
            
            try:
                contenido += '\n\ty{}->i{}_{};'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
                contenido += '\n\ty{}->i{}_{}[dir=back];'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
            except:
                pass
            
            pivote = pivote.siguiente
          
        contenido += '\n}'
        dot = "Docs/matrix_{}.txt".format(type_player)
        with open(dot, 'w') as grafo:
            grafo.write(contenido)
        result = "Docs/matrix_{}.pdf".format(type_player)
        os.system("neato -Tpdf " + dot + " -o " + result)
        # webbrowser.open(result)

    def do_Graphics_adjacency(self,type_player):
        global Org_c,Row_c,Col_c
        contenido = '''digraph G{node[shape=box, width=0.7, height=0.7, fontname="Arial", fillcolor="white", style=filled] edge[style = "bold"] node[label = "''' + str(self.capa) +'''" pos = "-1,1!"]raiz;'''
        
        pivote = self.filas.primero
        posx = 0
        while pivote != None:
            contenido += '\n\tnode[label = "{}" pos="-1,-{}!" shape=box]x{};'.format(pivote.id, posx, pivote.id)
            pivote = pivote.siguiente
            posx += 1

        pivote = self.filas.primero
        while pivote.siguiente != None:
            contenido += '\n\tx{}->x{};'.format(pivote.id, pivote.siguiente.id)
            pivote = pivote.siguiente

        contenido += '\n\traiz->x{};'.format(self.filas.primero.id)


        pivote = self.filas.primero
        posx = 0
        while pivote != None:
            pivote_celda : Nodo_Interno = pivote.acceso
            posyy = -1
            while pivote_celda != None:
                pivotey = self.columnas.primero
                while pivotey != None:
                    if pivotey.id == pivote_celda.coordenadaY:
                        posyy += 1
                        break             
                    pivotey = pivotey.siguiente
                if pivote_celda.caracter == 'x':
                    contenido += '\n\tnode[label="{}" pos="{},-{}!" shape=box]i{}_{};'.format(
                        pivote_celda.coordenadaY,posyy, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                pivote_celda = pivote_celda.derecha

            pivote_celda = pivote.acceso
            while pivote_celda != None:
                if pivote_celda.derecha != None:
                    contenido += '\n\ti{}_{}->i{}_{};'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.derecha.coordenadaX, pivote_celda.derecha.coordenadaY)
                pivote_celda = pivote_celda.derecha
            try:
                contenido += '\n\tx{}->i{}_{};'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
            except:
                pass
            pivote = pivote.siguiente
            posx += 1
          

        contenido += '\n}'
        dot = "Docs/matrix_{}.txt".format(type_player)
        with open(dot, 'w') as grafo:
            grafo.write(contenido)
        result = "Docs/matrix_{}.pdf".format(type_player)
        os.system("neato -Tpdf " + dot + " -o " + result)
        # webbrowser.open(result)

    def do_Graphics_grafo(self,type_player):
        global Org_c,Row_c,Col_c
        contenido =  "digraph G{"
        contenido += '\nnode[fontname="Helvetica,Arial,sans-serif"]'
        contenido += '\nedge[fontname="Helvetica,Arial,sans-serif", arrowsize=0.5,]'
        contenido += "\nrankdir=LR;"
        contenido += "\nnode[shape = circle];"

        contenido += '\n\t0->{};'.format(self.filas.primero.id)

        pivote = self.filas.primero
        posx = 0
        while pivote != None:

            pivote_celda = pivote.acceso
            while pivote_celda != None:
                if pivote_celda.derecha != None:
                    contenido += '\n\t{}->{};'.format(pivote_celda.coordenadaX,
                    pivote_celda.derecha.coordenadaY)
                pivote_celda = pivote_celda.derecha

            try:
                contenido += '\n\t{}->{};'.format(pivote.id, pivote.acceso.coordenadaY)
            except:
                pass

            pivote = pivote.siguiente
            posx += 1
        
        contenido += '\n}'
        dot = "Docs/matrix_{}.txt".format(type_player)
        with open(dot, 'w') as grafo:
            grafo.write(contenido)
        result = "Docs/matrix_{}.pdf".format(type_player)
        os.system("neato -Tpdf " + dot + " -o " + result)
        # webbrowser.open(result)


class Box():
    def __init__(self, box,box_posY,box_posX,color,font):
        self.font: str = font
        self.color: str = color
        self.posX: int = int(box_posX) #filas
        self.posY: int = int(box_posY) #columnas
        self.next = None
        self.prev = None
        self.box =  box

class Boxes_List():
    def __init__(self):
        self.boxes_head : Box = None
        self.boxes_last = None
        self.boxes_size = 0


    def add_to_end(self,box,posY,posX,color,fuente):
        new_boxes = Box(box,posY,posX,color,fuente)
        self.boxes_size += 1
        if self.boxes_head is None:
            self.boxes_head = new_boxes
            self.boxes_last = new_boxes
        else:
            self.boxes_last.next =  new_boxes
            new_boxes.prev = self.boxes_last
            self.boxes_last = new_boxes
        return new_boxes

    def get_By_Pos(self, pos_x, pos_y):
        tmp = self.boxes_head
        while tmp != None:
            if tmp.posY == pos_y and tmp.posX == pos_x:
                return tmp
            tmp = tmp.next

    def insert_in_pos(self,posX,posY,color,fuente):
        tmp = self.boxes_head
        while tmp != None:
            if tmp.posX == posX and tmp.posY == posY and tmp.color != Maroon and tmp.color != Navy and tmp.color != Teal and tmp.color != Gray:
                tmp.color = color
                tmp.fuente = fuente
            tmp = tmp.next


    def auto_shot(self):
        global matrix_size
        row = random.randint(1,matrix_size)
        col = random.randint(1,matrix_size)

        st = self.get_By_Pos(row,col)

        tmp: Box =  self.boxes_head

        while tmp != None:
            if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == withe:
                tmp.color = Shot
                mb.showerror("Disparo Fallido", "Fallido, \nCoordenada: X: " + str(tmp.posX) + " Y: " + str(tmp.posY) + " Vacia!")
            if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Maroon:
                tmp.color = Shot
                mb.showinfo("Disparo Acertado", "Acertado en Portaavion" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
            if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Navy:
                tmp.color = Shot
                mb.showinfo("Disparo Acertado", "Acertado en Submarino" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
            if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Gray:
                tmp.color = Shot
                mb.showinfo("Disparo Acertado", "Acertado en Destructor" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
            if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Teal:
                tmp.color = Shot
                mb.showinfo("Disparo Acertado", "Acertado en Buque" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
            tmp = tmp.next


    def do_shot(self, posx, posy, name):
        global user_life, user_tokens, game_over, invited_name, invited_life, invited_tokens

        if (name == "host"):
            row = int(posx)
            col = int(posy)

            st = self.get_By_Pos(row,col)

            tmp: Box =  self.boxes_head

            while tmp != None:
                if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == withe:
                    tmp.color = Shot
                    mb.showerror("Disparo Fallido", "Fallido !, \nCoordenada: X: " + str(tmp.posX) + " Y: " + str(tmp.posY) + " Vacia!")
                    user_life -= 1
                    if(user_life == 0):
                        game_over = True
                    

                if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Maroon:
                    tmp.color = Shot
                    mb.showinfo("Disparo Acertado", "Acertado en Portaavion !" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
                    user_tokens += 20

                    up_coins = {
                            "nick": active_user,
                            "monedas": str(user_tokens)
                        }

                    requests.put(f'{base_url}/up_coins', json = up_coins)

                if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Navy:
                    tmp.color = Shot
                    mb.showinfo("Disparo Acertado", "Acertado en Submarino !" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
                    user_tokens += 20

                    up_coins = {
                            "nick": active_user,
                            "monedas": str(user_tokens)
                        }

                    requests.put(f'{base_url}/up_coins', json = up_coins)

                if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Gray:
                    tmp.color = Shot
                    mb.showinfo("Disparo Acertado", "Acertado en Destructor !" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
                    user_tokens += 20

                    up_coins = {
                            "nick": active_user,
                            "monedas": str(user_tokens)
                        }

                    requests.put(f'{base_url}/up_coins', json = up_coins)

                if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Teal:
                    tmp.color = Shot
                    mb.showinfo("Disparo Acertado", "Acertado en Buque !" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
                    user_tokens += 20

                    up_coins = {
                            "nick": active_user,
                            "monedas": str(user_tokens)
                        }

                    requests.put(f'{base_url}/up_coins', json = up_coins)

                tmp = tmp.next

        elif(name == "slave"):

            row = int(posx)
            col = int(posy)

            st = self.get_By_Pos(row,col)

            tmp: Box =  self.boxes_head

            while tmp != None:
                if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == withe:
                    tmp.color = Shot
                    mb.showerror("Disparo Fallido", "Fallido !, \nCoordenada: X: " + str(tmp.posX) + " Y: " + str(tmp.posY) + " Vacia!")
                    invited_life -= 1
                    if(invited_life == 0):
                        game_over = True
                    
                if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Maroon:
                    tmp.color = Shot
                    mb.showinfo("Disparo Acertado", "Acertado en Portaavion !" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
                    invited_tokens += 20

                if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Navy:
                    tmp.color = Shot
                    mb.showinfo("Disparo Acertado", "Acertado en Submarino !" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
                    invited_tokens += 20

                if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Gray:
                    tmp.color = Shot
                    mb.showinfo("Disparo Acertado", "Acertado en Destructor !" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
                    invited_tokens += 20

                if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == Teal:
                    tmp.color = Shot
                    mb.showinfo("Disparo Acertado", "Acertado en Buque !" + "\nUbicaion destruida: X: " + str(tmp.posX) + " Y: " + str(tmp.posY))
                    invited_tokens += 20

                tmp = tmp.next


    def do_shot_tuto(self, posx, posy):
        global user_life, user_tokens, game_over

        row = int(posx)
        col = int(posy)

        st = self.get_By_Pos(row,col)

        tmp: Box =  self.boxes_head

        while tmp != None:
            if tmp.posX == st.posX and tmp.posY == st.posY and tmp.color == withe:
                tmp.color = Shot                
            tmp = tmp.next

    def add_protaviones(self):

        global matrix_size, rec_pa

        row = random.randint(1,matrix_size)
        col = random.randint(1,matrix_size)

        pivote = self.get_By_Pos(row,col)

        tmp: Box =  self.boxes_head

 
        #derecha
        tmpr1 = self.get_By_Pos(row,col+1)
        tmpr2 = self.get_By_Pos(row,col+2)
        tmpr3 = self.get_By_Pos(row,col+3)

        #iquierda
        tmpl1 = self.get_By_Pos(row,col-1)
        tmpl2 = self.get_By_Pos(row,col-2)
        tmpl3 = self.get_By_Pos(row,col-3)

        #arriba
        tmpu1 = self.get_By_Pos(row+1,col)
        tmpu2 = self.get_By_Pos(row+2,col)
        tmpu3 = self.get_By_Pos(row+3,col)

        #abajo
        tmpd1 = self.get_By_Pos(row-1,col)
        tmpd2 = self.get_By_Pos(row-2,col)
        tmpd3 = self.get_By_Pos(row-3,col)


        while tmp != None:
            if (tmp.posX == pivote.posX and tmp.posY == pivote.posY and tmp.color == withe):
                op = random.randint(1,4)
  
                if(op == 1):
                    if(tmpr1 != None and tmpr2 != None and tmpr3 != None):
                        if(tmpr1.color == withe and tmpr2.color == withe and tmpr3.color == withe):
                            tmp.color = Maroon
                            tmpr1.color = Maroon
                            tmpr2.color = Maroon
                            tmpr3.color = Maroon
                            rec_pa += 1
                        else:
                            pass
                elif(op == 2):
                    if(tmpl1 != None and tmpl2 != None and tmpl3 != None):
                        if(tmpl1.color == withe and tmpl2.color == withe and tmpl3.color == withe):
                            tmp.color = Maroon
                            tmpl1.color = Maroon
                            tmpl2.color = Maroon
                            tmpl3.color = Maroon
                            rec_pa += 1
                        else:
                            pass
                elif(op == 3):
                    if(tmpu1 != None and tmpu2 != None and tmpu3 != None):
                        if(tmpu1.color == withe and tmpu2.color == withe and tmpu3.color == withe):
                            tmp.color = Maroon
                            tmpu1.color = Maroon
                            tmpu2.color = Maroon
                            tmpu3.color = Maroon
                            rec_pa += 1
                        else:
                            pass
                elif(op == 4):
                    if(tmpd1 != None and tmpd2 != None and tmpd3 != None):
                        if(tmpd1.color == withe and tmpd2.color == withe and tmpd3.color == withe):
                            tmp.color = Maroon
                            tmpd1.color = Maroon
                            tmpd2.color = Maroon
                            tmpd3.color = Maroon
                            rec_pa += 1
                        else:
                            pass
                else:
                    self.add_protaviones()
            
            tmp = tmp.next



    def add_submarino(self):
    
        global matrix_size, rec_sb

        row = random.randint(1,matrix_size)
        col = random.randint(1,matrix_size)

        pivote = self.get_By_Pos(row,col)

        tmp: Box =  self.boxes_head

        #derecha
        tmpr1 = self.get_By_Pos(row,col+1)
        tmpr2 = self.get_By_Pos(row,col+2)

        #iquierda
        tmpl1 = self.get_By_Pos(row,col-1)
        tmpl2 = self.get_By_Pos(row,col-2)

        #arriba
        tmpu1 = self.get_By_Pos(row+1,col)
        tmpu2 = self.get_By_Pos(row+2,col)

        #abajo
        tmpd1 = self.get_By_Pos(row-1,col)
        tmpd2 = self.get_By_Pos(row-2,col)

        while tmp != None:
            if (tmp.posX == pivote.posX and tmp.posY == pivote.posY and tmp.color == withe):
                op = random.randint(1,4)

                if(op == 1):
                    if(tmpr1 != None and tmpr2 != None):
                        if(tmpr1.color == withe and tmpr2.color == withe):
                            tmp.color = Navy
                            tmpr1.color = Navy
                            tmpr2.color = Navy
                            rec_sb += 1
                        else:
                            pass
                elif(op == 2):
                    if(tmpl1 != None and tmpl2 != None):
                        if(tmpl1.color == withe and tmpl2.color == withe):
                            tmp.color = Navy
                            tmpl1.color = Navy
                            tmpl2.color = Navy
                            rec_sb += 1
                        else:
                            pass

                elif(op == 3):
                    if(tmpu1 != None and tmpu2 != None):
                        if(tmpu1.color == withe and tmpu2.color == withe):
                            tmp.color = Navy
                            tmpu1.color = Navy
                            tmpu2.color = Navy
                            rec_sb += 1
                        else:
                            pass
                elif(op == 4):
                    if(tmpd1 != None and tmpd2 != None):
                        if(tmpd1.color == withe and tmpd2.color == withe):
                            tmp.color = Navy
                            tmpd1.color = Navy
                            tmpd2.color = Navy
                            rec_sb += 1
                        else:
                            pass
                else:
                    self.add_submarino()
            
            tmp = tmp.next

   



    def add_destructor(self):

        global matrix_size, rec_dt

        row = random.randint(1,matrix_size)
        col = random.randint(1,matrix_size)

        pivote = self.get_By_Pos(row,col)

        tmp: Box =  self.boxes_head

        #derecha
        tmpr1 = self.get_By_Pos(row,col+1)

        #iquierda
        tmpl1 = self.get_By_Pos(row,col-1)

        #arriba
        tmpu1 = self.get_By_Pos(row+1,col)

        #abajo
        tmpd1 = self.get_By_Pos(row-1,col)

        while tmp != None:
            if (tmp.posX == pivote.posX and tmp.posY == pivote.posY and tmp.color == withe):
                op = random.randint(1,4)

                if(op == 1):
                    if(tmpr1 != None):
                        if(tmpr1.color == withe):
                            tmp.color = Gray
                            tmpr1.color = Gray
                            rec_dt += 1
                        else:
                            pass

                elif(op == 2):
                    if(tmpl1 != None):
                        if(tmpl1.color == withe):
                            tmp.color = Gray
                            tmpl1.color = Gray
                            rec_dt += 1
                        else:
                            pass

                elif(op == 3):
                    if(tmpu1 != None):
                        if(tmpu1.color == withe):
                            tmp.color = Gray
                            tmpu1.color = Gray
                            rec_dt += 1
                        else:
                            pass

                elif(op == 4):
                    if(tmpd1 != None):
                        if(tmpd1.color == withe):
                            tmp.color = Gray
                            tmpd1.color = Gray
                            rec_dt += 1
                        else:
                            pass

                else:
                    self.add_destructor()
            
            tmp = tmp.next

    def add_buque(self):

        global matrix_size, rec_bq

        row = random.randint(1,matrix_size)
        col = random.randint(1,matrix_size)

        bq = self.get_By_Pos(row,col)

        tmp: Box =  self.boxes_head

        while tmp != None:
            if tmp.posX == bq.posX and tmp.posY == bq.posY and tmp.color == withe:
                tmp.color = Teal
                rec_bq += 1
            tmp = tmp.next

       

    def generate_prototipo(self):
        global matrix_size

        pos_x = 0
        pos_y = 0
        contador = 1 

        rows = matrix_size
        columns = matrix_size

        for i in range(matrix_size):
            count_rows = 0
            while int(rows) > count_rows:
                count_cols = 0
                color = '{}'.format(str(contador))
                self.add_to_end(color,pos_x+1,pos_y+1,withe,withe)
                contador += 1
                pos_y += 1 
                while int(columns) > count_cols:
                    count_cols += 1
                count_rows += 1
                if pos_y >= int(columns):
                    pos_x += 1
                    pos_y = 0


matrix_aux = Boxes_List()
matrix_aux2 = Boxes_List()
Hash_Table = Tabla_Hash(13)
new_blockchain = Blockchain()

def rejoin_datas():
    global matrix_size, matrix_aux, matrix_aux2, user_life
    global portaviones, submarinos, destructores, buques
    global rec_pa, rec_sb, rec_dt, rec_bq
    global invited_life, invited_name, game_over, game_over2
    global rec_pa_d1, rec_sb_d1, rec_dt_d1, rec_bq_d1
    global rec_pa_d2, rec_sb_d2, rec_dt_d2, rec_bq_d2

    matrix_size = 0
    matrix_aux.boxes_head = None
    matrix_aux2.boxes_head = None

    portaviones = 0
    submarinos = 0
    destructores = 0 
    buques = 0

    rec_pa = 0
    rec_sb = 0
    rec_dt = 0
    rec_bq = 0

    #Cant Barcos Destruidos
    rec_pa_d1 = 0
    rec_sb_d1 = 0
    rec_dt_d1 = 0
    rec_bq_d1 = 0

    rec_pa_d2 = 0
    rec_sb_d2 = 0
    rec_dt_d2 = 0
    rec_bq_d2 = 0

    user_life = 3

    invited_life = 3
    invited_name = ""

    game_over = False
    game_over2 = False

def cant_barcos(size):
    global portaviones, submarinos, destructores, buques

    aux =  ((size-1)//10)+1

    portaviones  = int(aux)
    submarinos = int(aux*2)
    destructores = int(aux*3)
    buques = int(aux*4)

def generate_plays(matrix_aux: Boxes_List, player_name):

    matrix = MatrizDispersa(0)

    tmp = matrix_aux.boxes_head
    while tmp != None:
        x = 0
        y = 0
        if tmp.color == Maroon:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'p',Maroon)
        if tmp.color == Navy:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'s',Navy)
        if tmp.color == Gray:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'d',Gray)
        if tmp.color == Teal:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'b',Teal)
        if tmp.color == Shot:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'x',Shot)
        tmp = tmp.next

    matrix.do_Graphics(player_name)

def auto_generate(matrix_aux: Boxes_List, player_name):
    global matrix_size
    global portaviones, submarinos, destructores, buques
    global rec_pa, rec_sb, rec_dt, rec_bq

    cant_barcos(matrix_size)

    matrix = MatrizDispersa(0)

    matrix_aux.generate_prototipo()

    while (rec_pa < portaviones):
        matrix_aux.add_protaviones()
    while (rec_sb < submarinos):
        matrix_aux.add_submarino()
    while (rec_dt < destructores):
        matrix_aux.add_destructor()
    while (rec_bq < buques):
        matrix_aux.add_buque()
        

    tmp = matrix_aux.boxes_head

    while tmp != None:
        x = 0
        y = 0
        if tmp.color == Maroon:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'p',Maroon)
        if tmp.color == Navy:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'s',Navy)
        if tmp.color == Gray:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'d',Gray)
        if tmp.color == Teal:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'b',Teal)
        if tmp.color == Shot:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'x',Shot)
        tmp = tmp.next
    
    matrix.do_Graphics(player_name)

def manual_generate(matrix_aux: Boxes_List, player_name):
    global matrix_size
    global portaviones, submarinos, destructores, buques
    global rec_pa, rec_sb, rec_dt, rec_bq

    cant_barcos(matrix_size)

    matrix = MatrizDispersa(0)

    tmp = matrix_aux.boxes_head

    while tmp != None:
        x = 0
        y = 0
        if tmp.color == Maroon:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'p',Maroon)
        if tmp.color == Navy:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'s',Navy)
        if tmp.color == Gray:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'d',Gray)
        if tmp.color == Teal:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'b',Teal)
        if tmp.color == Shot:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'x',Shot)
        tmp = tmp.next
    
    matrix.do_Graphics(player_name)
    return matrix_aux

def show_insert(matrix_aux: Boxes_List):
    global matrix_size

    matrix = MatrizDispersa(0)

    tmp = matrix_aux.boxes_head

    while tmp != None:
        x = 0
        y = 0
        if tmp.color == Maroon:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'p',Maroon)
        if tmp.color == Navy:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'s',Navy)
        if tmp.color == Gray:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'d',Gray)
        if tmp.color == Teal:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'b',Teal)
        if tmp.color == withe:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'*',withe)
        tmp = tmp.next
    
    matrix.do_Graphics('Insertion')


def show_adjacency(matrix_aux: Boxes_List):
    global matrix_size

    matrix = MatrizDispersa(0)

    tmp = matrix_aux.boxes_head

    while tmp != None:
        x = 0
        y = 0
        if tmp.color == Shot:
            x = tmp.posX
            y = tmp.posY
            matrix.insert(x,y,'x',Shot)
        tmp = tmp.next
    
    matrix.do_Graphics_adjacency('Adjacency')
    matrix.do_Graphics_grafo('Grafo')

def count_boats(matrix_aux: Boxes_List):
    global game_over2
    global rec_pa, rec_sb, rec_dt, rec_bq
    global user_life

    game_over2 = True

    cont_pa = 0
    cont_sb = 0
    cont_dt = 0
    cont_bq = 0

    tmp = matrix_aux.boxes_head
  
    while tmp != None:
        if tmp.color == Maroon:
            cont_pa += 1
            game_over2 = False
        if tmp.color == Navy:
            cont_sb += 1
            game_over2 = False
        if tmp.color == Gray:
            cont_dt += 1
            game_over2 = False
        if tmp.color == Teal:
            cont_bq += 1
            game_over2 = False
        tmp = tmp.next
    
    rec_pa = int(cont_pa/4)
    rec_sb = int(cont_sb/3)
    rec_dt = int(cont_dt/2)
    rec_bq = int(cont_bq/1)

def count_boats_d1(matrix_aux: Boxes_List):
    global rec_pa_d1, rec_sb_d1, rec_dt_d1, rec_bq_d1
    global portaviones, submarinos, destructores, buques

    cont_pai = int(portaviones*4)
    cont_sbi = int(submarinos*3)
    cont_dti = int(destructores*2)
    cont_bqi = int(buques*1)

    cont_paf = 0
    cont_sbf = 0
    cont_dtf = 0
    cont_bqf = 0

    tmp = matrix_aux.boxes_head
    while tmp != None:
        if tmp.color == Maroon:
            cont_paf += 1
        if tmp.color == Navy:
            cont_sbf += 1
        if tmp.color == Gray:
            cont_dtf += 1
        if tmp.color == Teal:
            cont_bqf += 1
        tmp = tmp.next

    if(cont_pai == cont_paf):
        rec_pa_d1 = 0
    if(cont_sbi == cont_sbf):
        rec_sb_d1 = 0
    if(cont_dti == cont_dtf):
        rec_dt_d1 = 0
    if(cont_bqi == cont_bqf):
        rec_bq_d1 = 0
    
    if(cont_pai != cont_paf):
        aux = cont_pai-cont_paf
        for i in range(cont_pai):
            if(int(aux/4) == i):
                rec_pa_d1 = i
    if(cont_sbi != cont_sbf):
        aux = cont_sbi-cont_sbf
        for i in range(cont_sbi):
            if(int(aux/3) == i):
                rec_sb_d1 = i
    if(cont_dti != cont_dtf):
        aux = cont_dti-cont_dtf
        for i in range(cont_dti):
            if(int(aux/2) == i):
                rec_dt_d1 = i
    if(cont_bqi != cont_bqf):
        rec_bq_d1 = cont_bqi-cont_bqf

    # print("pa destruidos:", rec_pa_d1)
    # print("sb destruidos:", rec_sb_d1)
    # print("dt destruidos:", rec_dt_d1)
    # print("bq destruidos:", rec_bq_d1)

def count_boats_d2(matrix_aux: Boxes_List):
    global rec_pa_d2, rec_sb_d2, rec_dt_d2, rec_bq_d2
    global portaviones, submarinos, destructores, buques

    cont_pai = int(portaviones*4)
    cont_sbi = int(submarinos*3)
    cont_dti = int(destructores*2)
    cont_bqi = int(buques*1)

    cont_paf = 0
    cont_sbf = 0
    cont_dtf = 0
    cont_bqf = 0

    tmp = matrix_aux.boxes_head
    while tmp != None:
        if tmp.color == Maroon:
            cont_paf += 1
        if tmp.color == Navy:
            cont_sbf += 1
        if tmp.color == Gray:
            cont_dtf += 1
        if tmp.color == Teal:
            cont_bqf += 1
        tmp = tmp.next

    if(cont_pai == cont_paf):
        rec_pa_d2 = 0
    if(cont_sbi == cont_sbf):
        rec_sb_d2 = 0
    if(cont_dti == cont_dtf):
        rec_dt_d2 = 0
    if(cont_bqi == cont_bqf):
        rec_bq_d2 = 0
    
    if(cont_pai != cont_paf):
        aux = cont_pai-cont_paf
        for i in range(cont_pai):
            if(int(aux/4) == i):
                rec_pa_d2 = i
    if(cont_sbi != cont_sbf):
        aux = cont_sbi-cont_sbf
        for i in range(cont_sbi):
            if(int(aux/3) == i):
                rec_sb_d2 = i
    if(cont_dti != cont_dtf):
        aux = cont_dti-cont_dtf
        for i in range(cont_dti):
            if(int(aux/2) == i):
                rec_dt_d2 = i
    if(cont_bqi != cont_bqf):
        rec_bq_d2 = cont_bqi-cont_bqf

    # print("2pa destruidos:", rec_pa_d2)
    # print("2sb destruidos:", rec_sb_d2)
    # print("2dt destruidos:", rec_dt_d2)
    # print("2bq destruidos:", rec_bq_d2)


def get_image(ruta):
    deathwing=Image.open(ruta)
    image2=deathwing.resize((620,620),Image.Resampling.LANCZOS)
    Deathwing2=ImageTk.PhotoImage(image2)

    return Deathwing2

def get_image2(ruta):
    deathwing=Image.open(ruta)
    image2=deathwing.resize((450,450),Image.Resampling.LANCZOS)
    Deathwing2=ImageTk.PhotoImage(image2)

    return Deathwing2


def create_img(ruta, nombre):
    pdf = fitz.open(ruta) #ruta del pdf a convertir
    page = pdf.load_page(0)
    pix = page.get_pixmap()
    pix.pil_save(nombre) #nombre apra guardar imagen


#---------------------------INTERFAZ GRAFICA DE USUARIO

class home():
    def __init__(self) -> None:
        #-----------------------------------------home-------------------------------------------------
        self.root = tk.Tk()
        self.root.title('Battleship')
        self.root.geometry('400x250+550+200')

        self.user_logn = Label(self.root,text = "BATTLESHIP").place(x = 170, y=80)
        self.btn_login = Button(self.root, width = 17, text="Login", command= self.login )
        self.btn_login.place(x=60, y=180)
        self.btn_Singin = Button(self.root, width = 17, text="Sign Up" , command=self.sign_up )
        self.btn_Singin.place(x=210, y=180)


        self.root.resizable(0,0)
        self.root.mainloop()
        
     #---------------------------------------------ventana de login----------------------------------------
    def login(self):
        self.root.destroy()
        self.logn = tk.Tk()
        self.logn.title('Login')
        self.logn.geometry('400x250+550+200')


        self.user_logn = Label(self.logn, text = "Login").place(x = 180, y=20)
        self.user_name = Label(self.logn, text = "User Name").place(x = 50, y=80)
        self.user_pass = Label(self.logn, text = "Password").place(x = 50, y=135)
        self.user_text = Entry(self.logn)
        self.user_text.place(x=200, y=80, width=150 , height=25)
        self.pass_text = Entry(self.logn)
        self.pass_text.place(x=200, y=135, width=150 , height=25)
        self.btn_Send = Button(self.logn, width = 17, text="Login", command = lambda: self.match_login(self.user_text.get(),self.pass_text.get()))
        self.btn_Send.place(x=140, y=190)

        self.logn.resizable(0,0)
        self.logn.mainloop()

    def match_login(self,name,passs):
        global active_user
        global active_pass
        global user_tokens

        login = {
	                "nick": name,
	                "password": passs
                }
        x = requests.get(f'{base_url}/login', json = login)
        data = x.text

        coins = login = {
	                "nick": name
                }

        y = requests.get(f'{base_url}/coins', json = coins)
        data2 = y.text
        
        if(data == name):
            mb.showinfo('Welcome', 'Welcome ' + name)
            active_user = name
            active_pass = passs
            user_tokens = int(data2) 
            self.user_menu()
        elif(name == "EDD" and passs == "edd123"):
            mb.showinfo('Welcome', 'Welcome ' + "ADMIN")
            self.admin_menu()
        elif(data == "incorrecta"):
            mb.showerror("Request Failed", "Sorry, Incorrect Password")

        else:
            mb.showerror("Request Failed", "Sorry, No matches")
            self.logn.destroy()
            home()

    #---------------------------------------------ventana de Sign Up----------------------------------------
    def sign_up(self):
        self.root.destroy()
        self.signup = tk.Tk()
        self.signup.title('Sign Up')
        self.signup.geometry('400x320+550+200')


        self.user_logn = Label(self.signup, text = "Sign Up").place(x = 180, y=20)
        self.user_name = Label(self.signup, text = "User Name").place(x = 50, y=80)
        self.user_age = Label(self.signup, text = "Age").place(x = 50, y=135)
        self.user_pass = Label(self.signup, text = "Password").place(x = 50, y=190)

        self.user_text = Entry(self.signup)
        self.user_text.place(x=200, y=80, width=150 , height=25)
        self.age_text = Entry(self.signup)
        self.age_text.place(x=200, y=135, width=150 , height=25)
        self.pass_text = Entry(self.signup)
        self.pass_text.place(x=200, y=190, width=150 , height=25)

        self.btn_Send = Button(self.signup, width = 17, text="Sign Up", command = lambda: self.user_signup(self.user_text.get(),self.pass_text.get(),self.age_text.get()))
        self.btn_Send.place(x=140, y=250)

        self.signup.resizable(0,0)
        self.signup.mainloop()
    

    def user_signup(self,user_name,user_pass,user_age):

        user_id = random.randint(1,1000);

        signup = {  
                    "id": str(user_id),
	                "nick": user_name,
	                "password": user_pass,
	                "edad": user_age
                }

        x = requests.post(f'{base_url}/sign_up', json = signup)
        data = x.text

        if(data == "repetido"):
            mb.showerror("Request Failed", "Sorry, User Actually Exist !")
        elif(data == "registrado"):
            mb.showinfo('Welcome', 'User Registered !')

        self.signup.destroy()
        home()
 
       
    #------------------------------------------menu usuario-------------------------------------------
    def user_menu(self):
        global active_user
        self.logn.destroy()
        self.user_menu = tk.Tk()
        self.user_menu.title('Users Menu')
        self.user_menu.geometry('250x300+650+200')


        self.active = tk.Label(self.user_menu, text = f"Active User: {active_user}")
        self.active.place(x = 80, y=20)

        self.btn_edit = Button(self.user_menu, width = 14, text="Edit Information", command=self.edit_info)
        self.btn_edit.place(x=70, y=50)
        self.btn_delete = Button(self.user_menu, width = 14, text="Delete Account", command=self.delete_acc)
        self.btn_delete.place(x=70, y=90)
        self.btn_tutorial = Button(self.user_menu, width = 14, text="Tutorial", command=self.show_tutorial)
        self.btn_tutorial.place(x=70, y=130)
        self.btn_shop = Button(self.user_menu, width = 14, text="Shop", command=self.shops)
        self.btn_shop.place(x=70, y=170)
        self.btn_plays = Button(self.user_menu, width = 14, text="Play", command=self.plys)
        self.btn_plays.place(x=70, y=210)
        self.btn_logout = Button(self.user_menu, width = 14, text="Logout", command= self.user_logout )
        self.btn_logout.place(x=70, y=250)

        self.user_menu.after(1000, self.reload_auser)

        self.user_menu.resizable(0,0)
        self.user_menu.mainloop()


    def reload_auser(self):
        global active_user
        self.active.config(text = f"Active User: {active_user}")

        self.user_menu.after(1000, self.reload_auser)
    
    def user_logout(self):
        self.user_menu.destroy()
        home()

    

    #---------------------------------------------ventana de Editar info----------------------------------------
    def edit_info(self):
        self.user_menu.withdraw()
        self.edit_info = tk.Tk()
        self.edit_info.title('Edit Information')
        self.edit_info.geometry('400x320+550+200')


        self.user_logn = Label(self.edit_info, text = "Edit Information").place(x = 165, y=25)
        self.user_name = Label(self.edit_info, text = "User Name").place(x = 50, y=80)
        self.user_age = Label(self.edit_info, text = "Age").place(x = 50, y=135)
        self.user_pass = Label(self.edit_info, text = "Password").place(x = 50, y=190)

        self.user_text = Entry(self.edit_info)
        self.user_text.place(x=200, y=80, width=150 , height=25)
        self.age_text = Entry(self.edit_info)
        self.age_text.place(x=200, y=135, width=150 , height=25)
        self.pass_text = Entry(self.edit_info)
        self.pass_text.place(x=200, y=190, width=150 , height=25)

        self.btn_Send = Button(self.edit_info, width = 18, text="Exit and Save", command = lambda: self.exit_save(self.user_text.get(),self.pass_text.get(),self.age_text.get()))
        self.btn_Send.place(x=140, y=250)

        self.edit_info.resizable(0,0)
        self.edit_info.mainloop()
    

    def exit_save(self, nick, passs, age):
        global active_user
        edit = {
	                "name":  active_user,
                    "nick": nick,
                    "password": passs,
                    "edad": age
                }

        if(nick != ""):
            active_user = nick
            
        
        requests.put(f'{base_url}/edit', json = edit)

        self.edit_info.destroy()
        self.user_menu.deiconify()
    
    #-----------------------------------------delete information-------------------------------------------------
    
    def delete_acc(self):
        self.user_menu.withdraw()
        self.delete = tk.Tk()
        self.delete.title('Delete Account')
        self.delete.geometry('400x250+550+200')

        self.user_delet = Label(self.delete, text = "If you delete your account, you will lose everything!").place(x = 70, y=80)
        self.btn_delete = Button(self.delete, width = 17, text="Confirm", command= self.confirm )
        self.btn_delete.place(x=60, y=180)
        self.btn_cancel = Button(self.delete, width = 17, text="Cancel" , command=self.cancel )
        self.btn_cancel.place(x=210, y=180)


        self.delete.resizable(0,0)
        self.delete.mainloop()

    def confirm(self):
        global active_user
        global active_pass

        delete = {
	                "nick": active_user,
	                "password": active_pass
                }

        requests.delete(f'{base_url}/delete', json = delete)

        self.delete.destroy()
        home()

    def cancel(self):
        self.delete.destroy()
        self.user_menu.deiconify()

    #-----------------------------------Tutorial--------------------------------------------

    def show_tutorial(self):
        global matrix_size, matrix_aux
        x = requests.get(f'{base_url}/tuto')
        datas = x.json()

        rejoin_datas()

        ancho = datas[1]['ancho']
        alto = datas[1]['alto']

        if (int(ancho) == int(alto)):
            matrix_size = int(ancho)
        else:
            mb.showerror("Request Failed", "Sorry, Invalid Dimensions")

        matrix_aux.generate_prototipo()

        for i in datas:
            matrix_aux.do_shot_tuto(i['x'],i['y'])

        generate_plays(matrix_aux,"Tutorial")

    #------------------------------------tienda---------------------------------------------
    def shops(self):
        global active_user, user_tokens, src_objects, total_price, cant_cart

        self.user_menu.withdraw()
        self.shops = tk.Tk()
        self.shops.title('Shops')
        self.shops.geometry('700x550+600+200')

        self.txt_shop = Label(self.shops, text = "SHOP").place(x = 325, y=60)
        self.txt_shop_user = tk.Label(self.shops, text = f"Active User: {active_user}")
        self.txt_shop_user.place(x = 500, y=20)
        self.txt_shop_tokens = tk.Label(self.shops, text = f"Tokens Available: {user_tokens}")
        self.txt_shop_tokens.place(x = 500, y=45)

        self.style = ttk.Style()
        self.style.theme_use("default")

        self.style.configure("Treeview", 
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
            )

        self.style.map('Treeview', background=[('selected', 'blue')])


        self.tree_frame = Frame(self.shops)
        self.tree_frame.pack(pady=120)
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)
        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
        self.my_tree.pack()

        self.tree_scroll.config(command=self.my_tree.yview)

        self.my_tree['columns'] = ("Id", "Name", "Category", "Price")

        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Id", anchor=CENTER, width=100)
        self.my_tree.column("Name", anchor=CENTER, width=175)
        self.my_tree.column("Category", anchor=CENTER, width=175)
        self.my_tree.column("Price", anchor=CENTER, width=175)

        self.my_tree.heading("#0", text="", anchor=CENTER)
        self.my_tree.heading("Id", text="Id", anchor=CENTER)
        self.my_tree.heading("Name", text="Name",  anchor=CENTER)
        self.my_tree.heading("Category", text="Category", anchor=CENTER)
        self.my_tree.heading("Price", text="Price", anchor=CENTER)

        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="lightblue")

        
        count2=0

        x = requests.get(f'{base_url}/items')
        datas = x.json()
        
        for categoria in datas:
            for articulo in categoria:
                if count2 % 2 == 0:
                    self.my_tree.insert(parent='', index='end', iid=count2, text="", values=(articulo['id'], articulo['nombre'], articulo['categoria'], articulo['precio']), tags=('evenrow',))
                else:
                    self.my_tree.insert(parent='', index='end', iid=count2, text="", values=(articulo['id'], articulo['nombre'], articulo['categoria'], articulo['precio']), tags=('oddrow',))
                count2 += 1


        self.add_frame = Frame(self.shops)
        self.add_frame.pack(pady=0)

        self.nl = Label(self.add_frame, text="Id")
        self.nl.grid(row=0, column=0)

        self.il = Label(self.add_frame, text="Name")
        self.il.grid(row=0, column=1)

        self.tl = Label(self.add_frame, text="Category")
        self.tl.grid(row=0, column=2)

        self.cl = Label(self.add_frame, text="Price")
        self.cl.grid(row=0, column=3)

        self.id_box = Entry(self.add_frame)
        self.id_box.grid(row=1, column=0)
        self.id_box.config(state= "disabled")

        self.name_box = Entry(self.add_frame)
        self.name_box.grid(row=1, column=1)
        self.name_box.config(state= "disabled")

        self.catgry_box = Entry(self.add_frame)
        self.catgry_box.grid(row=1, column=2)
        self.catgry_box.config(state= "disabled")

        self.price_box = Entry(self.add_frame)
        self.price_box.grid(row=1, column=3)
        self.price_box.config(state= "disabled")
        
        def select_record():
            try:
                    
                self.id_box.config(state= "normal")
                self.name_box.config(state= "normal")
                self.catgry_box.config(state= "normal")
                self.price_box.config(state= "normal")

                self.id_box.delete(0, END)
                self.name_box.delete(0, END)
                self.catgry_box.delete(0, END)
                self.price_box.delete(0, END)

                self.selected = self.my_tree.focus()
                self.values = self.my_tree.item(self.selected, 'values')

                self.id_box.insert(0, self.values[0])
                self.name_box.insert(0, self.values[1])
                self.catgry_box.insert(0, self.values[2])
                self.price_box.insert(0, self.values[3])

                self.id_box.config(state= "disabled")
                self.name_box.config(state= "disabled")
                self.catgry_box.config(state= "disabled")
                self.price_box.config(state= "disabled")

            except:
                pass

        # Create Binding Click function
        def clicker(e):
            select_record()

        # Bindings
        self.my_tree.bind("<ButtonRelease-1>", clicker)


        self.btn_logout = Button(self.shops, width = 7, text="Back", command=self.back_from_shop)
        self.btn_logout.place(x=27, y=15)


        self.btn_buy = Button(self.shops, width = 14, text="Add to Cart", command = lambda: 
        self.add_to_cart(self.id_box.get(),self.name_box.get(),self.price_box.get()))
        self.btn_buy.place(x=290, y=420)

        self.btn_show = tk.Button(self.shops, width = 16, text=f"Cart: {cant_cart} Total: {total_price}", command = self.do_buys)
        self.btn_show.place(x= 545, y=370)

        self.shops.after(1000, self.reload_data_shop)

        self.shops.resizable(0,0)
        self.shops.mainloop()

    def reload_data_shop(self):
        global active_user, user_tokens, cant_cart, total_price
        self.txt_shop_user.config(text = f"Active User: {active_user}")
        self.txt_shop_tokens.config(text = f"Tokens Available: {user_tokens}")
        self.btn_show.config(text=f"Cart: {cant_cart} Total: {total_price}")

        self.shops.after(1000, self.reload_data_shop)

    def add_to_cart(self, id_item, name_item, price_item):
        global Hash_Table, active_id, cant_cart, total_price
        if(id_item != None and id_item != ''):
            Hash_Table.insert(active_id, int(id_item), name_item, price_item)
            cant_cart += 1
            total_price += int(price_item)
        #crear un json pra retornar los datos desde la tabla hash ?


    def do_buys(self):
        global Hash_Table,cant_cart, total_price

        self.shops.withdraw()
        self.do_buys = tk.Tk()
        self.do_buys.title('Shopping Cart')
        self.do_buys.geometry('280x460+650+150')


        self.txt_shop_att = tk.Label(self.do_buys, text =  f"Tokens: {user_tokens}")
        self.txt_shop_att.place(x = 50, y=2)
        self.txt_shop_qtt = tk.Label(self.do_buys, text = f"Quantity: {cant_cart}")
        self.txt_shop_qtt.place(x = 160, y=2)
        self.txt_shop_tt = tk.Label(self.do_buys, text = f"Total: {total_price}")
        self.txt_shop_tt.place(x = 160, y=20)
        

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

        self.my_tree2['columns'] = ("Id", "Name", "Price")

        self.my_tree2.column("#0", width=0, stretch=NO)
        self.my_tree2.column("Id", anchor=CENTER, width=50)
        self.my_tree2.column("Name", anchor=CENTER, width=100)
        self.my_tree2.column("Price", anchor=CENTER, width=50)

        self.my_tree2.heading("#0", text="", anchor=CENTER)
        self.my_tree2.heading("Id", text="Id", anchor=CENTER)
        self.my_tree2.heading("Name", text="Name",  anchor=CENTER)
        self.my_tree2.heading("Price", text="Price", anchor=CENTER)

        self.my_tree2.tag_configure('oddrow', background="white")
        self.my_tree2.tag_configure('evenrow', background="lightblue")

        self.add_frame2 = Frame(self.do_buys)
        self.add_frame2.pack(pady=40)

        self.nl2 = Label(self.add_frame2, text="Id")
        self.nl2.grid(row=0, column=0)

        self.il2 = Label(self.add_frame2, text="Name")
        self.il2.grid(row=0, column=1)


        self.cl2 = Label(self.add_frame2, text="Price")
        self.cl2.grid(row=0, column=2)

        self.id_box2 = Entry(self.add_frame2)
        self.id_box2.grid(row=1, column=0)
        self.id_box2.config(width=12, state= "disabled")

        self.name_box2 = Entry(self.add_frame2)
        self.name_box2.grid(row=1, column=1)
        self.name_box2.config(width=12, state= "disabled")

        self.price_box2 = Entry(self.add_frame2)
        self.price_box2.grid(row=1, column=2)
        self.price_box2.config(width=12, state= "disabled")

        def select_record():
            try:
                    
                self.id_box2.config(state= "normal")
                self.name_box2.config(state= "normal")
                self.price_box2.config(state= "normal")

                self.id_box2.delete(0, END)
                self.name_box2.delete(0, END)
                self.price_box2.delete(0, END)

                self.selected = self.my_tree2.focus()
                self.values = self.my_tree2.item(self.selected, 'values')

                self.id_box2.insert(0, self.values[0])
                self.name_box2.insert(0, self.values[1])
                self.price_box2.insert(0, self.values[2])

                self.id_box2.config(state= "disabled")
                self.name_box2.config(state= "disabled")
                self.price_box2.config(state= "disabled")

            except:
                pass

        # Create Binding Click function
        def clicker(e):
            select_record()

        # Bindings
        self.my_tree2.bind("<ButtonRelease-1>", clicker)

        self.btn_backk = Button(self.do_buys, width = 5, text="Back", command=self.back_from_cart)
        self.btn_backk.place(x=30, y=420)

        self.btn_buy2 = Button(self.do_buys, width = 10, text="Delete", command = lambda: self.delete_from_cart(self.id_box2.get(),self.price_box2.get()))
        self.btn_buy2.place(x=50, y=290)

        self.btn_show2 = Button(self.do_buys, width = 10, text="Buy", command=self.pay)
        self.btn_show2.place(x=130, y=290)

        self.btn_buy2 = Button(self.do_buys, width = 10, text="Cancel", command=self.clear_cart)
        self.btn_buy2.place(x=50, y=325)

        self.btn_show2 = Button(self.do_buys, width = 10, text="Graphviz", command=self.show_graph_cart)
        self.btn_show2.place(x=130, y=325)

        self.do_buys.after(3000, self.reload_cart)

        self.do_buys.resizable(0,0)
        self.do_buys.mainloop()


    def reload_cart(self):
        global count, cant_cart, total_price

        for record in self.my_tree2.get_children():
            self.my_tree2.delete(record)
        count = 0

        aux_list: L_Simple = Hash_Table.show_datas()

        tmp = aux_list.primero
        while tmp != None:
            if count % 2 == 0:
                self.my_tree2.insert(parent='', index='end', iid=count, text="", values=(tmp.id,tmp.nombre,tmp.precio), tags=('evenrow',))
            else:
                self.my_tree2.insert(parent='', index='end', iid=count, text="", values=(tmp.id,tmp.nombre,tmp.precio), tags=('oddrow',))
            count += 1
            tmp = tmp.siguiente
        
        
        self.txt_shop_qtt.config(text = f"Quantity: {cant_cart}")
        self.txt_shop_tt.config(text = f"Total: {total_price}")

        self.do_buys.after(3000, self.reload_cart)


    def back_from_shop(self):
        self.shops.destroy()
        self.user_menu.deiconify()

    def back_from_cart(self):
        self.do_buys.destroy()
        self.shops.deiconify()

    def show_graph_cart(self):
        global Hash_Table
        Hash_Table.do_Graphics('Cart')

    def clear_cart(self):
        global Hash_Table, count, cant_cart, total_price
        Hash_Table.delete_all()
        for record in self.my_tree2.get_children():
            self.my_tree2.delete(record)
        count = 0
        cant_cart = 0
        total_price = 0


    def delete_from_cart(self, id, price):
        global Hash_Table, count, cant_cart, total_price

        Hash_Table.delete_by_key(int(id))
        x = self.my_tree2.selection()[0]
        self.my_tree2.delete(x)
        count -= 1
        cant_cart -= 1
        total_price -= int(price)

    def pay(self):
        global Hash_Table,new_blockchain, user_tokens

        if (user_tokens >= total_price):
            
            user_tokens -= total_price
            
            aux_list: L_Simple = Hash_Table.show_datas()

            new_blockchain.insertBlock(aux_list)
            
            self.clear_cart()
            self.back_from_cart()
            
        else:
            mb.showerror("Request Failed", "You don't have enough coins")


    def plys(self):

        rejoin_datas()

        self.user_menu.withdraw()
        self.plys = tk.Tk()
        self.plys.title('Play')
        self.plys.geometry('400x250+550+200')

        self.txt_title = Label(self.plys, text = " > BATTLESHIP < ").place(x=155, y=20)
        self.txt_mode = Label(self.plys, text = "Configuration Module").place(x=140, y=50)

        self.invitd_name = Label(self.plys, text = "Temporary guest name:").place(x=50, y=90)

        self.invitd_text = Entry(self.plys)
        self.invitd_text.place(x=200, y=90, width=80 , height=25)

        self.table_dim = Label(self.plys, text = "Board Size (m x m) -> m:").place(x=50, y=140)

        self.user_text = Entry(self.plys)
        self.user_text.place(x=200, y=140, width=80 , height=25)

        self.btn_set = Button(self.plys, width = 5, height= 4, text="Set", command = lambda: self.setSize(self.user_text.get(), self.invitd_text.get()))
        self.btn_set.place(x=300, y=92)


        self.btn_Send = Button(self.plys, width = 18, text="Auto Generate Board", command = self.confirm)
        self.btn_Send.place(x=40, y=200)

        self.btn_Send2 = Button(self.plys, width = 18, text="Board Settings", command = self.confirm2)
        self.btn_Send2.place(x=220, y=200)

        self.btn_back = Button(self.plys, width = 5, text="Back", command=self.back_to_user_menu)
        self.btn_back.place(x=20, y=20)

        self.plys.resizable(0,0)
        self.plys.mainloop()

    def setSize(self, size, name):
        global matrix_size, invited_name
        if (size == "" or size == None):
            mb.showerror("Request Failed", "Sorry, Type a Dimension")
        elif(name == "" or name == None):
            mb.showerror("Request Failed", "Sorry, Type a Name for Invited")
        elif (int(size) <= 9):
            mb.showerror("Request Failed", "Sorry, Allowed Size m >= 10")
        else:
            invited_name = name
            matrix_size = int(size)
            mb.showinfo("Request Done", "Ok, Preset is Done!")
           
           
    def confirm(self):
        global matrix_size

        if (matrix_size == "" or matrix_size == None):
            mb.showerror("Request Failed", "Sorry, Type a Dimension")
        elif (int(matrix_size) <= 9):
            mb.showerror("Request Failed", "Sorry, Allowed Size m >= 10")
        else:
            self.plys.withdraw()
            self.do_play("auto")


    def confirm2(self):
        global matrix_size

        if (matrix_size == "" or matrix_size == None):
            mb.showerror("Request Failed", "Sorry, Type a Dimension")
        elif (int(matrix_size) <= 9):
            mb.showerror("Request Failed", "Sorry, Allowed Size m >= 10")
        else:
            self.settings()

    def back_to_user_menu(self):
        self.plys.destroy()
        self.user_menu.deiconify()
        

    #-------------------------------------realizar jugadas------------------------------------

    def do_play(self, tipo):
        global user_life, active_user, invited_life, invited_name, matrix_size, user_tokens, game_over, active_user, invited_tokens, matrix_aux, matrix_aux2
        global rec_pa, rec_sb, rec_dt, rec_bq

        user_life = 3
        invited_life = 3

        if(tipo == "auto"):
            auto_generate(matrix_aux,"host")
        elif(tipo == "manual"):
            manual_generate(matrix_aux,"host")

        rec_pa,rec_sb,rec_dt,rec_bq = 0,0,0,0

        auto_generate(matrix_aux2,"slave")

        create_img('Docs/matrix_host.pdf','Docs/host.png')
        create_img('Docs/matrix_slave.pdf','Docs/slave.png')

        self.do_ply = tk.Toplevel()
        self.do_ply.title('Do Plays')
        self.do_ply.geometry('1300x770+370+50')
        # self.do_ply['bg']='green'

        self.txt_tks = tk.Label(self.do_ply, text = f"Tokens: {user_tokens}")
        self.txt_tks.place(x = 525, y=10)
        self.txt_lfs = tk.Label(self.do_ply, text = f"Lives: {user_life}")
        self.txt_lfs.place(x = 525, y=30)

        self.txt_tks2 = tk.Label(self.do_ply, text = f"Tokens: {invited_tokens}")
        self.txt_tks2.place(x = 1200, y=10)
        self.txt_lfs2 = tk.Label(self.do_ply, text = f"Lives: {invited_life}")
        self.txt_lfs2.place(x = 1200, y=30)

        self.active = tk.Label(self.do_ply, text = f"Active User: {active_user}").place(x = 300, y=10)

        self.active = tk.Label(self.do_ply, text = f"Invited User: {invited_name}").place(x = 920, y=10)

        self.txt_enc = Label(self.do_ply, text = "Enter Coordinates").place(x = 355, y=50)
        self.txt_x = Label(self.do_ply, text = "X: ").place(x=340, y=75)
        self.txt_y = Label(self.do_ply, text = "Y: ").place(x=400, y=75)

        self.user_text = Entry(self.do_ply)
        self.user_text.place(x=360, y=75, width=35 , height=20)

        self.user_text2 = Entry(self.do_ply)
        self.user_text2.place(x=420, y=75, width=35 , height=20)

        self.btn_ing_jug = Button(self.do_ply, width = 14, text="Make Move", command = lambda: self.attacks(self.user_text.get(),self.user_text2.get(), matrix_size, "host"))
        self.btn_ing_jug.place(x=210, y=75)


        self.txt_enc2 = Label(self.do_ply, text = "Enter Coordinates").place(x = 985, y=50)
        self.txt_x2 = Label(self.do_ply, text = "X: ").place(x=970, y=75)
        self.txt_y2 = Label(self.do_ply, text = "Y: ").place(x=1030, y=75)

        self.invited_text = Entry(self.do_ply)
        self.invited_text.place(x=990, y=75, width=35 , height=20)

        self.invited_text2 = Entry(self.do_ply)
        self.invited_text2.place(x=1050, y=75, width=35 , height=20)

        self.btn_ing_jug2 = Button(self.do_ply, width = 14, text="Make Move", command = lambda: self.attacks(self.invited_text.get(),self.invited_text2.get(), matrix_size, "slave"))
        self.btn_ing_jug2.place(x=840, y=75)

        self.host_frame = Frame(self.do_ply, height=620, width=620)
        self.host_frame.pack()
        self.host_frame.place(x=20,y=120)

        self.host_table = get_image('Docs/host.png')

        self.host_label = tk.Label(self.host_frame, image= self.host_table)
        self.host_label.pack()

        self.slave_frame = Frame(self.do_ply, height=620, width=620)
        self.slave_frame.pack()
        self.slave_frame.place(x=660,y=120)

        self.slave_table = get_image('Docs/slave.png')

        self.slave_label = tk.Label(self.slave_frame, image= self.slave_table)
        self.slave_label.pack()


        self.btn_leave = Button(self.do_ply, width = 7, text="Leave", command = self.abandone)
        self.btn_leave.place(x=20, y=10)

        self.do_ply.after(1000, self.reload)

        self.do_ply.resizable(0,0)
        self.do_ply.mainloop()

        
    def reload(self):
        global user_life, user_tokens, invited_life, invited_tokens

        self.host_table = get_image('Docs/host.png')
        self.slave_table = get_image('Docs/slave.png')

        self.txt_tks.config(text = f"Tokens: {user_tokens}")
        self.txt_lfs.config(text = f"Lives: {user_life}")

        self.txt_tks2.config(text = f"Tokens: {invited_tokens}")
        self.txt_lfs2.config(text = f"Lives: {invited_life}")

        self.host_label.config(image= self.host_table)
        self.slave_label.config(image= self.slave_table)

        self.do_ply.after(1000, self.reload)


    def attacks(self, posx, posy, size, name):
        global game_over2, game_over, active_user, matrix_aux2, invited_name, invited_life, matrix_aux

        if (name == "host"):

            self.user_text.delete(0, END)
            self.user_text2.delete(0, END)

            if (posx != "" and posy != "" and int(posx) <= int(size) and int(posy) <= int(size)):
                up_plays = {
                        "nick": active_user,
                        "x": posx,
                        "y": posy
                    }

                requests.post(f'{base_url}/up_plays', json = up_plays)

                matrix_aux2.do_shot(posx,posy,"host")
                generate_plays(matrix_aux2,"slave")
                create_img('Docs/matrix_slave.pdf','Docs/slave.png')
                count_boats(matrix_aux2)
                count_boats_d1(matrix_aux2)
                count_boats_d2(matrix_aux)
                if(game_over == True):
                    mb.showerror("Game Over", f"{active_user} !,You ran out of lives!")
                    show_adjacency(matrix_aux2)
                    self.descalificado()

                if(game_over2 == True):
                    mb.showinfo("Game Over", f"{active_user} !, You Win!")
                    show_adjacency(matrix_aux2)
                    self.descalificado()
            else:
                mb.showerror("Request Failed", "Sorry, Invalid Move")

        elif(name == "slave"):

            self.invited_text.delete(0, END)
            self.invited_text2.delete(0, END)

            if (posx != "" and posy != "" and int(posx) <= int(size) and int(posy) <= int(size)):

                matrix_aux.do_shot(posx,posy,"slave")
                generate_plays(matrix_aux,"host")
                create_img('Docs/matrix_host.pdf','Docs/host.png')
                count_boats(matrix_aux)
                count_boats_d1(matrix_aux2)
                count_boats_d2(matrix_aux)
                if(game_over == True):
                    mb.showerror("Game Over", f"{invited_name}!, You ran out of lives!")
                    show_adjacency(matrix_aux2)
                    self.descalificado()

                if(game_over2 == True):
                    mb.showinfo("Game Over", f"{invited_name} !, You Win!")
                    show_adjacency(matrix_aux2)
                    self.descalificado()
            else:
                mb.showerror("Request Failed", "Sorry, Invalid Move")
        
    def show_results(self):
        global rec_pa_d1, rec_sb_d1, rec_dt_d1, rec_bq_d1
        global rec_pa_d2, rec_sb_d2, rec_dt_d2, rec_bq_d2

        self.results = tk.Toplevel()
        self.results.title('Results')
        self.results.geometry('600x670+500+50')

        create_img('Docs/matrix_Adjacency.pdf','Docs/adjcnt.png')
        create_img('Docs/matrix_Grafo.pdf','Docs/grafo.png')

        self.local_user = tk.Label(self.results, text = f"Usuario Local: {active_user}").place(x = 60, y=20)
        self.local_total = tk.Label(self.results, text = f"Barcos Destruidos - Total:").place(x = 60, y=40)
        self.local_pa = tk.Label(self.results, text = f"PortaAviones: \t       {rec_pa_d1}").place(x = 60, y=60)
        self.local_sb = tk.Label(self.results, text = f"Submarinos: \t       {rec_sb_d1}").place(x = 60, y=80)
        self.local_dt = tk.Label(self.results, text = f"Destructores: \t       {rec_dt_d1}").place(x = 60, y=100)
        self.local_bq = tk.Label(self.results, text = f"Buques: \t\t       {rec_bq_d1}").place(x = 60, y=120)

        self.invited_user = tk.Label(self.results, text = f"Usuario Invitado: {invited_name}").place(x = 390, y=20)
        self.local_total = tk.Label(self.results, text = f"Barcos Destruidos - Total:").place(x = 390, y=40)
        self.invited_pa = tk.Label(self.results, text = f"PortaAviones: \t       {rec_pa_d2}").place(x = 390, y=60)
        self.invited_sb = tk.Label(self.results, text = f"Submarinos: \t       {rec_sb_d2}").place(x = 390, y=80)
        self.invited_dt = tk.Label(self.results, text = f"Destructores: \t       {rec_dt_d2}").place(x = 390, y=100)
        self.invited_bq = tk.Label(self.results, text = f"Buques: \t\t       {rec_bq_d2}").place(x = 390, y=120)

        self.btn_show_ad = Button(self.results, width = 14, text="Lista Adyacencia", command=self.reload_adjcnt)
        self.btn_show_ad.place(x=240, y=50)

        self.btn_show_ad = Button(self.results, width = 14, text=" Grafo ", command=self.reload_grafo)
        self.btn_show_ad.place(x=240, y=90)

        self.btn_show_ad = Button(self.results, width = 10, text=" Salir ", command=self.salir_rep)
        self.btn_show_ad.place(x=40, y=620)

        self.results.resizable(0,0)
        self.results.mainloop()


    def reload_adjcnt(self):
        self.local_frame = Frame(self.results, height=450, width=450)
        self.local_frame.pack()
        self.local_frame.place(x=70,y=150)
        self.local_img = get_image2('Docs/adjcnt.png')
        self.local_label = tk.Label(self.local_frame, image= self.local_img)
        self.local_label.pack()

    def reload_grafo(self):
        self.local_frame = Frame(self.results, height=450, width=450)
        self.local_frame.pack()
        self.local_frame.place(x=70,y=150)
        self.local_img2 = get_image2('Docs/grafo.png')
        self.local_label2 = tk.Label(self.local_frame, image= self.local_img2)
        self.local_label2.pack()

    def salir_rep(self):
        self.results.destroy()
        
        self.user_menu.deiconify()

        
    def descalificado(self):
        self.do_ply.destroy()
        self.plys.destroy()
        self.show_results()
        

    def abandone(self):
        global user_tokens
        if(user_tokens >= 20):
            mb.showinfo("Game Over", "You Leave, You Lost!")

            user_tokens -= 20

            up_coins = {
	                "nick": active_user,
                    "monedas": str(user_tokens)
                }

            requests.put(f'{base_url}/up_coins', json = up_coins)

            self.do_ply.destroy()
            self.plys.destroy()
            self.user_menu.deiconify()

        else:
            mb.showerror("Request Failed", "You can't leave, you need at least 20 Tokens")





    #-----------------------------configurar ubicacion de barcos----------------------------------------
    def settings(self):
        global user_life, matrix_size, user_tokens, game_over, active_user, matrix_aux
        global portaviones, submarinos, destructores, buques

        user_life = 3

        cant_barcos(matrix_size)

        matrix_aux.generate_prototipo()

        show_insert(matrix_aux)

        create_img('Docs/matrix_insertion.pdf','Docs/settings.png')
        

        self.plys.withdraw()
        self.settngs = tk.Toplevel()
        self.settngs.title('Settings')
        self.settngs.geometry('1010x650+550+200')

        self.t_1 = Label(self.settngs, text = "Configuracion del Tablero").place(x = 135, y=100)
        self.t_2 = Label(self.settngs, text = "Dimensiones: X: {}, Y: {}".format(matrix_size,matrix_size) ).place(x = 138, y=120)

        #-----------portaviones--------------------------

        self.titulo = Label(self.settngs, text = "Ingrese Coordenadas").place(x = 180, y=175)

        self.txt_x1 = Label(self.settngs, text = "X: ").place(x = 150, y=200)
        self.txt_y1 = Label(self.settngs, text = "Y: ").place(x = 150, y=220)

        self.x1 = Entry(self.settngs)
        self.x1.place(x=170, y=200, width=20 , height=20)
        self.y1 = Entry(self.settngs)
        self.y1.place(x=170, y=220, width=20 , height=20)

        
        self.txt_x2 = Label(self.settngs, text = "X: ").place(x = 200, y=200)
        self.txt_y2 = Label(self.settngs, text = "Y: ").place(x = 200, y=220)

        self.x2 = Entry(self.settngs)
        self.x2.place(x=220, y=200, width=20 , height=20)
        self.y2 = Entry(self.settngs)
        self.y2.place(x=220, y=220, width=20 , height=20)

        
        self.txt_x3 = Label(self.settngs, text = "X: ").place(x = 250, y=200)
        self.txt_y3 = Label(self.settngs, text = "Y: ").place(x = 250, y=220)

        self.x3 = Entry(self.settngs)
        self.x3.place(x=270, y=200, width=20 , height=20)
        self.y3 = Entry(self.settngs)
        self.y3.place(x=270, y=220, width=20 , height=20)

        self.txt_x4 = Label(self.settngs, text = "X: ").place(x = 300, y=200)
        self.txt_y4 = Label(self.settngs, text = "Y: ").place(x = 300, y=220)

        self.x4 = Entry(self.settngs)
        self.x4.place(x=320, y=200, width=20 , height=20)
        self.y4 = Entry(self.settngs)
        self.y4.place(x=320, y=220, width=20 , height=20)

        self.btn_pa = Button(self.settngs, width = 14, text="Porta Aviones", command = lambda: self.verify_cant_pa(self.x1.get(),self.y1.get(),self.x2.get(),self.y2.get(),self.x3.get(),self.y3.get(),self.x4.get(),self.y4.get()))
        self.btn_pa.place(x=20, y=200)

        self.txt_cant_pa = Label(self.settngs, text = "No. Permitido: " + str(portaviones)).place(x = 20, y=230)


         #-----------Submarino--------------------------


        self.titulo2 = Label(self.settngs, text = "Ingrese Coordenadas").place(x = 180, y=250)

        self.txt_X1 = Label(self.settngs, text = "X: ").place(x = 150, y=270)
        self.txt_Y1 = Label(self.settngs, text = "Y: ").place(x = 150, y=295)

        self.X1 = Entry(self.settngs)
        self.X1.place(x=170, y=275, width=20 , height=20)
        self.Y1 = Entry(self.settngs)
        self.Y1.place(x=170, y=295, width=20 , height=20)

        
        self.txt_X2 = Label(self.settngs, text = "X: ").place(x = 200, y=275)
        self.txt_Y2 = Label(self.settngs, text = "Y: ").place(x = 200, y=295)

        self.X2 = Entry(self.settngs)
        self.X2.place(x=220, y=275, width=20 , height=20)
        self.Y2 = Entry(self.settngs)
        self.Y2.place(x=220, y=295, width=20 , height=20)

        
        self.txt_X3 = Label(self.settngs, text = "X: ").place(x = 250, y=275)
        self.txt_Y3 = Label(self.settngs, text = "Y: ").place(x = 250, y=295)

        self.X3 = Entry(self.settngs)
        self.X3.place(x=270, y=275, width=20 , height=20)
        self.Y3 = Entry(self.settngs)
        self.Y3.place(x=270, y=295, width=20 , height=20)

        self.btn_sb = Button(self.settngs, width = 14, text="Submarino", command = lambda: self.verify_cant_sb(self.X1.get(),self.Y1.get(),self.X2.get(),self.Y2.get(),self.X3.get(),self.Y3.get()))
        self.btn_sb.place(x=20, y=275)

        self.txt_cant_sb = Label(self.settngs, text = "No. Permitido: " + str(submarinos)).place(x = 20, y=305)



         #-----------Destructor--------------------------

        self.titulo3 = Label(self.settngs, text = "Ingrese Coordenadas").place(x = 180, y=325)

        self.txt_x_1 = Label(self.settngs, text = "X: ").place(x = 150, y=350)
        self.txt_y_1 = Label(self.settngs, text = "Y: ").place(x = 150, y=370)

        self.x_1 = Entry(self.settngs)
        self.x_1.place(x=170, y=350, width=20 , height=20)
        self.y_1 = Entry(self.settngs)
        self.y_1.place(x=170, y=370, width=20 , height=20)

        
        self.txt_x_2 = Label(self.settngs, text = "X: ").place(x = 200, y=350)
        self.txt_y_2 = Label(self.settngs, text = "Y: ").place(x = 200, y=370)

        self.x_2 = Entry(self.settngs)
        self.x_2.place(x=220, y=350, width=20 , height=20)
        self.y_2 = Entry(self.settngs)
        self.y_2.place(x=220, y=370, width=20 , height=20)

        self.btn_dt = Button(self.settngs, width = 14, text="Destructor", command = lambda: self.verify_cant_dt(self.x_1.get(),self.y_1.get(),self.x_2.get(),self.y_2.get()))
        self.btn_dt.place(x=20, y=350)

        self.txt_cant_dt = Label(self.settngs, text = "No. Permitido: " + str(destructores)).place(x = 20, y=380)


        #-----------Buque--------------------------

        self.titulo4 = Label(self.settngs, text = "Ingrese Coordenadas").place(x = 180, y=400)

        self.txt_X_1 = Label(self.settngs, text = "X: ").place(x = 150, y=425)
        self.txt_Y_1 = Label(self.settngs, text = "Y: ").place(x = 150, y=445)

        self.X_1 = Entry(self.settngs)
        self.X_1.place(x=170, y=425, width=20 , height=20)
        self.Y_1 = Entry(self.settngs)
        self.Y_1.place(x=170, y=445, width=20 , height=20)

        self.btn_bq = Button(self.settngs, width = 14, text="Buque", command = lambda: self.verify_cant_bq(self.X_1.get(),self.Y_1.get()))
        self.btn_bq.place(x=20, y=425)

        self.txt_cant_bq = Label(self.settngs, text = "No. Permitido: " + str(buques)).place(x = 20, y=455)


        #--------------------------Botones------------------------------------------------

        self.btn_back = Button(self.settngs, width = 5, text="Atras", command = self.back)
        self.btn_back.place(x=20, y=20)

        self.btn_save_play = Button(self.settngs, width = 14, text="Save and Play", command = self.save)
        self.btn_save_play.place(x=150, y=550)


        self.sttng_frame = Frame(self.settngs, height=400, width=400)
        self.sttng_frame.pack()
        self.sttng_frame.place(x=370,y=15)

        self.sttng_table = get_image('Docs/settings.png')

        self.sttng_label = tk.Label(self.sttng_frame, image= self.sttng_table)
        self.sttng_label.pack()

        self.settngs.after(1000, self.reload_sttngs)

        self.settngs.resizable(0,0)
        self.settngs.mainloop()

        
    def reload_sttngs(self):
        global user_life, user_tokens, invited_life

        self.sttng_table = get_image('Docs/settings.png')

        self.sttng_label.config(image= self.sttng_table)

        self.settngs.after(1000, self.reload_sttngs)

    def verify_cant_pa(self,x1,y1,x2,y2,x3,y3,x4,y4):
        global matrix_aux, matrix_size

        self.x1.delete(0, END)
        self.y1.delete(0, END)

        self.x2.delete(0, END)
        self.y2.delete(0, END)

        self.x3.delete(0, END)
        self.y3.delete(0, END)

        self.x4.delete(0, END)
        self.y4.delete(0, END)

        if(int(x1) <= matrix_size and int(y1) <= matrix_size and int(x2) <= matrix_size and int(y2) <= matrix_size and int(x3) <= matrix_size and int(y3) <= matrix_size and int(x4) <= matrix_size and int(y4) <= matrix_size):
            count_boats(matrix_aux)
            global portaviones
            global rec_pa

            if(rec_pa < portaviones):
                self.add_portavion(x1,y1,x2,y2,x3,y3,x4,y4)
            else:
                mb.showerror("Out of Space", "All AirCraft Carriers have already been placed!")
        else:
            mb.showerror("Request Failed", "Sorry, Invalid Insert")


            
    def verify_cant_sb(self,x1,y1,x2,y2,x3,y3):
        global matrix_aux, matrix_size  

        self.X1.delete(0, END)
        self.Y1.delete(0, END)

        self.X2.delete(0, END)
        self.Y2.delete(0, END)

        self.X3.delete(0, END)
        self.Y3.delete(0, END)

        if(int(x1) <= matrix_size and int(y1) <= matrix_size and int(x2) <= matrix_size and int(y2) <= matrix_size and int(x3) <= matrix_size and int(y3) <= matrix_size):

            count_boats(matrix_aux)
            global submarinos
            global rec_sb

            if(rec_sb < submarinos):
                self.add_submarino(x1,y1,x2,y2,x3,y3)
            else:
                mb.showerror("Out of Space", "All Submarines have already been placed!")
        else:
            mb.showerror("Request Failed", "Sorry, Invalid Insert")

    def verify_cant_dt(self,x1,y1,x2,y2):
        global matrix_aux

        if(int(x1) <= matrix_size and int(y1) <= matrix_size and int(x2) <= matrix_size and int(y2) <= matrix_size):

            self.x_1.delete(0, END)
            self.y_1.delete(0, END)

            self.x_2.delete(0, END)
            self.y_2.delete(0, END)

            count_boats(matrix_aux)
            global destructores
            global rec_dt

            if(rec_dt < destructores):
                self.add_destructor(x1,y1,x2,y2)
            else:
                mb.showerror("Out of Space", "All Destructors have already been placed!")

        else:
            mb.showerror("Request Failed", "Sorry, Invalid Insert")    

    def verify_cant_bq(self,x1,y1):
        global matrix_aux

        self.X_1.delete(0, END)
        self.Y_1.delete(0, END)

        if(int(x1) <= matrix_size and int(y1) <= matrix_size):
            count_boats(matrix_aux)
            global buques
            global rec_bq

            if(rec_bq < buques):
                self.add_buque(x1,y1)
            else:
                mb.showerror("Out of Space", "All Ships have already been placed!")
    
        else:
            mb.showerror("Request Failed", "Sorry, Invalid Insert")



    def add_portavion(self,x1,y1,x2,y2,x3,y3,x4,y4):
        global matrix_aux
        
        matrix_aux.insert_in_pos(int(x1),int(y1), Maroon, Maroon)
        matrix_aux.insert_in_pos(int(x2),int(y2), Maroon, Maroon)
        matrix_aux.insert_in_pos(int(x3),int(y3), Maroon, Maroon)
        matrix_aux.insert_in_pos(int(x4),int(y4), Maroon, Maroon)
        show_insert(matrix_aux)
        create_img('Docs/matrix_insertion.pdf','Docs/settings.png')

    def add_submarino(self,x1,y1,x2,y2,x3,y3):
        global matrix_aux
        matrix_aux.insert_in_pos(int(x1),int(y1), Navy, Navy)
        matrix_aux.insert_in_pos(int(x2),int(y2), Navy, Navy)
        matrix_aux.insert_in_pos(int(x3),int(y3), Navy, Navy)
        show_insert(matrix_aux)
        create_img('Docs/matrix_insertion.pdf','Docs/settings.png')

    def add_destructor(self,x1,y1,x2,y2):
        global matrix_aux
        matrix_aux.insert_in_pos(int(x1),int(y1), Gray, Gray)
        matrix_aux.insert_in_pos(int(x2),int(y2), Gray, Gray)
        show_insert(matrix_aux)
        create_img('Docs/matrix_insertion.pdf','Docs/settings.png')

    def add_buque(self,x1,y1):
        global matrix_aux
        matrix_aux.insert_in_pos(int(x1),int(y1), Teal, Teal)
        show_insert(matrix_aux)
        create_img('Docs/matrix_insertion.pdf','Docs/settings.png')
    
    def save(self):
        global portaviones, submarinos, destructores, buques
        global rec_pa, rec_sb, rec_dt, rec_bq, matrix_size

        if (rec_pa < portaviones or rec_sb < submarinos or rec_dt < destructores or rec_bq < buques):
            mb.showerror("Request Failed", "Sorry, You need to complete Insertions!")
        else:
            self.settngs.withdraw()
            self.do_play("manual")

    
    def back(self):
        self.settngs.destroy()
        self.plys.destroy()
        self.user_menu.deiconify()


    #------------------------------------menu Administrador---------------------------------------------
    def admin_menu(self):
        self.logn.destroy()
        self.admin_menu = tk.Tk()
        self.admin_menu.title('Admin Menu')
        self.admin_menu.geometry('250x250+650+200')

        self.active = Label(self.admin_menu, text = "Admin User").place(x = 90, y=20)

        self.btn_loadfile = Button(self.admin_menu, width = 14, text="Data Upload", command=self.load_file )
        self.btn_loadfile.place(x=70, y=80)
        self.btn_reports = Button(self.admin_menu, width = 14, text="Reports", command=self.report_menu )
        self.btn_reports.place(x=70, y=120)
        self.btn_logout = Button(self.admin_menu, width = 14, text="Logout", command= self.admin_logout )
        self.btn_logout.place(x=70, y=160)

        self.admin_menu.resizable(0,0)
        self.admin_menu.mainloop()

    def admin_logout(self):
        self.admin_menu.destroy()
        home()

    def load_file(self):
        try:
            filename = askopenfilename()
            print(filename)
            masiva = {
	                "ruta": filename
                }

            requests.post(f'{base_url}/masiva', json = masiva)
        except:
            print('error happend')
    
    #-------------------menu reportes------------------------------------------------------
    def report_menu(self):
        self.admin_menu.withdraw()
        self.report_menu = tk.Tk()
        self.report_menu.title('Reports Menu')
        self.report_menu.geometry('250x430+650+200')


        self.active = Label(self.report_menu, text = "REPORTS").place(x = 105, y=20)

        self.btn_rpt_listaC = Button(self.report_menu, width = 16, text="Circular List", command=self.crc_graph)
        self.btn_rpt_listaC.place(x=70, y=50)
        self.btn_rpt_listaL = Button(self.report_menu, width = 16, text="List of Lists", command=self.ldl_graph)
        self.btn_rpt_listaL.place(x=70, y=90)
        self.btn_rpt_colaM = Button(self.report_menu, width = 16, text="Moves Queue", command=self.cola_graph)
        self.btn_rpt_colaM.place(x=70, y=130)
        self.btn_rpt_listaP = Button(self.report_menu, width = 16, text="List of Stack", command=self.ldp_graph)
        self.btn_rpt_listaP.place(x=70, y=170)
        self.btn_rpt_listaU = Button(self.report_menu, width = 16, text="Users List", command=self.users_list)
        self.btn_rpt_listaU.place(x=70, y=210)
        self.btn_rpt_listaA = Button(self.report_menu, width = 16, text="Items List", command = self.items_list)
        self.btn_rpt_listaA.place(x=70, y=250)

        self.ent_set_prefix = Entry(self.report_menu)
        self.ent_set_prefix.place(x=70, y=293, width=38, height=20)
        self.btn_rpt_Prefix = Button(self.report_menu, width = 10, text="Set Prefix", command = lambda: self.set_prefix(self.ent_set_prefix.get()))
        self.btn_rpt_Prefix.place(x=111, y=290)

        self.btn_rpt_Block_Chain = Button(self.report_menu, width = 16, text="Blockchain", command=self.show_block_chain)
        self.btn_rpt_Block_Chain.place(x=70, y=330)

        self.btn_exit = Button(self.report_menu, width = 16, text="Exit", command= self.report_logout )
        self.btn_exit.place(x=70, y=370)


        self.report_menu.resizable(0,0)
        self.report_menu.mainloop()
    
    def show_block_chain(self):
        global new_blockchain
        new_blockchain.do_graphics()

    def set_prefix(self, prefix):
        global new_blockchain
        if(prefix != None and prefix != ""):
            new_blockchain.set_prefix(prefix)
            mb.showinfo("OK", "New Prefix Setted")
            self.ent_set_prefix.delete(0, END)
        else:
            mb.showerror("Request Failed", "Sorry, Type a Prefix")


    #depliegue de usuarios ascendente y descendente
    def users_list(self):
        x = requests.get(f'{base_url}/usersUp')
        y = requests.get(f'{base_url}/usersDw')
        datasUp = x.json()
        datasDw = y.json()


        # env = Environment(loader=FileSystemLoader('Templates/'),
        #                 autoescape=select_autoescape(['html']))
        # template = env.get_template('report_users.html')
        # template = env.get_template('report_users.html')
        # template = env.get_template('report_users.html')

        # html_file = open('users.html', 'w+', encoding='utf-8')
        # html_file.write(template.render(UP=datasUp,DW=datasDw))
        # html_file.close()
        # startfile('users.html')
    
    #depliegue de Articulos ascendente y descendente
    def items_list(self):
        x = requests.get(f'{base_url}/itemsUp')
        y = requests.get(f'{base_url}/itemsDw')
        datasUp = x.json()
        datasDw = y.json()


        # env = Environment(loader=FileSystemLoader('Templates/'),
        #                 autoescape=select_autoescape(['html']))
        # template = env.get_template('report_items.html')
        # template = env.get_template('report_items.html')
        # template = env.get_template('report_items.html')

        # html_file = open('items.html', 'w+', encoding='utf-8')
        # html_file.write(template.render(UP=datasUp,DW=datasDw))
        # html_file.close()
        # startfile('items.html')

    def ldp_graph(self):
        x = requests.get(f'{base_url}/pila_graph')
        data = x.text
        
        if(data == "grafica"):
            mb.showinfo('Welcome', 'List of Stacks!')
        elif(data == "nografica"):
            mb.showerror("Request Failed", "Sorry, List Empty!")

    def crc_graph(self):

        x = requests.get(f'{base_url}/circular_graph')
        data = x.text
        
        if(data == "grafica"):
            mb.showinfo('Welcome', 'Users Circular list!')
        elif(data == "nografica"):
            mb.showerror("Request Failed", "Sorry, List Empty!")

    def ldl_graph(self):

        x = requests.get(f'{base_url}/listas_graph')
        data = x.text
        
        if(data == "grafica"):
            mb.showinfo('Welcome', 'List of Lists!')
        elif(data == "nografica"):
            mb.showerror("Request Failed", "Sorry, List Empty!")

    def cola_graph(self):

        x = requests.get(f'{base_url}/cola_graph')
        data = x.text
        
        if(data == "grafica"):
            mb.showinfo('Welcome', 'Moves Queue!')
        elif(data == "nografica"):
            mb.showerror("Request Failed", "Sorry, List Empty!")

    def report_logout(self):
        self.report_menu.destroy()
        self.admin_menu.deiconify()

if __name__ == '__main__':
    home()



