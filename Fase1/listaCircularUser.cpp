

#include <fstream>

#include "json/json.h"
#include <iostream>
#include <memory>
#include <string>


using namespace std;
using std::stoi;

#include "listaCircularUser.h"
#include "menu.h"
#include "nodoUser.h"



void listaCircularUser::loadFile(string ruta) {

    nodoUser* nuevo;
    ifstream ifs(ruta);
    Json::Reader reader;
    Json::Value obj;
    reader.parse(ifs, obj);
    const Json::Value& dataUser = obj["usuarios"];
    const Json::Value& dataArticle = obj["articulos"];
    for (int i = 0; i < dataUser.size(); i++) {

        nuevo = new nodoUser();

        string coins = dataUser[i]["monedas"].asString();
        string age = dataUser[i]["edad"].asString();
  
        nuevo->setNick(dataUser[i]["nick"].asString());
        nuevo->setPassword(dataUser[i]["password"].asString());
        nuevo->setCoins(stoi(coins));
        nuevo->setAge(stoi(age));

        addToEnd(nuevo);
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

void listaCircularUser::login(listaCircularUser listaUsers) {
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
                    secMenu.sec_menu(listaUsers, actual->getNick());

                }
                else {
                    cout << ">password incorrecto!\n";
                    system("pause");
                }
            }
            actual = actual->siguiente;
        } while (actual != primero && encontrado != true);

        if (!encontrado) {
            cout << "\n usuario no Encontrado\n\n";
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

                char opcion;
                bool repetir = true;

                do {
                    system("cls");

                    cout << "\n\n1. Modificar Nick" << endl;
                    cout << "2. Modificar Password" << endl;
                    cout << "3. Modificar Edad" << endl;
                    cout << "4. Guardar y Salir" << endl;

                    cout << "\nIngrese una opcion: " << endl;
                    cin >> opcion;

                    switch (opcion) {
                    case '1':
                        cout << "Ingresa el nuevo Nick: ";
                        cin >> aux;
                        actual->setNick(aux);
                        system("pause");
                        break;

                    case '2':
                        cout << "Ingresa el nuevo Password: ";
                        cin >> aux;
                        actual->setPassword(aux);
                        system("pause");
                        break;

                    case '3':
                        cout << "Ingresa tu nueva Edad: ";
                        cin >> aux;
                        actual->setAge(aux2);
                        system("pause");
                        break;

                    case '4':
                        repetir = false;
                        break;

                    default:
                        cout << ">Elija una opcion valida" << endl;
                        system("pause");
                        break;
                    }
                } while (repetir);
            }
            actual = actual->siguiente;
        } while (actual != primero && encontrado != true);
    }
}

bool listaCircularUser::deleteUser() {
    nodoUser* actual = new nodoUser();
    actual = primero;
    nodoUser* anterior = new nodoUser();
    anterior = NULL;
    bool confirm = false;
    bool encontrado = false;
    char opcion;
    bool repetir = true;
    string aux;
    string aux2;

    do {
        system("cls");

        cout << "\n\n -> Se eliminaran todo sus datos <- \n\n" << endl;
        cout << "1. Confirmar Eliminacion" << endl;
        cout << "2. Cancelar y Salir" << endl;

        cout << "\nIngrese una opcion: " << endl;
        cin >> opcion;

        switch (opcion) {
        case '1':
            cout << ">Ingrese su nombre se usuario: " << endl;
            cin >> aux;
            cout << ">Ingrese su password: " << endl;
            cin >> aux2;
            confirm = true;
            repetir = false;
            break;

        case '2':
            repetir = false;
            break;

        default:
            cout << ">Elija una opcion valida" << endl;
            system("pause");
            break;
        }
    } while (repetir);

    // si si ha confirmado se procede a eliminar
    if (confirm == true && primero != NULL) {
        do {
            if (actual->getNick() == aux && actual->getPassword() == aux2) {

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
                encontrado = true;
                return true;
            }
            anterior = actual;
            actual = actual->siguiente;
        } while (actual != primero && encontrado != true);

        return false;

    }
    else {
        cout << ">Eliminacion Cancelada!" << endl;

    }
    return false;
}

void listaCircularUser::showList() {
    nodoUser* actual = new nodoUser();
    actual = primero;
    if (primero != NULL) {
        do {
            cout << "\tNombre: " << actual->getNick() << "\tPassword: " << actual->getPassword() << \
                "\tAge: " << actual->getAge() << "\tCoins: " << actual->getCoins() << "\n";
            actual = actual->siguiente;
        } while (actual != primero);
    }
    else {
        cout << "\n>La lista se Encuentra Vacia\n\n";
    }
}