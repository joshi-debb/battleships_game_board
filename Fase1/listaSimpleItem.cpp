



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
        primero->siguiente = NULL;
        ultimo = actual;
    }
    else {
        ultimo->siguiente = actual;
        actual->siguiente = NULL;
        ultimo = actual;
    }
    cout << "\n Item Ingresado\n\n";
}

void listaSimpleItem::showList() {
    nodoItem* actual = new nodoItem();

    actual = primero;

    cout << "\n>Tienda: " << endl;

    cout << " Id:" << "\tNombre:\t\t\t " << "Categoria:\t\t " << " Precio: " << endl;

    if (primero != NULL) {
        while (actual != NULL) {
            cout << " " << actual->getId() << "\t" << actual->getName() << "\t\t\t " << actual->getCategory() << "\t\t\t " << actual->getPrice() << endl;
            actual = actual->siguiente;
        }
    }
    else {
        cout << "\nLista Vacia!" << endl;
    }
}

void listaSimpleItem::bubbleSortUP(listaSimpleItem listaItems) {

    if (listaItems.primero != NULL) {
        nodoItem* pivote = NULL, *actual = NULL;

        string id, category, name, src;
        int price = 0;


        pivote = listaItems.primero;
        while (pivote != listaItems.ultimo) {
            actual = pivote->siguiente;
            while (actual != NULL) {
                if (pivote->getPrice() > actual->getPrice()) {

                    id = pivote->getId();
                    category = pivote->getCategory();
                    name = pivote->getName();
                    src = pivote->getSrc();
                    price = pivote->getPrice();

                    pivote->setId(actual->getId());
                    pivote->setCategory(actual->getCategory());
                    pivote->setName(actual->getName());
                    pivote->setSrc(actual->getSrc());
                    pivote->setPrice(actual->getPrice());

                    actual->setId(id);
                    actual->setCategory(category);
                    actual->setName(name);
                    actual->setSrc(src);
                    actual->setPrice(price);
          
                }
                actual = actual->siguiente;
            }
            pivote = pivote->siguiente;
        }
    }
}

void listaSimpleItem::bubbleSortDW(listaSimpleItem listaItems) {

    if (listaItems.primero != NULL) {
        nodoItem* pivote = NULL, * actual = NULL;

        string id, category, name, src;
        int price = 0;


        pivote = listaItems.primero;
        while (pivote != listaItems.ultimo) {
            actual = pivote->siguiente;
            while (actual != NULL) {
                if (pivote->getPrice() < actual->getPrice()) {

                    id = pivote->getId();
                    category = pivote->getCategory();
                    name = pivote->getName();
                    src = pivote->getSrc();
                    price = pivote->getPrice();

                    pivote->setId(actual->getId());
                    pivote->setCategory(actual->getCategory());
                    pivote->setName(actual->getName());
                    pivote->setSrc(actual->getSrc());
                    pivote->setPrice(actual->getPrice());

                    actual->setId(id);
                    actual->setCategory(category);
                    actual->setName(name);
                    actual->setSrc(src);
                    actual->setPrice(price);

                }
                actual = actual->siguiente;
            }
            pivote = pivote->siguiente;
        }
    }
}