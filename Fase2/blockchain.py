
from tabla_hash import L_Simple
from hashlib import sha256
from datetime import datetime
import os
import webbrowser


class Block:
    def __init__(self, lista: L_Simple, timestamp:str, nonce, previoushash, hash, index) -> None:
        self.timestamp = timestamp
        self.nonce = nonce
        self.previoushash = previoushash
        self.hash = hash
        self.index = index
        self.next = None
        self.lista = lista

      
class Blockchain:
    def __init__(self) -> None:
        self.genesis = None
        self.actual = None
        self.prefix = "0000"

    def get_index(self):
        return self.actual.index + 1 if self.actual else 0

    def get_previoushash(self):
        return self.actual.hash if self.actual else '0000'

    def set_prefix(self, prefix):
        self.prefix = prefix

    def get_prefix(self):
        return self.prefix


    def proof_of_work(self, timestamp, previoushash):
        nonce = 0
        Ubicado = ""
        while True:
                nonce += 1
                StringHash = str(self.get_index())+timestamp+previoushash+str(nonce)
                if(str(sha256(StringHash.encode('utf-8')).hexdigest()).find(self.get_prefix()) == 0):
                        Ubicado = sha256(StringHash.encode('utf-8')).hexdigest()
                    
                        break;
        return Ubicado,nonce
    
        
    def insertBlock(self, lista):
        timestamp = datetime.now().strftime("%d-%m-%Y::%H:%M:%S")
        previoushash = self.get_previoushash()
        hashh,nonce = self.proof_of_work(timestamp,previoushash)
        new = Block(lista, timestamp,nonce,previoushash,hashh, self.get_index())

        if self.genesis == None:
            self.genesis = new
            self.actual = self.genesis
        else:
            tmp = self.actual
            while tmp.next is not None:
                 tmp = tmp.next
            self.actual.next = new
            self.actual = new


    def do_graphics(self):
        contenido = '''digraph G{ node [shape=record, fontname="Arial"]'''
        aux = self.genesis
        while aux is not None:
            contenido += '''\nB_{} ['''.format(aux.index)
            contenido += '''shape=plain label=<<table border="0" cellpadding="0">'''
            contenido += '''<tr> <td> <table border="0" cellborder="0" cellspacing="10" >'''
            contenido += '''<tr> <td align="left">INDEX:      {}</td> </tr>'''.format(aux.index)
            contenido += '''<tr> <td align="left">TIME STAMP: {}</td> </tr>'''.format(aux.timestamp)
            contenido += '''<tr> <td align="left">NONCE:      {}</td> </tr>'''.format(aux.nonce)
            contenido += '''<tr> <td align="left">PREV_HASH:  {}  </td> </tr>'''.format(aux.previoushash)
            contenido += '''<tr> <td align="left">NEW_HASH:   {}  </td> </tr>'''.format(aux.hash)
            contenido += '''<tr> <td align="left">Shopping Information: \n </td> </tr>'''
            tmp = aux.lista.primero
            while tmp != None:
                contenido += '<tr> <td align="left">Item_ID: {} , Item_Name: {} , Item_Price: {}</td> </tr>'.format(tmp.id, tmp.nombre, tmp.precio)
                tmp = tmp.siguiente
            contenido += '''</table> </td> </tr>'''
            contenido += ''' </table>> ] '''
            aux = aux.next 
        aux2:Block = self.genesis
        while aux2.next is not None:
            contenido += "B_{} -> B_{}; \n".format(aux2.index,aux2.next.index)
            aux2 = aux2.next
        contenido += '\n}'
        
        dot = "Blockchain.dot"
        with open(dot, 'w') as grafo:
            grafo.write(contenido)
        result = "Blockchain.png"
        os.system("dot -Tpng " + dot + " -o " + result)
        webbrowser.open(result)

 

