



#include <fstream>

#include "json/json.h"
#include <iostream>
#include <memory>
#include <string>


#include "listaSimpleHeaders.h"
#include "nodoItem.h"


#include <windows.h> 
#include <sstream>

using namespace std;
using std::stoi;




void listaSimpleHeaders::loadFile(string ruta) {

    nodoItem* nuevo;
    ifstream ifs(ruta);
    Json::Reader reader;
    Json::Value obj;
    reader.parse(ifs, obj);
    const Json::Value& dataArticle = obj["articulos"];
    for (int i = 0; i < dataArticle.size(); i++) {

        nuevo = new nodoItem();

        string price = dataArticle[i]["precio"].asString();

        nuevo->setId(dataArticle[i]["id"].asString());
        nuevo->setCategory(dataArticle[i]["categoria"].asString());
        nuevo->setPrice(stoi(price));
        nuevo->setName(dataArticle[i]["nombre"].asString());
        nuevo->setSrc(dataArticle[i]["src"].asString());

        Insertar(nuevo, dataArticle[i]["categoria"].asString());
    }
}


void listaSimpleHeaders::Insertar(nodoItem* item, string categoria) {
    if (primero == NULL) {//lista se encuentra vacia
        nodoHeaderItem* nuevo = new nodoHeaderItem();
        nuevo->categoria = categoria;
        nuevo->listainterna.addToEnd(item);
        primero = nuevo;
    }
    else {//la lista no se encuentra vacia
        nodoHeaderItem* busqueda = BuscarPrincipal(primero, categoria);
        nodoHeaderItem* nuevo = new nodoHeaderItem();
        nuevo->setCat(categoria);
        nuevo->listainterna.addToEnd(item);
        if (busqueda == NULL) {
            nodoHeaderItem* auxActual = primero;
            while (auxActual != NULL) {
                if (auxActual->sig == NULL) {
                    auxActual->sig = nuevo;
                    break;
                }
                auxActual = auxActual->sig;
            }
        }
        else {//si la categoria existe se inserta en la misma
            busqueda->listainterna.addToEnd(item);
        }
    }
}

nodoHeaderItem* listaSimpleHeaders::BuscarPrincipal(nodoHeaderItem* primeroL, string categoria) {
    if (primeroL == NULL) {
        return primeroL;
    }
    else {
        nodoHeaderItem* auxActual = primeroL;
        while (auxActual != NULL) {
            if (auxActual->getCat() == categoria) {
                break;
            }
            auxActual = auxActual->sig;
        }
        return auxActual;
    }
}


void listaSimpleHeaders::Imprimir() {
    nodoHeaderItem* aux = primero;
    while (aux != NULL) {
        cout << "[" << aux->getCat() << "]->";
        nodoItem* auxI = aux->listainterna.primero;
        while (auxI != NULL) {
            cout << "[" << auxI->getCategory() << auxI->getName() << "]->";
            auxI = auxI->siguiente;
        }
        cout << ("NULL");
        cout << ("\n | \n");
        aux = aux->sig;
    }
}



void listaSimpleHeaders::GenerarGrafo() {
    string dot = "";

    dot += "digraph G {\n";
    dot += + "label=\"Estructura: Lista De Listas\";\n";
    dot += + "node [shape=box];\n";

    nodoHeaderItem* aux = primero;
    while (aux != NULL) {
        dot += "N" + (aux->getCat()) + "[label=\"" + (aux->getCat()) + "\"];\n";

        nodoItem* auxI = aux->listainterna.primero;
        while (auxI != NULL) {
            dot += "N" + (auxI->getName()) + "[label=\"" + (auxI->getName()) + "\"];\n";
            auxI = auxI->siguiente;
        }

        aux = aux->sig;
    }

        dot += "{rank=same;\n";

            aux = primero;
            while (aux != NULL) {
                dot += "N" + (aux->getCat());
                if (aux->sig != NULL) {
                    dot += "->";
                }
                aux = aux->sig;
            }

        dot += "}\n";

        
            aux = primero;
            while (aux != NULL) {
                dot += "{rank=none;\n";
                dot += "N" + (aux->getCat()) + "->";

                nodoItem* auxI = aux->listainterna.primero;
                while (auxI != NULL) {
                    dot += "N" + (auxI->getName());
                    if (auxI->siguiente != NULL) {
                        dot += "->";
                    }
                    auxI = auxI->siguiente;
                }

                aux = aux->sig;
                dot += "}\n";
            }
    
    dot += "}\n";

    cout << dot;

    ofstream file;
    file.open("Pruebas.dot");
    file << dot;
    file.close();

    system(("dot -Tpng Pruebas.dot -o  Pruebas.png"));

    system(("Pruebas.png"));

}