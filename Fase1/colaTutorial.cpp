


#include <fstream>

#include "json/json.h"
#include <iostream>
#include <memory>
#include <string>

#include "crow.h"


using namespace std;
using std::stoi;

#include "colaTutorial.h"
#include "nodoTutorial.h"


void colaTutorial::loadFile(string ruta) {

    nodoTutorial* nuevo;
    ifstream ifs(ruta);
    Json::Reader reader;
    Json::Value obj;
    Json::Value attrib;
    reader.parse(ifs, obj);
    const Json::Value& dataTable = obj["tutorial"];

    nuevo = new nodoTutorial();

    string Alto = dataTable["alto"].asString();
    string Ancho = dataTable["ancho"].asString();

    cout << "(" << Alto << " <-> " << Ancho << ")" << endl;

    nuevo->setAlto(stoi(Alto));
    nuevo->setAncho(stoi(Ancho));

    addToEnd(nuevo);

    for (int i = 0; i < dataTable["movimientos"].size(); i++) {

        nuevo = new nodoTutorial();

        string posX = dataTable["movimientos"][i]["x"].asString();
        string posY = dataTable["movimientos"][i]["y"].asString();

        cout << "(" << posX << "," << posY << ")" << endl;

        nuevo->setX(stoi(posX));
        nuevo->setY(stoi(posY));

        addToEnd(nuevo);
    }
}

void colaTutorial::addToEnd(nodoTutorial* tuto) {

    nodoTutorial* nuevo = new nodoTutorial();
    nuevo = tuto;

    if (primero == NULL) {
        primero = nuevo;
        primero->siguiente = NULL;
        ultimo = primero;
    }
    else {
        ultimo->siguiente = nuevo;
        nuevo->siguiente = NULL;
        ultimo = nuevo;
    }

    cout << "\n>Nodo Ingresado!\n\n";
}

vector<crow::json::wvalue> colaTutorial::showQueue() {

    std::vector<crow::json::wvalue> datos;
    nodoTutorial* actual = new nodoTutorial();
    
    

    actual = primero->siguiente;
    if (primero->siguiente!= NULL) {
        do {
            crow::json::wvalue x;
            x["alto"] = primero->getAlto();
            x["ancho"] = primero->getAncho();
            x["x"] = actual->getX();
            x["y"] = actual->getY();
            datos.push_back(x);
            actual = actual->siguiente;
        } while (actual != ultimo->siguiente);
    }
    else {
        cout << "\n>La cola se Encuentra Vacia\n\n";
    }
    return datos;
}

void colaTutorial::doGraphics() {
    string dot = "";

    dot += "digraph G {\n";
    dot += +"label=\"Estructura: Cola\";\n";
    dot += +"node [shape=box];\n";

    nodoTutorial* aux = primero->siguiente;
    do {
        dot += "N" + to_string(aux->getX()) + to_string(aux->getY()) + "[label=\""+ "(" + to_string(aux->getX()) + "," +  to_string(aux->getY()) +")"+ "\"];\n";
        aux = aux->siguiente;
    } while (aux != ultimo->siguiente);


    dot += "{rank=same;\n";
    aux = primero->siguiente;
    do {
        dot += "N" + to_string(aux->getX()) + to_string(aux->getY());
        if (aux != ultimo) {
            dot += " -> ";
        }
        aux = aux->siguiente;
    } while (aux != ultimo->siguiente);
    dot += "}\n";


    dot += "}\n";

    cout << dot;

    ofstream file;
    file.open("cola.dot");
    file << dot;
    file.close();

    system(("dot -Tpng cola.dot -o  cola.png"));

    system(("cola.png"));

}


bool colaTutorial::is_empty() {
    nodoTutorial* actual = new nodoTutorial();
    actual = primero;

    if (primero == NULL) {
        return true;
    }
    return false;
}