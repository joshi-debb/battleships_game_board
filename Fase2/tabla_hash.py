
import os
import webbrowser

import fitz

verde_limon = "#59CE8F"
gris_bajo = "#E8F9FD"


class N_Simple():
    def __init__(self, id, nombre, precio):
        self.id: int = int(id)
        self.nombre = nombre
        self.precio = precio
        self.siguiente = None
        self.anterior = None

class L_Simple():
    def __init__(self):
        self.primero: N_Simple = None
        self.ultimo: N_Simple = None
        self.size = 0

    def add_to_end(self, id,nombre,precio):
        nuevo = N_Simple(id,nombre,precio)
        if self.primero == None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo

    def clear_L_simple(self):
        self.primero = None
        self.ultimo = None
        self.size = 0



class Nodo_Item():
    def __init__(self, id, nombre, precio):
        self.id: int = int(id)
        self.nombre = nombre
        self.precio = precio

class Nodo_Simple():
    def __init__(self, id):
        self.id: int = int(id)
        self.siguiente = None
        self.anterior = None
        self.acceso = None

class Lista_Simple():
    def __init__(self):
        self.primero: Nodo_Simple = None
        self.ultimo: Nodo_Simple = None
        self.size = 0

    def insertar_nodoSimple(self, nuevo):
        self.size += 1
        if self.primero == None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo

    def getEncabezado(self, id) -> Nodo_Simple:
        tmp = self.primero
        while tmp != None:
            if id == tmp.id:
                return tmp
            tmp = tmp.siguiente
        return None


class Nodo_Hash():
    def __init__(self, x, datos):
        self.datos = datos
        self.coordenadaX = int(x)
        self.derecha = None


class Tabla_Hash():
    def __init__(self, size):
        self.size_M = size
        self.colide = 0
        self.Max_ocupacion = 80
        self.Min_ocupacion = 0
        self.ocupados = 0
        self.Indice = Lista_Simple()

        for i in range(1,self.size_M+1):
            nodo_X = self.Indice.getEncabezado(i)
            if nodo_X == None:
                nodo_X = Nodo_Simple(i)
                self.Indice.insertar_nodoSimple(nodo_X)


    def insert(self, id_user, id_item, name_item, precio):

        if( self.porcentaje_ocupacion() <= self.Max_ocupacion):
            new_Item = Nodo_Item(id_item, name_item, precio)
        
            aux_key = self.Hash(id_user, name_item)

            if (self.exist_key(aux_key)):

                self.colide += 1

                key = self.double_dispersion(aux_key)
                
                nuevo = Nodo_Hash(key, new_Item)
                nodo_X = self.Indice.getEncabezado(key)

                if nodo_X.acceso == None:
                    nodo_X.acceso = nuevo

                self.ocupados += 1
                print(new_Item.nombre)

            else:
                nuevo = Nodo_Hash(aux_key, new_Item)
                nodo_X = self.Indice.getEncabezado(aux_key)

                if nodo_X.acceso == None:
                    nodo_X.acceso = nuevo
            
                self.ocupados += 1
                print(new_Item.nombre)
        else:
            self.re_Hash()
            self.insert(id_user, id_item, name_item)


    def Hash(self, id_user, p_name):
        aux = 0
        for caracter in str(p_name):
            aux += ord(caracter)
        prekey = id_user+int(aux)
        key = (prekey % self.size_M)
        return key

    
    def double_dispersion(self, prekey):
        key = ((prekey % 3)+1)*self.colide % self.size_M
        return key

    def exist_key(self, key):
        pivote = self.Indice.primero
        while pivote != None:
            pivote_celda : Nodo_Hash = pivote.acceso
            while pivote_celda != None:
                if (pivote.id == key and pivote_celda.datos != None):
                    return True
                pivote_celda = pivote_celda.derecha 
            pivote = pivote.siguiente
        return False

    def delete_by_key(self, key):
        pivote = self.Indice.primero
        while pivote != None:
            pivote_celda : Nodo_Hash = pivote.acceso
            while pivote_celda != None:
                if (pivote_celda.datos != None):
                    if(pivote_celda.datos.id == key):
                        print("eliminado: ",pivote_celda.datos.nombre)
                        pivote_celda.datos = None
                pivote_celda = pivote_celda.derecha 
            pivote = pivote.siguiente

    
    def delete_all(self):
        pivote = self.Indice.primero
        while pivote != None:
            pivote_celda : Nodo_Hash = pivote.acceso
            while pivote_celda != None:
                if (pivote_celda.datos != None):
                    pivote_celda.datos = None
                pivote_celda = pivote_celda.derecha 
            pivote = pivote.siguiente

    def show_datas(self):
        lista_aux = L_Simple()
        pivote = self.Indice.primero
        while pivote != None:
            pivote_celda : Nodo_Hash = pivote.acceso
            while pivote_celda != None:
                if (pivote_celda.datos != None):
                    lista_aux.add_to_end(pivote_celda.datos.id,pivote_celda.datos.nombre,pivote_celda.datos.precio)
                pivote_celda = pivote_celda.derecha 
            pivote = pivote.siguiente
        return lista_aux
    
    def re_Hash(self):

        aux = self.get_next_prime(self.size_M)

        for i in range(self.size_M,aux+1):
            nodo_X = self.Indice.getEncabezado(i)
            if nodo_X == None:
                nodo_X = Nodo_Simple(i)
                self.Indice.insertar_nodoSimple(nodo_X)

        self.size_M = aux

    def get_next_prime(self, primo_actual):
        cont = primo_actual
        cont += 1
        for n in range(2, cont):
            if cont % n == 0:
                cont += 1
        return cont
    
    def porcentaje_ocupacion(self):
        aux = round(self.ocupados*100/self.size_M)
        return aux


    def do_Graphics(self,type_player):
        contenido = '''digraph G{node[shape=box, fontname="Arial", fillcolor="white", style=filled] edge[style = "bold"] node[label = "''' + str(0) +'''" pos = "-1,1!"]raiz;'''
        
        pivote = self.Indice.primero
        posx = 0
        while pivote != None:
            contenido += '\n\tnode[label = "{}" fillcolor="{}" pos="-1,-{}!" shape=box]x{};'.format(pivote.id,verde_limon,posx, pivote.id)
            pivote = pivote.siguiente
            posx += 1

        pivote = self.Indice.primero
        while pivote.siguiente != None:
            contenido += '\n\tx{}->x{};'.format(pivote.id, pivote.siguiente.id)
            pivote = pivote.siguiente

        contenido += '\n\traiz->x{};'.format(self.Indice.primero.id)

        pivote = self.Indice.primero
        posx = 0
        while pivote != None:
            pivote_celda : Nodo_Hash = pivote.acceso
            while pivote_celda != None:
                if pivote_celda.datos != None:
                    contenido += '\n\tnode[label="Id: {}\nNombre: {}" pos="1,-{}!" fillcolor="{}" shape=box]i{}_1;'.format(pivote_celda.datos.id, pivote_celda.datos.nombre,posx,gris_bajo,pivote_celda.coordenadaX)
                pivote_celda = pivote_celda.derecha

            pivote_celda = pivote.acceso
            while pivote_celda != None:
                if pivote_celda.derecha != None:
                    contenido += '\n\ti{}_1->i{}_1;'.format(pivote_celda.coordenadaX, pivote_celda.derecha.coordenadaX)
                pivote_celda = pivote_celda.derecha

            pivote_celda = pivote.acceso
            if(pivote_celda != None):
                contenido += '\n\tx{}->i{}_1;'.format(pivote.id, pivote.acceso.coordenadaX)

            pivote = pivote.siguiente
            posx += 1
          
        contenido += '\n}'

        dot = "Hash_{}.txt".format(type_player)
        with open(dot, 'w') as grafo:
            grafo.write(contenido)
        result = "Hash_{}.pdf".format(type_player)
        os.system("neato -Tpdf " + dot + " -o " + result)

        pdf = fitz.open(result)
        page = pdf.load_page(0)
        pix = page.get_pixmap()
        pix.pil_save("Hashtable.png")

        webbrowser.open("Hashtable.png")






