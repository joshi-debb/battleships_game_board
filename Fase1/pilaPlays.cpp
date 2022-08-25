

#include <fstream>

#include "json/json.h"
#include <iostream>
#include <memory>
#include <string>


using namespace std;
using std::stoi;

#include "pilaPlays.h"
#include "nodoPlays.h"


void pilaPlays::addToEnd(nodoPlays* plays) {

    nodoPlays* nuevo = new nodoPlays();
    nuevo = plays;

    nuevo->siguiente = primero;
    primero = nuevo;

    cout << "\n>Nodo Ingresado!\n\n";
}

void pilaPlays::showStack() {
    nodoPlays* actual = new nodoPlays();
    actual = primero;

    cout << "Jugadas: " << endl;

    if (primero != NULL) {
        while (actual != NULL) {
            cout << "(" << actual->getX() << "," << actual->getY() << ")" << endl;
            actual = actual->siguiente;
        }
    }
    else {
        cout << "\nLista Vacia!" << endl;
    }
}

void pilaPlays::doGraphics() {
    string dot = "";

    dot += "digraph G {\n";
    dot += +"label=\"Estructura: Pila\";\n";
    dot += +"node [shape=box];\n";

    nodoPlays* aux = primero;
    do {
        dot += "N" + to_string(aux->getX()) + to_string(aux->getY()) + "[label=\"" + "(" + to_string(aux->getX()) + "," + to_string(aux->getY()) + ")" + "\"];\n";
        aux = aux->siguiente;
    } while (aux != NULL);


    dot += "{rank=none;\n";
    aux = primero;
    do {
        dot += "N" + to_string(aux->getX()) + to_string(aux->getY());
        if (aux != NULL) {
            dot += " -> ";
        }
        aux = aux->siguiente;
    } while (aux != NULL);
    dot += "}\n";


    dot += "}\n";

    cout << dot;

    ofstream file;
    file.open("pila.dot");
    file << dot;
    file.close();

    system(("dot -Tpng pila.dot -o  pila.png"));

    system(("pila.png"));

}