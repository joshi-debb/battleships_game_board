

#include <fstream>

#include "json/json.h"
#include <iostream>
#include <memory>
#include <string>


using namespace std;
using std::stoi;

#include "listaCircularUser.h"
#include "listaSimpleItem.h"
#include "listaSimplePlays.h"
#include "menu.h"
#include "nodoUser.h"
#include "crow.h"


void listaCircularUser::loadFile(string ruta) {

    nodoUser* nuevo;
    ifstream ifs(ruta);
    Json::Reader reader;
    Json::Value obj;
    reader.parse(ifs, obj);
    const Json::Value& dataUser = obj["usuarios"];
    string aux = "";

    for (int i = 0; i < dataUser.size(); i++) {

        aux = dataUser[i]["nick"].asString();

        if (searchExist(aux) != true) {

            nuevo = new nodoUser();

            string coins = dataUser[i]["monedas"].asString();
            string age = dataUser[i]["edad"].asString();
            nuevo->setNick(dataUser[i]["nick"].asString());
            nuevo->setPassword(dataUser[i]["password"].asString());
            nuevo->setCoins(stoi(coins));
            nuevo->setAge(stoi(age));

            addToEnd(nuevo);
        }
        else {
            cout << "Usuario Repetido y omitido" << endl;
        }

    }
}

void listaCircularUser::addToEnd(nodoUser* user) {

    nodoUser* nuevo = new nodoUser();
    nuevo = user;

    if (primero == NULL) {
        primero = nuevo;
        ultimo = nuevo;
        primero->siguiente = primero;
        primero->atras = ultimo;
    }
    else {
        ultimo->siguiente = nuevo;
        nuevo->atras = ultimo;
        nuevo->siguiente = primero;
        ultimo = nuevo;
        primero->atras = ultimo;
    }
    cout << "\n>Usuario Registrado!\n\n";
}

void listaCircularUser::login(listaCircularUser listaUsers, listaSimpleItem listItems, colaTutorial queue, listaSimplePlays* stack) {
    nodoUser* actual = new nodoUser();
    actual = primero;
    bool encontrado = false;
    string aux;
    if (primero == NULL) {
        cout << "No hay usuarios registrados!\n\n";
    }
    else {
        cout << " > Ingrese el nombre del usuario: ";
        cin >> aux;
        do {
            if (actual->getNick() == aux) {
                cout << ">Usuario Encontrado!\n\n";
                encontrado = true;

                string pass;
                cout << " > Ingrese su Password: ";
                cin >> pass;

                if (pass == actual->getPassword() && aux == actual->getNick()) {
                    menu secMenu;
                    secMenu.sec_menu(listaUsers, actual, listItems, queue, stack);

                }
                else {
                    cout << ">password incorrecto!\n";
                    system("pause");
                }
            }
            actual = actual->siguiente;
        } while (actual != primero && encontrado != true);

        if (!encontrado) {
            cout << "\n>usuario no Encontrado\n\n";
        }
    }
}

void listaCircularUser::editInfo(string _nick) {
    nodoUser* actual = new nodoUser();
    actual = primero;
    bool encontrado = false;
    string aux = "";
    int aux2 = 0;
    if (primero != NULL) {
        do {
            if (actual->getNick() == _nick) {
                actual->setNick(aux);
                actual->setPassword(aux);
                actual->setAge(aux2);
            }
            actual = actual->siguiente;
        } while (actual != primero && encontrado != true);
    }
}

bool listaCircularUser::deleteUser(string nick, string pass) {
    nodoUser* actual = new nodoUser();
    actual = primero;
    nodoUser* anterior = new nodoUser();
    anterior = NULL;
  
    bool encontrado = false;

    if (primero != NULL) {
        do {
            if (actual->getNick() == nick && actual->getPassword() == pass) {

                if (actual == primero) {
                    primero = primero->siguiente;
                    primero->atras = ultimo;
                    ultimo->siguiente = primero;
                }
                else if (actual == ultimo) {
                    ultimo = anterior;
                    ultimo->siguiente = primero;
                    primero->atras = ultimo;
                }
                else {
                    anterior->siguiente = actual->siguiente;
                    actual->siguiente->atras = anterior;
                }
                cout << "\n>Usuario Eliminado!\n\n";

            }
            anterior = actual;
            actual = actual->siguiente;
        } while (actual != primero && encontrado != true);

        encontrado = true;
        return true;

    }
    else {
        cout << ">Eliminacion Cancelada!" << endl;

    }
    return false;
}

void listaCircularUser::showList() {
    nodoUser* actual = new nodoUser();
    actual = primero;

    cout << ">Listado de Usuarios: " << endl;

    if (primero != NULL) {
        do {
            cout << " Nombre: " << actual->getNick() << "\tPassword: " << actual->getPassword() << \
                "\tAge: " << actual->getAge() << "\tCoins: " << actual->getCoins() << "\n";
            actual = actual->siguiente;
        } while (actual != primero);
    }
    else {
        cout << "\n>La lista se Encuentra Vacia\n\n";
    }
}

void listaCircularUser::doGraphics() {
    string dot = "";

    dot += "digraph G {\n";
    dot += "label=\"Estructura: Lista Circular\";\n";
    dot += "node [shape=box];\n";

    nodoUser* aux = primero;
    do {
        dot += "N" + (aux->getNick()) + "[label=\"" + (aux->getNick()) + "\"];\n";
        aux = aux->siguiente;
    } while (aux != primero);


    dot += "{rank=same;\n";
    aux = primero;
    do {
        dot += "N" + (aux->getNick());
        dot += "->";
        aux = aux->siguiente;

    } while (aux != primero);

    ultimo = primero;
    do {
        dot += "N" + (aux->getNick());
        dot += "->";
        aux = aux->atras;

    } while (aux != ultimo);
    dot += "N" + (aux->getNick());
    dot += "}\n";


    dot += "}\n";

    cout << dot;

    ofstream file;
    file.open("listaCiruclar.dot");
    file << dot;
    file.close();

    system(("dot -Tpng listaCiruclar.dot -o  listaCiruclar.png"));

    system(("listaCiruclar.png"));

}

vector<crow::json::wvalue> listaCircularUser::bubbleSortUP() {

        std::vector<crow::json::wvalue> datos;

        nodoUser* pivote = NULL, * actual = NULL;

        string nick, password;
        int coins = 0;
        int age = 0;

        if (primero != NULL) {
        pivote = primero;
        while (pivote != ultimo) {
            actual = pivote->siguiente;
            while (actual != primero) {
                if (pivote->getAge() > actual->getAge()) {

                    nick = pivote->getNick();
                    password = pivote->getPassword();
                    age = pivote->getAge();
                    coins = pivote->getCoins();

                    pivote->setNick(actual->getNick());
                    pivote->setPassword(actual->getPassword());
                    pivote->setAge(actual->getAge());
                    pivote->setCoins(actual->getCoins());

                    actual->setNick(nick);
                    actual->setPassword(password);
                    actual->setAge(age);
                    actual->setCoins(coins);

                }
                actual = actual->siguiente;
            }
            pivote = pivote->siguiente;
        }

        nodoUser* actual1 = new nodoUser();
        actual1 = primero;


        do {
            crow::json::wvalue x;
            x["nick"] = actual1->getNick();
            x["password"] = actual1->getPassword();
            x["edad"] = actual1->getAge();
            x["monedas"] = actual1->getCoins();
            datos.push_back(x);
            actual1 = actual1->siguiente;
        } while (actual1 != primero);


    }
    else {
        cout << "\n>La lista se Encuentra Vacia\n\n";
    }
    return datos;


}

vector<crow::json::wvalue> listaCircularUser::bubbleSortDW() {

    std::vector<crow::json::wvalue> datos;

    nodoUser* pivote = NULL, * actual = NULL;

    string nick, password;
    int coins = 0;
    int age = 0;

    if (primero != NULL) {
        pivote = primero;
        while (pivote != ultimo) {
            actual = pivote->siguiente;
            while (actual != primero) {
                if (pivote->getAge() < actual->getAge()) {

                    nick = pivote->getNick();
                    password = pivote->getPassword();
                    age = pivote->getAge();
                    coins = pivote->getCoins();

                    pivote->setNick(actual->getNick());
                    pivote->setPassword(actual->getPassword());
                    pivote->setAge(actual->getAge());
                    pivote->setCoins(actual->getCoins());

                    actual->setNick(nick);
                    actual->setPassword(password);
                    actual->setAge(age);
                    actual->setCoins(coins);

                }
                actual = actual->siguiente;
            }
            pivote = pivote->siguiente;
        }

        nodoUser* actual1 = new nodoUser();
        actual1 = primero;


        do {
            crow::json::wvalue x;
            x["nick"] = actual1->getNick();
            x["password"] = actual1->getPassword();
            x["edad"] = actual1->getAge();
            x["monedas"] = actual1->getCoins();
            datos.push_back(x);
            actual1 = actual1->siguiente;
        } while (actual1 != primero);

    }
    else {
        cout << "\n>La lista se Encuentra Vacia\n\n";
    }
    return datos;
}


bool listaCircularUser::searchExist(string _nick) {
    nodoUser* actual = new nodoUser();
    actual = primero;
    string aux = _nick;

    if (primero != NULL) {
        do {
            if (actual->getNick() == aux) {
                return true;
            }
            actual = actual->siguiente;
        } while (actual != primero);
    }
    return false;
}



nodoUser* listaCircularUser::searchUsers(string _nick) {
    nodoUser* actual = new nodoUser();
    actual = primero;
    string aux = _nick;

    if (primero != NULL) {
        do {
            if (actual->getNick() == aux) {
                return actual;
            }
            actual = actual->siguiente;
        } while (actual != primero);
    }
    return nullptr;
}



bool listaCircularUser::is_empty() {
    nodoUser* actual = new nodoUser();
    actual = primero;

    if (primero == NULL) {
        return true;
    } 
    return false;
}