


#include <fstream>

#include "json/json.h"
#include <iostream>
#include <memory>
#include <string>


#include "listaSimplePlays.h"
#include "nodoHeaderPlays.h"
#include "nodoPlays.h"
#include "pilaPlays.h"
#include "nodoUser.h"


#include <windows.h> 
#include <sstream>

using namespace std;
using std::stoi;


void listaSimplePlays::doGamePlays(nodoUser* user, int posX, int posY) {

    nodoUser* nuevoUser = new nodoUser();
    nuevoUser = user;

    nodoPlays* nuevo = new nodoPlays();
    nuevo->setX(posX);
    nuevo->setY(posY);

    Insertar(nuevo,nuevoUser->getNick());

}

void listaSimplePlays::Insertar(nodoPlays* plays, string categoria) {
    if (primero == NULL) {
        nodoHeaderPlays* nuevo = new nodoHeaderPlays();
        nuevo->categoria = categoria;
        nuevo->inStack.addToEnd(plays);
        primero = nuevo;
    }
    else {
        nodoHeaderPlays* busqueda = BuscarPrincipal(primero, categoria);
        nodoHeaderPlays* nuevo = new nodoHeaderPlays();
        nuevo->setCat(categoria);
        nuevo->inStack.addToEnd(plays);
        if (busqueda == NULL) {
            nodoHeaderPlays* auxActual = primero;
            while (auxActual != NULL) {
                if (auxActual->siguiente == NULL) {
                    auxActual->siguiente = nuevo;
                    break;
                }
                auxActual = auxActual->siguiente;
            }
        }
        else {
            busqueda->inStack.addToEnd(plays);
        }
    }
}

nodoHeaderPlays* listaSimplePlays::BuscarPrincipal(nodoHeaderPlays* primeroL, string categoria) {
    if (primeroL == NULL) {
        return primeroL;
    }
    else {
        nodoHeaderPlays* auxActual = primeroL;
        while (auxActual != NULL) {
            if (auxActual->getCat() == categoria) {
                break;
            }
            auxActual = auxActual->siguiente;
        }
        return auxActual;
    }
}

void listaSimplePlays::showStruct() {
    nodoHeaderPlays* aux = primero;
    while (aux != NULL) {
        cout << "[" << aux->getCat() << "]->";
        nodoPlays* aux2 = aux->inStack.primero;
        while (aux2 != NULL) {
            cout << "[" << aux2->getX() << "," << aux2->getY() << "]->";
            aux2 = aux2->siguiente;
        }
        cout << ("NULL");
        cout << ("\n | \n");
        aux = aux->siguiente;
    }
}

void listaSimplePlays::doGraphics() {
 
    string dot = "";

    dot += "digraph G {\n";
    dot += +"label=\"Estructura: Lista De Pilas\";\n";
    dot += +"node [shape=box];\n";

    nodoHeaderPlays* aux = primero;
    while (aux != NULL) {
        dot += "N" + (aux->getCat()) + "[label=\"" + (aux->getCat()) + "\"];\n";

        nodoPlays* aux2 = aux->inStack.primero;
        while (aux2 != NULL) {
            dot += "N" + to_string(aux2->getX()) + to_string(aux2->getY()) + "[label=\"" + "(" + to_string(aux2->getX()) + "," + to_string(aux2->getY()) + ")" + "\"];\n";
            aux2 = aux2->siguiente;
        }
        aux = aux->siguiente;
    }

    dot += "{rank=same;\n";

    aux = primero;
    while (aux != NULL) {
        dot += "N" + (aux->getCat());
        if (aux->siguiente != NULL) {
            dot += "->";
        }
        aux = aux->siguiente;
    }

    dot += "}\n";


        aux = primero;
        while (aux != NULL) {
            dot += "{rank=none;\n";
            dot += "N" + (aux->getCat()) + "->";

            nodoPlays* aux2 = aux->inStack.primero;
            while (aux2 != NULL) {
                dot += "N" + to_string(aux2->getX()) + to_string(aux2->getY());
                if (aux2->siguiente != NULL) {
                    dot += "->";
                }
                aux2 = aux2->siguiente;
            }

            aux = aux->siguiente;
            dot += "}\n";
        }

    dot += "}\n";

    cout << dot;

    ofstream file;
    file.open("pilas.dot");
    file << dot;
    file.close();

    system(("dot -Tpng pilas.dot -o  pilas.png"));

    system(("pilas.png"));

  

}



bool listaSimplePlays::is_empty() {

    nodoHeaderPlays* aux = primero;

    if (aux == NULL) {
        return true;
    }
    return false;
}