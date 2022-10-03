

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
    string aux1 = "";
    string aux2 = "";

    for (int i = 0; i < dataArticle.size(); i++) {

        aux1 = dataArticle[i]["nombre"].asString();

        if (searchExist(aux1) != true) {

            nuevo = new nodoItem();

            string price = dataArticle[i]["precio"].asString();

            nuevo->setId(dataArticle[i]["id"].asString());
            nuevo->setCategory(dataArticle[i]["categoria"].asString());
            nuevo->setPrice(stoi(price));
            nuevo->setName(dataArticle[i]["nombre"].asString());
            nuevo->setSrc(dataArticle[i]["src"].asString());

            Insertar(nuevo, dataArticle[i]["categoria"].asString());
        
        }

        else {
            cout << "Elemento Repetido y omitido" << endl;
        }

       
    }
}


void listaSimpleHeaders::Insertar(nodoItem* item, string categoria) {
    if (primero == NULL) {
        nodoHeaderItem* nuevo = new nodoHeaderItem();
        nuevo->categoria = categoria;
        nuevo->inList.addToEnd(item);
        primero = nuevo;
    }
    else {
        nodoHeaderItem* busqueda = BuscarPrincipal(primero, categoria);
        nodoHeaderItem* nuevo = new nodoHeaderItem();
        nuevo->setCat(categoria);
        nuevo->inList.addToEnd(item);
        if (busqueda == NULL) {
            nodoHeaderItem* auxActual = primero;
            while (auxActual != NULL) {
                if (auxActual->siguiente == NULL) {
                    auxActual->siguiente = nuevo;
                    break;
                }
                auxActual = auxActual->siguiente;
            }
        }
        else {
            busqueda->inList.addToEnd(item);
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
            auxActual = auxActual->siguiente;
        }
        return auxActual;
    }
}

vector<crow::json::wvalue> listaSimpleHeaders::showStruct() {

    std::vector<crow::json::wvalue> datas;

    nodoHeaderItem* aux = primero;
    while (aux != NULL) {
        std::vector<crow::json::wvalue> datos;
        
        nodoItem* aux2 = aux->inList.primero;
        while (aux2 != NULL) {
            crow::json::wvalue x;
            x["id"] = aux2->getId();
            x["categoria"] = aux2->getCategory();
            x["precio"] = aux2->getPrice();
            x["nombre"] = aux2->getName();
            x["src"] = aux2->getSrc();
            datos.push_back(x);
            aux2 = aux2->siguiente;
        }
        datas.push_back(datos);
        aux = aux->siguiente;
    }
    return datas;
}

void listaSimpleHeaders::showList() {
    nodoHeaderItem* aux = primero;
    while (aux != NULL) {
        nodoItem* aux2 = aux->inList.primero;
        while (aux2 != NULL) {
            cout << "Id: " << aux2->getId() << "\t Name: " << aux2->getName() << "\t Categoria: " << aux2->getCategory() << "\t Precio: " << aux2->getPrice() << endl;
            aux2 = aux2->siguiente;
        }
        aux = aux->siguiente;
    }
}

void listaSimpleHeaders::doGraphics() {
    string dot = "";

    dot += "digraph G {\n";
    dot += + "label=\"Estructura: Lista De Listas\";\n";
    dot += + "node [shape=box];\n";

    nodoHeaderItem* aux = primero;
    while (aux != NULL) {
        dot += "\"" + aux->getCat() + "\"" + "[label=\"" + aux->getCat() + "\"];\n";
        

        nodoItem* aux2 = aux->inList.primero;
        while (aux2 != NULL) {
            dot += "\"" + aux2->getName() + "\"" + "[label=\"" + aux2->getName() + "\"];\n";
            aux2 = aux2->siguiente;
        }

        aux = aux->siguiente;
    }

        dot += "{rank=same;\n";

            aux = primero;
            while (aux != NULL) {
                dot += "\"" + aux->getCat() + "\"";
                if (aux->siguiente != NULL) {
                    dot += "->";
                }
                aux = aux->siguiente;
            }

        dot += "}\n";

        
            aux = primero;
            while (aux != NULL) {
                dot += "{rank=none;\n";
                dot += "\"" + aux->getCat() + "\"" + "->";

                nodoItem* aux2 = aux->inList.primero;
                while (aux2 != NULL) {
                    dot += "\"" + aux2->getName() + "\"";
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
    file.open("listaDeListas.dot");
    file << dot;
    file.close();

    system(("dot -Tpng listaDeListas.dot -o  listaDeListas.png"));

    system(("listaDeListas.png"));

}


bool listaSimpleHeaders::searchExist(string name) {
    nodoHeaderItem* aux = primero;

    while (aux != NULL) {
        nodoItem* aux2 = aux->inList.primero;
        while (aux2 != NULL) {
            if (aux2->getName() == name) {
                return true;
            }
            aux2 = aux2->siguiente;
        }
        aux = aux->siguiente;
    }

    return false;

}


bool listaSimpleHeaders::is_empty() {
    nodoHeaderItem* aux = primero;

    if (aux == NULL) {
        return true;
    }
    return false;

}

