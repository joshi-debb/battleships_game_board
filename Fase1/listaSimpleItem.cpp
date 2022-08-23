
#include <fstream>

#include "json/json.h"
#include <iostream>
#include <memory>
#include <string>



using namespace std;


#include "listaSimpleItem.h"
#include "nodoItem.h"




void listaSimpleItem::loadFile(string ruta) {

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

        addToEnd(nuevo);
    }
}


void listaSimpleItem::addToEnd(nodoItem* item) {
    nodoItem* actual = new nodoItem();
    actual = item;

    if (primero == NULL) {
        primero = actual;
    }
    else {
        nodoItem* auxActual = primero;
        nodoItem* auxSiguiente;
        while (auxActual != NULL) {
            auxSiguiente = auxActual->siguiente;
            if (actual->getPrice() < auxActual->getPrice()) {
                actual->siguiente = auxActual;
                primero = actual;
                break;
            }
            else if (auxSiguiente == NULL) {
                auxActual->siguiente = actual;
                break;
            }
            else if (actual->getPrice() < auxSiguiente->getPrice()) {
                auxActual->siguiente = actual;
                actual->siguiente = auxSiguiente;
                break;
            }
            auxActual = auxActual->siguiente;
        }
    }
}



void listaSimpleItem::showList() {
    nodoItem* actual = new nodoItem();
    actual = primero;

    cout << "\n\n>Tienda: " << endl;

    cout << " Id: " << "Nombre:\t\t\t " << "Categoria:\t\t " << "Precio: " << endl;

    if (primero != NULL) {
        while (actual != NULL) {
            cout << " " << actual->getId() << "\t" << actual->getName() << "\t\t\t " << actual->getCategory() << "\t\t " << actual->getPrice() << endl;
            actual = actual->siguiente;
        }
    }
    else {
        cout << "\nLista Vacia!" << endl;
    }
}