



#include <fstream>

#include "json/json.h"
#include <iostream>
#include <memory>
#include <string>

using namespace std;

#include "listaSimpleItem.h"
#include "nodoItem.h"
#include "crow.h"

void listaSimpleItem::loadFile(string ruta) {

    nodoItem* nuevo;
    ifstream ifs(ruta);
    Json::Reader reader;
    Json::Value obj;
    reader.parse(ifs, obj);
    const Json::Value& dataArticle = obj["articulos"];

    string aux = "";
    for (int i = 0; i < dataArticle.size(); i++) {

        aux = dataArticle[i]["nombre"].asString();

        if (searchExist(aux) != true) {

            nuevo = new nodoItem();

            string price = dataArticle[i]["precio"].asString();

            nuevo->setId(dataArticle[i]["id"].asString());
            nuevo->setCategory(dataArticle[i]["categoria"].asString());
            nuevo->setPrice(stoi(price));
            nuevo->setName(dataArticle[i]["nombre"].asString());
            nuevo->setSrc(dataArticle[i]["src"].asString());

            addToEnd(nuevo);


        }
        else {
            cout << "Elemento Repetido y omitido" << endl;
        }

       
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

vector<crow::json::wvalue> listaSimpleItem::bubbleSortUP() {
    
    std::vector<crow::json::wvalue> datos;

    if (primero != NULL) {
        nodoItem* pivote = NULL, * actual = NULL;

        string id, category, name, src;
        int price = 0;

        pivote = primero;
        while (pivote != ultimo) {
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

        nodoItem* actual1 = new nodoItem();
        actual1 = primero;

        while (actual1 != NULL) {
            crow::json::wvalue x;
            x["id"] = actual1->getId();
            x["categoria"] = actual1->getCategory();
            x["precio"] = actual1->getPrice();
            x["nombre"] = actual1->getName();
            x["src"] = actual1->getSrc();
            datos.push_back(x);
            actual1 = actual1->siguiente;
        }
    }
    else {
        cout << "\n>La lista se Encuentra Vacia\n\n";
    }

    return datos;
}


vector<crow::json::wvalue> listaSimpleItem::bubbleSortDW() {

    std::vector<crow::json::wvalue> datos;

    if (primero != NULL) {
        nodoItem* pivote = NULL, * actual = NULL;

        string id, category, name, src;
        int price = 0;


        pivote = primero;
        while (pivote != ultimo) {
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

        nodoItem* actual1 = new nodoItem();
        actual1 = primero;

        while (actual1 != NULL) {
            crow::json::wvalue x;
            x["id"] = actual1->getId();
            x["categoria"] = actual1->getCategory();
            x["precio"] = actual1->getPrice();
            x["nombre"] = actual1->getName();
            x["src"] = actual1->getSrc();
            datos.push_back(x);
            actual1 = actual1->siguiente;
        }

    }
    else {
        cout << "\n>La lista se Encuentra Vacia\n\n";
    }

    return datos;
    
}


bool listaSimpleItem::searchExist(string name) {

    nodoItem* actual = new nodoItem();

    actual = primero;

    if (primero != NULL) {
        while (actual != NULL) {
            if (actual->getName() == name) {
                return true;
            }
            actual = actual->siguiente;
        }
    }

    return false;

}

nodoItem* listaSimpleItem::searchUsers(string name) {
    nodoItem* actual = new nodoItem();
    actual = primero;
    string aux = name;

    if (primero != NULL) {
        do {
            if (actual->getName() == aux) {
                return actual;
            }
            actual = actual->siguiente;
        } while (actual != primero);
    }
    return nullptr;
}


bool listaSimpleItem::is_empty() {
    nodoItem* actual = new nodoItem();
    actual = primero;

    if (primero == NULL) {
        return true;
    }
    return false;
}
