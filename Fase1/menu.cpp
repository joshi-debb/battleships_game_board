#include "menu.h"

#include <iostream>
#include <cstdlib>

#include "listaCircularUser.h"
#include "listaSimpleHeaders.h"
#include "listaSimpleItem.h"
#include "nodoUser.h"


// menus
void menu::main_menu(listaCircularUser listaUsers, listaSimpleHeaders structList, listaSimpleItem listItem) {


    nodoUser* nuevo;

    char opcion;
    bool repetir = true;

    string ruta;

    string n;
    string p;
    int a = 0;

    do {
        system("cls");

        cout << "\n\nMenu" << endl;
        cout << "1. Carga Masiva" << endl;
        cout << "2. Registrar Usuario" << endl;
        cout << "3. Login" << endl;
        cout << "4. Reportes" << endl;
        cout << "5. Salir del Juego" << endl;

        cout << "\nIngrese una opcion: " << endl;
        cin >> opcion;

        switch (opcion) {
            case '1':

                cout << "Bienvenido a la carga masiva!";
                cout << "Ingrese el nombre de su archivo con extension: " << endl;
                cin >> ruta;

                listaUsers.loadFile(ruta);
                structList.loadFile(ruta);
                listItem.loadFile(ruta);
                system("pause");
                break;

            case '2':

                nuevo = new nodoUser();
                cout << "\n-> Bienvenido al registro de Usuarios! <- \n\n";
                cout << " > Ingrese su nombre de usuario: ";
                cin >> n;
                nuevo->setNick(n);
                cout << " > Ingrese su Edad: ";
                cin >> a;
                nuevo->setAge(a);
                cout << " > Ingrese su Password: ";
                cin >> p;
                nuevo->setPassword(p);

                listaUsers.addToEnd(nuevo);
                system("pause");
                break;

            case '3':
                listaUsers.login(listaUsers);
                system("pause");
                break;

            case '4':

                third_menu(listaUsers,structList,listItem);
                system("pause");
                break;

            case '5':
                repetir = false;
                break;

            default:
                cout << "Elija una opcion valida" << endl;
                system("pause");
                break;
            }
    } while (repetir);
}

void menu::sec_menu(listaCircularUser listaUsers, string _nick) {

    char opcion;
    bool repetir = true;

    do {
        system("cls");

        cout << "\n\n>Usuario Activo: " << _nick << "\n\n";

        cout << "a. Editar Informacion" << endl;
        cout << "b. Eliminar Cuenta" << endl;
        cout << "c. Ver el tutorial" << endl;
        cout << "d. Ver articulos de la tienda" << endl;
        cout << "e. Realizar movimientos" << endl;
        cout << "f. Volver al menu principal" << endl;

        cout << "\nIngrese una opcion: " << endl;
        cin >> opcion;

        switch (opcion) {
        case 'a':
            listaUsers.editInfo(_nick);
            system("pause");
            break;

        case 'b':
            if (listaUsers.deleteUser() == true) {
                repetir = false;
            }
            system("pause");
            break;

        case 'c':

            system("pause");
            break;

        case 'd':

            system("pause");
            break;

        case 'e':

            system("pause");
            break;

        case 'f':
            repetir = false;
            break;

        default:
            cout << "Elija una opcion valida" << endl;
            system("pause");
            break;
        }
    } while (repetir);
}

void menu::third_menu(listaCircularUser listaUsers,listaSimpleHeaders structList,listaSimpleItem listItem) {

    char opcion;
    bool repetir = true;

    do {
        system("cls");

        cout << "\n\n> -> Reportes <- " << "!\n\n";

        cout << "a. Lista Ciruclar" << endl;
        cout << "b. Lista de Listas" << endl;
        cout << "c. Cola de Movimientos" << endl;
        cout << "d. Pila de Pilas" << endl;
        cout << "e. Listado de Usuarios" << endl;
        cout << "f. Listado de Articulos" << endl;
        cout << "g. salir de reportes" << endl;

        cout << "\nIngrese una opcion: " << endl;
        cin >> opcion;

        switch (opcion) {
        case 'a':
            cout << "Grafico de Estructura" << endl;
            listaUsers.doGraphics();
            system("pause");
            break;

        case 'b':

            cout << "Grafico de Estructura" << endl;
            structList.Imprimir();
            structList.doGraphics();
            system("pause");
            break;

        case 'c':\

            cout << "Grafico de Estructura" << endl;
            system("pause");
            break;

        case 'd':

            cout << "Grafico de Estructura" << endl;
            system("pause");
            break;

        case 'e':

            listaUsers.showList();
            system("pause");
            break;

        case 'f':


            listItem.showList();
            system("pause");
            break;

        case 'g':
            repetir = false;
            break;

        default:
            cout << "Elija una opcion valida" << endl;
            system("pause");
            break;
        }
    } while (repetir);
}